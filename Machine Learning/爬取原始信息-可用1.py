import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os
import datetime

# --- 配置部分 ---
# 目标URL (链家成都新津区二手房示例)
BASE_URL = "https://cd.lianjia.com/ershoufang/rs/"

# 请求头，模拟浏览器访问，防止被反爬
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://cd.lianjia.com/'
}

def get_house_list(url):
    """
    获取房源列表页数据
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)

        if response.status_code == 200:
            # 打印响应的前500个字符，用于调试
            print(f"Debug - Response Content (First 500 chars):\n{response.text[:500]}") 
            return response.text
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"请求发生错误: {e}")
        return None

def parse_html(html):
    """
    解析HTML，提取房源信息
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # 修改点：尝试匹配包含 LOGCLICKDATA 的 li 标签
    # 使用 lambda 函数检查 class 属性是否包含 'LOGCLICKDATA'
    house_list = soup.find_all('li', class_=lambda x: x and 'LOGCLICKDATA' in x)
    
    # 如果上面的方法没有找到，尝试查找父容器
    if not house_list:
        print("尝试通过父容器查找房源...")
        list_content = soup.find('ul', class_='sellListContent')
        if list_content:
            house_list = list_content.find_all('li')
        else:
            print("未找到房源列表容器。")
            return []
    
    print(f"找到 {len(house_list)} 个房源条目。")
    
    data_rows = []
    
    for house in house_list:
        try:
            # 1. 提取标题 (包含小区名)
            title_div = house.find('div', class_='title')
            title = title_div.a.text.strip() if title_div else "无标题"
            
            # 2. 提取位置信息 (小区名 - 区域)
            # 例如：金秋乐园二期 - 花源
            position_div = house.find('div', class_='positionInfo')
            position_text = position_div.get_text(strip=True, separator='|') if position_div else "未知位置"
            
            # 3. 提取房屋属性 (室厅 | 面积 | 朝向 | 装修 | 楼层 | 类型)
            # 例如：2室1厅 | 71.42平米 | 南 | 简装 | 高楼层(共7层) | 塔楼
            house_info_div = house.find('div', class_='houseInfo')
            house_info_text = house_info_div.get_text(strip=True, separator='|') if house_info_div else "未知信息"
            
            # 4. 提取总价 (例如：35万)
            total_price_div = house.find('div', class_='totalPrice')
            total_price = total_price_div.span.text.strip() if total_price_div else "0"
            
            # 5. 提取单价 (例如：4901元/平)
            unit_price_div = house.find('div', class_='unitPrice')
            unit_price = unit_price_div.get_text(strip=True) if unit_price_div else "0"
            
            # --- 数据清洗与拼接 ---
            
            # 提取区县：根据示例，我们需要精确到区县。
            # 链家的位置信息通常是 "小区名 - 区域名"。
            # 我们尝试从 position_text 中提取区域名。
            parts = position_text.split('-')
            district = parts[1].strip() if len(parts) > 1 else "未知区县"
            
            # 拼接 B 列关键词：区县 | 房屋属性
            # 根据要求：成都市新津区|2室1厅|71.42平米|南|简装|高楼层(共7层)|塔楼
            # 这里我们假设 "成都市" 是固定的，如果你在其他城市爬取，可以修改这里
            # 如果 position_text 包含了完整的行政区名，直接用 district 即可
            # 为了符合你的示例 "成都市新津区"，我们手动加上 "成都市"
            full_district = f"成都市{district}"
            
            # 拼接关键词
            # 格式：区县 | 房屋属性 (用 | 分割)
            keyword_str = f"{full_district}|{house_info_text}"
            
            # 清洗总价：去掉 "万"
            price_clean = total_price.replace("万", "")
            
            # 清洗单价：去掉 "元/平"
            unit_price_clean = unit_price.replace("元/平", "").replace(",", "")

            # 只有当总价不为 "0" 时才保存数据
            if price_clean != "0":
                data_rows.append({
                    '房源信息': keyword_str,
                    '房产总价(万元)': price_clean,
                    '单价(元/平)': unit_price_clean
                })
            else:
                print(f"跳过无效数据: 标题='{title}', 总价=0")
            
        except Exception as e:
            print(f"解析单条房源出错: {e}")
            continue
            
    return data_rows

def save_to_excel(data, filename):
    """
    将数据保存到 Excel，如果文件存在则追加（模拟），不存在则新建。
    为了简单起见，这里每次读取旧数据，合并新数据，然后覆盖写入。
    这样可以保证程序意外终止后数据不丢失。
    """
    # 如果文件已存在，读取旧数据
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
    combined_df.insert(0, '序号', range(1, len(combined_df) + 1))
    
    # 保存到 Excel
    try:
        combined_df.to_excel(filename, index=False)
        print(f"成功保存 {len(data)} 条数据到 {filename}，当前总计 {len(combined_df)} 条。")
    except Exception as e:
        print(f"保存 Excel 失败: {e}")

def main():
    print("开始爬取链家二手房数据...")
    
    # 生成带时间戳的文件名，格式：房源信息-YYYYMMDD-HH-MM-SS.xlsx
    current_time = datetime.datetime.now().strftime("%Y%m%d-%H-%M-%S")
    output_filename_with_time = f"房源信息-{current_time}.xlsx"
    
    # 第一页
    target_url = BASE_URL
    print(f"正在抓取: {target_url}")
    
    html_content = get_house_list(target_url)
    
    if html_content:
        new_data = parse_html(html_content)
        if new_data:
            # 使用带时间戳的文件名
            save_to_excel(new_data, output_filename_with_time)
        else:
            print("未在当前页面解析到数据。")
    else:
        print("获取页面内容失败。")
        
    # --- 如果需要爬取多页，可以在这里添加循环 ---
    # 链家的分页规则通常是 rs/pg2/, rs/pg3/ ...
    # 示例：
    # for page in range(1, 3): # 爬取前2页
    #     url = f"{BASE_URL}pg{page}/"
    #     # ... 重复请求和解析逻辑 ...
    #     time.sleep(random.uniform(1, 3)) # 随机延时，礼貌爬取

    print("爬取任务结束。")

if __name__ == "__main__":
    main()
