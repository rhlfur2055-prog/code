# -*- coding: utf-8 -*-
"""
05_해시, 05_힙, 06_정렬, 06_트리, 07_정렬, 07_탐색 콘텐츠
"""

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

ALGORITHM_CONTENTS = {
    # ===== 05_해시 =====
    "05_해시/hash-concept": {
        "title": "해시 개념",
        "description": "해시 함수와 해시 테이블의 원리를 학습합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 해시란?", "content": """## 🔥 한 줄 요약
> **키를 숫자로 변환해서 O(1)에 접근** - 딕셔너리의 비밀

### 왜 배워야 하나?
- 조회/삽입/삭제 모두 **O(1)** 평균
- 코테에서 O(n²) → O(n) 최적화의 핵심
- 실무: 캐시, 세션, 데이터베이스 인덱스

### 해시 함수
```
해시 함수: 키 → 숫자 (인덱스)
"apple" → 3
"banana" → 7
```

### 시간복잡도
| 연산 | 평균 | 최악 |
|-----|-----|-----|
| 삽입 | O(1) | O(n) |
| 검색 | O(1) | O(n) |
| 삭제 | O(1) | O(n) |"""},
            {"type": "code", "language": "Python", "code": """# Python 딕셔너리 = 해시 테이블
hash_map = {}

# 삽입 O(1)
hash_map["apple"] = 100
hash_map["banana"] = 200

# 조회 O(1)
print(hash_map["apple"])  # 100
print(hash_map.get("grape", 0))  # 0 (기본값)

# 존재 확인 O(1)
if "apple" in hash_map:
    print("exists!")

# 삭제 O(1)
del hash_map["apple"]

# 활용: 빈도수 카운팅
from collections import Counter
nums = [1, 1, 2, 2, 2, 3]
count = Counter(nums)
print(count)  # {2: 3, 1: 2, 3: 1}

# 활용: Two Sum O(n)
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 플랫폼 | 포인트 |
|-----|-------|-------|
| Two Sum | LeetCode | 기본 해시 |
| 완주하지 못한 선수 | 프로그래머스 | Counter |
| 숫자의 표현 (1152) | 백준 | 해시 셋 |"""}
        ]
    },

    "05_해시/hash-collision": {
        "title": "해시 충돌",
        "description": "해시 충돌 해결 방법과 좋은 해시 함수의 조건을 학습합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 충돌이란?", "content": """## 다른 키 → 같은 해시값
```
hash("apple") = 3
hash("grape") = 3  ← 충돌!
```

### 해결 방법
1. **체이닝 (Chaining)**: 같은 버킷에 연결 리스트로 저장
2. **개방 주소법 (Open Addressing)**: 다른 빈 칸 찾기
   - 선형 탐사: 순서대로 찾기
   - 이차 탐사: 제곱으로 찾기
   - 이중 해싱: 다른 해시 함수로 찾기"""},
            {"type": "code", "language": "Python", "code": """# 체이닝 구현
class HashTableChaining:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return hash(key) % self.size

    def put(self, key, value):
        idx = self._hash(key)
        for i, (k, v) in enumerate(self.table[idx]):
            if k == key:
                self.table[idx][i] = (key, value)
                return
        self.table[idx].append((key, value))

    def get(self, key):
        idx = self._hash(key)
        for k, v in self.table[idx]:
            if k == key:
                return v
        return None"""},
            {"type": "practice", "title": "🎯 연습", "content": """해시 충돌 상황을 이해하고 적절한 테이블 크기를 선택하는 것이 중요합니다.
- 적재율(Load Factor) = 요소 수 / 테이블 크기
- 보통 0.75 이하 유지 권장"""}
        ]
    },

    "05_해시/hash-basic": {
        "title": "해시 기초",
        "description": "해시의 기본 연산과 활용법을 학습합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 해시 기초", "content": """## Python 해시 자료구조

### dict (딕셔너리)
- 키-값 쌍 저장
- 키로 빠른 조회

### set (집합)
- 중복 없는 값 저장
- 존재 확인 O(1)
- 집합 연산 (합집합, 교집합)"""},
            {"type": "code", "language": "Python", "code": """# Set 활용
s = {1, 2, 3}
s.add(4)           # 추가
s.remove(1)        # 삭제
print(2 in s)      # 존재 확인 O(1)

# 중복 제거
arr = [1, 1, 2, 2, 3]
unique = list(set(arr))  # [1, 2, 3]

# 집합 연산
a = {1, 2, 3}
b = {2, 3, 4}
print(a | b)  # 합집합 {1, 2, 3, 4}
print(a & b)  # 교집합 {2, 3}
print(a - b)  # 차집합 {1}

# defaultdict
from collections import defaultdict
graph = defaultdict(list)
graph[1].append(2)
graph[1].append(3)"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 플랫폼 |
|-----|-------|
| Contains Duplicate | LeetCode |
| 전화번호 목록 | 프로그래머스 |"""}
        ]
    },

    "05_해시/hashset-hashmap": {
        "title": "HashSet과 HashMap",
        "description": "Set과 Map의 차이와 활용법을 학습합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 Set vs Map", "content": """## 차이점

| 특징 | Set (집합) | Map (딕셔너리) |
|-----|----------|--------------|
| 저장 | 값만 | 키-값 쌍 |
| 용도 | 존재 여부 | 매핑 관계 |
| 예시 | 방문 체크 | 빈도 카운트 |

### 언제 뭘 쓸까?
- 있다/없다 확인 → Set
- 값을 저장하고 조회 → Map"""},
            {"type": "code", "language": "Python", "code": """# Set 활용: 방문 체크
visited = set()
visited.add(node)
if node in visited:
    pass  # 이미 방문

# Map 활용: 빈도 카운트
freq = {}
for char in "hello":
    freq[char] = freq.get(char, 0) + 1
# {'h': 1, 'e': 1, 'l': 2, 'o': 1}

# Map 활용: 인덱스 저장
indices = {}
for i, val in enumerate(arr):
    indices[val] = i"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 위장 | Map |
| 베스트앨범 | Map + 정렬 |"""}
        ]
    },

    "05_해시/hash-problem": {
        "title": "해시 응용 문제",
        "description": "해시를 활용한 다양한 문제 패턴입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🎯 해시 문제 패턴", "content": """## 패턴 정리

1. **빈도 카운팅**: Counter 활용
2. **존재 확인**: Set 활용
3. **매핑**: Dict 활용
4. **그룹핑**: defaultdict(list)
5. **캐싱**: 계산 결과 저장"""},
            {"type": "code", "language": "Python", "code": """from collections import Counter, defaultdict

# 패턴 1: 아나그램 그룹
def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))
        groups[key].append(s)
    return list(groups.values())

# 패턴 2: 서로 다른 문자 확인
def first_unique_char(s):
    count = Counter(s)
    for i, char in enumerate(s):
        if count[char] == 1:
            return i
    return -1

# 패턴 3: 연속 부분 배열 (합이 k)
def subarray_sum(nums, k):
    count = 0
    prefix_sum = 0
    seen = {0: 1}
    for num in nums:
        prefix_sum += num
        count += seen.get(prefix_sum - k, 0)
        seen[prefix_sum] = seen.get(prefix_sum, 0) + 1
    return count"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 플랫폼 |
|-----|-------|
| Group Anagrams | LeetCode |
| First Unique Character | LeetCode |
| Subarray Sum Equals K | LeetCode |"""}
        ]
    },

    # ===== 05_힙 =====
    "05_힙/heap-concept": {
        "title": "힙 개념",
        "description": "완전 이진 트리 기반의 힙 구조를 학습합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 힙이란?", "content": """## 🔥 한 줄 요약
> **완전 이진 트리 + 힙 속성** - 최댓값/최솟값을 O(log n)에 추출

### 힙 속성
- **최소 힙**: 부모 ≤ 자식
- **최대 힙**: 부모 ≥ 자식

### 배열로 표현
```
부모 인덱스: (i - 1) // 2
왼쪽 자식: 2 * i + 1
오른쪽 자식: 2 * i + 2
```

### 시간복잡도
| 연산 | 복잡도 |
|-----|-------|
| 삽입 | O(log n) |
| 최소/최대 추출 | O(log n) |
| 최소/최대 확인 | O(1) |"""},
            {"type": "code", "language": "Python", "code": """import heapq

# 최소 힙
min_heap = []
heapq.heappush(min_heap, 3)
heapq.heappush(min_heap, 1)
heapq.heappush(min_heap, 2)
print(heapq.heappop(min_heap))  # 1

# 최대 힙 (부호 반전)
max_heap = []
for num in [3, 1, 2]:
    heapq.heappush(max_heap, -num)
print(-heapq.heappop(max_heap))  # 3

# 리스트를 힙으로
arr = [3, 1, 4, 1, 5]
heapq.heapify(arr)  # O(n)"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 최소 힙 (1927) | 기본 |
| 최대 힙 (11279) | 부호 반전 |"""}
        ]
    },

    "05_힙/heap-operation": {
        "title": "힙 연산",
        "description": "힙의 삽입, 삭제, heapify 연산을 학습합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 힙 연산", "content": """## 핵심 연산

### 1. 삽입 (push)
1. 맨 끝에 추가
2. 위로 올라가며 교환 (heapify up)

### 2. 추출 (pop)
1. 루트 제거, 맨 끝 요소를 루트로
2. 아래로 내려가며 교환 (heapify down)

### 3. heapify
- 배열을 힙으로 만들기
- O(n) 시간복잡도"""},
            {"type": "code", "language": "Python", "code": """import heapq

# heappush와 heappop 조합
heap = []
for num in [5, 3, 8, 1, 2]:
    heapq.heappush(heap, num)

sorted_arr = []
while heap:
    sorted_arr.append(heapq.heappop(heap))
print(sorted_arr)  # [1, 2, 3, 5, 8]

# heapreplace: pop 후 push (더 효율적)
heap = [1, 2, 3]
heapq.heapreplace(heap, 4)  # 1 pop, 4 push
print(heap)  # [2, 4, 3]

# nlargest, nsmallest
nums = [3, 1, 4, 1, 5, 9, 2, 6]
print(heapq.nlargest(3, nums))   # [9, 6, 5]
print(heapq.nsmallest(3, nums))  # [1, 1, 2]"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 절댓값 힙 (11286) | 커스텀 정렬 |
| 가운데를 말해요 (1655) | 두 개 힙 |"""}
        ]
    },

    "05_힙/top-k": {
        "title": "Top K 문제",
        "description": "힙을 활용한 K번째 큰/작은 수 찾기입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 Top K 패턴", "content": """## 접근법

### 방법 1: 정렬
- O(n log n)
- 간단하지만 비효율

### 방법 2: 힙 (크기 K 유지)
- O(n log k)
- K가 작으면 매우 효율적

### 방법 3: Quick Select
- O(n) 평균
- 구현 복잡"""},
            {"type": "code", "language": "Python", "code": """import heapq
from collections import Counter

# K번째 큰 수
def kth_largest(nums, k):
    heap = nums[:k]
    heapq.heapify(heap)
    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)
    return heap[0]

# K번째 작은 수
def kth_smallest(nums, k):
    heap = [-x for x in nums[:k]]
    heapq.heapify(heap)
    for num in nums[k:]:
        if num < -heap[0]:
            heapq.heapreplace(heap, -num)
    return -heap[0]

# Top K 빈도수
def top_k_frequent(nums, k):
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)

print(top_k_frequent([1,1,1,2,2,3], 2))  # [1, 2]"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| Kth Largest Element | LeetCode |
| Top K Frequent Elements | LeetCode |
| K Closest Points to Origin | LeetCode |"""}
        ]
    },

    # ===== 06_정렬 =====
    "06_정렬/sort-intro": {
        "title": "정렬 입문",
        "description": "정렬의 기본 개념과 Python 정렬 함수를 학습합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 정렬이란?", "content": """## 🔥 한 줄 요약
> **데이터를 특정 순서로 배치** - 탐색, 중복 제거, 비교의 기초

### Python 정렬
- `sort()`: 원본 수정, 반환 None
- `sorted()`: 새 리스트 반환

### 시간복잡도
- Python 정렬: **O(n log n)** (Timsort)
- 안정 정렬 (같은 값의 순서 유지)"""},
            {"type": "code", "language": "Python", "code": """# 기본 정렬
arr = [3, 1, 4, 1, 5]
arr.sort()              # 오름차순, 원본 수정
sorted_arr = sorted(arr)  # 새 리스트 반환

# 내림차순
arr.sort(reverse=True)

# key 함수
words = ["banana", "apple", "cherry"]
words.sort(key=len)  # 길이순

# 튜플 정렬 (다중 조건)
data = [(1, 'b'), (2, 'a'), (1, 'a')]
data.sort(key=lambda x: (x[0], x[1]))
# [(1, 'a'), (1, 'b'), (2, 'a')]

# 내림차순 + 오름차순 혼합
data.sort(key=lambda x: (-x[0], x[1]))

# 딕셔너리 정렬
d = {'b': 2, 'a': 3, 'c': 1}
sorted(d.items(), key=lambda x: x[1])  # 값 기준"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 수 정렬하기 (2750) | 기본 |
| 좌표 정렬하기 (11650) | 튜플 |
| 단어 정렬 (1181) | 다중 조건 |"""}
        ]
    },

    "06_정렬/merge-sort": {
        "title": "병합 정렬",
        "description": "분할 정복 기반의 O(n log n) 안정 정렬입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 병합 정렬", "content": """## 🔥 한 줄 요약
> **반으로 나누고, 정렬하며 합친다** - 분할 정복의 대표

### 특징
- 시간: O(n log n) **항상**
- 공간: O(n) 추가 필요
- 안정 정렬

### 과정
```
[38, 27, 43, 3, 9, 82, 10]
       ↓ 분할
[38, 27, 43] [3, 9, 82, 10]
       ↓ 분할
[38] [27, 43] [3, 9] [82, 10]
       ↓ 병합
[27, 38, 43] [3, 9, 10, 82]
       ↓ 병합
[3, 9, 10, 27, 38, 43, 82]
```"""},
            {"type": "code", "language": "Python", "code": """def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
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

print(merge_sort([38, 27, 43, 3, 9, 82, 10]))"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 수 정렬하기 2 (2751) | O(n log n) 필요 |
| 버블 소트 (1517) | 역전 개수 (merge sort 응용) |"""}
        ]
    },

    "06_정렬/quick-sort": {
        "title": "퀵 정렬",
        "description": "피벗 기반의 분할 정복 정렬입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 퀵 정렬", "content": """## 🔥 한 줄 요약
> **피벗 기준으로 작은 것/큰 것 분리** - 평균 O(n log n), 최악 O(n²)

### 특징
- 평균: O(n log n)
- 최악: O(n²) (이미 정렬된 경우)
- 불안정 정렬
- 실전에서 가장 빠름 (캐시 효율)"""},
            {"type": "code", "language": "Python", "code": """def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)

# in-place 버전
def quick_sort_inplace(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quick_sort_inplace(arr, low, pi - 1)
        quick_sort_inplace(arr, pi + 1, high)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| K번째 수 (11004) | Quick Select |
| 소트인사이드 (1427) | 내림차순 |"""}
        ]
    },

    "06_정렬/sort-compare": {
        "title": "정렬 비교",
        "description": "다양한 정렬 알고리즘의 특징을 비교합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 정렬 비교", "content": """## 정렬 알고리즘 비교

| 정렬 | 평균 | 최악 | 공간 | 안정 |
|-----|-----|-----|-----|-----|
| 버블 | O(n²) | O(n²) | O(1) | ✅ |
| 선택 | O(n²) | O(n²) | O(1) | ❌ |
| 삽입 | O(n²) | O(n²) | O(1) | ✅ |
| 병합 | O(n log n) | O(n log n) | O(n) | ✅ |
| 퀵 | O(n log n) | O(n²) | O(log n) | ❌ |
| 힙 | O(n log n) | O(n log n) | O(1) | ❌ |
| 계수 | O(n+k) | O(n+k) | O(k) | ✅ |

### 선택 가이드
- 거의 정렬됨: **삽입 정렬**
- 안정 필요: **병합 정렬**
- 메모리 제한: **힙 정렬**
- 일반적: **퀵 정렬** or Python 내장"""},
            {"type": "code", "language": "Python", "code": """# Python 내장 정렬 사용이 대부분 최선!
arr.sort()  # Timsort: 안정, O(n log n)

# 특수한 경우만 직접 구현
# 1. 역전 개수 세기 → merge sort 변형
# 2. K번째 수 찾기 → quick select
# 3. 범위 제한 → counting sort"""},
            {"type": "practice", "title": "🎯 연습", "content": """정렬 알고리즘 선택 퀴즈:
- N=10만, 메모리 제한 → 힙 정렬
- 거의 정렬된 데이터 → 삽입 정렬
- 일반적인 경우 → Python sort()"""}
        ]
    },

    "06_정렬/practice-sort": {
        "title": "정렬 실전",
        "description": "정렬을 활용한 실전 문제 패턴입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🎯 정렬 패턴", "content": """## 정렬 활용 패턴

1. **정렬 후 탐색**: 이진 탐색 가능
2. **정렬 후 투 포인터**: 양끝에서 탐색
3. **커스텀 정렬**: key 함수 활용
4. **구간 정렬**: 시작/끝 기준
5. **위상 정렬**: 선후 관계"""},
            {"type": "code", "language": "Python", "code": """# 구간 합치기
def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged

# 가장 큰 수 만들기
def largest_number(nums):
    from functools import cmp_to_key
    def compare(x, y):
        if x + y > y + x:
            return -1
        elif x + y < y + x:
            return 1
        return 0

    nums = list(map(str, nums))
    nums.sort(key=cmp_to_key(compare))
    return str(int(''.join(nums)))

print(largest_number([3, 30, 34, 5, 9]))  # "9534330" """},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| Merge Intervals | LeetCode |
| 가장 큰 수 | 프로그래머스 |
| H-Index | 프로그래머스 |"""}
        ]
    },

    # ===== 06_트리 =====
    "06_트리/tree-concept": {
        "title": "트리 개념",
        "description": "트리의 기본 개념과 용어를 학습합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 트리란?", "content": """## 🔥 한 줄 요약
