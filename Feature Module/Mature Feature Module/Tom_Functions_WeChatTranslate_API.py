import requests
import json
import sys
import os
import time

# 基于当前工作空间构建目标路径，并添加到系统路径中
target_dir = os.path.join(os.path.dirname(__file__), "Feature Module", "Mature Feature Module")
if target_dir not in sys.path:
    sys.path.append(target_dir)

from Tom_Functions_Os import tom_save_json


# 计算截至时间，并返回更新后的数据
def tom_calculate_expire_time(data: dict) -> dict:

    current_time = time.time()  # 获取当前时间
    # print("当前时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time)))
    valid_time = data["expires_in"]  # 获取有效时长（s）
    expire_time = current_time + valid_time - 5  # 计算截至时间
    print("获取凭据有效时间截至：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(expire_time)))

    return data | {"credential_get_time": current_time, "credential_expire_time": expire_time}


def need_update_credential(target_dir: str, credential_filename: str = "credential.json") -> bool:

    current_time = time.time()  # 获取当前时间
    try:  # 尝试读取凭据，处理文件不存在的情况
        with open(os.path.join(target_dir, credential_filename), "r", encoding="utf-8") as credential_translate_read:
            data = json.load(credential_translate_read)
    except FileNotFoundError:
        return True
    expire_time = data["credential_expire_time"]  # 获取截至时间

    if current_time < expire_time:  # 判断是否需要更新凭据
        return False
    return True


def tom_get_credential(target_dir: str, credential_filename: str = "credential.json"):
    # 凭据有效时长7200s，用小程序id和密钥获取凭据
    xcx_id = "wx4ed1cfeddfc9de0c"
    xcx_pw = "decb870a2e94954c3ac4f0929b9f97c5"
    get_credential_url = "https://api.weixin.qq.com/cgi-bin/stable_token"
    credential_request_data = {"grant_type": "client_credential", "appid": xcx_id, "secret": xcx_pw}
    try_count = 1
    need_update = True
    while try_count <= 3 and need_update:
        need_update = need_update_credential(target_dir, credential_filename)
        if need_update:
            try:
                credential_translate_post = requests.post(get_credential_url, json=credential_request_data)
                credential_translate = credential_translate_post.json()
                # print("获取的凭据信息：", credential_translate)
                credential_translate_processed = tom_calculate_expire_time(credential_translate)
                tom_save_json(target_dir, credential_filename, credential_translate_processed)
                pass

            except Exception as e:
                print(f"Error occurred while importing get_credential: {e}")
                try_count += 1
                time.sleep(3)
        else:
            print(f"第{try_count}次获取凭据有效")

    if try_count > 3:
        raise Exception("获取凭据失败，请检查网络连接或小程序id和密钥是否正确")
    with open(os.path.join(target_dir, credential_filename), "r", encoding="utf-8") as credential_translate_read:
        credential = json.load(credential_translate_read)
    return credential["access_token"]


def tom_translate(text: str, credential: str, translate_type: str = "中译英") -> str:
    # 输入检查
    if translate_type == "中译英":
        translate_info = {"access_token": credential, "from": "zh_CN", "to": "en_US"}
    elif translate_type == "英译中":
        translate_info = {"access_token": credential, "from": "en_US", "to": "zh_CN"}
    else:
        raise Exception("翻译类型错误，请输入 中译英 或 英译中 ")

    # 翻译API地址
    translate_url_front = "https://api.weixin.qq.com/cgi-bin/media/voice/translatecontent"
    translate_url_behind = f"?access_token={translate_info['access_token']}&lfrom={translate_info['from']}&lto={translate_info['to']}"
    translate_url = translate_url_front + translate_url_behind

    translate_return_data = requests.post(translate_url, data=text).json()
    # print("翻译返回数据：", translate_return_data)
    translate_return_text = translate_return_data["to_content"]
    return translate_return_text
