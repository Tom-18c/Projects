from typing import Union


class Feature_OnlyStoreData_Str_Int:
    # 仅用作存储数据
    def __init__(self, tom_feature_str: str, tom_which_location: int = 1) -> None:
        self.tom_feature_str = tom_feature_str
        self.tom_which_location = tom_which_location
        # self.tom_find_next = tom_find_next


def tom_calculate_next_current(feature_str):
    # next数组计算方式，表示当前最大相同前后缀字符数
    # 初始化：tom_next结果数组、tom_pre当前位置最大相同前后缀字符数、tom_j当前位置指针
    tom_next = [0] * len(feature_str)
    tom_pre, tom_j = 0, 1

    # tom_j只增不减
    while tom_j < len(feature_str):
        if feature_str[tom_j] == feature_str[tom_pre]:
            # 当前位置能继续匹配字符，最大相同前后缀字符数加1，指针右移
            tom_pre += 1
            tom_next[tom_j] = tom_pre
            tom_j += 1
        elif tom_pre > 0:
            # 未回溯到字符串首，进行回溯操作
            tom_pre = tom_next[tom_pre - 1]
        else:
            # 已回溯到字符串首，指针右移，计算下一个
            tom_next[tom_j] = tom_pre
            tom_j += 1

    # print("特征字符串next数组为：", tom_next)
    return tom_next


def tom_kmp(main_str, feature_str, tom_next, tom_kmp_i=0):
    if tom_kmp_i < 0:
        return -1

    # 初始化：tom_kmp_i为主字符串指针、tom_kmp_j为特征字符串指针
    tom_kmp_j = 0
    tom_main_str_len = len(main_str)
    tom_feature_str_len = len(feature_str)

    # tom_kmp_i只增不减
    while tom_kmp_i < tom_main_str_len and tom_kmp_j < tom_feature_str_len:
        if main_str[tom_kmp_i] == feature_str[tom_kmp_j]:
            # 当前位置能继续匹配字符，两指针同时右移
            tom_kmp_i += 1
            tom_kmp_j += 1
        elif tom_kmp_j > 0:
            # 未回溯到特征字符串首，进行回溯操作
            tom_kmp_j = tom_next[tom_kmp_j - 1]
        else:
            # 已回溯到特征字符串首，主字符串指针右移，计算下一个
            tom_kmp_i += 1

    # 返回匹配结果
    if tom_kmp_j == tom_feature_str_len:
        return tom_kmp_i - tom_kmp_j
    else:
        return -1


def tom_list_all_index(main_str, feature_str):
    tom_all_index = []
    tom_index = 0
    # 只计算一次 tom_next 数组
    tom_next = tom_calculate_next_current(feature_str)

    while True:
        # 将已计算好的 tom_next 传入，避免重复计算
        tom_index = tom_kmp(main_str, feature_str, tom_next, tom_index)
        if tom_index < 0:
            break
        tom_all_index.append(tom_index)
        tom_index += 1

    return tom_all_index


