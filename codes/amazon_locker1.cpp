locker有个C++的
// Design a package pickup station with lockers of varying sizes. Each locker can hold at most one package, as long as the package size does not exceed the locker size.

locker 是按体积定义的吗
问能不能给一个locker 的 example

ic
稍等

// 我会用有序映射和多队列结构来实现按尺寸快速分配最合适的空柜。
// I will use an ordered map and multiple queues to allocate the best-fit empty locker by size.

// 我先把所有空柜按尺寸放到对应的队列里，方便直接取到最小能装下包裹的柜子。
//  First, I bucket all free lockers by size into separate queues so I can directly fetch the smallest locker that fits the package.

// 然后我用一个有序映射从最小尺寸到最大尺寸排序这些队列，这样查找第一个能用的队列是对数时间。
// Then I keep an ordered map from size to those queues so finding the first non-empty fitting queue takes logarithmic time.
// 存包裹时，lower_bound 找到最小的合适尺寸，弹出一个柜子，记录包裹ID到柜子ID的映
// On store, I use lower_bound to find the smallest fitting size, pop one locker, and map the package ID to that locker ID.
// 中文: 取包裹时，根据ID查映射，回收柜子并放回对应尺寸队列，保证后续可复用。
// English: On retrieve, I lookup by package ID, push the locker back into its size queue for reuse.
---
// # initLockers runs in O(N) time, where N is the number of lockers, because it loops once over all lockers
// # storePackage does a map.lower_bound in O(log S) time (S=size categories, constant 5) plus O(1) queue and hash insert on average
// # storePackage worst-case can incur O(P) time if the hash map degrades, where P is number of stored packages
// # retrievePackage does O(1) average time for hash lookup and queue push, with worst-case O(P) if the hash map degrades
// # Overall average time per operation is O(log S) ~ O(1), and worst-case is O(P) due to hash collisions
// # Space complexity is O(N + P) to store N locker IDs in queues and P entries in the package-to-locker map
--
#include <map>                  // I’m pulling in map so I can keep lockers in order by size
#include <queue>                // I need queue to hold free locker IDs per size
#include <unordered_map>        // I want fast lookup from package ID to locker ID
#include <vector>               // I’ll store locker sizes and IDs in vectors
#include <string>               // I’ll use string for package IDs
#include <stdexcept>            // I’ll throw runtime errors on bad calls

using namespace std;           // I’m using the std namespace to save typing
让她刷新，你也刷新 刷新前，记得复制
enum Size { XS = 0, S = 1, M = 2, L = 3, XL = 4 };  // I define five discrete sizes

map<Size, queue<int>> freeLockers;      // I map each size to a queue of free locker IDs
unordered_map<string, int> pkgToLocker; // I map each package ID to its assigned locker ID

void initLockers(const vector<Size>& sizes, const vector<int>& ids) {
    // I set up each locker by pushing its ID into the right size queue
    for (size_t i = 0; i < sizes.size(); ++i) {
        freeLockers[sizes[i]].push(ids[i]);  // push locker IDs into freeLockers[size]
    }
}

int storePackage(const string& pkgId, Size pkgSize) {
    // I find the first locker size that can fit this package
    auto it = freeLockers.lower_bound(pkgSize);
    // We use binary search (lower_bound) to efficiently find the smallest locker size ≥ the package size, instead of scanning every size option one by one.
    // 不是吧，二分查找 找到最小的可以用的size。
    // 不然就得遍历了。
    // I check if no suitable size or no free locker there
    // 就是遍历的时候找不到空着的locker了
    it->second.empty() 用来判断虽然该尺寸在映射中存在，但对应的队列里没有空闲的柜子可用。
    if (it == freeLockers.end() || it->second.empty()) {
        throw runtime_error("No suitable locker"); // no free locker found
    }
    // I grab the front locker ID from that queue
    int lockerId = it->second.front();
    it->second.pop();                   // I mark that locker as used
    pkgToLocker[pkgId] = lockerId;      // I save the mapping from package to locker
    
    if (it->second.empty()) {
        freeLockers.erase(it);
    }

    return lockerId;                    // I return which locker we used
}

void retrievePackage(const string& pkgId, Size pkgSize) {
    // I look up where the package was stored
    auto it = pkgToLocker.find(pkgId);
    if (it == pkgToLocker.end()) {
        throw runtime_error("Unknown package"); // bad package ID
    }
    // I get the locker ID and free it
    int lockerId = it->second;
    pkgToLocker.erase(it);               // I remove the mapping
    freeLockers[pkgSize].push(lockerId); // I put the locker back as free
}

A nicer approach is to store both the lockerId and the Size in our map, so retrieval can look up everything it needs.
// define a mapping from package ID to (locker ID, size)
unordered_map<string, pair<int,Size>> pkgToLocker;

那倒不用。。

int main() {
    // I list all locker sizes and their IDs
    vector<Size> sizes = { S, M, M, L, XS, XL };
    vector<int> ids    = { 1, 2, 3, 4, 5, 6 };
    initLockers(sizes, ids);             // I initialize free lockers

    int idA = storePackage("A123", M);   // I store package A123 in a medium locker
    int idB = storePackage("B456", S);   // I store package B456 in a small locker

    retrievePackage("A123", M);          // I retrieve package A123 and free the locker

    return 0;                            // I end the program
}