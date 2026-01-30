# -*- coding: utf-8 -*-
"""
03_문자열, 03_연결리스트, 04_스택큐 콘텐츠
"""

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

ALGORITHM_CONTENTS = {
    # ===== 03_문자열 =====
    "03_문자열/string-basic": {
        "title": "문자열 기초",
        "description": "문자열 처리의 기본 개념과 주요 연산을 학습합니다.",
        "language": "Python",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 문자열이란?",
                "content": """## 🔥 한 줄 요약
> **문자들의 배열** - 텍스트 처리의 모든 것

---

## 💡 왜 배워야 하나?

### 실무에서:
- **입력 검증**: 이메일, 전화번호, 비밀번호 형식 검사
- **데이터 파싱**: JSON, CSV, 로그 파일 처리
- **검색 엔진**: 텍스트 매칭, 자동완성

### 코딩테스트에서:
- 출제 빈도: ⭐⭐⭐⭐⭐
- 문자열 처리는 거의 모든 문제에 등장

---

## 🎯 핵심 개념

### Python 문자열 특징
- **불변(Immutable)**: 한번 생성하면 수정 불가
- **시퀀스 타입**: 인덱싱, 슬라이싱 가능
- **유니코드 지원**: 한글, 이모지 등 처리 가능

### 주요 시간복잡도
| 연산 | 시간복잡도 |
|-----|----------|
| 인덱스 접근 s[i] | O(1) |
| 슬라이싱 s[i:j] | O(j-i) |
| 연결 s + t | O(len(s) + len(t)) |
| in 연산 | O(n) |
| 길이 len(s) | O(1) |"""
            },
            {
                "type": "code",
                "language": "Python",
                "code": """# 🔰 문자열 기본 연산

s = "Hello, World!"

# 1. 기본 연산
print(len(s))           # 13
print(s[0])             # 'H'
print(s[-1])            # '!'
print(s[0:5])           # 'Hello'
print(s[::-1])          # '!dlroW ,olleH' (뒤집기)

# 2. 검색
print('World' in s)     # True
print(s.find('o'))      # 4 (첫 번째 위치)
print(s.count('o'))     # 2 (개수)

# 3. 변환
print(s.lower())        # 소문자
print(s.upper())        # 대문자
print(s.replace('World', 'Python'))  # 치환

# 4. 분할과 결합
words = s.split(', ')   # ['Hello', 'World!']
joined = '-'.join(words)  # 'Hello-World!'

# 5. 공백 처리
text = "  hello  "
print(text.strip())     # 'hello'
print(text.lstrip())    # 'hello  '
print(text.rstrip())    # '  hello'

# 6. 문자열 검사
print("123".isdigit())  # True
print("abc".isalpha())  # True
print("abc123".isalnum())  # True

# 7. 효율적인 문자열 연결
# ❌ Bad: O(n²)
result = ""
for i in range(1000):
    result += str(i)

# ✅ Good: O(n)
result = ''.join(str(i) for i in range(1000))

# 8. 아스키 코드
print(ord('A'))  # 65
print(chr(65))   # 'A'"""
            },
            {
                "type": "practice",
                "title": "🎯 연습 문제",
                "content": """### 필수 문제
| 문제 | 플랫폼 | 포인트 |
|-----|-------|-------|
| 문자열 반복 (2675) | 백준 | 기초 |
| 단어의 개수 (1152) | 백준 | split |
| Valid Palindrome | LeetCode | 회문 |
| Reverse String | LeetCode | 뒤집기 |"""
            }
        ]
    },

    "03_문자열/kmp": {
        "title": "KMP 알고리즘",
        "description": "실패 함수를 이용한 O(n+m) 문자열 검색 알고리즘입니다.",
        "language": "Python",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 KMP란?",
                "content": """## 🔥 한 줄 요약
> **실패 함수로 불필요한 비교를 건너뛰는 문자열 검색** - O(n×m) → O(n+m)

---

## 💡 왜 배워야 하나?

### 실무에서:
- **텍스트 에디터**: Ctrl+F 검색 기능
- **DNA 서열 분석**: 패턴 매칭
- **네트워크**: 패킷 필터링

### 핵심 아이디어
```
패턴: ABABC
실패 함수: [0, 0, 1, 2, 0]

불일치 시, 처음부터 다시 비교하지 않고
이미 일치한 접두사 정보를 활용해 건너뛰기!
```"""
            },
            {
                "type": "code",
                "language": "Python",
                "code": """# 🔰 KMP 알고리즘

def build_failure(pattern):
    \"\"\"실패 함수 (부분 일치 테이블) 생성\"\"\"
    m = len(pattern)
    failure = [0] * m
    j = 0

    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = failure[j - 1]

        if pattern[i] == pattern[j]:
            j += 1
            failure[i] = j

    return failure

def kmp_search(text, pattern):
    \"\"\"KMP로 패턴 검색\"\"\"
    n, m = len(text), len(pattern)
    failure = build_failure(pattern)
    results = []
    j = 0

    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = failure[j - 1]

        if text[i] == pattern[j]:
            j += 1
            if j == m:  # 패턴 찾음
                results.append(i - m + 1)
                j = failure[j - 1]

    return results

# 테스트
text = "ABABDABACDABABCABAB"
pattern = "ABABC"
print(kmp_search(text, pattern))  # [10]
print(build_failure(pattern))  # [0, 0, 1, 2, 0]"""
            },
            {
                "type": "practice",
                "title": "🎯 연습 문제",
                "content": """| 문제 | 플랫폼 | 포인트 |
|-----|-------|-------|
| 찾기 (1786) | 백준 | KMP 기본 |
| 부분 문자열 (16916) | 백준 | KMP 응용 |
| Implement strStr() | LeetCode | 기본 |"""
            }
        ]
    },

    # ===== 03_연결리스트 =====
    "03_연결리스트/linkedlist-concept": {
        "title": "연결 리스트 개념",
        "description": "연결 리스트의 구조와 배열과의 차이점을 학습합니다.",
        "language": "Python",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 연결 리스트란?",
                "content": """## 🔥 한 줄 요약
> **노드들이 포인터로 연결된 선형 자료구조** - 삽입/삭제 O(1), 접근 O(n)

---

## 💡 배열 vs 연결 리스트

| 연산 | 배열 | 연결 리스트 |
|-----|-----|-----------|
| 인덱스 접근 | O(1) ✅ | O(n) |
| 맨 앞 삽입 | O(n) | O(1) ✅ |
| 맨 뒤 삽입 | O(1) | O(1)* |
| 중간 삽입 | O(n) | O(1)* |
| 메모리 | 연속 | 분산 |

*위치를 알고 있을 때

### 종류
1. **단일 연결 리스트**: 다음 노드만 가리킴
2. **이중 연결 리스트**: 앞/뒤 노드 모두 가리킴
3. **원형 연결 리스트**: 마지막이 처음을 가리킴"""
            },
            {
                "type": "code",
                "language": "Python",
                "code": """# 🔰 연결 리스트 구현

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, val):
        if not self.head:
            self.head = ListNode(val)
            return

        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = ListNode(val)

    def prepend(self, val):
        new_node = ListNode(val)
        new_node.next = self.head
        self.head = new_node

    def delete(self, val):
        if not self.head:
            return

        if self.head.val == val:
            self.head = self.head.next
            return

        curr = self.head
        while curr.next and curr.next.val != val:
            curr = curr.next

        if curr.next:
            curr.next = curr.next.next

    def display(self):
        result = []
        curr = self.head
        while curr:
            result.append(curr.val)
            curr = curr.next
        return result

# 테스트
ll = LinkedList()
ll.append(1)
ll.append(2)
ll.append(3)
print(ll.display())  # [1, 2, 3]
ll.prepend(0)
print(ll.display())  # [0, 1, 2, 3]
ll.delete(2)
print(ll.display())  # [0, 1, 3]"""
            },
            {
                "type": "practice",
                "title": "🎯 연습 문제",
                "content": """| 문제 | 플랫폼 | 포인트 |
|-----|-------|-------|
| Reverse Linked List | LeetCode | 뒤집기 |
| Merge Two Sorted Lists | LeetCode | 병합 |
| Remove Nth Node From End | LeetCode | 투포인터 |"""
            }
        ]
    },

    "03_연결리스트/linkedlist-operation": {
        "title": "연결 리스트 연산",
        "description": "연결 리스트의 주요 연산과 구현 방법을 학습합니다.",
        "language": "Python",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 주요 연산",
                "content": """## 필수 연산들

### 1. 뒤집기 (Reverse)
```
1 → 2 → 3 → NULL
3 → 2 → 1 → NULL
```

### 2. 중간 노드 찾기
- 투 포인터: slow는 1칸, fast는 2칸
- fast가 끝에 도달하면 slow가 중간

### 3. 병합 (Merge)
- 두 정렬된 리스트를 하나로

### 4. 사이클 감지
- Floyd's Cycle Detection (토끼와 거북이)"""
            },
            {
                "type": "code",
                "language": "Python",
                "code": """# 🔰 연결 리스트 필수 연산

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# 1. 뒤집기
def reverse_list(head):
    prev = None
    curr = head

    while curr:
        next_temp = curr.next
        curr.next = prev
        prev = curr
        curr = next_temp

    return prev

# 2. 중간 노드 찾기
def find_middle(head):
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow

# 3. 두 정렬 리스트 병합
def merge_two_lists(l1, l2):
    dummy = ListNode(0)
    curr = dummy

    while l1 and l2:
        if l1.val < l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next

    curr.next = l1 or l2
    return dummy.next

# 4. N번째 노드 삭제 (뒤에서)
def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    slow = fast = dummy

    # fast를 n+1칸 이동
    for _ in range(n + 1):
        fast = fast.next

    # slow와 fast 동시 이동
    while fast:
        slow = slow.next
        fast = fast.next

    # slow.next가 삭제할 노드
    slow.next = slow.next.next
    return dummy.next"""
            },
            {
                "type": "practice",
                "title": "🎯 연습 문제",
                "content": """| 문제 | 플랫폼 | 포인트 |
|-----|-------|-------|
| Palindrome Linked List | LeetCode | 중간+뒤집기 |
| Add Two Numbers | LeetCode | 자리올림 |
| Intersection of Two Linked Lists | LeetCode | 길이 맞추기 |"""
            }
        ]
    },

    "03_연결리스트/linkedlist-cycle": {
        "title": "연결 리스트 사이클",
        "description": "Floyd의 토끼와 거북이 알고리즘으로 사이클을 감지합니다.",
        "language": "Python",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 사이클 감지",
                "content": """## 🔥 한 줄 요약
> **두 포인터가 만나면 사이클 존재** - 토끼와 거북이 알고리즘

---

## Floyd's Cycle Detection

### 원리
```
slow: 1칸씩 이동
fast: 2칸씩 이동

사이클이 있으면 → 결국 만남
사이클이 없으면 → fast가 끝에 도달
```

### 사이클 시작점 찾기
1. slow, fast가 만나는 지점 찾기
2. slow를 head로 이동
3. slow, fast 모두 1칸씩 이동
4. 다시 만나는 지점 = 사이클 시작점"""
            },
            {
                "type": "code",
                "language": "Python",
                "code": """# 🔰 사이클 감지 및 시작점 찾기

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# 1. 사이클 존재 여부
def has_cycle(head):
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            return True

    return False

# 2. 사이클 시작점 찾기
def detect_cycle(head):
    slow = fast = head

    # 1단계: 만나는 지점 찾기
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            # 2단계: 시작점 찾기
            slow = head
            while slow != fast:
                slow = slow.next
                fast = fast.next
            return slow  # 사이클 시작점

    return None  # 사이클 없음

# 3. 사이클 길이
def cycle_length(head):
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            # 한 바퀴 돌아서 길이 측정
            length = 1
            current = slow.next
            while current != slow:
                length += 1
                current = current.next
            return length

    return 0"""
            },
            {
                "type": "practice",
                "title": "🎯 연습 문제",
                "content": """| 문제 | 플랫폼 | 포인트 |
|-----|-------|-------|
| Linked List Cycle | LeetCode | 존재 여부 |
| Linked List Cycle II | LeetCode | 시작점 |
| Find the Duplicate Number | LeetCode | 응용 |"""
            }
        ]
    },

    # ===== 04_스택큐 =====
    "04_스택큐/stack-concept": {
        "title": "스택 개념",
        "description": "LIFO 구조의 스택과 주요 활용 사례를 학습합니다.",
        "language": "Python",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 스택이란?",
                "content": """## 🔥 한 줄 요약
> **Last In First Out (LIFO)** - 가장 나중에 들어온 것이 먼저 나감

---

## 💡 왜 배워야 하나?

### 실무에서:
- **Undo 기능**: 최근 작업부터 취소
- **브라우저 뒤로가기**: 방문 기록 스택
- **함수 호출 스택**: 재귀, 콜스택
- **괄호 매칭**: 코드 에디터, 컴파일러

### 코딩테스트에서:
- 출제 빈도: ⭐⭐⭐⭐⭐
- "괄호", "역순", "가장 최근" 키워드

---

## 🎯 핵심 연산

| 연산 | 설명 | 시간복잡도 |
|-----|------|----------|
| push | 맨 위에 추가 | O(1) |
| pop | 맨 위 제거 및 반환 | O(1) |
| peek/top | 맨 위 확인 | O(1) |
| isEmpty | 비어있는지 확인 | O(1) |"""
            },
            {
                "type": "code",
                "language": "Python",
                "code": """# 🔰 스택 구현 및 활용

# Python에서는 리스트를 스택으로 사용
stack = []

# 기본 연산
stack.append(1)    # push
stack.append(2)
stack.append(3)
print(stack)       # [1, 2, 3]

top = stack.pop()  # pop
print(top)         # 3
print(stack)       # [1, 2]

peek = stack[-1]   # peek
print(peek)        # 2

is_empty = len(stack) == 0

# 활용 1: 괄호 매칭
def is_valid_parentheses(s):
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}

    for char in s:
        if char in '({[':
            stack.append(char)
        elif char in ')}]':
            if not stack or stack.pop() != pairs[char]:
                return False

    return len(stack) == 0

print(is_valid_parentheses("()[]{}"))  # True
print(is_valid_parentheses("([)]"))    # False

# 활용 2: 문자열 뒤집기
def reverse_string(s):
    stack = list(s)
    result = ""
    while stack:
        result += stack.pop()
    return result

# 활용 3: 10진수 → 2진수 변환
def decimal_to_binary(n):
    stack = []
    while n > 0:
        stack.append(n % 2)
        n //= 2

    result = ""
    while stack:
        result += str(stack.pop())
    return result or "0"

print(decimal_to_binary(10))  # "1010" """
            },
            {
                "type": "practice",
                "title": "🎯 연습 문제",
                "content": """| 문제 | 플랫폼 | 포인트 |
|-----|-------|-------|
| 스택 (10828) | 백준 | 기본 구현 |
| 괄호 (9012) | 백준 | 괄호 매칭 |
| Valid Parentheses | LeetCode | 세 종류 괄호 |
| Min Stack | LeetCode | 최솟값 O(1) |"""
            }
        ]
    },

    "04_스택큐/queue-concept": {
        "title": "큐 개념",
        "description": "FIFO 구조의 큐와 주요 활용 사례를 학습합니다.",
        "language": "Python",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 큐란?",
                "content": """## 🔥 한 줄 요약
> **First In First Out (FIFO)** - 먼저 들어온 것이 먼저 나감

---

## 💡 왜 배워야 하나?

### 실무에서:
- **메시지 큐**: Kafka, RabbitMQ
- **작업 스케줄링**: 프린터 대기열
- **BFS**: 그래프 탐색
- **캐시**: LRU 구현

### 코딩테스트에서:
- 출제 빈도: ⭐⭐⭐⭐⭐
- BFS 필수, "순서대로", "대기열" 키워드

---

## 🎯 핵심 연산

| 연산 | 설명 | 시간복잡도 |
|-----|------|----------|
| enqueue | 뒤에 추가 | O(1) |
| dequeue | 앞에서 제거 | O(1) |
| front | 앞 요소 확인 | O(1) |
| isEmpty | 비어있는지 | O(1) |"""
            },
            {
                "type": "code",
                "language": "Python",
                "code": """# 🔰 큐 구현 및 활용

from collections import deque

# Python에서는 deque 사용 (리스트의 pop(0)은 O(n)!)
queue = deque()

# 기본 연산
queue.append(1)     # enqueue
queue.append(2)
queue.append(3)
print(list(queue))  # [1, 2, 3]

front = queue.popleft()  # dequeue
print(front)        # 1
print(list(queue))  # [2, 3]

peek = queue[0]     # front (peek)
print(peek)         # 2

# 활용 1: BFS 기본 구조
def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return result

# 활용 2: 최근 N개 요소만 유지
class RecentCounter:
    def __init__(self, n):
        self.queue = deque()
        self.n = n

    def add(self, val):
        self.queue.append(val)
        if len(self.queue) > self.n:
            self.queue.popleft()

    def get_recent(self):
        return list(self.queue)

# 활용 3: 원형 큐
class CircularQueue:
    def __init__(self, k):
        self.queue = [None] * k
        self.size = k
        self.front = self.rear = -1

    def enqueue(self, val):
        if self.is_full():
            return False
        if self.is_empty():
            self.front = 0
        self.rear = (self.rear + 1) % self.size
        self.queue[self.rear] = val
        return True

    def dequeue(self):
        if self.is_empty():
            return None
        val = self.queue[self.front]
        if self.front == self.rear:
            self.front = self.rear = -1
        else:
            self.front = (self.front + 1) % self.size
        return val

    def is_empty(self):
        return self.front == -1

    def is_full(self):
        return (self.rear + 1) % self.size == self.front"""
            },
            {
                "type": "practice",
                "title": "🎯 연습 문제",
                "content": """| 문제 | 플랫폼 | 포인트 |
|-----|-------|-------|
| 큐 (10845) | 백준 | 기본 구현 |
| 요세푸스 문제 (1158) | 백준 | 원형 큐 |
| Design Circular Queue | LeetCode | 원형 큐 |
| Number of Recent Calls | LeetCode | 시간 윈도우 |"""
            }
        ]
    },

    "04_스택큐/deque": {
        "title": "덱 (Deque)",
        "description": "양쪽에서 삽입/삭제 가능한 덱을 학습합니다.",
        "language": "Python",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 덱이란?",
                "content": """## 🔥 한 줄 요약
> **Double-Ended Queue** - 양쪽에서 삽입/삭제 가능한 자료구조

---

## 덱 = 스택 + 큐

| 연산 | 시간복잡도 |
|-----|----------|
| appendleft | O(1) |
| append | O(1) |
| popleft | O(1) |
| pop | O(1) |

### 활용 사례
- 슬라이딩 윈도우 최대/최소
- 회문 검사
- 작업 스케줄링"""
            },
            {
                "type": "code",
                "language": "Python",
                "code": """from collections import deque

# 기본 연산
dq = deque()

dq.append(1)       # 오른쪽 추가
dq.appendleft(0)   # 왼쪽 추가
dq.append(2)
print(list(dq))    # [0, 1, 2]

dq.pop()           # 오른쪽 제거
dq.popleft()       # 왼쪽 제거
print(list(dq))    # [1]

# 슬라이딩 윈도우 최댓값 (덱 활용)
def max_sliding_window(nums, k):
    dq = deque()  # 인덱스 저장
    result = []

    for i in range(len(nums)):
        # 윈도우 벗어난 요소 제거
        if dq and dq[0] < i - k + 1:
            dq.popleft()

        # 현재 값보다 작은 값들 제거
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()

        dq.append(i)

        # 윈도우 완성 후 최댓값 기록
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result

print(max_sliding_window([1,3,-1,-3,5,3,6,7], 3))
# [3, 3, 5, 5, 6, 7]"""
            },
            {
                "type": "practice",
                "title": "🎯 연습 문제",
                "content": """| 문제 | 플랫폼 | 포인트 |
|-----|-------|-------|
| 덱 (10866) | 백준 | 기본 구현 |
| AC (5430) | 백준 | 덱 활용 |
| Sliding Window Maximum | LeetCode | 모노토닉 덱 |"""
            }
        ]
    },

    "04_스택큐/priority-queue": {
        "title": "우선순위 큐",
        "description": "힙 기반의 우선순위 큐를 학습합니다.",
        "language": "Python",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 우선순위 큐란?",
                "content": """## 🔥 한 줄 요약
> **우선순위가 높은 것이 먼저 나오는 큐** - 힙으로 구현

---

## 힙 vs 정렬

| 연산 | 우선순위 큐(힙) | 정렬 |
|-----|--------------|-----|
| 삽입 | O(log n) | O(n) |
| 최솟값 추출 | O(log n) | O(1) |
| 최솟값 확인 | O(1) | O(1) |

### 활용
- 다익스트라 최단 경로
- 작업 스케줄링
- K번째 큰/작은 수"""
            },
            {
                "type": "code",
                "language": "Python",
                "code": """import heapq

# 최소 힙 (기본)
min_heap = []
heapq.heappush(min_heap, 3)
heapq.heappush(min_heap, 1)
heapq.heappush(min_heap, 2)
print(heapq.heappop(min_heap))  # 1 (최솟값)

# 최대 힙 (부호 반전)
max_heap = []
heapq.heappush(max_heap, -3)
heapq.heappush(max_heap, -1)
heapq.heappush(max_heap, -2)
print(-heapq.heappop(max_heap))  # 3 (최댓값)

# K번째 큰 수
def kth_largest(nums, k):
    heap = nums[:k]
    heapq.heapify(heap)  # O(k)

    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)  # O(log k)

    return heap[0]

print(kth_largest([3,2,1,5,6,4], 2))  # 5

# 힙 정렬
def heap_sort(arr):
    heapq.heapify(arr)
    return [heapq.heappop(arr) for _ in range(len(arr))]"""
            },
            {
                "type": "practice",
                "title": "🎯 연습 문제",
                "content": """| 문제 | 플랫폼 | 포인트 |
|-----|-------|-------|
| 최소 힙 (1927) | 백준 | 기본 |
| 최대 힙 (11279) | 백준 | 부호 반전 |
| Kth Largest Element | LeetCode | K번째 |
| Top K Frequent Elements | LeetCode | 빈도 |"""
            }
        ]
    },

    "04_스택큐/monotonic-stack": {
        "title": "모노토닉 스택",
        "description": "단조 증가/감소를 유지하는 스택 기법입니다.",
        "language": "Python",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 모노토닉 스택이란?",
                "content": """## 🔥 한 줄 요약
> **단조 증가/감소 순서를 유지하는 스택** - O(n²) → O(n)

---

## 활용 사례
- 다음 큰/작은 수 찾기 (NGE, NLE)
- 히스토그램 최대 넓이
- 빗물 받기

### 핵심 아이디어
```
현재 값보다 작은(또는 큰) 값들을 스택에서 제거
→ 스택 맨 위 = 현재 값의 "다음 큰 수"
```"""
            },
            {
                "type": "code",
                "language": "Python",
                "code": """# 다음 큰 수 (Next Greater Element)
def next_greater_element(nums):
    n = len(nums)
    result = [-1] * n
    stack = []  # 인덱스 저장

    for i in range(n):
        # 현재 값이 스택 top보다 크면
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)

    return result

print(next_greater_element([2,1,2,4,3]))
# [4, 2, 4, -1, -1]

# 히스토그램 최대 넓이
def largest_rectangle(heights):
    stack = []  # (인덱스, 높이)
    max_area = 0
    heights.append(0)  # 마지막 처리용

    for i, h in enumerate(heights):
        start = i
        while stack and stack[-1][1] > h:
            idx, height = stack.pop()
            max_area = max(max_area, height * (i - idx))
            start = idx
        stack.append((start, h))

    return max_area

print(largest_rectangle([2,1,5,6,2,3]))  # 10"""
            },
            {
                "type": "practice",
                "title": "🎯 연습 문제",
                "content": """| 문제 | 플랫폼 | 포인트 |
|-----|-------|-------|
| 오큰수 (17298) | 백준 | NGE |
| 히스토그램 (6549) | 백준 | 최대 넓이 |
| Daily Temperatures | LeetCode | NGE 응용 |
| Trapping Rain Water | LeetCode | 스택/투포 |"""
            }
        ]
    },

    "04_스택큐/stack-problem": {
        "title": "스택 응용 문제",
        "description": "스택을 활용한 다양한 문제 패턴을 학습합니다.",
        "language": "Python",
        "sections": [
            {
                "type": "concept",
                "title": "🎯 스택 문제 패턴",
                "content": """## 스택 문제 유형

### 1. 괄호 매칭
- 여는 괄호: push
- 닫는 괄호: pop 후 매칭 확인

### 2. 수식 계산
- 후위 표기법 계산
- 중위 → 후위 변환

### 3. 문자열 처리
- 역순 출력
- 뒤집기

### 4. 다음/이전 큰/작은 수
- 모노토닉 스택"""
            },
            {
                "type": "code",
                "language": "Python",
                "code": """# 후위 표기법 계산
def eval_postfix(expression):
    stack = []
    operators = {'+', '-', '*', '/'}

    for token in expression.split():
        if token not in operators:
            stack.append(int(token))
        else:
            b = stack.pop()
            a = stack.pop()
            if token == '+': stack.append(a + b)
            elif token == '-': stack.append(a - b)
            elif token == '*': stack.append(a * b)
            elif token == '/': stack.append(int(a / b))

    return stack[0]

print(eval_postfix("2 3 + 4 *"))  # (2+3)*4 = 20

# 중위 → 후위 변환
def infix_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    stack = []
    result = []

    for token in expression.split():
        if token.isdigit():
            result.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                result.append(stack.pop())
            stack.pop()  # '(' 제거
        else:  # 연산자
            while (stack and stack[-1] != '(' and
                   stack[-1] in precedence and
                   precedence[stack[-1]] >= precedence[token]):
                result.append(stack.pop())
            stack.append(token)

    while stack:
        result.append(stack.pop())

    return ' '.join(result)"""
            },
            {
                "type": "practice",
                "title": "🎯 연습 문제",
                "content": """| 문제 | 플랫폼 | 포인트 |
|-----|-------|-------|
| 후위 표기식2 (1935) | 백준 | 후위 계산 |
| 후위 표기식 (1918) | 백준 | 중위→후위 |
| Basic Calculator | LeetCode | 수식 계산 |
| Decode String | LeetCode | 중첩 처리 |"""
            }
        ]
    },

    "04_스택큐/practice-stack-queue": {
        "title": "스택/큐 실전",
        "description": "스택과 큐를 활용한 실전 문제 풀이입니다.",
        "language": "Python",
        "sections": [
            {
                "type": "concept",
                "title": "🎯 실전 패턴 정리",
                "content": """## 스택 vs 큐 선택 기준

### 스택 사용
- 역순 처리
- 짝 맞추기 (괄호)
- 가장 최근 것 처리
- DFS, 재귀 시뮬레이션

### 큐 사용
- 순서대로 처리
- BFS
- 시간순 처리
- 버퍼, 대기열"""
            },
            {
                "type": "code",
                "language": "Python",
                "code": """from collections import deque

# 문제 1: 스택으로 큐 구현
class MyQueue:
    def __init__(self):
        self.stack_in = []
        self.stack_out = []

    def push(self, x):
        self.stack_in.append(x)

    def pop(self):
        if not self.stack_out:
            while self.stack_in:
                self.stack_out.append(self.stack_in.pop())
        return self.stack_out.pop()

# 문제 2: 큐로 스택 구현
class MyStack:
    def __init__(self):
        self.queue = deque()

    def push(self, x):
        self.queue.append(x)
        for _ in range(len(self.queue) - 1):
            self.queue.append(self.queue.popleft())

    def pop(self):
        return self.queue.popleft()

# 문제 3: 프린터 큐
def printer_queue(priorities, location):
    queue = deque(enumerate(priorities))
    order = 0

    while queue:
        idx, priority = queue.popleft()
        if any(p > priority for _, p in queue):
            queue.append((idx, priority))
        else:
            order += 1
            if idx == location:
                return order"""
            },
            {
                "type": "practice",
                "title": "🎯 필수 문제",
                "content": """| 문제 | 플랫폼 | 포인트 |
|-----|-------|-------|
| 프린터 큐 (1966) | 백준 | 시뮬레이션 |
| Implement Queue using Stacks | LeetCode | 스택→큐 |
| Implement Stack using Queues | LeetCode | 큐→스택 |
| 카드2 (2164) | 백준 | 큐 시뮬 |"""
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
            print(f"✓ {key}")

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n{updated_count}개 완료!")
    return updated_count

if __name__ == "__main__":
    generate_content()
