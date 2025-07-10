# -*- coding: utf-8 -*-
# 二分查找各种写法及注释说明

def binary_search(arr, target):
    """
    标准二分查找，查找等于target的元素下标
    """
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            # 目标在右侧，left右移
            left = mid + 1
        else:
            # 目标在左侧，right左移
            right = mid - 1
    return -1

def lower_bound(arr, target):
    """
    查找第一个大于等于target的位置（lower_bound）
    """
    left, right = 0, len(arr) - 1
    ans = -1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] >= target:
            # 记录答案，继续往左找
            ans = mid
            right = mid - 1
        else:
            # 目标在右侧
            left = mid + 1
    return ans

def upper_bound(arr, target):
    """
    查找第一个大于target的位置（upper_bound）
    """
    left, right = 0, len(arr) - 1
    ans = -1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] > target:
            # 记录答案，继续往左找
            ans = mid
            right = mid - 1
        else:
            # 目标在右侧
            left = mid + 1
    return ans

def last_le(arr, target):
    """
    查找最后一个小于等于target的位置
    """
    left, right = 0, len(arr) - 1
    ans = -1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] <= target:
            # 记录答案，继续往右找
            ans = mid
            left = mid + 1
        else:
            # 目标在左侧
            right = mid - 1
    return ans

def last_lt(arr, target):
    """
    查找最后一个小于target的位置
    """
    left, right = 0, len(arr) - 1
    ans = -1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] < target:
            # 记录答案，继续往右找
            ans = mid
            left = mid + 1
        else:
            # 目标在左侧
            right = mid - 1
    return ans

# 总结：
# 1. arr[mid] < target: 目标在右边，left = mid + 1
# 2. arr[mid] > target: 目标在左边，right = mid - 1
# 3. arr[mid] == target: 找到目标，返回mid
# 4. 查找第一个 >= target: 用 >=，right = mid - 1
# 5. 查找第一个 > target: 用 >，right = mid - 1
# 6. 查找最后一个 <= target: 用 <=，left = mid + 1
# 7. 查找最后一个 < target: 用 <，left = mid + 1

# 记忆口诀：
# 想要“更大”就往右（left = mid + 1）
# 想要“更小”就往左（right = mid - 1）
# 满足条件时记录答案，然后继续缩小范围，寻找更优解

if __name__ == "__main__":
    arr = [1, 2, 4, 4, 5, 7, 9]
    target = 4
    print("标准二分查找:", binary_search(arr, target))
    print("第一个大于等于target的位置:", lower_bound(arr, target))
    print("第一个大于target的位置:", upper_bound(arr, target))
    print("最后一个小于等于target的位置:", last_le(arr, target))
    print("最后一个小于target的位置:", last_lt(arr, target))
