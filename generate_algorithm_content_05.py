# -*- coding: utf-8 -*-
"""
08_탐색, 08_트리, 09_그래프, 10_최단경로 콘텐츠
"""

import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

ALGORITHM_CONTENTS = {
    # ===== 08_탐색 =====
    "08_탐색/linear-search": {
        "title": "선형 탐색",
        "description": "처음부터 끝까지 순차적으로 탐색하는 O(n) 알고리즘입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 선형 탐색", "content": """## 🔥 한 줄 요약
> **처음부터 하나씩 확인** - 가장 단순, O(n)

### 특징
- 정렬 불필요
- 시간: O(n)
- 데이터가 적거나 정렬 비용이 클 때 사용"""},
            {"type": "code", "language": "Python", "code": """def linear_search(arr, target):
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1

# Python 내장
arr = [3, 1, 4, 1, 5]
if target in arr:
    idx = arr.index(target)"""},
            {"type": "practice", "title": "🎯 연습", "content": """선형 탐색은 기본. 데이터가 많으면 이진 탐색이나 해시 사용."""}
        ]
    },

    "08_탐색/binary-search-variant": {
        "title": "이진 탐색 변형",
        "description": "Lower Bound, Upper Bound 등 이진 탐색 변형입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 이진 탐색 변형", "content": """## 변형 종류

### Lower Bound
- target **이상**인 첫 위치
- `bisect_left`

### Upper Bound
- target **초과**인 첫 위치
- `bisect_right`

### 활용
- 범위 내 개수 = upper - lower
- 삽입 위치 찾기"""},
            {"type": "code", "language": "Python", "code": """from bisect import bisect_left, bisect_right

arr = [1, 2, 2, 2, 3, 4]

# Lower Bound: 2 이상인 첫 위치
print(bisect_left(arr, 2))   # 1

# Upper Bound: 2 초과인 첫 위치
print(bisect_right(arr, 2))  # 4

# 2의 개수
count = bisect_right(arr, 2) - bisect_left(arr, 2)  # 3

# 직접 구현
def lower_bound(arr, target):
    left, right = 0, len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 숫자 카드 2 (10816) | 개수 |
| 랜선 자르기 (1654) | 파라메트릭 |"""}
        ]
    },

    # ===== 08_트리 =====
    "08_트리/tree-basic": {
        "title": "트리 기초",
        "description": "트리의 기본 속성과 구현을 학습합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 트리 기초", "content": """## 트리 속성

- 노드 N개 → 간선 N-1개
- 루트에서 모든 노드까지 경로 유일
- 사이클 없음

### 용어
- 부모, 자식, 형제
- 조상, 자손
- 레벨, 높이, 깊이"""},
            {"type": "code", "language": "Python", "code": """class TreeNode:
    def __init__(self, val):
        self.val = val
        self.children = []

# 부모 배열로 트리 표현
# parent[i] = i의 부모 노드
parent = [-1, 0, 0, 1, 1]  # 0이 루트

# 인접 리스트로 트리 표현
tree = {
    0: [1, 2],
    1: [3, 4],
    2: [],
    3: [],
    4: []
}"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 트리의 부모 찾기 (11725) | BFS/DFS |
| 트리의 지름 (1167) | DFS 2회 |"""}
        ]
    },

    "08_트리/binary-tree": {
        "title": "이진 트리",
        "description": "자식이 최대 2개인 이진 트리를 학습합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 이진 트리", "content": """## 이진 트리 종류

### 완전 이진 트리
- 왼쪽부터 차례로 채움
- 힙에 사용

### 포화 이진 트리
- 모든 레벨이 꽉 참
- 노드 수 = 2^h - 1

### 높이 h 이진 트리
- 최소 노드: h개 (편향)
- 최대 노드: 2^h - 1개"""},
            {"type": "code", "language": "Python", "code": """class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# 높이 계산
def height(node):
    if not node:
        return 0
    return 1 + max(height(node.left), height(node.right))

# 노드 수 계산
def count(node):
    if not node:
        return 0
    return 1 + count(node.left) + count(node.right)

# 완전 이진 트리: 배열로 표현
# 부모 i의 왼쪽 자식: 2*i+1, 오른쪽 자식: 2*i+2
arr = [1, 2, 3, 4, 5]  # 레벨 순서"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| Invert Binary Tree | LeetCode |
| Symmetric Tree | LeetCode |"""}
        ]
    },

    "08_트리/bst": {
        "title": "이진 탐색 트리 (BST)",
        "description": "왼쪽 < 부모 < 오른쪽 속성의 BST를 학습합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 BST란?", "content": """## 🔥 한 줄 요약
> **왼쪽 자식 < 부모 < 오른쪽 자식** - 탐색/삽입/삭제 O(log n)

### 특징
- 중위 순회 = 정렬된 순서
- 평균 O(log n), 최악 O(n)

### 주의
- 균형 유지 안 하면 편향될 수 있음"""},
            {"type": "code", "language": "Python", "code": """class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def search(root, target):
    if not root or root.val == target:
        return root
    if target < root.val:
        return search(root.left, target)
    return search(root.right, target)

def insert(root, val):
    if not root:
        return TreeNode(val)
    if val < root.val:
        root.left = insert(root.left, val)
    else:
        root.right = insert(root.right, val)
    return root

# 중위 순회 = 정렬 결과
def inorder(root):
    if not root:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| Validate BST | LeetCode |
| Kth Smallest Element in BST | LeetCode |
| 이진 검색 트리 (5639) | 백준 |"""}
        ]
    },

    # ===== 09_그래프 =====
    "09_그래프/graph-concept": {
        "title": "그래프 개념",
        "description": "그래프의 기본 개념과 용어를 학습합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 그래프란?", "content": """## 🔥 한 줄 요약
> **정점(Vertex)과 간선(Edge)으로 연결된 자료구조**

### 그래프 종류
- **무방향 vs 방향**
- **가중치 vs 비가중치**
- **연결 vs 비연결**
- **사이클 있음 vs 없음 (DAG)**

### 용어
- 정점 (Vertex, Node)
- 간선 (Edge)
- 차수 (Degree): 연결된 간선 수
- 경로 (Path): 정점들의 나열
- 사이클 (Cycle): 시작=끝인 경로"""},
            {"type": "code", "language": "Python", "code": """# 그래프 표현

# 1. 인접 행렬 (2차원 배열)
# 장점: O(1) 연결 확인
# 단점: O(V²) 공간
adj_matrix = [
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 0]
]

# 2. 인접 리스트 (대부분 이걸 사용)
# 장점: O(V+E) 공간
# 단점: O(V) 연결 확인
from collections import defaultdict
adj_list = defaultdict(list)
adj_list[0] = [1, 2]
adj_list[1] = [0, 3]
adj_list[2] = [0, 3]
adj_list[3] = [1, 2]"""},
            {"type": "practice", "title": "🎯 연습", "content": """그래프 문제는 DFS/BFS로 탐색하는 것이 기본!"""}
        ]
    },

    "09_그래프/graph-representation": {
        "title": "그래프 표현",
        "description": "인접 행렬과 인접 리스트로 그래프를 표현합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 그래프 표현법", "content": """## 인접 행렬 vs 인접 리스트

| 특성 | 인접 행렬 | 인접 리스트 |
|-----|---------|-----------|
| 공간 | O(V²) | O(V+E) |
| 연결 확인 | O(1) | O(V) |
| 모든 간선 순회 | O(V²) | O(V+E) |
| 적합한 경우 | 밀집 그래프 | 희소 그래프 |

### 코테에서는 거의 인접 리스트 사용!"""},
            {"type": "code", "language": "Python", "code": """# 입력 처리 패턴
n, m = map(int, input().split())  # 정점, 간선 수

# 인접 리스트
graph = [[] for _ in range(n + 1)]
for _ in range(m):
    a, b = map(int, input().split())
    graph[a].append(b)
    graph[b].append(a)  # 무방향이면

# 가중치 그래프
graph = [[] for _ in range(n + 1)]
for _ in range(m):
    a, b, w = map(int, input().split())
    graph[a].append((b, w))
    graph[b].append((a, w))"""},
            {"type": "practice", "title": "🎯 연습", "content": """그래프 입력 처리는 숙달 필수!"""}
        ]
    },

    "09_그래프/dfs": {
        "title": "DFS (깊이 우선 탐색)",
        "description": "스택/재귀를 이용한 깊이 우선 탐색입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 DFS란?", "content": """## 🔥 한 줄 요약
> **한 방향으로 끝까지 가고, 막히면 돌아와서 다른 길** - 스택/재귀 사용

### 특징
- 시간: O(V+E)
- 공간: O(V) 재귀 깊이
- 모든 경로 탐색, 백트래킹

### 활용
- 경로 찾기
- 사이클 검출
- 연결 요소
- 위상 정렬"""},
            {"type": "code", "language": "Python", "code": """# 재귀 DFS
def dfs_recursive(graph, node, visited):
    visited.add(node)
    print(node)  # 방문 처리

    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)

# 스택 DFS
def dfs_stack(graph, start):
    visited = set()
    stack = [start]

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            print(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    stack.append(neighbor)

# 사용
graph = {
    1: [2, 3],
    2: [4, 5],
    3: [],
    4: [],
    5: []
}
dfs_recursive(graph, 1, set())"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| DFS와 BFS (1260) | 기본 |
| 연결 요소의 개수 (11724) | 개수 세기 |
| 타겟 넘버 | 프로그래머스 |"""}
        ]
    },

    "09_그래프/bfs": {
        "title": "BFS (너비 우선 탐색)",
        "description": "큐를 이용한 너비 우선 탐색입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 BFS란?", "content": """## 🔥 한 줄 요약
> **가까운 것부터 차례로 탐색** - 큐 사용, 최단 경로!

### 특징
- 시간: O(V+E)
- 공간: O(V)
- **비가중치 최단 경로 보장**

### 활용
- 최단 경로 (비가중치)
- 레벨별 탐색
- 연결 확인"""},
            {"type": "code", "language": "Python", "code": """from collections import deque

def bfs(graph, start):
    visited = set([start])
    queue = deque([start])

    while queue:
        node = queue.popleft()
        print(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

# 최단 거리 구하기
def bfs_distance(graph, start, end):
    visited = set([start])
    queue = deque([(start, 0)])  # (노드, 거리)

    while queue:
        node, dist = queue.popleft()
        if node == end:
            return dist

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))

    return -1  # 도달 불가"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| DFS와 BFS (1260) | 기본 |
| 미로 탐색 (2178) | 최단 거리 |
| 토마토 (7576) | 다중 시작점 |
| 숨바꼭질 (1697) | 상태 공간 |"""}
        ]
    },

    "09_그래프/dfs-bfs-compare": {
        "title": "DFS vs BFS",
        "description": "DFS와 BFS의 차이점과 선택 기준입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 DFS vs BFS", "content": """## 비교

| 특성 | DFS | BFS |
|-----|-----|-----|
| 자료구조 | 스택/재귀 | 큐 |
| 탐색 순서 | 깊이 우선 | 너비 우선 |
| 최단 경로 | ❌ | ✅ (비가중치) |
| 메모리 | 경로 길이 | 너비 |

### 선택 기준
- **최단 경로** 필요 → BFS
- **모든 경로 탐색** → DFS
- **경로 조건** (백트래킹) → DFS
- **그래프가 넓음** → DFS
- **그래프가 깊음** → BFS"""},
            {"type": "code", "language": "Python", "code": """# DFS: 모든 경로 찾기
def all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    paths = []
    for node in graph[start]:
        if node not in path:
            paths.extend(all_paths(graph, node, end, path))
    return paths

# BFS: 최단 경로 (비가중치)
from collections import deque
def shortest_path(graph, start, end):
    queue = deque([(start, [start])])
    visited = {start}
    while queue:
        node, path = queue.popleft()
        if node == end:
            return path
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return []"""},
            {"type": "practice", "title": "🎯 연습", "content": """문제 유형 파악:
- "최단", "최소 이동" → BFS
- "모든 경우", "조건 만족" → DFS"""}
        ]
    },

    "09_그래프/connected-component": {
        "title": "연결 요소",
        "description": "그래프에서 연결된 컴포넌트를 찾습니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 연결 요소", "content": """## 🔥 한 줄 요약
> **서로 연결된 노드들의 그룹** - DFS/BFS로 개수 세기

### 개수 세기 알고리즘
1. 모든 노드 순회
2. 방문 안 한 노드에서 DFS/BFS
3. 탐색 시작할 때마다 카운트 +1"""},
            {"type": "code", "language": "Python", "code": """def count_components(n, graph):
    visited = [False] * (n + 1)
    count = 0

    def dfs(node):
        visited[node] = True
        for neighbor in graph[node]:
            if not visited[neighbor]:
                dfs(neighbor)

    for i in range(1, n + 1):
        if not visited[i]:
            dfs(i)
            count += 1

    return count

# Union-Find로도 가능
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px != py:
            self.parent[px] = py"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 연결 요소의 개수 (11724) | 기본 |
| 섬의 개수 (4963) | 2D 그리드 |
| Number of Islands | LeetCode |"""}
        ]
    },

    "09_그래프/cycle-detection": {
        "title": "사이클 탐지",
        "description": "그래프에서 사이클 존재 여부를 확인합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 사이클 탐지", "content": """## 방법

### 무방향 그래프
- DFS로 이미 방문한 노드를 다시 만남 (부모 제외)

### 방향 그래프
- 방문 상태 3가지로 관리
  - 0: 미방문
  - 1: 현재 경로에서 방문 중
  - 2: 완전 탐색 완료"""},
            {"type": "code", "language": "Python", "code": """# 무방향 그래프 사이클
def has_cycle_undirected(n, graph):
    visited = [False] * (n + 1)

    def dfs(node, parent):
        visited[node] = True
        for neighbor in graph[node]:
            if not visited[neighbor]:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                return True
        return False

    for i in range(1, n + 1):
        if not visited[i]:
            if dfs(i, -1):
                return True
    return False

# 방향 그래프 사이클
def has_cycle_directed(n, graph):
    state = [0] * (n + 1)  # 0: 미방문, 1: 방문중, 2: 완료

    def dfs(node):
        state[node] = 1
        for neighbor in graph[node]:
            if state[neighbor] == 1:  # 사이클!
                return True
            if state[neighbor] == 0:
                if dfs(neighbor):
                    return True
        state[node] = 2
        return False

    for i in range(1, n + 1):
        if state[i] == 0:
            if dfs(i):
                return True
    return False"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| Course Schedule | LeetCode |
| 텀 프로젝트 (9466) | 백준 |"""}
        ]
    },

    "09_그래프/topological-sort": {
        "title": "위상 정렬",
        "description": "DAG에서 선후 관계를 지키며 정렬합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 위상 정렬", "content": """## 🔥 한 줄 요약
> **선행 조건을 지키며 순서대로 나열** - DAG(비순환 방향 그래프)에서만 가능

### 활용
- 강의 수강 순서
- 빌드 의존성
- 작업 스케줄링

### 방법
1. **Kahn's Algorithm**: 진입차수 0인 것부터
2. **DFS**: 후위 순회 역순"""},
            {"type": "code", "language": "Python", "code": """from collections import deque

# Kahn's Algorithm (BFS 기반)
def topological_sort(n, graph):
    indegree = [0] * (n + 1)
    for node in range(1, n + 1):
        for neighbor in graph[node]:
            indegree[neighbor] += 1

    queue = deque()
    for i in range(1, n + 1):
        if indegree[i] == 0:
            queue.append(i)

    result = []
    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    if len(result) != n:
        return []  # 사이클 존재
    return result

# DFS 기반
def topological_sort_dfs(n, graph):
    visited = [False] * (n + 1)
    result = []

    def dfs(node):
        visited[node] = True
        for neighbor in graph[node]:
            if not visited[neighbor]:
                dfs(neighbor)
        result.append(node)

    for i in range(1, n + 1):
        if not visited[i]:
            dfs(i)

    return result[::-1]"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 줄 세우기 (2252) | 기본 |
| 작업 (2056) | DP와 결합 |
| Course Schedule II | LeetCode |"""}
        ]
    },

    "09_그래프/practice-graph": {
        "title": "그래프 실전",
        "description": "그래프 문제 풀이 패턴입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🎯 그래프 패턴", "content": """## 문제 유형별 접근

### 1. 탐색
- 연결 확인 → DFS/BFS
- 최단 거리 → BFS

### 2. 연결 요소
- 개수 세기 → DFS + 카운트
- 그룹화 → Union-Find

### 3. 최단 경로
- 비가중치 → BFS
- 가중치 → 다익스트라/벨만포드

### 4. 순서
- 선후 관계 → 위상 정렬"""},
            {"type": "code", "language": "Python", "code": """# 2D 그리드 탐색 패턴
dx = [-1, 1, 0, 0]  # 상하좌우
dy = [0, 0, -1, 1]

def bfs_grid(grid, start_x, start_y):
    n, m = len(grid), len(grid[0])
    visited = [[False] * m for _ in range(n)]
    queue = deque([(start_x, start_y)])
    visited[start_x][start_y] = True

    while queue:
        x, y = queue.popleft()
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if 0 <= nx < n and 0 <= ny < m:
                if not visited[nx][ny] and grid[nx][ny] == 1:
                    visited[nx][ny] = True
                    queue.append((nx, ny))"""},
            {"type": "practice", "title": "🎯 필수 문제", "content": """| 문제 | 유형 |
|-----|-----|
| 미로 탐색 (2178) | BFS 최단 |
| 토마토 (7576) | 다중 시작 |
| 연결 요소 (11724) | 컴포넌트 |
| 줄 세우기 (2252) | 위상 정렬 |"""}
        ]
    },

    # ===== 10_최단경로 =====
    "10_최단경로/dijkstra": {
        "title": "다익스트라",
        "description": "음이 아닌 가중치 그래프의 최단 경로를 O((V+E)log V)에 구합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 다익스트라", "content": """## 🔥 한 줄 요약
> **가장 가까운 노드부터 확정** - 그리디 + 우선순위 큐

### 조건
- 음수 가중치 ❌
- 한 정점에서 다른 모든 정점까지

### 시간복잡도
- 힙 사용: O((V+E) log V)
- 배열 사용: O(V²)"""},
            {"type": "code", "language": "Python", "code": """import heapq

def dijkstra(graph, start, n):
    dist = [float('inf')] * (n + 1)
    dist[start] = 0
    heap = [(0, start)]  # (거리, 노드)

    while heap:
        d, node = heapq.heappop(heap)

        if d > dist[node]:
            continue

        for neighbor, weight in graph[node]:
            new_dist = d + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))

    return dist

# 사용
graph = [[] for _ in range(n + 1)]
for _ in range(m):
    u, v, w = map(int, input().split())
    graph[u].append((v, w))

distances = dijkstra(graph, 1, n)"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 최단경로 (1753) | 기본 |
| 특정한 최단 경로 (1504) | 경유 |
| 최소비용 구하기 (1916) | 응용 |"""}
        ]
    },

    "10_최단경로/bellman-ford": {
        "title": "벨만-포드",
        "description": "음수 가중치가 있는 그래프의 최단 경로를 O(VE)에 구합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 벨만-포드", "content": """## 🔥 한 줄 요약
> **모든 간선을 V-1번 반복** - 음수 가중치 OK, 음수 사이클 탐지

### 특징
- 음수 가중치 ✅
- 음수 사이클 탐지 가능
- O(VE) - 다익스트라보다 느림"""},
            {"type": "code", "language": "Python", "code": """def bellman_ford(n, edges, start):
    dist = [float('inf')] * (n + 1)
    dist[start] = 0

    # V-1번 반복
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # 음수 사이클 체크 (한 번 더)
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            return None  # 음수 사이클 존재

    return dist"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 타임머신 (11657) | 음수 사이클 |
| 웜홀 (1865) | 음수 사이클 |"""}
        ]
    },

    "10_최단경로/floyd-warshall": {
        "title": "플로이드-워셜",
        "description": "모든 쌍의 최단 경로를 O(V³)에 구합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 플로이드-워셜", "content": """## 🔥 한 줄 요약
> **모든 노드를 경유지로 시도** - 모든 쌍 최단 거리

### 특징
- 시간: O(V³)
- 공간: O(V²)
- 음수 가중치 OK (음수 사이클 제외)
- V ≤ 500 정도에서 사용"""},
            {"type": "code", "language": "Python", "code": """def floyd_warshall(n, graph):
    INF = float('inf')
    dist = [[INF] * (n + 1) for _ in range(n + 1)]

    # 초기화
    for i in range(1, n + 1):
        dist[i][i] = 0
    for u, v, w in graph:
        dist[u][v] = w

    # k를 경유지로
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    return dist"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 플로이드 (11404) | 기본 |
| 케빈 베이컨의 6단계 법칙 (1389) | 응용 |"""}
        ]
    },

    "10_최단경로/shortest-path-compare": {
        "title": "최단 경로 비교",
        "description": "다익스트라, 벨만-포드, 플로이드-워셜을 비교합니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🔥 알고리즘 선택", "content": """## 비교표

| 알고리즘 | 시간 | 음수 | 음수사이클 | 용도 |
|---------|-----|-----|----------|-----|
| 다익스트라 | O((V+E)logV) | ❌ | ❌ | 단일 출발 |
| 벨만포드 | O(VE) | ✅ | 탐지 | 음수 있을 때 |
| 플로이드 | O(V³) | ✅ | ❌ | 모든 쌍 |

### 선택 가이드
- 음수 없음 + 한 점에서 → **다익스트라**
- 음수 있음 + 한 점에서 → **벨만-포드**
- 모든 쌍 필요 + V작음 → **플로이드**"""},
            {"type": "code", "language": "Python", "code": """# 문제 조건 확인하고 선택
# 1. V, E 크기 확인
# 2. 음수 가중치 여부
# 3. 단일 출발 vs 모든 쌍

# V = 10만 → 다익스트라
# V = 500, 모든 쌍 → 플로이드
# 음수 있음 → 벨만포드"""},
            {"type": "practice", "title": "🎯 연습", "content": """문제 읽고 적절한 알고리즘 선택이 핵심!"""}
        ]
    },

    "10_최단경로/practice-shortest": {
        "title": "최단 경로 실전",
        "description": "최단 경로 문제 풀이 패턴입니다.",
        "language": "Python",
        "sections": [
            {"type": "concept", "title": "🎯 패턴", "content": """## 자주 나오는 변형

### 1. 경유지 지정
- A → B → C 최단 = dist(A,B) + dist(B,C)

### 2. 간선 하나 제거
- 모든 간선 제거해보며 최단 계산

### 3. 최단 경로 개수
- 다익스트라 + 카운트 배열

### 4. 최단 경로 역추적
- 이전 노드 저장"""},
            {"type": "code", "language": "Python", "code": """# 경유지 있는 최단 경로
def via_shortest(graph, n, start, via, end):
    dist1 = dijkstra(graph, start, n)
    dist2 = dijkstra(graph, via, n)
    return dist1[via] + dist2[end]

# 경로 역추적
def dijkstra_with_path(graph, start, end, n):
    dist = [float('inf')] * (n + 1)
    prev = [-1] * (n + 1)
    dist[start] = 0
    heap = [(0, start)]

    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue
        for neighbor, weight in graph[node]:
            if d + weight < dist[neighbor]:
                dist[neighbor] = d + weight
                prev[neighbor] = node
                heapq.heappush(heap, (dist[neighbor], neighbor))

    # 경로 복원
    path = []
    node = end
    while node != -1:
        path.append(node)
        node = prev[node]
    return path[::-1]"""},
            {"type": "practice", "title": "🎯 연습", "content": """| 문제 | 포인트 |
|-----|-------|
| 특정한 최단 경로 (1504) | 경유 |
| 최단경로 (1753) | 기본 |
| 숨바꼭질 4 (13913) | 경로 출력 |"""}
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
