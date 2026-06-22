import requests
import json
import sys
import os


# 发送请求并保存到本地
def tom_send_request(module: str, url: str, headers: dict, other_data: dict):
    if module == "post":
        get_r1 = requests.post(url, data=other_data, headers=headers)
        # print(get_r1.json())
        print("=" * 20)
        return get_r1.json()
        pass
    elif module == "get":
        pass
    else:
        raise ValueError("请输入正确的请求方式！")
    pass


# 保存数据到本地
def tom_save_response(target_dir: str, filename: str, data: dict):
    os.makedirs(target_dir, exist_ok=True)
    XX = os.path.join(target_dir, "filename")
    with open(os.path.join(target_dir, filename), "w", encoding="utf-8") as f:
        json.dump(XX, f, ensure_ascii=False, indent=4)


# 校验返回数据是否正确
def tom_check_response(response_json_file: str):
    with open(response_json_file, "r", encoding="utf-8") as f_cheak:
        response_json = json.load(f_cheak)
        print(response_json)
        if response_json["errcode"] == 40001:
            xcx_id = "wx4ed1cfeddfc9de0c"
            xcx_pw = "decb870a2e94954c3ac4f0929b9f97c5"
            url = "https://api.weixin.qq.com/cgi-bin/stable_token"
            response_json2 = tom_send_request("post", url, None, {"appid": xcx_id, "secret": xcx_pw})
            tom_save_response(target_dir, "token.json", response_json2)
            return False
        else:
            print("response is ok")
            return True


if __name__ == "__main__":
    target_dir = r"G:\Apps\VSCode\Projects\Learn and Think\Call API\Data"
    # target_dir = os.path.join(os.path.dirname(__file__), "Learn and Think", "Call API", "Data")
    language_translate_before = "zh_CN"
    language_translate_after = "en_US"
    content = "你好，世界！"

    # api调用步骤1-准备基本信息-接口地址
    call_api_url_front = "https://api.weixin.qq.com/cgi-bin/media/voice/translatecontent"
    call_api_url_behind = f"?access_token=ACCESS_TOKEN&lfrom={language_translate_before}&lto={language_translate_after}"
    call_api_url = f"{call_api_url_front}{call_api_url_behind}"

    # api调用步骤1-准备基本信息-接口请求头
    load_data = {"content": content}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    # api调用步骤2-获取数据
    response_json = tom_send_request("post", call_api_url, headers, load_data)
    print(response_json)
    tom_save_response(target_dir, "response.json", response_json)
    tom_check_response(os.path.join(target_dir, "response.json"))


# 获取稳定版接口调用凭据
# /cgi-bin/stable_token
