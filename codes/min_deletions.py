"""
Problem Summary
Task: Determine the minimum number of deletions required to transform two input strings into anagrams of each other.
Approach:

Count Character Frequencies: Track occurrences of each character in both strings.

Identify Common Characters: For each character, take the minimum count between the two strings.

Calculate Deletions: Subtract twice the total common characters from the combined length of both strings.
"""
from collections import Counter

def makeAnagram(s1, s2):
    """
    计算使两个字符串变为anagram所需的最小删除次数
    
    思路：
    1. 统计两个字符串的字符频次
    2. 对每个字符，计算两个字符串中该字符出现次数的差值
    3. 将所有差值的绝对值相加
    """
    if not s1 and not s2:
        return 0
    
    # 统计字符频次
    count1 = Counter(s1)
    count2 = Counter(s2)
    
    # 获取所有出现的字符
    all_chars = set(count1.keys()) | set(count2.keys())
    
    total_deletions = 0
    
    # 计算每个字符需要删除的次数
    for char in all_chars:
        freq1 = count1.get(char, 0)
        freq2 = count2.get(char, 0)
        # 删除次数 = 两个字符串中该字符频次差的绝对值
        total_deletions += abs(freq1 - freq2)
    
    return total_deletions

def makeAnagramOptimized(s1, s2):
    """
    优化版本：直接在一次遍历中计算差值
    """
    if not s1 and not s2:
        return 0
    
    # 使用一个字典记录字符频次差
    char_diff = {}
    
    # s1中的字符计数+1
    for char in s1:
        char_diff[char] = char_diff.get(char, 0) + 1
    
    # s2中的字符计数-1
    for char in s2:
        char_diff[char] = char_diff.get(char, 0) - 1
    
    # 计算总删除次数
    total_deletions = 0
    for count in char_diff.values():
        total_deletions += abs(count)
    
    return total_deletions

def makeAnagramDetailed(s1, s2):
    """
    详细版本：返回删除次数和具体需要删除的字符信息
    """
    if not s1 and not s2:
        return 0, [], []
    
    count1 = Counter(s1)
    count2 = Counter(s2)
    all_chars = set(count1.keys()) | set(count2.keys())
    
    total_deletions = 0
    delete_from_s1 = []
    delete_from_s2 = []
    
    for char in all_chars:
        freq1 = count1.get(char, 0)
        freq2 = count2.get(char, 0)
        
        if freq1 > freq2:
            # 需要从s1中删除多余的字符
            delete_count = freq1 - freq2
            delete_from_s1.extend([char] * delete_count)
            total_deletions += delete_count
        elif freq2 > freq1:
            # 需要从s2中删除多余的字符
            delete_count = freq2 - freq1
            delete_from_s2.extend([char] * delete_count)
            total_deletions += delete_count
    
    return total_deletions, delete_from_s1, delete_from_s2

def makeAnagramArray(s1, s2):
    """
    数组版本：仅支持小写字母a-z
    空间复杂度更优
    """
    if not s1 and not s2:
        return 0
    
    # 使用数组记录字符频次差，假设只有小写字母
    char_diff = [0] * 26
    
    # s1中的字符计数+1
    for char in s1:
        if 'a' <= char <= 'z':
            char_diff[ord(char) - ord('a')] += 1
    
    # s2中的字符计数-1
    for char in s2:
        if 'a' <= char <= 'z':
            char_diff[ord(char) - ord('a')] -= 1
    
    # 计算总删除次数
    total_deletions = sum(abs(count) for count in char_diff)
    
    return total_deletions