# -*- coding: utf-8 -*-
"""
02_배열 섹션 콘텐츠 생성기
"""

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

ALGORITHM_CONTENTS = {
    # ===== 02_배열 =====
    "02_배열/array-basic": {
        "title": "배열 기초",
        "description": "배열의 개념, 메모리 구조, 기본 연산을 학습합니다.",
        "language": "Python",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 배열이란?",
                "content": """## 🔥 한 줄 요약
> **같은 타입의 데이터를 연속된 메모리에 저장하는 자료구조** - 인덱스로 O(1) 접근!

---

## 💡 왜 배워야 하나?

### 실무에서:
- **모든 데이터 처리의 기본**: 리스트, 벡터, ArrayList 전부 배열 기반
- **DB 결과 저장**: SELECT 결과 → 배열로 반환
- **API 응답**: JSON 배열 형태로 데이터 전송

### 코딩테스트에서:
- 출제 빈도: ⭐⭐⭐⭐⭐ (거의 모든 문제에 등장)
- 배열 없이 풀 수 있는 문제가 거의 없음

---

## 🎯 핵심 개념 (5분 컷)

### 📚 사물함으로 이해하기
```
학교 사물함을 생각해봐:
- 1번부터 100번까지 번호가 붙어있음 (인덱스)
- 각 칸은 같은 크기 (같은 타입)
- 번호만 알면 바로 찾아감 (O(1) 접근)
```

### 배열의 특징
| 특징 | 설명 | 시간복잡도 |
|-----|------|----------|
| **인덱스 접근** | arr[i]로 바로 접근 | O(1) |
| **삽입 (끝)** | append | O(1) |
| **삽입 (중간)** | 뒤의 요소 이동 필요 | O(n) |
| **삭제 (중간)** | 뒤의 요소 이동 필요 | O(n) |
| **검색** | 하나씩 확인 | O(n) |

### 메모리 구조
```
인덱스:  [0]  [1]  [2]  [3]  [4]
값:      10   20   30   40   50
주소:   100  104  108  112  116  (int = 4바이트)

arr[2]의 주소 = 시작주소 + (2 × 4) = 108
→ 바로 계산 가능! = O(1)
```"""
            },
            {
                "type": "code",
                "language": "Python",
                "code": """# 🔰 배열 기본 연산

# 1. 배열 생성
arr = [1, 2, 3, 4, 5]           # 리터럴
arr = list(range(1, 6))         # range 사용
arr = [0] * 5                   # 0으로 초기화
arr = [i**2 for i in range(5)]  # 컴프리헨션

# 2. 접근 및 수정 - O(1)
print(arr[0])      # 첫 번째 요소
print(arr[-1])     # 마지막 요소
arr[2] = 100       # 수정

# 3. 삽입
arr.append(6)      # 끝에 추가 - O(1)
arr.insert(0, 0)   # 맨 앞에 추가 - O(n)

# 4. 삭제
arr.pop()          # 마지막 제거 - O(1)
arr.pop(0)         # 첫 번째 제거 - O(n)
arr.remove(3)      # 값으로 제거 - O(n)

# 5. 검색
if 4 in arr:       # 존재 확인 - O(n)
    idx = arr.index(4)  # 인덱스 찾기

# 6. 슬라이싱
sub = arr[1:4]     # 1~3번 인덱스
rev = arr[::-1]    # 뒤집기

# 7. 순회
for i, val in enumerate(arr):
    print(f"arr[{i}] = {val}")

# 8. 정렬
arr.sort()              # 오름차순 (in-place)
arr.sort(reverse=True)  # 내림차순
sorted_arr = sorted(arr)  # 새 배열 반환"""
            },
            {
                "type": "best-practice",
                "title": "✅ 배열 Best Practice",
                "content": """**1️⃣ 리스트 컴프리헨션 활용**

❌ **Bad:**
```python
squares = []
for i in range(10):
    squares.append(i ** 2)
```

✅ **Good:**
```python
squares = [i ** 2 for i in range(10)]
```

---

**2️⃣ 불필요한 인덱스 접근 피하기**

❌ **Bad:**
```python
for i in range(len(arr)):
    print(arr[i])
```

✅ **Good:**
```python
for item in arr:
    print(item)

# 인덱스가 필요하면
for i, item in enumerate(arr):
    print(i, item)
```

---

**3️⃣ 메모리 효율적인 초기화**

❌ **Bad:**
```python
# 2차원 배열 잘못된 초기화
matrix = [[0] * n] * m  # 같은 리스트 참조!
matrix[0][0] = 1
print(matrix)  # [[1,0,0], [1,0,0], [1,0,0]] 😱
```

✅ **Good:**
```python
matrix = [[0] * n for _ in range(m)]
matrix[0][0] = 1
print(matrix)  # [[1,0,0], [0,0,0], [0,0,0]] ✅
```"""
            },
            {
                "type": "practice",
                "title": "🎯 연습 문제",
                "content": """### Level 1: 기초
| 문제 | 플랫폼 | 포인트 |
|-----|-------|-------|
| 최댓값 (2562) | 백준 | 순회, 최대 |
| 숫자의 합 (11720) | 백준 | 문자→숫자 |
| 평균 (1546) | 백준 | 평균 계산 |

### Level 2: 응용
| 문제 | 플랫폼 | 포인트 |
|-----|-------|-------|
| 나머지 (3052) | 백준 | Set 활용 |
| OX퀴즈 (8958) | 백준 | 연속 카운트 |

### 직접 구현
1. 배열에서 두 번째로 큰 수 찾기
2. 배열 회전 (오른쪽으로 k칸)
3. 중복 제거"""
            }
        ]
    },

    "02_배열/two-pointer": {
        "title": "투 포인터",
        "description": "두 개의 포인터로 배열을 효율적으로 탐색하는 기법입니다.",
        "language": "Python",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 투 포인터란?",
                "content": """## 🔥 한 줄 요약
> **두 개의 포인터를 이동시키며 원하는 조건을 찾는 기법** - O(n²)를 O(n)으로!

---

## 💡 왜 배워야 하나?

### 실무에서:
- **두 배열 병합**: 정렬된 두 리스트 합치기
- **구간 검색**: 연속 구간에서 조건 만족하는 경우
- **문자열 처리**: 회문 검사, 아나그램

### 코딩테스트에서:
- 출제 빈도: ⭐⭐⭐⭐⭐
- 대표 기업: 카카오, 네이버 **필수 유형**
- "합이 K인 쌍", "연속 부분 배열" 문제

---

## 🎯 핵심 개념 (5분 컷)

### 📚 책 양쪽에서 접근하기
```
두꺼운 책에서 특정 페이지를 찾을 때:
- 한 사람은 앞에서부터 (left)
- 한 사람은 뒤에서부터 (right)
- 만나면 끝!
```

### 투 포인터 유형

**1. 양끝에서 시작 (Opposite Direction)**
```
[1, 2, 3, 4, 5, 6, 7]
 ↑                 ↑
left             right
```
- 사용: 정렬된 배열에서 합 찾기

**2. 같은 방향 (Same Direction)**
```
[1, 2, 3, 4, 5, 6, 7]
 ↑  ↑
slow fast
```
- 사용: 슬라이딩 윈도우, 중복 제거"""
            },
            {
                "type": "code",
                "language": "Python",
                "code": """# 🔰 투 포인터 기본 패턴

# 1. 양끝에서 시작: 정렬된 배열에서 합이 target인 쌍 찾기
def two_sum_sorted(arr, target):
    left, right = 0, len(arr) - 1

    while left < right:
        current_sum = arr[left] + arr[right]

        if current_sum == target:
            return [left, right]  # 찾았다!
        elif current_sum < target:
            left += 1   # 합이 작으면 왼쪽 증가
        else:
            right -= 1  # 합이 크면 오른쪽 감소

    return [-1, -1]  # 못 찾음

# 테스트
arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
print(two_sum_sorted(arr, 10))  # [0, 8] (1+9=10)

# 2. 같은 방향: 연속 부분 배열의 합
def min_subarray_len(arr, target):
    \"\"\"합이 target 이상인 최소 길이 부분 배열\"\"\"
    n = len(arr)
    left = 0
    current_sum = 0
    min_len = float('inf')

    for right in range(n):
        current_sum += arr[right]

        while current_sum >= target:
            min_len = min(min_len, right - left + 1)
            current_sum -= arr[left]
            left += 1

    return min_len if min_len != float('inf') else 0

# 3. 중복 제거 (정렬된 배열)
def remove_duplicates(arr):
    if not arr:
        return 0

    slow = 0
    for fast in range(1, len(arr)):
        if arr[fast] != arr[slow]:
            slow += 1
            arr[slow] = arr[fast]

    return slow + 1  # 유일한 요소 개수

# 4. 회문 검사
def is_palindrome(s):
    left, right = 0, len(s) - 1

    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1

    return True

print(is_palindrome("racecar"))  # True"""
            },
            {
                "type": "common-mistake",
                "title": "⚠️ 투 포인터 실수 TOP 3",
                "content": """**1️⃣ 정렬 안 하고 사용**

❌ **Bad:**
```python
arr = [3, 1, 4, 1, 5]  # 정렬 안 됨!
two_sum_sorted(arr, 6)  # 잘못된 결과
```

✅ **Good:**
```python
arr = [3, 1, 4, 1, 5]
arr.sort()  # 먼저 정렬!
two_sum_sorted(arr, 6)
```

---

**2️⃣ 포인터 이동 조건 실수**

❌ **Bad:**
```python
while left <= right:  # 같을 때도 실행 → 무한루프 가능
    if condition:
        left += 1
        right -= 1
```

✅ **Good:**
```python
while left < right:  # 엇갈리면 종료
    if condition:
        left += 1
    else:
        right -= 1
```

---

**3️⃣ 경계 조건 무시**

```python
# 빈 배열이나 길이 1인 경우 체크
def two_pointer_func(arr):
    if len(arr) < 2:
        return -1  # 예외 처리

    left, right = 0, len(arr) - 1
    # ...
```"""
            },
            {
                "type": "practice",
                "title": "🎯 연습 문제",
                "content": """### Level 1: 기초
| 문제 | 플랫폼 | 포인트 |
|-----|-------|-------|
| 수들의 합 2 (2003) | 백준 | 기본 투포인터 |
| Two Sum II | LeetCode | 정렬된 배열 |

### Level 2: 응용
| 문제 | 플랫폼 | 포인트 |
|-----|-------|-------|
| 부분합 (1806) | 백준 | 최소 길이 |
| 소수의 연속합 (1644) | 백준 | 누적합+투포 |
| 3Sum | LeetCode | 세 수의 합 |

### Level 3: 심화
| 문제 | 플랫폼 | 포인트 |
|-----|-------|-------|
| Container With Most Water | LeetCode | 최적화 |
| Trapping Rain Water | LeetCode | 어려움 |"""
            }
        ]
    },

    "02_배열/sliding-window": {
        "title": "슬라이딩 윈도우",
        "description": "고정/가변 크기 윈도우로 연속 구간을 효율적으로 처리합니다.",
        "language": "Python",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 슬라이딩 윈도우란?",
                "content": """## 🔥 한 줄 요약
> **창문을 밀면서 보는 것처럼 연속 구간을 처리** - O(n²)를 O(n)으로!

---

## 💡 왜 배워야 하나?

### 실무에서:
- **실시간 데이터 분석**: 최근 N분간 평균 트래픽
- **네트워크**: TCP 슬라이딩 윈도우 프로토콜
- **스트리밍 처리**: Kafka, Flink의 윈도우 연산

### 코딩테스트에서:
- 출제 빈도: ⭐⭐⭐⭐⭐
- "연속 K개", "부분 배열", "부분 문자열" 키워드

---

## 🎯 핵심 개념 (5분 컷)

### 📚 기차 창문으로 이해하기
```
기차 창문(윈도우)으로 풍경(배열)을 본다:
- 창문 크기는 고정 (또는 가변)
- 기차가 이동하면 새 풍경이 들어오고 옛 풍경은 나감
- 모든 풍경을 다시 볼 필요 없이 변화만 반영!
```

### 유형 2가지

**1. 고정 크기 윈도우**
```
배열: [1, 3, 2, 6, -1, 4, 1, 8, 2]
크기: 3

[1, 3, 2] → sum = 6
   [3, 2, 6] → sum = 6 - 1 + 6 = 11  (빠지고 들어온 것만!)
      [2, 6, -1] → sum = 11 - 3 + (-1) = 7
```

**2. 가변 크기 윈도우**
```
조건을 만족할 때까지 확장
조건 초과하면 축소
→ 투 포인터와 유사
```"""
            },
            {
                "type": "code",
                "language": "Python",
                "code": """# 🔰 슬라이딩 윈도우 패턴

# 1. 고정 크기: 연속 K개 최대 합
def max_sum_subarray(arr, k):
    n = len(arr)
    if n < k:
        return -1

    # 첫 윈도우 합 계산
    window_sum = sum(arr[:k])
    max_sum = window_sum

    # 윈도우 슬라이딩
    for i in range(k, n):
        window_sum += arr[i] - arr[i - k]  # 들어온 것 + 나간 것 -
        max_sum = max(max_sum, window_sum)

    return max_sum

arr = [1, 4, 2, 10, 2, 3, 1, 0, 20]
print(max_sum_subarray(arr, 4))  # 24 (10+2+3+1... 아니 2+10+2+3=17? 다시: 3+1+0+20=24)

# 2. 고정 크기: 연속 K개 평균
def moving_average(arr, k):
    n = len(arr)
    result = []
    window_sum = sum(arr[:k])
    result.append(window_sum / k)

    for i in range(k, n):
        window_sum += arr[i] - arr[i - k]
        result.append(window_sum / k)

    return result

# 3. 가변 크기: 합이 target 이상인 최소 길이
def min_length_subarray(arr, target):
    n = len(arr)
    min_len = float('inf')
    window_sum = 0
    left = 0

    for right in range(n):
        window_sum += arr[right]

        while window_sum >= target:
            min_len = min(min_len, right - left + 1)
            window_sum -= arr[left]
            left += 1

    return min_len if min_len != float('inf') else 0

# 4. 가변 크기: 중복 없는 최장 부분 문자열
def longest_unique_substring(s):
    char_set = set()
    left = 0
    max_len = 0

    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1

        char_set.add(s[right])
        max_len = max(max_len, right - left + 1)

    return max_len

print(longest_unique_substring("abcabcbb"))  # 3 ("abc")"""
            },
            {
                "type": "tip",
                "title": "💡 슬라이딩 윈도우 vs 투 포인터",
                "content": """### 언제 뭘 쓸까?

| 상황 | 기법 | 예시 |
|-----|-----|-----|
| 연속 구간의 합/평균 | 슬라이딩 윈도우 | 연속 K개 최대합 |
| 두 값의 조합 | 투 포인터 | 합이 K인 두 수 |
| 조건 만족 구간 | 둘 다 가능 | 합이 K 이상인 최소 구간 |
| 정렬된 배열 | 투 포인터 | 이진 탐색 대안 |

### 슬라이딩 윈도우 키워드
- "연속", "부분 배열", "부분 문자열"
- "K개", "길이가 K인"
- "최대/최소 구간"

### 시간복잡도 비교
```python
# 브루트포스: O(n × k)
for i in range(n - k + 1):
    window_sum = sum(arr[i:i+k])  # 매번 k개 더함

# 슬라이딩 윈도우: O(n)
window_sum = sum(arr[:k])
for i in range(k, n):
    window_sum += arr[i] - arr[i-k]  # O(1)
```"""
            },
            {
                "type": "practice",
                "title": "🎯 연습 문제",
                "content": """### Level 1: 고정 윈도우
| 문제 | 플랫폼 | 포인트 |
|-----|-------|-------|
| 구간 합 구하기 4 (11659) | 백준 | 누적합 기초 |
| Maximum Average Subarray I | LeetCode | 고정 윈도우 |

### Level 2: 가변 윈도우
| 문제 | 플랫폼 | 포인트 |
|-----|-------|-------|
| 부분합 (1806) | 백준 | 최소 길이 |
| Longest Substring Without Repeating | LeetCode | 문자열 윈도우 |

### Level 3: 심화
| 문제 | 플랫폼 | 포인트 |
|-----|-------|-------|
| Sliding Window Maximum | LeetCode | 덱 활용 |
| Minimum Window Substring | LeetCode | 해시맵+윈도우 |"""
            }
        ]
    },

    "02_배열/prefix-sum": {
        "title": "누적합 (Prefix Sum)",
        "description": "구간 합을 O(1)에 계산하는 누적합 기법을 학습합니다.",
        "language": "Python",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 누적합이란?",
                "content": """## 🔥 한 줄 요약
> **미리 합을 저장해두고 구간 합을 O(1)에 계산** - 전처리 O(n), 쿼리 O(1)

---

## 💡 왜 배워야 하나?

### 실무에서:
- **데이터 분석**: 일별 매출의 월별 합계
- **게임 개발**: 데미지 누적, 점수 계산
- **이미지 처리**: 적분 이미지 (SAT)

### 코딩테스트에서:
- 출제 빈도: ⭐⭐⭐⭐⭐
- "구간 합", "부분 합" 키워드 = 무조건 누적합

---

## 🎯 핵심 개념 (5분 컷)

### 📚 통장 잔액으로 이해하기
```
통장 거래 내역:
1월: +100만
2월: +50만
3월: -30만
4월: +80만

누적 잔액:
prefix[1] = 100
prefix[2] = 150
prefix[3] = 120
prefix[4] = 200

"2월~4월 총 입출금?" = prefix[4] - prefix[1] = 100만원
→ 한 번의 빼기로 끝!
```

### 핵심 공식
```
prefix[i] = arr[0] + arr[1] + ... + arr[i]

구간 합 (i ~ j) = prefix[j] - prefix[i-1]
```

### 시간복잡도 비교
| 방법 | 전처리 | 쿼리 1회 | Q회 쿼리 |
|-----|-------|---------|---------|
| 브루트포스 | O(1) | O(n) | O(Q×n) |
| 누적합 | O(n) | O(1) | O(Q) |"""
            },
            {
                "type": "code",
                "language": "Python",
                "code": """# 🔰 누적합 기본 패턴

# 1. 1차원 누적합
def build_prefix_sum(arr):
    n = len(arr)
    prefix = [0] * (n + 1)  # 1-indexed (편의상)

    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]

    return prefix

def range_sum(prefix, left, right):
    \"\"\"arr[left] ~ arr[right] 합계 (0-indexed)\"\"\"
    return prefix[right + 1] - prefix[left]

# 사용 예시
arr = [1, 2, 3, 4, 5]
prefix = build_prefix_sum(arr)
print(prefix)  # [0, 1, 3, 6, 10, 15]

print(range_sum(prefix, 1, 3))  # 2+3+4 = 9
print(range_sum(prefix, 0, 4))  # 1+2+3+4+5 = 15

# 2. 2차원 누적합
def build_prefix_sum_2d(matrix):
    if not matrix:
        return []

    m, n = len(matrix), len(matrix[0])
    prefix = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m):
        for j in range(n):
            prefix[i+1][j+1] = (matrix[i][j]
                               + prefix[i][j+1]
                               + prefix[i+1][j]
                               - prefix[i][j])

    return prefix

def range_sum_2d(prefix, r1, c1, r2, c2):
    \"\"\"(r1,c1) ~ (r2,c2) 직사각형 합계\"\"\"
    return (prefix[r2+1][c2+1]
            - prefix[r1][c2+1]
            - prefix[r2+1][c1]
            + prefix[r1][c1])

# 3. 응용: 합이 K인 부분 배열 개수
from collections import defaultdict

def subarray_sum_equals_k(arr, k):
    count = 0
    current_sum = 0
    prefix_counts = defaultdict(int)
    prefix_counts[0] = 1  # 빈 prefix

    for num in arr:
        current_sum += num
        # current_sum - k가 이전에 나왔다면
        # 그 지점부터 현재까지의 합이 k
        count += prefix_counts[current_sum - k]
        prefix_counts[current_sum] += 1

    return count

print(subarray_sum_equals_k([1, 1, 1], 2))  # 2"""
            },
            {
                "type": "tip",
                "title": "💡 누적합 활용 팁",
                "content": """### 1-indexed vs 0-indexed

```python
# 0-indexed (직관적이지만 경계 처리 필요)
prefix[0] = arr[0]
for i in range(1, n):
    prefix[i] = prefix[i-1] + arr[i]

# 구간합: prefix[right] - prefix[left-1]
# left=0일 때 예외 처리 필요!

# 1-indexed (추천!)
prefix[0] = 0
for i in range(n):
    prefix[i+1] = prefix[i] + arr[i]

# 구간합: prefix[right+1] - prefix[left]
# 예외 처리 불필요!
```

### 차분 배열 (Difference Array)
```python
# 구간 [l, r]에 값 v를 더하기
# 매번 O(n) 대신 O(1)로!

diff = [0] * (n + 1)

# 구간 업데이트
diff[l] += v
diff[r + 1] -= v

# 최종 배열 복원
arr = []
current = 0
for d in diff[:-1]:
    current += d
    arr.append(current)
```"""
            },
            {
                "type": "practice",
                "title": "🎯 연습 문제",
                "content": """### Level 1: 기초
| 문제 | 플랫폼 | 포인트 |
|-----|-------|-------|
| 구간 합 구하기 4 (11659) | 백준 | 1차원 누적합 |
| 구간 합 구하기 5 (11660) | 백준 | 2차원 누적합 |

### Level 2: 응용
| 문제 | 플랫폼 | 포인트 |
|-----|-------|-------|
| 나머지 합 (10986) | 백준 | 모듈러 누적합 |
| Subarray Sum Equals K | LeetCode | 해시맵 활용 |

### Level 3: 심화
| 문제 | 플랫폼 | 포인트 |
|-----|-------|-------|
| Range Sum Query 2D | LeetCode | 2D 응용 |
| 구간 합 구하기 (2042) | 백준 | 세그먼트 트리 |"""
            }
        ]
    },

    "02_배열/kadane": {
        "title": "카데인 알고리즘",
        "description": "최대 부분 배열 합을 O(n)에 구하는 카데인 알고리즘입니다.",
        "language": "Python",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 카데인 알고리즘이란?",
                "content": """## 🔥 한 줄 요약
> **연속 부분 배열의 최대 합을 O(n)에 찾는 알고리즘** - DP의 교과서적 예제

---

## 💡 왜 배워야 하나?

### 실무에서:
- **주식 분석**: 최대 수익 구간 찾기
- **데이터 분석**: 연속된 이상치 구간 탐지
- **신호 처리**: 최대 에너지 구간

### 코딩테스트에서:
- 출제 빈도: ⭐⭐⭐⭐
- "최대 부분 배열", "연속 합" 키워드
- DP 입문 필수 문제

---

## 🎯 핵심 개념 (5분 컷)

### 📚 등산으로 이해하기
```
고도 변화: [-2, 1, -3, 4, -1, 2, 1, -5, 4]

질문: "가장 높이 올라갈 수 있는 연속 구간은?"

핵심 아이디어:
- 현재 위치에서 "이전까지의 합 + 나" vs "나만"
- 이전이 마이너스면 버리고 새로 시작!
```

### 핵심 공식
```
dp[i] = max(dp[i-1] + arr[i], arr[i])

해석:
- dp[i-1] + arr[i]: 이전 구간을 이어감
- arr[i]: 여기서 새로 시작

이전 합이 음수면 버리는 게 이득!
```

### 동작 예시
```
배열: [-2, 1, -3, 4, -1, 2, 1, -5, 4]

i=0: max(-2, -2) = -2
i=1: max(-2+1, 1) = 1    ← 새로 시작!
i=2: max(1-3, -3) = -2
i=3: max(-2+4, 4) = 4    ← 새로 시작!
i=4: max(4-1, -1) = 3
i=5: max(3+2, 2) = 5
i=6: max(5+1, 1) = 6     ← 최대!
i=7: max(6-5, -5) = 1
i=8: max(1+4, 4) = 5

최대 합 = 6 (구간: [4, -1, 2, 1])
```"""
            },
            {
                "type": "code",
                "language": "Python",
                "code": """# 🔰 카데인 알고리즘

# 1. 기본 버전
def max_subarray_sum(arr):
    if not arr:
        return 0

    max_ending_here = arr[0]  # 현재 위치까지의 최대 합
    max_so_far = arr[0]       # 전체 최대 합

    for i in range(1, len(arr)):
        # 이어갈지 vs 새로 시작할지
        max_ending_here = max(max_ending_here + arr[i], arr[i])
        max_so_far = max(max_so_far, max_ending_here)

    return max_so_far

arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print(max_subarray_sum(arr))  # 6

# 2. 구간 인덱스도 반환
def max_subarray_with_indices(arr):
    if not arr:
        return 0, -1, -1

    max_ending_here = arr[0]
    max_so_far = arr[0]
    start = end = temp_start = 0

    for i in range(1, len(arr)):
        if arr[i] > max_ending_here + arr[i]:
            max_ending_here = arr[i]
            temp_start = i  # 새로 시작
        else:
            max_ending_here = max_ending_here + arr[i]

        if max_ending_here > max_so_far:
            max_so_far = max_ending_here
            start = temp_start
            end = i

    return max_so_far, start, end

sum_val, start, end = max_subarray_with_indices(arr)
print(f"최대 합: {sum_val}, 구간: [{start}, {end}]")
# 최대 합: 6, 구간: [3, 6]

# 3. 모든 요소가 음수인 경우 처리
def max_subarray_sum_v2(arr):
    # 모두 음수면 가장 큰 음수 반환
    if max(arr) < 0:
        return max(arr)

    max_ending_here = 0
    max_so_far = 0

    for num in arr:
        max_ending_here = max(0, max_ending_here + num)
        max_so_far = max(max_so_far, max_ending_here)

    return max_so_far

# 4. 원형 배열에서 최대 부분 합
def max_circular_subarray_sum(arr):
    # 일반 카데인
    max_kadane = max_subarray_sum(arr)

    # 원형 고려: 전체 합 - 최소 부분 합
    total = sum(arr)
    # 배열 부호 반전 후 카데인 = 최소 부분 합
    min_kadane = -max_subarray_sum([-x for x in arr])

    # 모든 요소가 음수면 일반 카데인 결과 반환
    if min_kadane == total:
        return max_kadane

    return max(max_kadane, total - min_kadane)"""
            },
            {
                "type": "practice",
                "title": "🎯 연습 문제",
                "content": """### Level 1: 기초
| 문제 | 플랫폼 | 포인트 |
|-----|-------|-------|
| 연속합 (1912) | 백준 | 기본 카데인 |
| Maximum Subarray | LeetCode | 동일 |

### Level 2: 응용
| 문제 | 플랫폼 | 포인트 |
|-----|-------|-------|
| 최대 부분 배열 합 찾기 | 프로그래머스 | 구간 반환 |
| 연속합 2 (13398) | 백준 | 하나 제거 |

### Level 3: 심화
| 문제 | 플랫폼 | 포인트 |
|-----|-------|-------|
| Maximum Sum Circular Subarray | LeetCode | 원형 배열 |
| Maximum Product Subarray | LeetCode | 곱 버전 |"""
            }
        ]
    },

    "02_배열/practice-array": {
        "title": "배열 실전 문제",
        "description": "배열 관련 실전 문제 풀이 패턴을 학습합니다.",
        "language": "Python",
        "sections": [
            {
                "type": "concept",
                "title": "🎯 배열 문제 패턴",
                "content": """## 배열 문제 유형 정리

### 1️⃣ 순회 패턴
- 단순 순회: O(n)
- 이중 순회: O(n²)
- 역순 순회: `arr[::-1]` 또는 `reversed(arr)`

### 2️⃣ 투 포인터 패턴
- 양끝에서: 정렬된 배열의 합
- 같은 방향: 슬라이딩 윈도우, 중복 제거

### 3️⃣ 정렬 활용 패턴
- 정렬 후 이웃 비교
- K번째 수 찾기
- 중복 검사

### 4️⃣ 해시 활용 패턴
- 빈도수 카운팅
- 존재 여부 O(1) 확인
- 그룹핑

### 5️⃣ 누적합 패턴
- 구간 합 쿼리
- 차분 배열 (구간 업데이트)"""
            },
            {
                "type": "code",
                "language": "Python",
                "code": """# 🔰 배열 실전 문제 패턴

# 패턴 1: 두 수의 합 (해시 활용)
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# 패턴 2: 배열 회전
def rotate_array(nums, k):
    n = len(nums)
    k = k % n  # k가 n보다 클 경우

    # 방법 1: 슬라이싱
    return nums[-k:] + nums[:-k]

    # 방법 2: 역전 기법 (in-place)
    def reverse(arr, start, end):
        while start < end:
            arr[start], arr[end] = arr[end], arr[start]
            start += 1
            end -= 1

    reverse(nums, 0, n - 1)
    reverse(nums, 0, k - 1)
    reverse(nums, k, n - 1)

# 패턴 3: 과반수 요소 (보이어-무어 투표)
def majority_element(nums):
    candidate = None
    count = 0

    for num in nums:
        if count == 0:
            candidate = num
        count += 1 if num == candidate else -1

    return candidate

# 패턴 4: 중복 찾기 (공간 O(1))
def find_duplicate(nums):
    # Floyd's Cycle Detection
    slow = fast = nums[0]

    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break

    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]

    return slow

# 패턴 5: 배열 병합 (정렬된 두 배열)
def merge_sorted_arrays(nums1, m, nums2, n):
    # 뒤에서부터 채우기
    p1, p2, p = m - 1, n - 1, m + n - 1

    while p1 >= 0 and p2 >= 0:
        if nums1[p1] > nums2[p2]:
            nums1[p] = nums1[p1]
            p1 -= 1
        else:
            nums1[p] = nums2[p2]
            p2 -= 1
        p -= 1

    # nums2 남은 것 복사
    nums1[:p2 + 1] = nums2[:p2 + 1]"""
            },
            {
                "type": "practice",
                "title": "🎯 필수 연습 문제",
                "content": """### Must-Solve 문제 (면접 필수)

| 문제 | 플랫폼 | 패턴 |
|-----|-------|-----|
| Two Sum | LeetCode | 해시 |
| Best Time to Buy and Sell Stock | LeetCode | 단순 순회 |
| Contains Duplicate | LeetCode | 해시/정렬 |
| Product of Array Except Self | LeetCode | 누적곱 |
| Maximum Subarray | LeetCode | 카데인 |
| Merge Intervals | LeetCode | 정렬 |
| Rotate Array | LeetCode | 역전 기법 |
| Move Zeroes | LeetCode | 투 포인터 |

### 체크리스트
- [ ] 투 포인터 O(n²) → O(n) 최적화
- [ ] 해시맵으로 O(n) → O(1) 조회
- [ ] 정렬로 문제 단순화
- [ ] 누적합으로 구간 쿼리 O(1)
- [ ] 슬라이딩 윈도우 활용"""
            }
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
            print(f"✓ Updated: {key}")

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n총 {updated_count}개 항목 업데이트 완료!")
    return updated_count

if __name__ == "__main__":
    generate_content()