class Tom_Fun_Extract:
    def __init__(self, input_pending_str: str, input_feature_instance: Feature_OnlyStoreData_Str_Int, input_feature_instance2: Union[Feature_OnlyStoreData_Str_Int, None] = None):
        # 输入检查
        if not isinstance(input_pending_str, str):
            raise TypeError(f"input_pending_str must be str, not {type(input_pending_str).__name__}")
        if not isinstance(input_feature_instance, Feature_OnlyStoreData_Str_Int):
            raise TypeError(f"input_feature_instance must be a Feature_OnlyStoreData_Str_Int's instance, not {type(input_feature_instance).__name__}")

        self.input_pending_str = input_pending_str
        self.input_feature_instance = input_feature_instance
        self.input_feature_instance2 = input_feature_instance2

    def tom_before_slice(self):
        # 截取特征
        feature = str(self.input_feature_instance.tom_feature_str)
        feature_location = self.input_feature_instance.tom_which_location

        # 输入检查
        if not isinstance(feature_location, int):
            raise TypeError(f"feature_location must be int, not {type(feature_location).__name__}")
        if feature_location <= 0:
            raise ValueError(f"feature_location must be positive integer, not {feature_location}")

        # 返回结果
        tom_return_str = f"{feature}".join(self.input_pending_str.split(feature)[:feature_location])
        if len(self.input_pending_str) == len(tom_return_str):
            return ""
        return tom_return_str

    def tom_after_slice(self):
        # 截取特征
        feature = str(self.input_feature_instance.tom_feature_str)
        feature_location = self.input_feature_instance.tom_which_location

        # 输入检查
        if not isinstance(feature_location, int):
            raise TypeError(f"feature_location must be int, not {type(feature_location).__name__}")
        if feature_location <= 0:
            raise ValueError(f"feature_location must be positive integer, not {feature_location}")

        # 返回结果
        return f"{feature}".join(self.input_pending_str.split(feature)[feature_location:])

    def tom_before_slide(self):
        # 截取特征
        feature = str(self.input_feature_instance.tom_feature_str)
        feature_location = self.input_feature_instance.tom_which_location

        # 输入检查
        if not isinstance(feature_location, int):
            raise TypeError(f"feature_location must be int, not {type(feature_location).__name__}")
        if feature_location <= 0:
            raise ValueError(f"feature_location must be positive integer, not {feature_location}")

        # 找出所有特征字符串出现的位置
        index_position = tom_list_all_index(self.input_pending_str, feature)
        # print("特征所在原字符串索引：", index_position)
        if not index_position or feature_location > len(index_position):
            return ""
        return self.input_pending_str[: index_position[feature_location - 1]]

    def tom_after_slide(self):

        # 截取特征
        feature = str(self.input_feature_instance.tom_feature_str)
        feature_location = self.input_feature_instance.tom_which_location

        # 输入检查
        if not isinstance(feature_location, int):
            raise TypeError(f"feature_location must be int, not {type(feature_location).__name__}")
        if feature_location <= 0:
            raise ValueError(f"feature_location must be positive integer, not {feature_location}")

        # 找出所有特征字符串出现的位置
        index_position = tom_list_all_index(self.input_pending_str, feature)
        # print("特征所在原字符串索引：", index_position)
        if not index_position or feature_location > len(index_position):
            return ""
        return self.input_pending_str[index_position[feature_location - 1] + len(feature) :]

    def tom_between_slice(self):
        # 输入检查
        if not isinstance(self.input_feature_instance2, Feature_OnlyStoreData_Str_Int):
            raise TypeError(f"input_feature_instance2 must be a Feature_OnlyStoreData_Str_Int's instance, not {type(self.input_feature_instance2).__name__}")

        # 返回结果
        # 掐头
        tom_process_str = Tom_Fun_Extract(self.input_pending_str, self.input_feature_instance).tom_after_slice()
        if tom_process_str == "":
            return ""
        # 去尾
        tom_return_str = Tom_Fun_Extract(tom_process_str, self.input_feature_instance2).tom_before_slice()
        return tom_return_str

    def tom_between_slide(self):
        # 输入检查
        if not isinstance(self.input_feature_instance2, Feature_OnlyStoreData_Str_Int):
            raise TypeError(f"input_feature_instance2 must be a Feature_OnlyStoreData_Str_Int's instance, not {type(self.input_feature_instance2).__name__}")

        # 返回结果
        # 掐头
        tom_process_str = Tom_Fun_Extract(self.input_pending_str, self.input_feature_instance).tom_after_slide()
        if tom_process_str == "":
            return ""
        # 去尾
        tom_return_str = Tom_Fun_Extract(tom_process_str, self.input_feature_instance2).tom_before_slide()
        return tom_return_str


"""
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
"""
