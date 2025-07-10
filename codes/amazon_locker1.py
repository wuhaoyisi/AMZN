# Design a package pickup station with lockers of varying sizes. Each locker can hold at most one package, as long as the package size does not exceed the locker size.

# locker 是按体积定义的吗
# 问能不能给一个locker 的 example

# 我会用有序映射和多队列结构来实现按尺寸快速分配最合适的空柜。
# I will use an ordered map and multiple queues to allocate the best-fit empty locker by size.

# 我先把所有空柜按尺寸放到对应的队列里，方便直接取到最小能装下包裹的柜子。
# First, I bucket all free lockers by size into separate queues so I can directly fetch the smallest locker that fits the package.

# 然后我用一个有序映射从最小尺寸到最大尺寸排序这些队列，这样查找第一个能用的队列是对数时间。
# Then I keep an ordered map from size to those queues so finding the first non-empty fitting queue takes logarithmic time.

# 存包裹时，lower_bound 找到最小的合适尺寸，弹出一个柜子，记录包裹ID到柜子ID的映
# On store, I use lower_bound to find the smallest fitting size, pop one locker, and map the package ID to that locker ID.

# 中文: 取包裹时，根据ID查映射，回收柜子并放回对应尺寸队列，保证后续可复用。
# English: On retrieve, I lookup by package ID, push the locker back into its size queue for reuse.

from collections import deque
from enum import IntEnum

# I define five discrete sizes
class Size(IntEnum):
    XS = 0
    S = 1
    M = 2
    L = 3
    XL = 4

# I map each size to a queue of free locker IDs
freeLockers = dict()
# I map each package ID to its assigned locker ID
pkgToLocker = dict()

def initLockers(sizes, ids):
    # I set up each locker by pushing its ID into the right size queue
    for size, locker_id in zip(sizes, ids):
        if size not in freeLockers:
            freeLockers[size] = deque()
        freeLockers[size].append(locker_id)

def storePackage(pkgId, pkgSize):
    # I find the first locker size that can fit this package
    for size in sorted(freeLockers.keys()):
        if size >= pkgSize and freeLockers[size]:
            lockerId = freeLockers[size].popleft()
            pkgToLocker[pkgId] = (lockerId, size)
            if not freeLockers[size]:
                del freeLockers[size]
            return lockerId
    raise RuntimeError("No suitable locker")

def retrievePackage(pkgId):
    # I look up where the package was stored
    if pkgId not in pkgToLocker:
        raise RuntimeError("Unknown package")
    lockerId, size = pkgToLocker[pkgId]
    del pkgToLocker[pkgId]
    if size not in freeLockers:
        freeLockers[size] = deque()
    freeLockers[size].append(lockerId)

if __name__ == "__main__":
    # I list all locker sizes and their IDs
    sizes = [Size.S, Size.M, Size.M, Size.L, Size.XS, Size.XL]
    ids   = [1,      2,      3,      4,      5,      6]
    initLockers(sizes, ids)             # I initialize free lockers

    idA = storePackage("A123", Size.M)  # I store package A123 in a medium locker
    idB = storePackage("B456", Size.S)  # I store package B456 in a small locker

    retrievePackage("A123")             # I retrieve package A123 and free the locker

# # initLockers runs in O(N) time, where N is the number of lockers, because it loops once over all lockers
# # storePackage does a map.lower_bound in O(log S) time (S=size categories, constant 5) plus O(1) queue and hash insert on average
# # storePackage worst-case can incur O(P) time if the hash map degrades, where P is number of stored packages
# # retrievePackage does O(1) average time for hash lookup and queue push, with worst-case O(P) if the hash map degrades
# # Overall average time per operation is O(log S) ~ O(1), and worst-case is O(P) due to hash collisions
# # Space complexity is O(N + P) to store N locker IDs in queues and P entries in the package-to-locker map

# A nicer approach is to store both the lockerId and the Size in our map, so retrieval can look up everything it needs.
# define a mapping from package ID to (locker ID, size)
# unordered_map<string, pair<int,Size>> pkgToLocker;