> **계층적 자료구조** - 부모-자식 관계, 사이클 없음

### 트리 용어
- **루트 (Root)**: 최상위 노드
- **리프 (Leaf)**: 자식 없는 노드
- **깊이 (Depth)**: 루트부터 거리
- **높이 (Height)**: 리프까지 거리
- **차수 (Degree)**: 자식 수

### 이진 트리 종류
- **완전 이진 트리**: 왼쪽부터 채움
- **포화 이진 트리**: 모든 레벨 꽉 참
- **이진 탐색 트리**: 왼쪽 < 부모 < 오른쪽"""},
            {"type": "code", "language": "Python", "code": """class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# 트리 높이
def height(node):
    if not node:
        return 0
    return 1 + max(height(node.left), height(node.right))

# 노드 개수
def count_nodes(node):
    if not node:
        return 0
    return 1 + count_nodes(node.left) + count_nodes(node.right)"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| Maximum Depth of Binary Tree | LeetCode |
| Count Complete Tree Nodes | LeetCode |"""}
        ]
    },

    "06_트리/tree-traversal": {
        "title": "트리 순회",
        "description": "전위, 중위, 후위, 레벨 순회를 학습합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 순회 방법", "content": """## 순회 종류

### DFS (깊이 우선)
- **전위 (Preorder)**: 루트 → 왼쪽 → 오른쪽
- **중위 (Inorder)**: 왼쪽 → 루트 → 오른쪽
- **후위 (Postorder)**: 왼쪽 → 오른쪽 → 루트

