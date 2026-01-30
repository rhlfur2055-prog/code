# -*- coding: utf-8 -*-
"""
11_DP, 12_그리디, 13_백트래킹, 14_고급, 14_기타, 15_실전, index
"""

import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

ALGORITHM_CONTENTS = {
    # ===== 11_DP =====
    "11_DP/dp-concept": {
        "title": "DP 개념",
        "description": "동적 프로그래밍의 핵심 원리와 접근법을 학습합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 DP란?", "content": """## 🔥 한 줄 요약
> **큰 문제를 작은 문제로 나누고, 결과를 저장해서 재사용** - 중복 계산 제거

### 조건 (DP 사용 가능한 문제)
1. **최적 부분 구조**: 큰 문제의 해가 작은 문제의 해로 구성
2. **중복 부분 문제**: 같은 작은 문제가 반복

### 방식
- **Top-down (메모이제이션)**: 재귀 + 저장
- **Bottom-up (타뷸레이션)**: 작은 것부터 채우기

### 시간복잡도
- 부분 문제 수 × 부분 문제당 연산"""},
            {"type": "code", "language": "Python", "code": """# Top-down (메모이제이션)
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

# Bottom-up (타뷸레이션)
def fib_bottom_up(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]

# 공간 최적화
def fib_optimized(n):
    if n <= 1:
        return n
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 피보나치 함수 (1003) | 기본 |
| 1로 만들기 (1463) | DP 입문 |
| 계단 오르기 (2579) | 조건 있는 DP |"""}
        ]
    },

    "11_DP/dp-fibonacci": {
        "title": "피보나치와 DP",
        "description": "피보나치 수열로 DP 개념을 이해합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 피보나치 최적화", "content": """## 방법별 비교

| 방법 | 시간 | 공간 |
|-----|-----|-----|
| 재귀 | O(2ⁿ) | O(n) |
| 메모이제이션 | O(n) | O(n) |
| 타뷸레이션 | O(n) | O(n) |
| 공간 최적화 | O(n) | O(1) |
| 행렬 거듭제곱 | O(log n) | O(1) |"""},
            {"type": "code", "language": "Python", "code": """# 행렬 거듭제곱 O(log n)
def matrix_mult(A, B):
    return [
        [A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
        [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]]
    ]

def matrix_pow(M, n):
    if n == 1:
        return M
    if n % 2 == 0:
        half = matrix_pow(M, n // 2)
        return matrix_mult(half, half)
    return matrix_mult(M, matrix_pow(M, n - 1))

def fib_matrix(n):
    if n <= 1:
        return n
    M = [[1, 1], [1, 0]]
    result = matrix_pow(M, n)
    return result[0][1]"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 피보나치 수 (2747) | 기본 |
| 피보나치 수 6 (11444) | 행렬 거듭제곱 |"""}
        ]
    },

    "11_DP/dp-coin": {
        "title": "동전 교환",
        "description": "동전 교환 문제로 DP를 연습합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 동전 문제", "content": """## 유형

### 1. 최소 동전 개수
- dp[i] = i원을 만드는 최소 동전 수

### 2. 경우의 수
- dp[i] = i원을 만드는 방법 수

### 점화식
```
dp[i] = min(dp[i], dp[i - coin] + 1)
dp[i] += dp[i - coin]
```"""},
            {"type": "code", "language": "Python", "code": """# 최소 동전 개수
def min_coins(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] != float('inf'):
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1

# 경우의 수
def count_ways(coins, amount):
    dp = [0] * (amount + 1)
    dp[0] = 1

    for coin in coins:  # 순서 중요! (중복 방지)
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]

    return dp[amount]

print(min_coins([1, 5, 10], 15))  # 2 (10+5)
print(count_ways([1, 5, 10], 15))  # ?"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 동전 1 (2293) | 경우의 수 |
| 동전 2 (2294) | 최소 개수 |
| Coin Change | LeetCode |"""}
        ]
    },

    "11_DP/dp-knapsack": {
        "title": "배낭 문제",
        "description": "0/1 배낭 문제와 변형들을 학습합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 배낭 문제", "content": """## 🔥 한 줄 요약
> **제한된 용량에서 최대 가치 담기** - DP의 대표 문제

### 유형
- **0/1 배낭**: 물건을 쪼갤 수 없음 → DP
- **분할 배낭**: 물건을 쪼갤 수 있음 → 그리디

### 점화식
```
dp[i][w] = max(dp[i-1][w], dp[i-1][w-wi] + vi)
```"""},
            {"type": "code", "language": "Python", "code": """# 0/1 배낭 - 2차원 DP
def knapsack_2d(W, weights, values):
    n = len(weights)
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(W + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - weights[i-1]] + values[i-1])
            else:
                dp[i][w] = dp[i-1][w]

    return dp[n][W]

# 0/1 배낭 - 1차원 DP (공간 최적화)
def knapsack_1d(W, weights, values):
    n = len(weights)
    dp = [0] * (W + 1)

    for i in range(n):
        for w in range(W, weights[i] - 1, -1):  # 역순!
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

    return dp[W]

# 테스트
W = 7
weights = [3, 4, 2, 5]
values = [4, 5, 3, 7]
print(knapsack_1d(W, weights, values))"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 평범한 배낭 (12865) | 기본 |
| 동전 2 (2294) | 최소 개수 |
| Target Sum | LeetCode |"""}
        ]
    },

    "11_DP/dp-lis": {
        "title": "LIS (최장 증가 부분 수열)",
        "description": "O(n log n) LIS 알고리즘을 학습합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 LIS", "content": """## 🔥 한 줄 요약
> **원소 순서 유지하며 증가하는 가장 긴 부분 수열**

### 방법
- O(n²): dp[i] = i에서 끝나는 LIS 길이
- O(n log n): 이진 탐색 활용

### 예시
```
[10, 20, 10, 30, 20, 50]
LIS: [10, 20, 30, 50] → 길이 4
```"""},
            {"type": "code", "language": "Python", "code": """# O(n²) DP
def lis_n2(arr):
    n = len(arr)
    dp = [1] * n

    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)

# O(n log n) 이진 탐색
from bisect import bisect_left

def lis_nlogn(arr):
    tails = []

    for num in arr:
        pos = bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num

    return len(tails)

print(lis_nlogn([10, 20, 10, 30, 20, 50]))  # 4"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 가장 긴 증가하는 부분 수열 (11053) | O(n²) |
| 가장 긴 증가하는 부분 수열 2 (12015) | O(n log n) |
| Longest Increasing Subsequence | LeetCode |"""}
        ]
    },

    "11_DP/dp-lcs": {
        "title": "LCS (최장 공통 부분 수열)",
        "description": "두 문자열의 최장 공통 부분 수열을 구합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 LCS", "content": """## 🔥 한 줄 요약
> **두 수열에서 공통으로 나타나는 가장 긴 부분 수열**

### 점화식
```
if A[i] == B[j]:
    dp[i][j] = dp[i-1][j-1] + 1
else:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```

### 예시
```
A = "ABCBDAB"
B = "BDCAB"
LCS = "BCAB" → 길이 4
```"""},
            {"type": "code", "language": "Python", "code": """def lcs_length(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[m][n]

# LCS 문자열 복원
def lcs_string(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    # 역추적
    result = []
    i, j = m, n
    while i > 0 and j > 0:
        if s1[i-1] == s2[j-1]:
            result.append(s1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1

    return ''.join(reversed(result))

print(lcs_string("ABCBDAB", "BDCAB"))  # BCAB"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| LCS (9251) | 길이 |
| LCS 2 (9252) | 문자열 복원 |
| Longest Common Subsequence | LeetCode |"""}
        ]
    },

    "11_DP/dp-bitmask": {
        "title": "비트마스크 DP",
        "description": "집합을 비트로 표현하는 DP 기법입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 비트마스크 DP", "content": """## 🔥 한 줄 요약
> **집합의 상태를 비트로 표현** - 부분집합 DP

### 비트 연산
- i번째 원소 포함? `(state >> i) & 1`
- i번째 추가: `state | (1 << i)`
- i번째 제거: `state & ~(1 << i)`

### 활용
- 외판원 문제 (TSP)
- 할당 문제
- 부분집합 합"""},
            {"type": "code", "language": "Python", "code": """# 외판원 문제 (TSP)
def tsp(dist):
    n = len(dist)
    INF = float('inf')
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0  # 시작점 방문

    for state in range(1 << n):
        for u in range(n):
            if not (state & (1 << u)):
                continue
            for v in range(n):
                if state & (1 << v):
                    continue
                next_state = state | (1 << v)
                dp[next_state][v] = min(dp[next_state][v], dp[state][u] + dist[u][v])

    # 모든 노드 방문 후 시작점으로
    full = (1 << n) - 1
    result = INF
    for u in range(1, n):
        if dist[u][0] > 0:
            result = min(result, dp[full][u] + dist[u][0])

    return result"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 외판원 순회 (2098) | TSP 기본 |
| 발전소 (1102) | 비트마스크 |"""}
        ]
    },

    "11_DP/dp-matrix-chain": {
        "title": "행렬 곱셈 순서",
        "description": "구간 DP로 최적 연산 순서를 찾습니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 구간 DP", "content": """## 🔥 한 줄 요약
> **구간을 나누는 모든 경우를 고려** - 작은 구간 → 큰 구간

### 점화식
```
dp[i][j] = min(dp[i][k] + dp[k+1][j] + cost)
```

### 예시: 행렬 곱셈
- A(10×30) × B(30×5) × C(5×60)
- (AB)C vs A(BC) 연산 횟수가 다름"""},
            {"type": "code", "language": "Python", "code": """def matrix_chain_order(dims):
    n = len(dims) - 1
    dp = [[0] * n for _ in range(n)]

    # 길이별로 계산
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = dp[i][k] + dp[k+1][j] + dims[i] * dims[k+1] * dims[j+1]
                dp[i][j] = min(dp[i][j], cost)

    return dp[0][n-1]

dims = [10, 30, 5, 60]  # 3개 행렬
print(matrix_chain_order(dims))"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 행렬 곱셈 순서 (11049) | 구간 DP |
| 파일 합치기 (11066) | 유사 문제 |"""}
        ]
    },

    "11_DP/practice-dp": {
        "title": "DP 실전",
        "description": "DP 문제 접근법과 패턴입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🎯 DP 접근법", "content": """## DP 문제 풀이 순서

1. **문제 분석**: 최적화/카운팅 문제인가?
2. **상태 정의**: dp[i]가 무엇을 의미하는지
3. **점화식**: dp[i]를 어떻게 구하는지
4. **초기값**: 기저 조건
5. **순서**: 어떤 순서로 채울지
6. **정답**: 어디서 답을 가져올지

## 유형
- 선형: 1차원 dp[i]
- 구간: 2차원 dp[i][j]
- 배낭: dp[i][w]
- 비트마스크: dp[state][...]"""},
            {"type": "code", "language": "Python", "code": """# DP 템플릿

# 선형 DP
def linear_dp(n):
    dp = [0] * (n + 1)
    dp[0] = base_case

    for i in range(1, n + 1):
        dp[i] = transition(dp[i-1], ...)

    return dp[n]

# 2차원 DP
def grid_dp(grid):
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = grid[0][0]

    for i in range(m):
        for j in range(n):
            dp[i][j] = grid[i][j] + max(dp[i-1][j], dp[i][j-1])

    return dp[m-1][n-1]"""},
            {"type": "practice", "title": "🎯 필수 문제", "content": """| 문제 | 유형 |
|-----|-----|
| 1로 만들기 (1463) | 선형 |
| RGB거리 (1149) | 선형 |
| 평범한 배낭 (12865) | 배낭 |
| LCS (9251) | 2차원 |
| 가장 긴 증가하는 부분 수열 (11053) | LIS |"""}
        ]
    },

    # ===== 12_그리디 =====
    "12_그리디/greedy-concept": {
        "title": "그리디 개념",
        "description": "탐욕 알고리즘의 원리와 적용 조건을 학습합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 그리디란?", "content": """## 🔥 한 줄 요약
> **매 순간 최선의 선택** - 지역 최적 → 전역 최적 (보장 필요!)

### 그리디 적용 조건
1. **탐욕 선택 속성**: 지금의 최선이 전체의 최선
2. **최적 부분 구조**: 부분 해가 전체 해 구성

### 그리디 vs DP
- 그리디: 지금 최선 선택, 돌아보지 않음
- DP: 모든 경우 고려, 최적 선택"""},
            {"type": "code", "language": "Python", "code": """# 거스름돈 - 대표적 그리디
def min_coins_greedy(amount, coins):
    coins.sort(reverse=True)  # 큰 동전부터
    count = 0
    for coin in coins:
        count += amount // coin
        amount %= coin
    return count

# 주의: 그리디가 항상 맞진 않음!
# coins = [1, 5, 12]
# amount = 15
# 그리디: 12 + 1 + 1 + 1 = 4개
# 최적: 5 + 5 + 5 = 3개

# 회의실 배정 - 그리디 정당성 O
def max_meetings(meetings):
    meetings.sort(key=lambda x: x[1])  # 끝나는 시간 순
    count = 0
    end_time = 0

    for start, end in meetings:
        if start >= end_time:
            count += 1
            end_time = end

    return count"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 동전 0 (11047) | 거스름돈 |
| 회의실 배정 (1931) | 활동 선택 |
| ATM (11399) | 순서 정하기 |"""}
        ]
    },

    "12_그리디/activity-selection": {
        "title": "활동 선택",
        "description": "겹치지 않는 최대 활동 수를 선택합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 활동 선택 문제", "content": """## 🔥 한 줄 요약
> **끝나는 시간이 빠른 것 먼저** - 다음 활동 선택 여지 최대화

### 정당성
끝나는 시간이 빠른 활동을 선택하면
나머지 시간에 더 많은 활동을 넣을 수 있음"""},
            {"type": "code", "language": "Python", "code": """def activity_selection(activities):
    # 끝나는 시간으로 정렬
    activities.sort(key=lambda x: x[1])

    selected = []
    end_time = 0

    for start, end in activities:
        if start >= end_time:
            selected.append((start, end))
            end_time = end

    return selected

meetings = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 8), (5, 9), (6, 10), (8, 11)]
print(activity_selection(meetings))
# [(1, 4), (5, 7), (8, 11)]"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 회의실 배정 (1931) | 기본 |
| 강의실 배정 (11000) | 최소 강의실 |"""}
        ]
    },

    "12_그리디/greedy-interval": {
        "title": "구간 그리디",
        "description": "구간 관련 그리디 문제를 학습합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 구간 문제", "content": """## 구간 그리디 패턴

### 1. 최대 비겹침 (활동 선택)
- 끝나는 시간 순 정렬

### 2. 최소 개수로 커버
- 시작점 순 정렬

### 3. 겹치는 구간 병합
- 시작점 순 정렬 + 끝점 갱신"""},
            {"type": "code", "language": "Python", "code": """# 구간 병합
def merge_intervals(intervals):
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    return merged

# 최소 화살로 풍선 터뜨리기
def min_arrows(points):
    if not points:
        return 0

    points.sort(key=lambda x: x[1])
    arrows = 1
    end = points[0][1]

    for s, e in points[1:]:
        if s > end:
            arrows += 1
            end = e

    return arrows"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| Merge Intervals | LeetCode |
| Minimum Number of Arrows | LeetCode |"""}
        ]
    },

    "12_그리디/greedy-vs-dp": {
        "title": "그리디 vs DP",
        "description": "그리디와 DP의 차이와 선택 기준입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 비교", "content": """## 그리디 vs DP

| 특성 | 그리디 | DP |
|-----|------|-----|
| 접근 | 지금 최선 | 모든 경우 |
| 시간 | 보통 빠름 | 상태 수 × 전이 |
| 정당성 | 증명 필요 | 항상 최적 |

### 그리디 가능 여부 판단
1. 반례 찾아보기
2. 수학적 증명
3. 작은 예제로 확인"""},
            {"type": "code", "language": "Python", "code": """# 그리디 실패 예시: 동전

# 그리디 (실패)
coins = [1, 5, 12]
amount = 15
# 그리디: 12 + 1 + 1 + 1 = 4개

# DP (정답)
def min_coins_dp(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] != float('inf'):
                dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount]

# DP: 5 + 5 + 5 = 3개"""},
            {"type": "practice", "title": "🎯 연습", "content": """문제 접근:
1. 그리디로 해결 가능? → 반례 확인
2. 반례 있으면 → DP 고려"""}
        ]
    },

    "12_그리디/practice-greedy": {
        "title": "그리디 실전",
        "description": "그리디 문제 풀이 패턴입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🎯 패턴", "content": """## 그리디 패턴

### 1. 정렬 기반
- 어떤 기준으로 정렬?
- 작은 것부터? 큰 것부터?

### 2. 교환 논증
- 현재 선택이 최적이 아니면?
- 바꿔도 손해 없거나 이득?

### 3. 우선순위 큐
- 항상 최선의 것을 선택"""},
            {"type": "code", "language": "Python", "code": """import heapq

# 허프만 코딩 - 우선순위 큐 그리디
def huffman(freqs):
    heap = list(freqs)
    heapq.heapify(heap)
    total = 0

    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        total += a + b
        heapq.heappush(heap, a + b)

    return total

# 분할 가능 배낭 - 단가 기준 그리디
def fractional_knapsack(W, items):
    # 단가순 정렬
    items.sort(key=lambda x: x[1]/x[0], reverse=True)
    total = 0

    for weight, value in items:
        if W >= weight:
            total += value
            W -= weight
        else:
            total += value * (W / weight)
            break

    return total"""},
            {"type": "practice", "title": "🎯 필수 문제", "content": """| 문제 | 포인트 |
|-----|-------|
| 동전 0 (11047) | 거스름돈 |
| 회의실 배정 (1931) | 활동 선택 |
| 잃어버린 괄호 (1541) | 파싱 |
| 로프 (2217) | 정렬 |"""}
        ]
    },

    # ===== 13_백트래킹 =====
    "13_백트래킹/backtracking-concept": {
        "title": "백트래킹 개념",
        "description": "가지치기로 탐색 공간을 줄이는 기법입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 백트래킹이란?", "content": """## 🔥 한 줄 요약
> **해가 될 가능성 없으면 가지치기** - 완전탐색 최적화

### DFS + 가지치기
- 유망하지 않은 노드 = 더 이상 탐색 X
- 시간 복잡도 크게 감소 가능

### 활용
- 순열/조합
- N-Queen
- 스도쿠
- 부분집합 합"""},
            {"type": "code", "language": "Python", "code": """# 백트래킹 템플릿
def backtrack(state):
    if is_goal(state):
        process_solution(state)
        return

    for candidate in get_candidates(state):
        if is_promising(candidate):  # 가지치기
            state.add(candidate)
            backtrack(state)
            state.remove(candidate)  # 되돌리기

# 부분집합 합
def subset_sum(nums, target):
    results = []

    def backtrack(start, path, total):
        if total == target:
            results.append(path[:])
            return
        if total > target:  # 가지치기
            return

        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path, total + nums[i])
            path.pop()

    backtrack(0, [], 0)
    return results"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| N과 M (15649~) | 순열/조합 |
| N-Queen (9663) | 체스판 |
| 스도쿠 (2580) | 유효성 검사 |"""}
        ]
    },

    "13_백트래킹/permutation": {
        "title": "순열",
        "description": "n개 중 r개를 순서 있게 뽑는 순열입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 순열", "content": """## 🔥 한 줄 요약
> **순서가 중요한 나열** - nPr = n!/(n-r)!

### 특징
- 순서 O: [1,2]와 [2,1]은 다름
- 중복 X: 한 번 사용하면 다시 사용 X"""},
            {"type": "code", "language": "Python", "code": """# 백트래킹 순열
def permutations(nums, r):
    results = []
    used = [False] * len(nums)

    def backtrack(path):
        if len(path) == r:
            results.append(path[:])
            return

        for i in range(len(nums)):
            if not used[i]:
                used[i] = True
                path.append(nums[i])
                backtrack(path)
                path.pop()
                used[i] = False

    backtrack([])
    return results

# itertools 사용
from itertools import permutations
list(permutations([1,2,3], 2))
# [(1,2), (1,3), (2,1), (2,3), (3,1), (3,2)]"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| N과 M (1) (15649) | 기본 순열 |
| 모든 순열 (10974) | 전체 순열 |"""}
        ]
    },

    "13_백트래킹/combination": {
        "title": "조합",
        "description": "n개 중 r개를 순서 없이 뽑는 조합입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 조합", "content": """## 🔥 한 줄 요약
> **순서 상관없이 선택** - nCr = n!/r!(n-r)!

### 특징
- 순서 X: [1,2]와 [2,1]은 같음
- 시작 인덱스로 중복 방지"""},
            {"type": "code", "language": "Python", "code": """# 백트래킹 조합
def combinations(nums, r):
    results = []

    def backtrack(start, path):
        if len(path) == r:
            results.append(path[:])
            return

        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)  # 다음 인덱스부터
            path.pop()

    backtrack(0, [])
    return results

# itertools 사용
from itertools import combinations
list(combinations([1,2,3], 2))
# [(1,2), (1,3), (2,3)]"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| N과 M (2) (15650) | 기본 조합 |
| 로또 (6603) | 조합 출력 |"""}
        ]
    },

    "13_백트래킹/n-queen": {
        "title": "N-Queen",
        "description": "N×N 체스판에 N개의 퀸을 배치합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 N-Queen", "content": """## 🔥 한 줄 요약
> **서로 공격하지 않게 퀸 배치** - 백트래킹 대표 문제

### 가지치기 조건
퀸은 같은 행, 열, 대각선 공격:
- 같은 열 X
- 같은 대각선 X (|row1-row2| == |col1-col2|)"""},
            {"type": "code", "language": "Python", "code": """def n_queens(n):
    def is_safe(queens, row, col):
        for r, c in enumerate(queens):
            if c == col:  # 같은 열
                return False
            if abs(r - row) == abs(c - col):  # 대각선
                return False
        return True

    def backtrack(row, queens):
        if row == n:
            return 1

        count = 0
        for col in range(n):
            if is_safe(queens, row, col):
                queens.append(col)
                count += backtrack(row + 1, queens)
                queens.pop()
        return count

    return backtrack(0, [])

print(n_queens(8))  # 92"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| N-Queen (9663) | 개수 세기 |"""}
        ]
    },

    "13_백트래킹/backtracking-nqueen": {
        "title": "N-Queen 상세",
        "description": "N-Queen 최적화 기법입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 최적화", "content": """## 비트마스크 최적화

### 기존: O(n²) 충돌 검사
### 최적화: O(1) 비트 연산

- col: 사용된 열
- diag1: 우상향 대각선
- diag2: 좌상향 대각선"""},
            {"type": "code", "language": "Python", "code": """def n_queens_optimized(n):
    def backtrack(row, cols, diag1, diag2):
        if row == n:
            return 1

        count = 0
        available = ((1 << n) - 1) & ~(cols | diag1 | diag2)

        while available:
            pos = available & -available  # 가장 오른쪽 1
            available -= pos
            count += backtrack(
                row + 1,
                cols | pos,
                (diag1 | pos) << 1,
                (diag2 | pos) >> 1
            )

        return count

    return backtrack(0, 0, 0, 0)

print(n_queens_optimized(14))  # 빠름!"""},
            {"type": "practice", "title": "🎯 연습", "content": """비트마스크로 N=15 이상도 빠르게 해결 가능!"""}
        ]
    },

    "13_백트래킹/backtracking-permutation": {
        "title": "순열 백트래킹",
        "description": "중복 순열과 같은 수 처리입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 순열 변형", "content": """## 변형

### 중복 순열
- 같은 수 여러 번 선택 가능

### 같은 수가 있는 순열
- [1,1,2]의 순열 = 3개 (6개 아님)
- 정렬 후 같은 수 연속 처리"""},
            {"type": "code", "language": "Python", "code": """# 중복 순열
def permutations_with_repetition(nums, r):
    results = []

    def backtrack(path):
        if len(path) == r:
            results.append(path[:])
            return
        for num in nums:
            path.append(num)
            backtrack(path)
            path.pop()

    backtrack([])
    return results

# 같은 수가 있는 순열
def unique_permutations(nums):
    nums.sort()
    results = []
    used = [False] * len(nums)

    def backtrack(path):
        if len(path) == len(nums):
            results.append(path[:])
            return

        for i in range(len(nums)):
            if used[i]:
                continue
            # 같은 수면서 이전 것이 안 쓰였으면 스킵
            if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            used[i] = False

    backtrack([])
    return results

print(unique_permutations([1, 1, 2]))
# [[1,1,2], [1,2,1], [2,1,1]]"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| N과 M (3) (15651) | 중복 순열 |
| N과 M (9) (15663) | 같은 수 |"""}
        ]
    },

    "13_백트래킹/practice-backtracking": {
        "title": "백트래킹 실전",
        "description": "백트래킹 문제 접근법입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🎯 패턴", "content": """## 백트래킹 = DFS + 가지치기

### 코드 구조
1. 종료 조건 (목표 도달)
2. 후보 생성
3. 유망성 검사 (가지치기)
4. 선택 → 재귀 → 취소"""},
            {"type": "code", "language": "Python", "code": """# 스도쿠 풀기
def solve_sudoku(board):
    def is_valid(r, c, num):
        # 행, 열, 3x3 박스 검사
        for i in range(9):
            if board[r][i] == num:
                return False
            if board[i][c] == num:
                return False
        br, bc = 3 * (r // 3), 3 * (c // 3)
        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                if board[i][j] == num:
                    return False
        return True

    def solve():
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    for num in range(1, 10):
                        if is_valid(r, c, num):
                            board[r][c] = num
                            if solve():
                                return True
                            board[r][c] = 0
                    return False
        return True

    solve()
    return board"""},
            {"type": "practice", "title": "🎯 필수 문제", "content": """| 문제 | 포인트 |
|-----|-------|
| N과 M 시리즈 | 순열/조합 |
| N-Queen (9663) | 가지치기 |
| 스도쿠 (2580) | 유효성 검사 |
| 부분수열의 합 (1182) | 부분집합 |"""}
        ]
    },

    # ===== 14_고급 =====
    "14_고급/trie": {
        "title": "트라이",
        "description": "문자열 검색에 특화된 트리 자료구조입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 트라이란?", "content": """## 🔥 한 줄 요약
> **문자열을 저장하는 트리** - 검색/삽입 O(문자열 길이)

### 활용
- 자동완성
- 사전 구현
- 접두사 검색"""},
            {"type": "code", "language": "Python", "code": """class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

trie = Trie()
trie.insert("apple")
print(trie.search("apple"))    # True
print(trie.starts_with("app")) # True"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 전화번호 목록 (5052) | 접두사 |
| Implement Trie | LeetCode |"""}
        ]
    },

    "14_고급/segment-tree": {
        "title": "세그먼트 트리",
        "description": "구간 쿼리를 O(log n)에 처리합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 세그먼트 트리", "content": """## 🔥 한 줄 요약
> **구간 정보를 저장하는 트리** - 쿼리/업데이트 O(log n)

### 활용
- 구간 합
- 구간 최솟값/최댓값
- 구간 업데이트"""},
            {"type": "code", "language": "Python", "code": """class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self.build(arr, 1, 0, self.n - 1)

    def build(self, arr, node, start, end):
        if start == end:
            self.tree[node] = arr[start]
        else:
            mid = (start + end) // 2
            self.build(arr, 2*node, start, mid)
            self.build(arr, 2*node+1, mid+1, end)
            self.tree[node] = self.tree[2*node] + self.tree[2*node+1]

    def update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = val
        else:
            mid = (start + end) // 2
            if idx <= mid:
                self.update(2*node, start, mid, idx, val)
            else:
                self.update(2*node+1, mid+1, end, idx, val)
            self.tree[node] = self.tree[2*node] + self.tree[2*node+1]

    def query(self, node, start, end, left, right):
        if right < start or end < left:
            return 0
        if left <= start and end <= right:
            return self.tree[node]
        mid = (start + end) // 2
        return (self.query(2*node, start, mid, left, right) +
                self.query(2*node+1, mid+1, end, left, right))"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 구간 합 구하기 (2042) | 기본 |
| 최솟값과 최댓값 (2357) | 최솟값 |"""}
        ]
    },

    "14_고급/mst-prim": {
        "title": "프림 알고리즘",
        "description": "최소 신장 트리를 구하는 프림 알고리즘입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 프림", "content": """## 🔥 한 줄 요약
> **가장 가까운 노드부터 연결** - 우선순위 큐 사용

### 시간복잡도
O(E log V) - 힙 사용 시"""},
            {"type": "code", "language": "Python", "code": """import heapq

def prim(n, graph):
    visited = [False] * (n + 1)
    heap = [(0, 1)]  # (가중치, 노드)
    total = 0
    count = 0

    while heap and count < n:
        weight, node = heapq.heappop(heap)
        if visited[node]:
            continue
        visited[node] = True
        total += weight
        count += 1

        for next_node, next_weight in graph[node]:
            if not visited[next_node]:
                heapq.heappush(heap, (next_weight, next_node))

    return total if count == n else -1"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 최소 스패닝 트리 (1197) | 기본 |
| 네트워크 연결 (1922) | 응용 |"""}
        ]
    },

    # ===== 14_기타 =====
    "14_기타/union-find": {
        "title": "Union-Find",
        "description": "집합의 합집합과 찾기 연산입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 Union-Find", "content": """## 🔥 한 줄 요약
> **집합의 합치기/찾기** - 거의 O(1) (경로 압축 + rank)

### 활용
- 연결 요소
- 사이클 검출
- 크루스칼 MST"""},
            {"type": "code", "language": "Python", "code": """class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # 경로 압축
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        # rank 기반 합치기
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 집합의 표현 (1717) | 기본 |
| 여행 가자 (1976) | 연결 확인 |"""}
        ]
    },

    "14_기타/mst-kruskal": {
        "title": "크루스칼 알고리즘",
        "description": "Union-Find를 이용한 MST 알고리즘입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 크루스칼", "content": """## 🔥 한 줄 요약
> **가중치 작은 간선부터 연결** - Union-Find로 사이클 검사

### 시간복잡도
O(E log E) - 간선 정렬"""},
            {"type": "code", "language": "Python", "code": """def kruskal(n, edges):
    edges.sort(key=lambda x: x[2])  # 가중치 정렬
    uf = UnionFind(n + 1)
    total = 0
    count = 0

    for u, v, w in edges:
        if uf.union(u, v):  # 사이클 아니면 추가
            total += w
            count += 1
            if count == n - 1:
                break

    return total if count == n - 1 else -1

# Union-Find 클래스는 위 코드 참조"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 최소 스패닝 트리 (1197) | 기본 |
| 도시 분할 계획 (1647) | MST 변형 |"""}
        ]
    },

    # ===== 15_실전 =====
    "15_실전/coding-test-tip": {
        "title": "코딩 테스트 팁",
        "description": "실전 코딩 테스트 전략과 팁입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 실전 팁", "content": """## 시간 관리

| 난이도 | 시간 배분 |
|------|---------|
| 쉬움 | 15분 |
| 보통 | 30분 |
| 어려움 | 45분 |

## 접근 순서
1. 문제 읽기 (입출력 확인)
2. 예제 손으로 풀기
3. 알고리즘 선택
4. 코드 작성
5. 예제 테스트
6. 엣지 케이스 확인"""},
            {"type": "code", "language": "Python", "code": """# 빠른 입력
import sys
input = sys.stdin.readline

# 재귀 제한 해제
sys.setrecursionlimit(10**6)

# 자주 쓰는 import
from collections import defaultdict, deque, Counter
from heapq import heappush, heappop
from bisect import bisect_left, bisect_right
from itertools import permutations, combinations
from functools import lru_cache

# 디버깅 팁
def debug(*args):
    import sys
    print(*args, file=sys.stderr)"""},
            {"type": "practice", "title": "🎯 체크리스트", "content": """- [ ] 입출력 형식 확인
- [ ] 시간복잡도 계산
- [ ] 엣지 케이스 (0, 1, 최대값)
- [ ] 인덱스 범위 확인
- [ ] 정수 오버플로우"""}
        ]
    },

    "15_실전/interview-algorithm": {
        "title": "면접 알고리즘",
        "description": "기술 면접에서 자주 나오는 알고리즘입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 면접 필수", "content": """## 자주 나오는 주제

### 자료구조
- 배열, 연결 리스트, 스택, 큐
- 해시 테이블, 트리, 힙

### 알고리즘
- 이진 탐색
- DFS/BFS
- 동적 프로그래밍
- 정렬

### 설명 포인트
- 시간/공간 복잡도
- 다른 방법과 비교
- 실제 활용 사례"""},
            {"type": "code", "language": "Python", "code": """# 면접에서 자주 물어보는 것들

# 1. 해시 테이블 충돌 해결
# - 체이닝, 개방 주소법

# 2. 힙 vs 이진 탐색 트리
# - 힙: 최대/최소 O(1), 삽입 O(log n)
# - BST: 탐색/삽입/삭제 O(log n)

# 3. 퀵소트 vs 머지소트
# - 퀵: 평균 O(n log n), 최악 O(n²), in-place
# - 머지: 항상 O(n log n), O(n) 공간, 안정

# 4. DFS vs BFS
# - DFS: 경로, 백트래킹
# - BFS: 최단 거리, 레벨 탐색"""},
            {"type": "practice", "title": "🎯 준비", "content": """자주 나오는 문제:
- Two Sum
- LRU Cache
- 이진 탐색
- 트리 순회
- 그래프 탐색"""}
        ]
    },

    "15_실전/problem-pattern": {
        "title": "문제 패턴",
        "description": "문제 유형별 접근 패턴입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 패턴 인식", "content": """## 키워드 → 알고리즘

| 키워드 | 알고리즘 |
|-------|---------|
| 최단 경로 | BFS, 다익스트라 |
| 조합/순열 | 백트래킹 |
| 최적화 | DP, 그리디 |
| 정렬된 배열 | 이진 탐색 |
| 연속 구간 | 슬라이딩 윈도우 |
| 빈도수 | 해시맵 |
| 그래프 연결 | DFS/BFS, Union-Find |"""},
            {"type": "code", "language": "Python", "code": """# 문제 접근 템플릿

def solve():
    # 1. 입력 처리
    n = int(input())

    # 2. 시간복잡도 예측
    # N <= 10만 → O(n log n) 이하

    # 3. 알고리즘 선택
    # - 최단 경로? → BFS/다익스트라
    # - 모든 경우? → 백트래킹/DP
    # - 정렬된 배열? → 이진 탐색

    # 4. 구현

    # 5. 출력
    print(answer)"""},
            {"type": "practice", "title": "🎯 연습", "content": """패턴 인식 → 빠른 문제 풀이!

많은 문제를 풀며 패턴 익히기."""}
        ]
    },

    # ===== index =====
    "index": {
        "title": "알고리즘 & 자료구조",
        "description": "알고리즘과 자료구조 학습 가이드입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🎯 학습 로드맵", "content": """## 추천 학습 순서

### Phase 1: 기초 (1-2주)
1. 시간/공간 복잡도
2. 배열, 문자열
3. 스택, 큐

### Phase 2: 탐색 (2-3주)
1. 이진 탐색
2. DFS, BFS
3. 그래프 기초

### Phase 3: 최적화 (3-4주)
1. 동적 프로그래밍
2. 그리디
3. 백트래킹

### Phase 4: 심화 (4주+)
1. 최단 경로
2. 트리 알고리즘
3. 고급 자료구조"""},
            {"type": "code", "language": "Python", "code": """# 핵심 자료구조 정리

# 배열 - 인덱스 접근 O(1)
# 연결 리스트 - 삽입/삭제 O(1)
# 스택 - LIFO, O(1)
# 큐 - FIFO, O(1)
# 해시 - 조회/삽입 O(1)
# 힙 - 최소/최대 O(1), 삽입 O(log n)
# 트리 - 계층적 구조
# 그래프 - 관계 표현"""},
            {"type": "practice", "title": "🎯 학습 자료", "content": """### 추천 문제집
- 백준 단계별로 풀어보기
- LeetCode 75
- 프로그래머스 고득점 Kit

### 필수 문제 (50선)
기초, 정렬/탐색, 그래프, DP, 그리디 각 10문제씩 연습!"""}
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
