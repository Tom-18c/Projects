import os
import json


# 保存数据到本地，文件夹不存在则创建
def tom_save_json(target_dir: str, filename: str, data: dict) -> None:
    os.makedirs(target_dir, exist_ok=True)  # 文件夹不存在则创建
    target_file = os.path.join(target_dir, filename)
    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)  # 保存数据到本地
