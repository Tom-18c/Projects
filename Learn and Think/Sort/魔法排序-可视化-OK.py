import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import random
def merge_sort(arr, visualize=False):
    """
    归并排序算法
    参数:
        arr: 待排序的列表
        visualize: 是否可视化排序过程
    返回:
        排序后的列表
    """
    if visualize:
        return merge_sort_visualized(arr)
    return merge_sort_helper(arr)


def merge_sort_helper(arr):
    """
    归并排序的辅助函数（不包含可视化）
    """
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left_half = merge_sort_helper(arr[:mid])
    right_half = merge_sort_helper(arr[mid:])
    
    return merge(left_half, right_half)


def merge_sort_visualized(arr):
    """
    带可视化的归并排序
    """
    # 创建图形
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title("归并排序可视化")

    
    # 初始化条形图
    bars = ax.bar(range(len(arr)), arr, align='edge')
    ax.set_xlim(0, len(arr))
    ax.set_ylim(0, max(arr) * 1.1)
    
    # 存储排序过程中的状态
    states = []
    
    def merge(arr, left, mid, right):
        """
        合并两个已排序的子数组，并记录状态
        """
        left_arr = arr[left:mid+1]
        right_arr = arr[mid+1:right+1]
        
        i = j = 0
        k = left
        
        while i < len(left_arr) and j < len(right_arr):
            if left_arr[i] <= right_arr[j]:
                arr[k] = left_arr[i]
                i += 1
            else:
                arr[k] = right_arr[j]
                j += 1
            k += 1
            states.append(arr.copy())
        
        while i < len(left_arr):
            arr[k] = left_arr[i]
            i += 1
            k += 1
            states.append(arr.copy())
        
        while j < len(right_arr):
            arr[k] = right_arr[j]
            j += 1
            k += 1
            states.append(arr.copy())
    
    def merge_sort_recursive(arr, left, right):
        """
        递归实现归并排序，并记录状态
        """
        if left < right:
            mid = (left + right) // 2
            merge_sort_recursive(arr, left, mid)
            merge_sort_recursive(arr, mid+1, right)
            merge(arr, left, mid, right)
    
    # 执行排序并记录状态
    merge_sort_recursive(arr.copy(), 0, len(arr)-1)
    
    def update(frame):
        """更新动画帧"""
        for bar, val in zip(bars, states[frame]):
            bar.set_height(val)
        return bars
    
    # 创建动画
    ani = animation.FuncAnimation(
        fig, 
        update, 
        frames=len(states), 
        interval=0, 
        blit=True,
        repeat=False
    )
    
    plt.show()
    return arr


def merge(left, right):
    """
    合并两个已排序的列表
    """
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result


# 测试代码
if __name__ == "__main__":
    # 设置随机数种子，确保每次运行结果一致（可选）
    # random.seed(42)
    
    # 生成随机测试用例
    print("归并排序测试结果：")
    for i in range(1):  # 生成5个随机测试用例
        arr = [random.randint(4000, 10000) for _ in range(100)]
        sorted_arr = merge_sort(arr.copy())
        print(f"测试用例 {i+1}:")
        print(f"  原始数组长度: {len(arr)}")
        print(f"  排序结果前10个元素: {sorted_arr[:10]}...\n")
    
    # 可视化示例
    print("正在启动可视化演示...")
    visualize_arr = arr
    print(f"可视化数组长度: {len(visualize_arr)}")
    merge_sort(visualize_arr, visualize=True)


