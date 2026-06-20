import time
import random
import os
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
# 修改导入：使用 Edge 相关的模块
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
# from webdriver_manager.microsoft import EdgeChromiumDriverManager

# --- 配置部分 ---
# 目标URL (链家成都新津区二手房示例)
BASE_URL = "https://cd.lianjia.com/ershoufang/rs/"
# 单个城市最大抓取信息数量
information_each_city = 300

def setup_driver():
    """
    配置并返回一个 Edge WebDriver 实例
    """
    edge_options = Options()
    
    # --- 优化配置 ---
    
    # 1. 显式指定 Edge 浏览器的可执行文件路径
    edge_options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    
    # 2. 移除自动化标识
    edge_options.add_argument('--disable-blink-features=AutomationControlled') 
    edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    edge_options.add_experimental_option('useAutomationExtension', False)
    
    # 3. 设置窗口大小
    edge_options.add_argument('--window-size=1920,1080')
    
    # 4. 更新 User-Agent 为你提供的精确版本
    edge_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0')
    
    # 5. (可选) 添加参数以忽略证书错误，防止某些页面加载问题
    edge_options.add_argument('--ignore-certificate-errors')
    edge_options.add_argument('--ignore-ssl-errors')
    
    # 指定驱动路径
    driver_path = r"G:\Apps\VSCode\Projects\Machine Learning\msedgedriver.exe"
    service = Service(driver_path)
    
    driver = webdriver.Edge(service=service, options=edge_options)
    
    # 执行 CDP 命令隐藏 webdriver 属性
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            })
        """
    })
    
    # --- 尝试添加 Cookie (可选) ---
    # 注意：这些 Cookie 可能会过期，如果失效请手动登录一次后重新抓包获取
    try:
        driver.get("https://cd.lianjia.com/") # 先访问一次域名以设置域
        target_cookies = [
            {'name': 'lianjia_ssid', 'value': '40ca35ae-374c-4e52-bb4c-534df5a3b19c'},
            {'name': 'lianjia_token', 'value': '2.0012d5cd88491b24160378e4b96a2d82cf'},
            {'name': 'lianjia_uuid', 'value': '6d8d2be2-a214-458f-a958-3577d960d6be'},
            # 可以根据需要添加更多之前抓包获取的 Cookie
        ]
        for cookie in target_cookies:
            try:
                driver.add_cookie(cookie)
            except Exception as e:
                print(f"添加 Cookie 失败: {e}")
    except Exception as e:
        print(f"初始化 Cookie 失败: {e}")
    
    return driver


def get_house_list_selenium(driver, url):
    """
    使用 Selenium 获取页面源码
    """
    try:
        print(f"正在访问: {url}")
        
        # 设置页面加载超时时间为 30 秒
        driver.set_page_load_timeout(30)
        
        driver.get(url)
        
        # 随机等待，模拟人类操作
        time.sleep(random.uniform(3, 6))
        
        # 简单模拟鼠标移动
        try:
            from selenium.webdriver.common.action_chains import ActionChains
            actions = ActionChains(driver)
            # 移动到页面中间位置
            actions.move_by_offset(500, 300).perform()
            time.sleep(0.5)
            # 移动回原点
            actions.move_by_offset(-500, -300).perform()
        except:
            pass # 如果移动失败忽略
        
        # 获取页面源码
        page_source = driver.page_source
        
        # 检查是否包含极验封禁
        if '极验封禁' in page_source:
            print("\n[!] 严重警告：触发极验封禁！")
            print("[*] 建议停止程序，更换IP或等待一段时间后再试。")
            return None
            
        # 检查是否包含验证码
        if 'CAPTCHA' in page_source or '人机验证' in page_source:
            print("\n[!] 检测到人机验证页面！")
            print("[*] 请在打开的浏览器窗口中手动完成验证...")
            
            # --- 优化等待逻辑 ---
            # 不再固定等待 30 秒，而是循环检查 URL 是否变回目标 URL
            max_wait_time = 60  # 最多等待 60 秒
            check_interval = 2   # 每 2 秒检查一次
            waited_time = 0
            
            while waited_time < max_wait_time:
                time.sleep(check_interval)
                waited_time += check_interval
                
                # 检查当前 URL
                current_url = driver.current_url
                # 如果 URL 包含 hip.lianjia.com，说明还在验证页
                if 'hip.lianjia.com' in current_url:
                    print(f"[*] 等待验证中... ({waited_time}/{max_wait_time}秒)")
                    continue
                
                # 如果 URL 已经回到列表页，或者源码中不再有验证码，认为验证成功
                page_source = driver.page_source
                if 'CAPTCHA' not in page_source and '人机验证' not in page_source:
                    print("[*] 检测到验证已完成，继续抓取...")
                    # 再次等待一下让页面完全加载
                    time.sleep(random.uniform(2, 4))
                    return page_source
            
            print("[!] 等待超时，验证似乎未完成或失败。")
            return None
        
        return page_source

    except Exception as e:
        print(f"访问页面出错: {e}")
        return None

def parse_html(html):
    """
    解析HTML，提取房源信息
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # 尝试匹配包含 LOGCLICKDATA 的 li 标签
    house_list = soup.find_all('li', class_=lambda x: x and 'LOGCLICKDATA' in x)
    
    # 如果上面的方法没有找到，尝试查找父容器
    if not house_list:
        list_content = soup.find('ul', class_='sellListContent')
        if list_content:
            house_list = list_content.find_all('li')
        else:
            return []
    
    print(f"当前页找到 {len(house_list)} 个房源条目。")
    
    data_rows = []
    
    for house in house_list:
        try:
            # 1. 提取标题
            title_div = house.find('div', class_='title')
            title = title_div.a.text.strip() if title_div else "无标题"
            
            # 2. 提取位置信息
            position_div = house.find('div', class_='positionInfo')
            position_text = position_div.get_text(strip=True, separator='|') if position_div else "未知位置"
            
            # 3. 提取房屋属性
            house_info_div = house.find('div', class_='houseInfo')
            house_info_text = house_info_div.get_text(strip=True, separator='|') if house_info_div else "未知信息"
            
            # 4. 提取总价
            total_price_div = house.find('div', class_='totalPrice')
            total_price = total_price_div.span.text.strip() if total_price_div else "0"
            
            # 5. 提取单价
            unit_price_div = house.find('div', class_='unitPrice')
            unit_price = unit_price_div.get_text(strip=True) if unit_price_div else "0"
            
            # --- 数据清洗与拼接 ---
            parts = position_text.split('-')
            district = parts[1].strip() if len(parts) > 1 else "未知区县"
            full_district = f"成都市{district}"
            keyword_str = f"{full_district}|{house_info_text}"
            price_clean = total_price.replace("万", "")
            unit_price_clean = unit_price.replace("元/平", "").replace(",", "")

            if price_clean != "0":
                data_rows.append({
                    '房源信息': keyword_str,
                    '房产总价(万元)': price_clean,
                    '单价(元/平)': unit_price_clean
                })
            
        except Exception as e:
            print(f"解析单条房源出错: {e}")
            continue
            
    return data_rows

