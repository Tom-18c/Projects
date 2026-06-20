import subprocess
import sys
import shlex

def curl_bash_to_download(curl_bash: str, save_path: str = "downloaded_file.mp3"):
    """
    把浏览器复制的 curl bash 直接转换成下载命令，自动保存文件
    """
    # 替换换行、空格
    curl_bash = curl_bash.replace("\\\n", "").replace("\\", "").strip()
    
    # 解析 curl 命令
    args = shlex.split(curl_bash)
    
    # 自动添加保存参数
    args += ["-o", save_path]
    
    print(f"🚀 开始下载：{save_path}")
    
    # 执行下载
    try:
        subprocess.run(args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
        print(f"✅ 下载完成！文件保存到：{save_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ 下载失败：{e.stderr}")

if __name__ == "__main__":
    print("=" * 50)
    print("  cURL Bash 自动下载工具（爱给网/音频/视频通用）")
    print("=" * 50)
    
    # ======================================
    # 👇 在这里粘贴你从浏览器复制的 curl bash
    # ======================================
    curl_command = """
curl 'https://s2.aigei.com/src/aud/mp3/36/36cedd0b131d420a9493823bcf3719cf.mp3?e=1775994780&token=P7S2Xpzfz11vAkASLTkfHN7Fw-oOZBecqeJaxypL:m12ooY2Be7juKKtisu1FStEupGE=' \
  -H 'accept: */*' \
  -H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8' \
  -b 'gei_d_u=cced5c846bd04077bed654f617cc4fd9; gei_d_1=d9e38d327d1093e894bad920346fa399de0bc62d664ac9569f54414849da4d46133ace02b8920ec43e18a213da7bdf9499bdd2c8544b92d2b7cc89de00ca531b; hhhssi1ill1i=304bc63ea23fb2df5fe5f7bff50f04d4; oOO0OO0oOO00oo0o=true; OooOO000oOOO00o=d2f7174de4bb49a58fa000d193f314d1; wueiornjk234kj=6c3292772a3f4b399fd6f4d221b0262e; Hm_lvt_0e0ebfc9c3bdbfdcaa48ccbc43e864f9=1775986435,1775989520; HMACCOUNT=B611EA933110132C; Hm_lpvt_0e0ebfc9c3bdbfdcaa48ccbc43e864f9=1775991241' \
  -H 'priority: i' \
  -H 'range: bytes=0-' \
  -H 'referer: https://www.aigei.com/' \
  -H 'sec-ch-ua: "Chromium";v="146", "Not-A.Brand";v="24", "Microsoft Edge";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'sec-fetch-dest: audio' \
  -H 'sec-fetch-mode: no-cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0'
    """

    # 保存的文件名（可自己改）
    save_file = "我的音频文件.mp3"

    # 开始下载
    curl_bash_to_download(curl_command, save_file)