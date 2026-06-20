def js(num):
    if num == 0:
        return 1
    else:
        return num * js(num - 1)


num1 = input("请输入一个数：")

try:
    # 尝试将输入转换为整数
    num1 = int(num1)
    if num1 >= 0:
        print("输入正确")
        print(js(num1))  # 移除了多余的 int() 转换
    else:
        print("输入负数，无法计算")
except ValueError:
    # 如果转换失败，说明输入的不是有效的整数
    print("输入非整数，无法计算")
