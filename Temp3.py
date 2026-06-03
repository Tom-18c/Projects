# 滑动提取字符串
A = "123458888867890"
B = "1212121"

# def cheak_b_a()


# 自创算法，复杂度O(n^3)
def get_next_arr(pattern: str) -> list:
    pattern_len = len(pattern)
    next_arr = [0] * pattern_len
    # return next_arr

    cheak_start = 0
    cheak_pointer = 0
    # while cheak_pointer < pattern_len-1:
    for cheak_index in range(0, pattern_len):
        pattern_cut = pattern[: cheak_index + 1]
        if len(pattern_cut) <= 1:
            continue
        else:
            cheak_pointer = cheak_index
            cheak_flag = 1
            while cheak_pointer > 0 and cheak_flag == 1:
                if pattern_cut[:cheak_pointer] == pattern_cut[-cheak_pointer:]:
                    next_arr[cheak_index] = cheak_pointer
                    cheak_flag = 0
                    break
                else:
                    cheak_pointer -= 1

    return next_ar


C = get_next_arr(B)
print(C)
# print(result)
