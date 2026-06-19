import sys
import os

# 基于当前工作空间构建目标路径，并添加到系统路径中
target_dir = os.path.join(os.path.dirname(__file__), "Feature Module", "Mature Feature Module")
if target_dir not in sys.path:
    sys.path.append(target_dir)


# 导入 Functions.py 中的类和函数
from Tom_Functions import Tom_Fun_Extract, Feature_OnlyStoreData_Str_Int

# 用法举例
any_str = "968888+888888888880>520≤2350≤2400≤2700<5555"
feature_1 = Feature_OnlyStoreData_Str_Int("<", 1)
feature_2 = Feature_OnlyStoreData_Str_Int("≤", 3)
feature_3 = Feature_OnlyStoreData_Str_Int("888", 3)
print("========================================================================================")
print(f"以{feature_3.tom_feature_str}为特征，使用切片法，截取第{feature_3.tom_which_location}个特征前的所有内容，否则结果为空：")
print(Tom_Fun_Extract(any_str, feature_3).tom_before_slice())
print(f"以{feature_3.tom_feature_str}为特征，使用滑动法，截取第{feature_3.tom_which_location}个特征前的所有内容，否则结果为空：")
print(Tom_Fun_Extract(any_str, feature_3).tom_before_slide())
print("========================================================================================")
print(f"以{feature_3.tom_feature_str}为特征，使用切片法，截取第{feature_3.tom_which_location}个特征后的所有内容，否则结果为空：")
print(Tom_Fun_Extract(any_str, feature_3).tom_after_slice())
print(f"以{feature_3.tom_feature_str}为特征，使用滑动法，截取第{feature_3.tom_which_location}个特征后的所有内容，否则结果为空：")
print(Tom_Fun_Extract(any_str, feature_3).tom_after_slide())
print("========================================================================================")

# 用法举例2
any_str2 = "hhh门扇配2100mm，门扇开孔距下口600mmm，门扇开孔距锁方200mm，门扇离地3公分"
feature_11 = Feature_OnlyStoreData_Str_Int("开孔距下口", 1)
feature_12 = Feature_OnlyStoreData_Str_Int("mm", 2)
feature_13 = Feature_OnlyStoreData_Str_Int("门扇", 2)
print("========================================================================================")
print(Tom_Fun_Extract(any_str2, feature_11, feature_12).tom_between_slice())
print(Tom_Fun_Extract(any_str2, feature_13, feature_12).tom_between_slice())
print("========================================================================================")
print(Tom_Fun_Extract(any_str2, feature_11, feature_12).tom_between_slide())
print(Tom_Fun_Extract(any_str2, feature_13, feature_12).tom_between_slide())
print("========================================================================================")
