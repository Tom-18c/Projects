import numbers

indata11 = {"88": 1, "0<": 1, "≤": 2}
indata_illegal = {"8X8": 1, "≤": 10, "0<": None, "88": "2"}
a = "9688+8880<520≤2350≤2400≤2700"
b = "1234888888567"
indata_b = {"88": 3}


class Tom_Fun_Extract:
    def __init__(self, input_pending_str, input_dict):
        # 输入检查
        if not isinstance(input_pending_str, str):
            raise TypeError(f"input_pending_val must be str, not {type(input_pending_str).__name__}")
        if not isinstance(input_dict, dict):
            raise TypeError(f"input_dict must be a dictionary, not {type(input_dict).__name__}")

        self.input_pending_str = input_pending_str
        self.input_dict = input_dict

    def tom_before_slice(self, tom_item=0):
        # 输入检查
        if len(self.input_dict) < tom_item + 1:
            raise IndexError(f"tom_item {tom_item} is out of range for dictionary with length {len(self.input_dict)}")

        # 截取特征
        feature = str([*self.input_dict.items()][tom_item][0])
        feature_start = [*self.input_dict.items()][tom_item][1]

        # 输入检查
        if feature_start is None:
            raise ValueError(f"feature_start for item[{tom_item}] is not provided (None)")
        if not isinstance(feature_start, int):
            raise TypeError(f"feature_start must be int, not {type(feature_start).__name__}")
        if feature_start < 0:
            raise ValueError(f"feature_start must be non-negative, not {feature_start}")

        # 存在性检查
        # if feature not in self.input_pending_str:
        #     raise ValueError(f"feature {feature} not in input_pending_str {self.input_pending_str}")
        return f"{feature}".join(self.input_pending_str.split(feature)[:feature_start])

    def tom_before_slide(self, tom_item=0):
        # 输入检查
        if len(self.input_dict) < tom_item + 1:
            raise IndexError(f"tom_item {tom_item} is out of range for dictionary with length {len(self.input_dict)}")

        # 截取特征
        feature = str([*self.input_dict.items()][tom_item][0])
        feature_start = [*self.input_dict.items()][tom_item][1]

        # 输入检查
        if feature_start is None:
            raise ValueError(f"feature_start for item[{tom_item}] is not provided (None)")
        if not isinstance(feature_start, int):
            raise TypeError(f"feature_start must be int, not {type(feature_start).__name__}")
        if feature_start < 0:
            raise ValueError(f"feature_start must be non-negative, not {feature_start}")

        # 存在性检查
        # if feature not in self.input_pending_str:
        #     raise ValueError(f"feature {feature} not in input_pending_str {self.input_pending_str}")


print("以第1对键值对为特征，从前往后提取直到1个特征：")
print(Tom_Fun_Extract(a, indata11).tom_before_slice())
print("以第2对键值对为特征，从前往后提取直到1个特征：")
print(Tom_Fun_Extract(a, indata11).tom_before_slice(1))
print("以第3对键值对为特征，从前往后提取直到2个特征：")
print(Tom_Fun_Extract(a, indata11).tom_before_slice(2))
print("情况1")
print(Tom_Fun_Extract(a, indata_illegal).tom_before_slice(0))
print(Tom_Fun_Extract(a, indata_illegal).tom_before_slice(1))
# print(Tom_Fun_Extract(a, indata_illegal).tom_before_slice(2))
# print(Tom_Fun_Extract(a, indata_illegal).tom_before_slice(3))
print("情况2")
print(Tom_Fun_Extract(b, indata_b).tom_before_slice())
