import sys
import os
import json

if __name__ == "__main__":
    # 测试模块添加，基于当前工作空间构建目标路径，并添加到系统路径中
    target_dir = os.path.join(os.path.dirname(__file__), "Feature Module", "Mature Feature Module")
    if target_dir not in sys.path:
        sys.path.append(target_dir)

    # 测试对象添加
    tom_test_fun_list = []
    # tom_test_fun_list.append("Tom_Fun_Extract")
    # tom_test_fun_list.append("WeChatTranslate_API")
    tom_test_fun_list.append("批量翻译古诗词")

    if "Tom_Fun_Extract" in tom_test_fun_list:
        # 导入功能模块
        from Tom_Functions_str import Tom_Fun_Extract, Feature_OnlyStoreData_Str_Int

        print("\n以下为字符串截取模块举例说明结果：", end="\n\n")
        # 例
        any_str = "968888+888888888880>520≤2350≤2400≤2700<5555"
        feature_1 = Feature_OnlyStoreData_Str_Int("<", 1)
        feature_2 = Feature_OnlyStoreData_Str_Int("≤", 3)
        feature_3 = Feature_OnlyStoreData_Str_Int("888", 3)
        print("字符串any_str为：", any_str, sep="\t")
        print(f"以{feature_3.tom_feature_str}为特征，使用切片法，截取第{feature_3.tom_which_location}个特征前的所有内容，否则结果为空：", end="\t\t")
        print(Tom_Fun_Extract(any_str, feature_3).tom_before_slice())
        print(f"以{feature_3.tom_feature_str}为特征，使用滑动法，截取第{feature_3.tom_which_location}个特征前的所有内容，否则结果为空：", end="\t\t")
        print(Tom_Fun_Extract(any_str, feature_3).tom_before_slide())
        print(f"以{feature_3.tom_feature_str}为特征，使用切片法，截取第{feature_3.tom_which_location}个特征后的所有内容，否则结果为空：", end="\t\t")
        print(Tom_Fun_Extract(any_str, feature_3).tom_after_slice())
        print(f"以{feature_3.tom_feature_str}为特征，使用滑动法，截取第{feature_3.tom_which_location}个特征后的所有内容，否则结果为空：", end="\t\t")
        print(Tom_Fun_Extract(any_str, feature_3).tom_after_slide())
        print("=" * 128, end="\n\n")

        # 例2
        any_str2 = "hhh门扇配2100mm，门扇开孔距下口600mmm，门扇开孔距锁方200mm，门扇离地3公分"
        feature_11 = Feature_OnlyStoreData_Str_Int("开孔距下口", 1)
        feature_12 = Feature_OnlyStoreData_Str_Int("mm", 2)
        feature_13 = Feature_OnlyStoreData_Str_Int("门扇", 2)
        print("字符串any_str2为：", any_str2, sep="\t")
        print('以第1个"开孔距下口"和在他之后的第2个"mm"为特征，使用切片法，截取他们之间的内容，否则结果为空：', end="\t\t")
        print(Tom_Fun_Extract(any_str2, feature_11, feature_12).tom_between_slice())
        print('以第2个"门扇"和在他之后的第2个"mm"为特征，使用切片法，截取他们之间的内容，否则结果为空：     ', end="\t\t")
        print(Tom_Fun_Extract(any_str2, feature_13, feature_12).tom_between_slice())
        print('以第1个"开孔距下口"和在他之后的第2个"mm"为特征，使用滑动法，截取他们之间的内容，否则结果为空：', end="\t\t")
        print(Tom_Fun_Extract(any_str2, feature_11, feature_12).tom_between_slide())
        print('以第2个"门扇"和在他之后的第2个"mm"为特征，使用滑动法，截取他们之间的内容，否则结果为空：     ', end="\t\t")
        print(Tom_Fun_Extract(any_str2, feature_13, feature_12).tom_between_slide())
        print("=" * 256)

    if "WeChatTranslate_API" in tom_test_fun_list:
        # 导入功能模块
        from Tom_Functions_WeChatTranslate_API import tom_get_credential, tom_translate

        print("\n以下为API调用模块(微信翻译)举例说明结果：", end="\n\n")

        class Articles:
            def __init__(self, title, content, author=""):
                self.title = title
                self.content = content
                self.author = author

        article1 = Articles("过故人庄", "故人具鸡黍，邀我至田家。绿树村边合，青山郭外斜。开轩面场圃，把酒话桑麻。待到重阳日，还来就菊花。", "孟浩然")
        article2 = Articles("登鹳雀楼", "白日依山尽，黄河入海流。欲穷千里目，更上一层楼。", "王之涣")

        # 文件夹路径
        # target_dir = r"G:\Apps\VSCode\Projects\Learn and Think\Call API\Data"
        target_dir = os.path.join(os.path.dirname(__file__), "Learn and Think", "Call API", "Data")
        # 获取翻译凭据
        credential = tom_get_credential(target_dir, "credential_WeChatTranslate.json")

        # 例
        print(f"{article1.title} - {article1.author}", article1.content, sep="\n")
        translate1 = tom_translate(article1.title, credential)
        translate2 = tom_translate(article1.content, credential)
        translate3 = tom_translate(article1.author, credential)
        print(f"{translate1} - {translate3}", translate2, sep="\n")
        print("=" * 128, end="\n\n")
        # 例2
        print(f"{article2.title} - {article2.author}", article2.content, sep="\n")
        translate4 = tom_translate(article2.title, credential)
        translate5 = tom_translate(article2.content, credential)
        translate6 = tom_translate(article2.author, credential)
        print(f"{translate4} - {translate6}", translate5, sep="\n")
        print("=" * 256)

    if "批量翻译古诗词" in tom_test_fun_list:
        # 导入功能模块
        from Tom_Functions_WeChatTranslate_API import tom_get_credential, tom_translate

        # 路径
        # target_dir = r"G:\Apps\VSCode\Projects\Learn and Think\Call API\Data"
        target_dir = os.path.join(os.path.dirname(__file__), "Learn and Think", "Call API", "Data")
        file_name = "at_zh.json"
        # 获取翻译凭据
        credential = tom_get_credential(target_dir, "credential_WeChatTranslate.json")

        # 例
        with open(os.path.join(target_dir, file_name), "r", encoding="utf-8") as f:
            data = json.load(f)
        for key, value in data.items():
            print(key, value["content"], sep="\n")
            translate1 = tom_translate(key, credential)
            translate2 = tom_translate(value["content"], credential)
            print(translate1, translate2, sep="\n")
            print("=" * 128, end="\n\n")
