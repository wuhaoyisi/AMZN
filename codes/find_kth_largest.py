import heapq
import random

def find_kth_largest_sorting(deliveries, k):
    """
    原始版本：使用排序
    时间复杂度: O(n log n)
    空间复杂度: O(n)
    """
    if k <= 0 or k > len(deliveries):
        return None
    
    sorted_list = sorted(deliveries, reverse=True)
    return sorted_list[k-1]

def find_kth_largest_min_heap(deliveries, k):
    """
    最小堆版本：维护大小为k的最小堆
    时间复杂度: O(n log k)
    空间复杂度: O(k)
    适合k较小的情况
    """
    if k <= 0 or k > len(deliveries):
        return None
    
    # 维护大小为k的最小堆 min_heap for the larger half, so min[0] would be kth largestes, k-1 min would be replaced.
    min_heap = []
    
    for delivery in deliveries:
        if len(min_heap) < k:
            heapq.heappush(min_heap, delivery)
        elif delivery > min_heap[0]:
            # 当前元素比堆顶大，替换堆顶
            heapq.heapreplace(min_heap, delivery)
    
    # 堆顶就是第k大元素
    return min_heap[0]