"""
Coding 1 : 给定一个只包含不同整数的数组，求出任意两元素之间的最小绝对差，output 所有差值等于这个最小值的pair，pair里比较小的数线输出。所有元素升序排列之后print。排序＋线性扫描。写完问input的取值范围，有界的话可以忽略排列优化解法。
"""
def find_min_difference_pairs(nums):
    # edge case: need at least 2 elements to form pairs
    if len(nums) < 2:
        return []
    
    # step 1: sort array in ascending order for optimal adjacent comparison
    sorted_nums = sorted(nums)  # O(n log n)
    
    # step 2: find minimum absolute difference by scanning adjacent elements
    min_diff = float('inf')
    for i in range(len(sorted_nums) - 1):
        # since array is sorted, adjacent elements give minimum possible difference
        current_diff = sorted_nums[i + 1] - sorted_nums[i]
        min_diff = min(min_diff, current_diff)
    
    # step 3: collect all pairs with minimum difference
    result_pairs = []
    for i in range(len(sorted_nums) - 1):
        current_diff = sorted_nums[i + 1] - sorted_nums[i]
        if current_diff == min_diff:
            # add pair with smaller number first
            result_pairs.append((sorted_nums[i], sorted_nums[i + 1]))
    
    return result_pairs
