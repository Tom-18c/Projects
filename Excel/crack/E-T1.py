import os
import time
import itertools
import string
import win32com.client
import openpyxl
import signal
import sqlite3

# ================= 配置区域 =================
TARGET_FILE = r"G:\Desktop\测试\账号密码260328.xlsx"
KEYWORDS_FILE = r"G:\Desktop\测试\关键词.xlsx"
PROGRESS_DB = r"G:\Desktop\测试\crack_progress.db"  # 使用数据库存储进度
MIN_LEN = 6
MAX_LEN = 20
# ============================================

# 全局变量，用于控制优雅退出
keep_running = True


def signal_handler(sig, frame):
    global keep_running
    print("\n[!] 收到中断信号，正在安全保存进度并退出...")
    keep_running = False


def init_db():
    """初始化数据库，创建进度表"""
    conn = sqlite3.connect(PROGRESS_DB)
    cursor = conn.cursor()
    # 优先组合测试记录表
    cursor.execute("""CREATE TABLE IF NOT EXISTS tried_priority (password TEXT PRIMARY KEY)""")
    # 暴力遍历状态记录表（只保存一条记录，记录当前遍历的游标状态）
    cursor.execute("""CREATE TABLE IF NOT EXISTS brute_state (id INTEGER PRIMARY KEY, length INTEGER, indices TEXT)""")
    conn.commit()
    return conn


def save_priority_progress(conn, password):
    """保存优先测试的密码"""
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO tried_priority (password) VALUES (?)", (password,))
    conn.commit()


def is_priority_tried(conn, password):
    """检查优先密码是否已测试"""
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM tried_priority WHERE password=?", (password,))
    return cursor.fetchone() is not None


def load_brute_state(conn):
    """加载暴力遍历的断点状态"""
    cursor = conn.cursor()
    cursor.execute("SELECT length, indices FROM brute_state WHERE id=1")
    row = cursor.fetchone()
    if row:
        return row[0], list(map(int, row[1].split(",")))
    return None, None


def save_brute_state(conn, length, indices):
    """保存暴力遍历的当前状态（覆盖更新）"""
    cursor = conn.cursor()
    indices_str = ",".join(map(str, indices))
    cursor.execute("REPLACE INTO brute_state (id, length, indices) VALUES (1, ?, ?)", (length, indices_str))
    conn.commit()


def get_keywords():
    """从关键词文件中提取B列关键词"""
    keywords = []
    if not os.path.exists(KEYWORDS_FILE):
        print(f"[!] 关键词文件不存在: {KEYWORDS_FILE}，将跳过优先测试阶段。")
        return keywords

    wb = openpyxl.load_workbook(KEYWORDS_FILE, read_only=True)
    ws = wb.active
    for row in ws.iter_rows(min_row=2, min_col=2, max_col=2, values_only=True):
        if row[0] is not None:
            keywords.append(str(row[0]).strip())
    wb.close()
    print(f"[*] 已加载关键词: {keywords}")
    return keywords


def generate_priority_passwords(keywords):
    """生成优先测试的密码：基于关键词的组合"""
    if not keywords:
        return

    common_nums = ["134680"]
    for k in keywords:
        for num in common_nums:
            combined = k + num
            if MIN_LEN <= len(combined) <= MAX_LEN:
                yield combined
            combined = num + k
            if MIN_LEN <= len(combined) <= MAX_LEN:
                yield combined

    for k1, k2 in itertools.product(keywords, repeat=2):
        if k1 != k2:
            combined = k1 + k2
            if MIN_LEN <= len(combined) <= MAX_LEN:
                yield combined


def try_password(excel_app, password):
    """尝试使用指定密码打开Excel"""
    try:
        wb = excel_app.Workbooks.Open(TARGET_FILE, False, True, None, password)
        print(f"\n[+] 🎉🎉🎉 成功找到密码: {password} 🎉🎉🎉")
        wb.Close(SaveChanges=False)
        return True
    except Exception as e:
        return False


def main():
    global keep_running
    signal.signal(signal.SIGINT, signal_handler)

    if not os.path.exists(TARGET_FILE):
        print(f"[!] 目标文件不存在: {TARGET_FILE}")
        return

    conn = init_db()
    keywords = get_keywords()

    print("[*] 正在启动 Excel 应用程序...")
    try:
        excel_app = win32com.client.Dispatch("Excel.Application")
        excel_app.Visible = False
        excel_app.DisplayAlerts = False
    except Exception as e:
        print("[!] 无法启动Excel，请确保已安装Microsoft Excel且是Windows系统。")
        return

    print("[*] 开始破解流程...")
    start_time = time.time()
    count = 0

    try:
        # ============ 阶段1：优先测试关键词组合 ============
        print("=" * 50)
        print("[*] 阶段1：优先测试关键词组合...")
        print("=" * 50)

        for pwd in generate_priority_passwords(keywords):
            if not keep_running:
                break
            if is_priority_tried(conn, pwd):
                continue

            count += 1
            if try_password(excel_app, pwd):
                save_priority_progress(conn, pwd)
                keep_running = False  # 找到密码，结束循环
                break

            save_priority_progress(conn, pwd)
            if count % 10 == 0:
                print(f"\r[-] 阶段1已尝试 {count} 次，当前尝试: {pwd}    ", end="", flush=True)

        # ============ 阶段2：全量暴力遍历 ============
        if keep_running:
            print("\n" + "=" * 50)
            print("[*] 阶段2：关键词组合无效，开始全量遍历（耗时可能极长）...")
            print("=" * 50)

            chars = string.ascii_letters + string.digits
            count = 0

            # 读取断点状态
            start_length, start_indices = load_brute_state(conn)
            if start_length is not None:
                print(f"[*] 恢复上次进度：从长度 {start_length}，索引组合 {start_indices} 继续")
            else:
                start_length = MIN_LEN
                start_indices = None

            for length in range(start_length, MAX_LEN + 1):
                if not keep_running:
                    break

                # 核心优化：手动控制 itertools.product 的迭代过程，实现断点续传
                # 相当于多重循环，indices 记录了每一层循环的当前指针位置
                if start_indices is None or length != start_length:
                    current_indices = [0] * length
                else:
                    current_indices = start_indices[:]
                    start_indices = None  # 恢复后清空，防止下一长度受影响

                while keep_running:
                    # 1. 根据当前索引生成密码
                    pwd = "".join(chars[i] for i in current_indices)
                    count += 1

                    # 2. 尝试密码
                    if try_password(excel_app, pwd):
                        save_brute_state(conn, length, current_indices)
                        keep_running = False
                        break

                    # 3. 更新游标索引（模拟多重循环的进位机制）
                    pos = length - 1
                    while pos >= 0:
                        current_indices[pos] += 1
                        if current_indices[pos] < len(chars):
                            break  # 没有越界，进位结束
                        current_indices[pos] = 0  # 越界，当前位归零，向前借位
                        pos -= 1

                    # 4. 如果所有位都溢出，说明当前长度遍历完毕
                    if pos < 0:
                        break

                    # 5. 定期保存进度（每50次保存一次，平衡I/O性能与进度精度）
                    if count % 50 == 0:
                        save_brute_state(conn, length, current_indices)
                        print(f"\r[-] 阶段2已尝试 {count} 次，当前长度 {length}，当前: {pwd}    ", end="", flush=True)

    finally:
        try:
            excel_app.Quit()
        except:
            pass
        conn.close()
        print("\n[*] 程序已退出，进度已安全保存。")


if __name__ == "__main__":
    main()
