"""
给定一个由互不相同的正整数组成的数组a，以及另一个包含多次「左循环旋转次数」的数组 rotate。对于 rotate 中的每个数值k，对原始数组a执行k次左循环旋转，找到旋转后的数组中最大元素的index，吧所有index按顺序组成新数组并且返回。找到原始数组的 max, 然后用（orig_idx- k_mod）% n 获得新 位置
"""
def find_max_index_after_rotations(a, rotate):
    # edge case: empty array
    if not a:
        return []
    
    n = len(a)
    
    # step 1: find max element and its original index - O(n)
    max_value = max(a)
    original_max_index = a.index(max_value)
    
    result_indices = []
    
    # step 2: for each rotation, calculate new position using math formula
    for k in rotate:
        # left rotation by k: element at index i moves to (i - k) % n
        # handle negative results with proper modulo
        k_mod = k % n  # optimize for large k values
        new_max_index = (original_max_index - k_mod) % n
        result_indices.append(new_max_index)
    
    return result_indices

# helper function to demonstrate actual rotation (for verification)
def rotate_array_left(arr, k):
    # actual left rotation for testing - O(n)
    n = len(arr)
    k = k % n
    return arr[k:] + arr[:k]