### BFS (너비 우선)
- **레벨 순회**: 층별로 왼→오

### 언제 어떤 순회?
- 복사: 전위
- BST 정렬된 결과: 중위
- 삭제: 후위
- 최단 경로: 레벨"""},
            {"type": "code", "language": "Python", "code": """from collections import deque

# 전위 순회 (재귀)
def preorder(node):
    if not node:
        return []
    return [node.val] + preorder(node.left) + preorder(node.right)

# 중위 순회 (재귀)
def inorder(node):
    if not node:
        return []
    return inorder(node.left) + [node.val] + inorder(node.right)

# 후위 순회 (재귀)
def postorder(node):
    if not node:
        return []
    return postorder(node.left) + postorder(node.right) + [node.val]

# 레벨 순회 (BFS)
def level_order(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| Binary Tree Inorder Traversal | LeetCode |
| Binary Tree Level Order Traversal | LeetCode |
| 트리 순회 (1991) | 백준 |"""}
        ]
    },

    "06_트리/balanced-tree": {
        "title": "균형 트리",
        "description": "AVL 트리, 레드-블랙 트리 등 균형 유지 원리를 학습합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 균형 트리", "content": """## 왜 균형이 필요한가?

### 불균형 BST의 문제
```
1 → 2 → 3 → 4 → 5  (편향 트리)
탐색: O(n) ← 배열과 같음!
```

### 균형 유지 시
```
    3
   / \\
  2   4
 /     \\
1       5

탐색: O(log n)
```

### 균형 트리 종류
- **AVL 트리**: 높이 차이 ≤ 1
- **레드-블랙 트리**: 색상 규칙
- **B-트리**: DB 인덱스 (디스크 최적화)"""},
            {"type": "code", "language": "Python", "code": """# 균형 확인
def is_balanced(root):
    def check(node):
        if not node:
            return 0

        left = check(node.left)
        if left == -1:
            return -1

        right = check(node.right)
        if right == -1:
            return -1

        if abs(left - right) > 1:
            return -1

        return max(left, right) + 1

    return check(root) != -1

# Python에서는 보통 내장 자료구조 사용
# - dict: 해시 기반
# - sortedcontainers.SortedList: 균형 트리 기반"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| Balanced Binary Tree | LeetCode |
| Convert Sorted Array to BST | LeetCode |"""}
        ]
    },

    # ===== 07_정렬 (기본 정렬) =====
    "07_정렬/bubble-sort": {
        "title": "버블 정렬",
        "description": "인접 요소를 비교하며 정렬하는 O(n²) 알고리즘입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 버블 정렬", "content": """## 🔥 한 줄 요약
> **인접한 두 요소를 비교해서 교환** - 거품처럼 큰 값이 위로

### 특징
- 시간: O(n²)
- 공간: O(1)
- 안정 정렬
- 실전에서 거의 안 씀 (교육용)"""},
            {"type": "code", "language": "Python", "code": """def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:  # 최적화: 교환 없으면 종료
            break
    return arr"""},
            {"type": "practice", "title": "🎯 연습", "content": """버블 정렬은 개념 이해용. 실전에서는 Python sort() 사용!"""}
        ]
    },

    "07_정렬/selection-sort": {
        "title": "선택 정렬",
        "description": "최솟값을 찾아 앞으로 보내는 O(n²) 알고리즘입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 선택 정렬", "content": """## 🔥 한 줄 요약
> **최솟값을 찾아서 맨 앞으로** - 교환 횟수 최소

### 특징
- 시간: O(n²)
- 공간: O(1)
- 불안정 정렬
- 교환 횟수 O(n)으로 적음"""},
            {"type": "code", "language": "Python", "code": """def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr"""},
            {"type": "practice", "title": "🎯 연습", "content": """선택 정렬도 개념 이해용. 교환 비용이 클 때 고려할 수 있음."""}
        ]
    },

    "07_정렬/insertion-sort": {
        "title": "삽입 정렬",
        "description": "정렬된 부분에 새 요소를 삽입하는 O(n²) 알고리즘입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 삽입 정렬", "content": """## 🔥 한 줄 요약
> **카드 정렬하듯 알맞은 위치에 삽입** - 거의 정렬된 데이터에 효율적

### 특징
- 시간: O(n²), 거의 정렬된 경우 O(n)
- 공간: O(1)
- 안정 정렬
- 작은 데이터에 효율적"""},
            {"type": "code", "language": "Python", "code": """def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

# 거의 정렬된 데이터에서 O(n)에 가까운 성능"""},
            {"type": "practice", "title": "🎯 연습", "content": """삽입 정렬은 작은 데이터나 거의 정렬된 데이터에 좋음.
Timsort도 부분적으로 삽입 정렬 사용."""}
        ]
    },

    "07_정렬/heap-sort": {
        "title": "힙 정렬",
        "description": "힙을 이용한 O(n log n) in-place 정렬입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 힙 정렬", "content": """## 🔥 한 줄 요약
> **최대 힙에서 하나씩 추출** - O(n log n), O(1) 공간

### 특징
- 시간: O(n log n) 항상
- 공간: O(1)
- 불안정 정렬
- 메모리 제한 시 유용"""},
            {"type": "code", "language": "Python", "code": """def heap_sort(arr):
    def heapify(arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    n = len(arr)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Extract elements
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)

    return arr"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 수 정렬하기 2 (2751) | 직접 구현 |"""}
        ]
    },

    "07_정렬/counting-sort": {
        "title": "계수 정렬",
        "description": "범위가 제한된 정수를 O(n+k)에 정렬합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 계수 정렬", "content": """## 🔥 한 줄 요약
> **값의 개수를 세서 정렬** - 비교 없이 O(n+k)

### 특징
- 시간: O(n + k)
- 공간: O(k)
- 안정 정렬 가능
- 정수, 범위 제한 필요"""},
            {"type": "code", "language": "Python", "code": """def counting_sort(arr):
    if not arr:
        return arr

    min_val, max_val = min(arr), max(arr)
    count = [0] * (max_val - min_val + 1)

    for num in arr:
        count[num - min_val] += 1

    result = []
    for i, c in enumerate(count):
        result.extend([i + min_val] * c)

    return result

# 범위가 작을 때 매우 효율적
# 예: 성적 (0-100), 나이 (0-150)"""},
            {"type": "practice", "title": "🎯 연습", "content": """계수 정렬은 범위가 제한된 정수 정렬에 최적.
예: 수 정렬하기 3 (10989)"""}
        ]
    },

    "07_정렬/radix-sort": {
        "title": "기수 정렬",
        "description": "자릿수별로 정렬하는 O(d×n) 알고리즘입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 기수 정렬", "content": """## 🔥 한 줄 요약
> **자릿수별로 안정 정렬** - O(d × n)

### 특징
- 시간: O(d × n)
- 공간: O(n + k)
- 안정 정렬
- 자릿수가 적을 때 효율적"""},
            {"type": "code", "language": "Python", "code": """def radix_sort(arr):
    if not arr:
        return arr

    max_val = max(arr)
    exp = 1

    while max_val // exp > 0:
        counting_sort_by_digit(arr, exp)
        exp *= 10

    return arr

def counting_sort_by_digit(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for num in arr:
        digit = (num // exp) % 10
        count[digit] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1

    for i in range(n):
        arr[i] = output[i]"""},
            {"type": "practice", "title": "🎯 연습", "content": """기수 정렬은 자릿수가 적고 수가 많을 때 유리.
예: 전화번호 정렬"""}
        ]
    },

    # ===== 07_탐색 =====
    "07_탐색/binary-search": {
        "title": "이진 탐색",
        "description": "정렬된 배열에서 O(log n)에 원소를 찾습니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 이진 탐색", "content": """## 🔥 한 줄 요약
> **절반씩 버리며 찾기** - O(n) → O(log n)

### 전제 조건
- 데이터가 **정렬**되어 있어야 함

### 시간복잡도
- O(log n)
- 10억 개 데이터도 30번이면 찾음"""},
            {"type": "code", "language": "Python", "code": """def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1

# bisect 모듈 활용
from bisect import bisect_left, bisect_right

arr = [1, 2, 3, 3, 3, 4, 5]
print(bisect_left(arr, 3))   # 2 (3이 들어갈 가장 왼쪽)
print(bisect_right(arr, 3))  # 5 (3이 들어갈 가장 오른쪽)"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 수 찾기 (1920) | 기본 |
| 숫자 카드 2 (10816) | bisect |
| Binary Search | LeetCode |"""}
        ]
    },

    "07_탐색/parametric-search": {
        "title": "파라메트릭 서치",
        "description": "최적화 문제를 결정 문제로 바꿔 이진 탐색합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 파라메트릭 서치", "content": """## 🔥 한 줄 요약
> **"최솟값의 최댓값" 같은 최적화 문제를 이진 탐색으로 풀기**

### 패턴
1. "X가 가능한가?" 결정 함수 만들기
2. 가능한 X의 범위에서 이진 탐색
3. 조건 만족하는 최대/최소 X 찾기

### 키워드
- "최솟값의 최댓값"
- "최댓값의 최솟값"
- "M개 이하로 나누기" """},
            {"type": "code", "language": "Python", "code": """# 예: 랜선 자르기 - N개의 랜선을 K개 이상 만들 때 최대 길이
def max_length(cables, k):
    def can_make(length):
        if length == 0:
            return True
        return sum(c // length for c in cables) >= k

    left, right = 1, max(cables)
    answer = 0

    while left <= right:
        mid = (left + right) // 2
        if can_make(mid):
            answer = mid
            left = mid + 1
        else:
            right = mid - 1

    return answer

# 예: 공유기 설치 - N개 집에 C개 공유기, 최소 거리의 최대
def max_distance(houses, c):
    houses.sort()

    def can_install(dist):
        count = 1
        last = houses[0]
        for house in houses[1:]:
            if house - last >= dist:
                count += 1
                last = house
        return count >= c

    left, right = 1, houses[-1] - houses[0]
    answer = 0

    while left <= right:
        mid = (left + right) // 2
        if can_install(mid):
            answer = mid
            left = mid + 1
        else:
            right = mid - 1

    return answer"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 랜선 자르기 (1654) | 최대 길이 |
| 나무 자르기 (2805) | 높이 |
| 공유기 설치 (2110) | 최소 거리의 최대 |
| 입국심사 | 프로그래머스 |"""}
        ]
    },

    "07_탐색/practice-search": {
        "title": "탐색 실전",
        "description": "이진 탐색 활용 실전 문제 패턴입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🎯 탐색 패턴", "content": """## 이진 탐색 문제 인식

### 키워드
- "정렬된 배열에서..."
- "최솟값의 최댓값"
- "조건을 만족하는 최대/최소"
- "~안에 가능한가?"

### 주의사항
- left, right 초기값 범위
- mid 계산 시 오버플로우
- 종료 조건 left <= right vs left < right"""},
            {"type": "code", "language": "Python", "code": """# Lower Bound: target 이상인 첫 위치
def lower_bound(arr, target):
    left, right = 0, len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left

# Upper Bound: target 초과인 첫 위치
def upper_bound(arr, target):
    left, right = 0, len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] <= target:
            left = mid + 1
        else:
            right = mid
    return left

# 개수 세기
def count_occurrences(arr, target):
    return upper_bound(arr, target) - lower_bound(arr, target)"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 숫자 카드 2 (10816) | 개수 세기 |
| K번째 수 (1300) | 이진 탐색 심화 |"""}
        ]
    },
}

def generate_content():
    filepath = r"c:\tools\codemaster-next-main\codemaster-next-main\codemaster-next-main\src\data\contents\algorithm.json"

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated_count = 0

    for key, content in ALGORITHM_CONTENTS.items():
        if key in data:
            data[key]["description"] = content["description"]
            data[key]["language"] = content["language"]
            data[key]["isPlaceholder"] = False
            data[key]["sections"] = content["sections"]
            updated_count += 1
            print(f"✓ {key}")

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n{updated_count}개 완료!")
    return updated_count

if __name__ == "__main__":
    generate_content()