def save_to_excel(data, filename):
    """
    将数据保存到 Excel
    """
    if os.path.exists(filename):
        try:
            existing_df = pd.read_excel(filename)
            # 合并数据
            new_df = pd.DataFrame(data)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        except Exception as e:
            print(f"读取旧文件失败，将创建新文件: {e}")
            combined_df = pd.DataFrame(data)
    else:
        combined_df = pd.DataFrame(data)
    
    # 重新生成序号列 (A列)
    # 检查列是否存在，避免重复插入报错
    if '序号' in combined_df.columns:
        combined_df.drop(columns=['序号'], inplace=True)
    combined_df.insert(0, '序号', range(1, len(combined_df) + 1))
    
    try:
        combined_df.to_excel(filename, index=False)
        print(f"成功保存 {len(data)} 条数据到 {filename}，当前总计 {len(combined_df)} 条。")
    except Exception as e:
        print(f"保存 Excel 失败: {e}")

def main():
    print("正在启动浏览器，请稍候...")
    driver = setup_driver()
    
    print("开始爬取链家二手房数据...")
    
    # 设置输出目录
    output_dir = r"G:\Apps\VSCode\Projects\Outputs\房源信息"
    
    # 如果目录不存在，则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"已创建输出目录: {output_dir}")
    
    # 生成带时间戳的文件名
    current_time = datetime.datetime.now().strftime("%Y%m%d-%H-%M-%S")
    # 拼接完整路径
    output_filename_with_time = os.path.join(output_dir, f"房源信息-{current_time}.xlsx")
    
    all_data = []
    page = 1
    
    try:
        while len(all_data) < information_each_city:
            # 构造分页URL
            if page == 1:
                target_url = BASE_URL
            else:
                target_url = f"{BASE_URL}pg{page}/"
                
            print(f"\n正在抓取第 {page} 页: {target_url}")
            
            # 使用 Selenium 获取页面
            html_content = get_house_list_selenium(driver, target_url)
            
            if html_content:
                new_data = parse_html(html_content)
                if new_data:
                    all_data.extend(new_data)
                    print(f"已收集 {len(all_data)} 条有效数据，目标 {information_each_city} 条。")
                    
                    save_to_excel(all_data, output_filename_with_time)
                    
                    if len(all_data) >= information_each_city:
                        print("已达到目标数据量，停止抓取。")
                        break
                    
                    # 随机延时，模拟人类浏览
                    sleep_time = random.uniform(3, 8)
                    print(f"等待 {sleep_time:.2f} 秒后继续...")
                    time.sleep(sleep_time)
                    
                    page += 1
                else:
                    print("当前页未解析到有效数据，可能已到最后一页。")
                    break
            else:
                print("获取页面内容失败，停止抓取。")
                break

    except KeyboardInterrupt:
        print("\n检测到用户中断，正在保存当前数据...")
        if all_data:
            save_to_excel(all_data, output_filename_with_time)
        print("程序已退出。")
    finally:
        # 确保退出时关闭浏览器
        print("正在关闭浏览器...")
        driver.quit()
        print("爬取任务结束。")

if __name__ == "__main__":
    main()
