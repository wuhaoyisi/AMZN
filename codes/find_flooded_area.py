"""
给定一个长度为 N的地形高度数组
heights，和一个升序排列的喷泉位置数组fountains。每个喷泉只有当其所在位置高度大于水面时才会泵水；泵出的水会向左右两侧流动，只能通过高度低于喷泉自身高度的位置，一旦遇到高度≥喷泉高度的地形就停止流动。output哪里会被水淹没。
Q:
will there be negatives?
do we need to varify the input like it could be out of range?
"""

def flooded_areas_(heights, fountains):
    n = len(heights)
    flooded = [False] * n
    for f in fountains:
        fountain_height = heights[f]
        if fountain_height <= 0:
            continue
        # 向左找边界
        left = f - 1
        while left >= 0 and heights[left] < fountain_height:
            left -= 1
        # 向右找边界
        right = f + 1
        while right < n and heights[right] < fountain_height:
            right += 1
        # 标记被水覆盖的位置
        for i in range(left + 1, right):
            flooded[i] = True
    return flooded

from collections import deque

def flooded_areas_2d(heights, fountains):
    m, n = len(heights), len(heights[0])
    flooded = [[False] * n for _ in range(m)]  # Initialize flooded matrix
    directions = [(-1,0), (1,0), (0,-1), (0,1)]  # Four possible directions: up, down, left, right
    for fx, fy in fountains:
        fountain_height = heights[fx][fy]
        if fountain_height <= 0:
            continue  # Skip fountains not above water level
        queue = deque()
        visited = [[False] * n for _ in range(m)]  # Track visited cells for this fountain
        queue.append((fx, fy))
        visited[fx][fy] = True
        flooded[fx][fy] = True  # Mark fountain position as flooded
        while queue:
            x, y = queue.popleft()
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n:
                    # Only flow to unvisited, lower cells
                    if not visited[nx][ny] and heights[nx][ny] < fountain_height:
                        visited[nx][ny] = True
                        flooded[nx][ny] = True  # Mark as flooded
                        queue.append((nx, ny))
    return flooded

