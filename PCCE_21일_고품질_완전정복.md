# PCCE 파이썬 21일 완전 정복 (고품질 버전)

> 시험 정보: 50분 | 10문제 | 700점 합격 | 빈칸 60% + 결과예측 20% + 디버깅 20%

---

# 📘 1주차: 기초 완벽 마스터

---

## Day 1: print() - 화면 출력의 모든 것

### 개념 설명
print()는 괄호 안의 내용을 화면에 출력하는 함수입니다.

**핵심 규칙:**
- 문자열 → 따옴표 필수 `"Hello"` 또는 `'Hello'`
- 숫자/계산 → 따옴표 없음 `123`, `10+20`
- 여러 개 출력 → 쉼표로 구분 `print("a", "b")`

### 기본 문법
```python
# 1. 문자열 출력 (따옴표 필수)
print("Hello World")
print('안녕하세요')

# 2. 숫자 출력 (따옴표 없음)
print(123)
print(3.14)

# 3. 계산 결과 출력
print(10 + 20)      # 30
print(10 * 3)       # 30

# 4. 여러 값 출력 (쉼표로 구분, 공백 자동 삽입)
print("나이:", 25)   # 나이: 25
print(1, 2, 3)      # 1 2 3

# 5. sep 옵션 (구분자 변경)
print("A", "B", "C", sep="-")   # A-B-C
print(1, 2, 3, sep="")          # 123

# 6. end 옵션 (줄바꿈 대신 다른 문자)
print("Hello", end=" ")
print("World")                   # Hello World (한 줄에)
```

### PCCE 출제 패턴 분석

**패턴 1: 기본 빈칸**
```python
____("Hello, World!")
```
정답: `print`

**패턴 2: 따옴표 유무 구분**
```python
# 다음 중 오류가 나는 것은?
print("100")    # 문자열 "100" 출력
print(100)      # 숫자 100 출력
print(Hello)    # 오류! 변수 Hello가 없음
```

**패턴 3: sep 옵션**
```python
print("2024", "01", "15", sep="-")
# 출력 결과: ____
```
정답: `2024-01-15`

**패턴 4: 계산 결과**
```python
print(5 + 3 * 2)
# 출력 결과: ____
```
정답: `11` (곱셈 먼저!)

### 실전 문제 5개

**Q1. [빈칸] 기본**
```python
____("PCCE 합격!")
```
A: `print`

**Q2. [결과예측] sep 옵션**
```python
print("A", "B", "C", sep="*")
```
출력 결과는?
A: `A*B*C`

**Q3. [결과예측] 계산**
```python
print(100 - 30 + 5)
```
출력 결과는?
A: `75`

**Q4. [디버깅] 오류 찾기**
```python
print(Hello World)
```
오류 원인과 수정:
A: 따옴표 누락 → `print("Hello World")`

**Q5. [결과예측] 여러 값**
```python
print(10, 20, 30)
```
출력 결과는?
A: `10 20 30` (공백으로 구분)

### 함정 포인트
1. `print` vs `Print` → 소문자 `print`만 정답!
2. `print "Hello"` → 괄호 필수! `print("Hello")`
3. `print(Hello)` → 따옴표 필수! `print("Hello")`

---

## Day 2: input() - 사용자 입력 받기

### 개념 설명
input()은 사용자로부터 키보드 입력을 받는 함수입니다.

**핵심 규칙:**
- input()의 결과는 **무조건 문자열(str)**
- 숫자를 입력해도 문자열! "3"이지 3이 아님
- 괄호 안에 안내 메시지 넣기 가능

### 기본 문법
```python
# 1. 기본 입력
name = input()              # 입력 대기
print(name)                 # 입력값 출력

# 2. 안내 메시지와 함께
name = input("이름: ")       # "이름: " 출력 후 입력 대기
print("안녕,", name)

# 3. 숫자 입력 (주의!)
x = input("숫자: ")          # 사용자가 3 입력
print(x)                    # "3" (문자열!)
print(type(x))              # <class 'str'>

# 4. 문자열 연결 (+ 연산)
a = input()                 # "Hello" 입력
b = input()                 # "World" 입력
print(a + b)                # "HelloWorld"
```

### PCCE 최빈출 함정: input()은 무조건 문자열!

```python
x = input()    # 사용자가 3 입력
y = input()    # 사용자가 5 입력
print(x + y)   # 출력: "35" (문자열 연결!)
               # 8이 아님!!!
```

이것이 PCCE에서 가장 많이 틀리는 함정입니다.

### 실전 문제 5개

**Q1. [빈칸] 기본**
```python
name = ____("이름을 입력하세요: ")
print(name)
```
A: `input`

**Q2. [결과예측] 문자열 연결**
```python
a = input()  # "10" 입력
b = input()  # "20" 입력
print(a + b)
```
출력 결과는?
A: `1020` (문자열 연결!)

**Q3. [결과예측] 타입 확인**
```python
x = input()  # 100 입력
print(type(x))
```
출력 결과는?
A: `<class 'str'>` (문자열!)

**Q4. [빈칸] 변수 저장**
```python
age = ____("나이: ")
```
A: `input`

**Q5. [디버깅] 왜 30이 안 나오나?**
```python
x = input()  # 10 입력
y = input()  # 20 입력
print(x + y)  # "1020" 출력됨
```
30을 출력하려면?
A: `print(int(x) + int(y))`

### 함정 포인트
1. input() 결과는 **무조건 str**
2. "3" + "5" = "35" (문자열 연결)
3. 숫자 계산하려면 int() 변환 필수

---

## Day 3: int(), float() - 형변환

### 개념 설명
int()는 정수로, float()는 실수로 변환합니다.

**핵심 규칙:**
- int("123") → 123 (문자열을 정수로)
- float("3.14") → 3.14 (문자열을 실수로)
- int(3.7) → 3 (소수점 버림, 반올림 아님!)

### 기본 문법
```python
# 1. 문자열 → 정수
x = int("100")
print(x + 1)        # 101

# 2. 문자열 → 실수
y = float("3.14")
print(y * 2)        # 6.28

# 3. input과 함께 (가장 중요!)
age = int(input("나이: "))    # 25 입력
print(age + 1)               # 26

# 4. 실수 → 정수 (버림!)
print(int(3.9))     # 3 (반올림 아님!)
print(int(3.1))     # 3
print(int(-3.9))    # -3

# 5. 정수 → 실수
print(float(5))     # 5.0
```

### PCCE 필수 패턴: int(input())

```python
# 올바른 숫자 입력 방법
x = int(input("첫 번째 숫자: "))
y = int(input("두 번째 숫자: "))
print(x + y)    # 이제 정상적으로 덧셈!
```

### 실전 문제 5개

**Q1. [빈칸] 정수 변환**
```python
x = ____(input("숫자: "))
print(x * 2)
```
A: `int`

**Q2. [결과예측] int() 버림**
```python
print(int(9.9))
```
출력 결과는?
A: `9` (버림! 10 아님!)

**Q3. [결과예측] 정상 계산**
```python
a = int(input())  # 10 입력
b = int(input())  # 20 입력
print(a + b)
```
출력 결과는?
A: `30`

**Q4. [빈칸] 실수 변환**
```python
pi = ____(input())  # "3.14" 입력
print(pi * 2)       # 6.28 출력
```
A: `float`

**Q5. [디버깅] 오류 수정**
```python
x = int("3.14")  # 오류 발생!
```
오류 원인과 수정:
A: int()는 소수점 문자열 변환 불가 → `int(float("3.14"))` 또는 `float("3.14")`

### 함정 포인트
1. int("3.14") → 오류! (소수점 문자열은 int 직접 변환 불가)
2. int(3.9) → 3 (반올림 아님, 버림!)
3. int(input()) 형태 자주 출제

---

## Day 4: 변수 - 값 저장하기

### 개념 설명
변수는 값을 저장하는 이름표 붙은 상자입니다.

**핵심 규칙:**
- `=`는 "같다"가 아니라 **대입(저장)**
- 변수명 규칙: 영문, 숫자, 언더스코어(_) 사용 가능
- 숫자로 시작 불가, 예약어 사용 불가

### 기본 문법
```python
# 1. 변수에 값 저장
x = 10              # x에 10 저장
name = "홍길동"      # name에 "홍길동" 저장

# 2. 변수 사용
print(x)            # 10
print(x + 5)        # 15

# 3. 변수 값 변경
x = 10
x = 20              # 덮어쓰기
print(x)            # 20

# 4. 변수끼리 연산
a = 10
b = 20
c = a + b
print(c)            # 30

# 5. 변수 값 갱신
count = 0
count = count + 1   # count에 1 더하기
print(count)        # 1
```

### 변수명 규칙
```python
# 올바른 변수명
name = "홍길동"
age1 = 25
my_score = 100
_private = "비밀"

# 잘못된 변수명
1st = 10            # 숫자로 시작 불가!
my-name = "홍"      # 하이픈 불가!
for = 5             # 예약어 불가!
```

### 실전 문제 5개

**Q1. [빈칸] 변수 대입**
```python
x ____ 100
print(x)
```
A: `=`

**Q2. [결과예측] 변수 갱신**
```python
x = 5
x = x + 3
print(x)
```
출력 결과는?
A: `8`

**Q3. [결과예측] 변수 연산**
```python
a = 10
b = 3
print(a + b * 2)
```
출력 결과는?
A: `16` (곱셈 먼저: 10 + 6 = 16)

**Q4. [빈칸] 변수 덮어쓰기**
```python
x = 10
x ____ 20
print(x)  # 20 출력
```
A: `=`

**Q5. [디버깅] 변수명 오류**
```python
2nd_place = "은메달"
```
오류 원인과 수정:
A: 숫자로 시작 불가 → `second_place = "은메달"`

### 함정 포인트
1. `=`는 같다가 아니라 대입!
2. `x = x + 1`은 x에 1을 더해서 다시 저장
3. 변수명은 숫자로 시작 불가

---

## Day 5: 산술 연산자 - 계산하기

### 개념 설명
파이썬의 기본 산술 연산자입니다.

| 연산자 | 의미 | 예시 | 결과 |
|--------|------|------|------|
| + | 덧셈 | 10 + 3 | 13 |
| - | 뺄셈 | 10 - 3 | 7 |
| * | 곱셈 | 10 * 3 | 30 |
| / | 나눗셈 | 10 / 3 | 3.333... |
| // | 몫 | 10 // 3 | 3 |
| % | 나머지 | 10 % 3 | 1 |
| ** | 거듭제곱 | 2 ** 3 | 8 |

### 핵심: / 나눗셈은 항상 float!
```python
print(10 / 2)    # 5.0 (정수 아님!)
print(10 / 3)    # 3.333...
print(10 // 2)   # 5 (몫, 정수)
```

### 실전 문제 5개

**Q1. [결과예측] 나눗셈**
```python
print(10 / 4)
```
출력 결과는?
A: `2.5`

**Q2. [결과예측] 몫**
```python
print(17 // 5)
```
출력 결과는?
A: `3`

**Q3. [결과예측] 나머지**
```python
print(17 % 5)
```
출력 결과는?
A: `2`

**Q4. [빈칸] 거듭제곱**
```python
print(2 ____ 4)  # 16 출력
```
A: `**`

**Q5. [결과예측] 복합 연산**
```python
print(10 + 6 // 2)
```
출력 결과는?
A: `13` (// 먼저: 10 + 3 = 13)

### 함정 포인트
1. `/` 결과는 무조건 float! (10/2 = 5.0)
2. `//` 몫은 정수
3. `%` 나머지 자주 출제

---

## Day 6: 비교 연산자 - True/False

### 개념 설명
비교 연산자는 조건을 비교하여 True 또는 False를 반환합니다.

| 연산자 | 의미 | 예시 | 결과 |
|--------|------|------|------|
| == | 같다 | 5 == 5 | True |
| != | 다르다 | 5 != 3 | True |
| > | 크다 | 5 > 3 | True |
| < | 작다 | 5 < 3 | False |
| >= | 크거나 같다 | 5 >= 5 | True |
| <= | 작거나 같다 | 5 <= 3 | False |

### 핵심: = vs ==
```python
x = 5       # 대입 (x에 5 저장)
x == 5      # 비교 (x가 5와 같은가? → True)
```

### 실전 문제 5개

**Q1. [결과예측] 같다**
```python
print(10 == 10)
```
출력 결과는?
A: `True`

**Q2. [결과예측] 다르다**
```python
print(5 != 5)
```
출력 결과는?
A: `False`

**Q3. [빈칸] 비교**
```python
x = 10
print(x ____ 5)  # True 출력
```
A: `>` 또는 `>=` 또는 `!=`

**Q4. [결과예측] 문자열 비교**
```python
print("apple" == "apple")
```
출력 결과는?
A: `True`

**Q5. [디버깅] = vs ==**
```python
x = 10
if x = 10:    # 오류!
    print("10입니다")
```
오류 수정:
A: `if x == 10:`

### 함정 포인트
1. `=` 대입, `==` 비교 (가장 많이 틀림!)
2. `True`, `False` 대문자 시작!
3. `true`, `false`는 오류!

---

## Day 7: 논리 연산자 - and, or, not

### 개념 설명
여러 조건을 결합하는 연산자입니다.

| 연산자 | 의미 | 예시 |
|--------|------|------|
| and | 둘 다 True면 True | True and True → True |
| or | 하나라도 True면 True | True or False → True |
| not | 반대로 | not True → False |

### 진리표
```python
# and: 둘 다 True여야 True
True and True    # True
True and False   # False
False and True   # False
False and False  # False

# or: 하나만 True여도 True
True or True     # True
True or False    # True
False or True    # True
False or False   # False

# not: 반대
not True         # False
not False        # True
```

### 실전 문제 5개

**Q1. [결과예측] and**
```python
print(True and False)
```
출력 결과는?
A: `False`

**Q2. [결과예측] or**
```python
print(False or True)
```
출력 결과는?
A: `True`

**Q3. [결과예측] 복합**
```python
x = 10
print(x > 5 and x < 20)
```
출력 결과는?
A: `True`

**Q4. [빈칸]**
```python
print(True ____ False)  # True 출력
```
A: `or`

**Q5. [결과예측] not**
```python
print(not (5 > 3))
```
출력 결과는?
A: `False`

---

# 📗 2주차: 제어문 완전 정복

---

## Day 8: if문 - 조건 분기

### 개념 설명
조건이 True면 실행, False면 건너뜁니다.

### 기본 문법
```python
# if문 기본 구조
if 조건:
    실행문    # 들여쓰기 필수! (4칸)

# 예시
x = 10
if x > 5:
    print("5보다 큽니다")    # 실행됨
```

### 핵심: 콜론과 들여쓰기
```python
if x > 5:           # 콜론(:) 필수!
    print("크다")   # 들여쓰기 4칸 필수!
```

### 실전 문제 5개

**Q1. [빈칸] 콜론**
```python
if x > 0____
    print("양수")
```
A: `:`

**Q2. [디버깅] 들여쓰기**
```python
if x > 0:
print("양수")    # 오류!
```
수정:
A: `    print("양수")` (들여쓰기 추가)

**Q3. [빈칸] 조건문**
```python
____ x == 10:
    print("10입니다")
```
A: `if`

**Q4. [결과예측]**
```python
x = 3
if x > 5:
    print("A")
print("B")
```
출력 결과는?
A: `B` (if문 안의 print는 실행 안됨)

**Q5. [결과예측]**
```python
x = 10
if x >= 10:
    print("10 이상")
```
출력 결과는?
A: `10 이상`

---

## Day 9: if-else문 - 양자택일

### 개념 설명
조건이 True면 if 블록, False면 else 블록 실행.

### 기본 문법
```python
if 조건:
    실행문1    # 조건이 True일 때
else:
    실행문2    # 조건이 False일 때

# 예시
x = 3
if x > 5:
    print("크다")
else:
    print("작다")    # 이게 실행됨
```

### 실전 문제 5개

**Q1. [빈칸]**
```python
if x > 0:
    print("양수")
____:
    print("음수 또는 0")
```
A: `else`

**Q2. [결과예측]**
```python
x = 7
if x % 2 == 0:
    print("짝수")
else:
    print("홀수")
```
출력 결과는?
A: `홀수`

**Q3. [디버깅]**
```python
if x > 0:
    print("양수")
else x <= 0:        # 오류!
    print("음수")
```
수정:
A: `else:` (else 뒤에는 조건 없음!)

**Q4. [빈칸]**
```python
score = 85
if score >= 60:
    print("합격")
____:
    print("불합격")
```
A: `else`

**Q5. [결과예측]**
```python
x = 0
if x:
    print("참")
else:
    print("거짓")
```
출력 결과는?
A: `거짓` (0은 False로 취급)

---

## Day 10: if-elif-else문 - 다중 조건

### 개념 설명
여러 조건을 순서대로 검사합니다.

### 기본 문법
```python
score = 85

if score >= 90:
    print("A")
elif score >= 80:
    print("B")      # 이게 실행됨
elif score >= 70:
    print("C")
else:
    print("F")
```

### 실전 문제 5개

**Q1. [빈칸]**
```python
if x > 90:
    print("A")
____ x > 80:
    print("B")
```
A: `elif`

**Q2. [결과예측]**
```python
x = 75
if x >= 90:
    print("A")
elif x >= 80:
    print("B")
elif x >= 70:
    print("C")
else:
    print("F")
```
출력 결과는?
A: `C`

**Q3. [결과예측] elif 순서 주의**
```python
x = 95
if x >= 70:
    print("C")
elif x >= 80:
    print("B")
elif x >= 90:
    print("A")
```
출력 결과는?
A: `C` (첫 번째 조건에서 걸림!)

**Q4. [빈칸]**
```python
if x == 1:
    print("하나")
elif x == 2:
    print("둘")
____:
    print("기타")
```
A: `else`

**Q5. [디버깅]**
```python
if x > 0:
    print("양수")
elif x = 0:        # 오류!
    print("영")
```
수정:
A: `elif x == 0:`

---

## Day 11: 리스트 기초 - 여러 값 저장

### 개념 설명
리스트는 여러 값을 순서대로 저장하는 자료구조입니다.

### 기본 문법
```python
# 리스트 생성
fruits = ["사과", "바나나", "포도"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]

# 인덱싱 (0부터 시작!)
print(fruits[0])    # 사과 (첫 번째)
print(fruits[1])    # 바나나 (두 번째)
print(fruits[-1])   # 포도 (마지막)

# 슬라이싱
print(fruits[0:2])  # ["사과", "바나나"]
```

### 핵심: 인덱스는 0부터!
```python
a = [10, 20, 30, 40, 50]
# 인덱스: 0   1   2   3   4

print(a[0])     # 10 (첫 번째)
print(a[2])     # 30 (세 번째)
print(a[4])     # 50 (다섯 번째)
print(a[-1])    # 50 (마지막)
```

### 실전 문제 5개

**Q1. [결과예측]**
```python
a = [10, 20, 30, 40]
print(a[1])
```
출력 결과는?
A: `20` (두 번째 요소)

**Q2. [결과예측]**
```python
a = ["A", "B", "C", "D"]
print(a[-1])
```
출력 결과는?
A: `D` (마지막)

**Q3. [빈칸]**
```python
a = [1, 2, 3, 4, 5]
print(a[____])  # 3 출력
```
A: `2`

**Q4. [결과예측] 슬라이싱**
```python
a = [1, 2, 3, 4, 5]
print(a[1:4])
```
출력 결과는?
A: `[2, 3, 4]` (4번 인덱스 미포함!)

**Q5. [디버깅]**
```python
a = [1, 2, 3]
print(a[3])    # 오류!
```
오류 원인:
A: 인덱스 범위 초과 (0, 1, 2만 있음)

---

## Day 12: 리스트 메서드 - append, remove

### 개념 설명
리스트를 조작하는 메서드들입니다.

### 주요 메서드
```python
a = [1, 2, 3]

# append: 맨 뒤에 추가
a.append(4)
print(a)        # [1, 2, 3, 4]

# insert: 특정 위치에 삽입
a.insert(0, 0)
print(a)        # [0, 1, 2, 3, 4]

# remove: 값으로 삭제 (첫 번째만)
a.remove(2)
print(a)        # [0, 1, 3, 4]

# pop: 인덱스로 삭제 후 반환
x = a.pop(0)
print(x)        # 0
print(a)        # [1, 3, 4]

# pop(): 마지막 요소 삭제
y = a.pop()
print(y)        # 4
print(a)        # [1, 3]
```

### 실전 문제 5개

**Q1. [빈칸]**
```python
a = [1, 2, 3]
a.____(4)
print(a)  # [1, 2, 3, 4]
```
A: `append`

**Q2. [결과예측]**
```python
a = [1, 2, 3]
a.append(4)
a.append(5)
print(len(a))
```
출력 결과는?
A: `5`

**Q3. [빈칸]**
```python
a = [1, 2, 3, 2, 4]
a.____(2)
print(a)  # [1, 3, 2, 4]
```
A: `remove` (첫 번째 2만 삭제)

**Q4. [결과예측]**
```python
a = [10, 20, 30]
x = a.pop()
print(x)
print(a)
```
출력 결과는?
A: `30`, `[10, 20]`

**Q5. [결과예측]**
```python
a = [1, 2, 3]
a.insert(1, 100)
print(a)
```
출력 결과는?
A: `[1, 100, 2, 3]`

---

## Day 13: for문 - 반복 실행

### 개념 설명
for문은 리스트나 range의 요소를 하나씩 꺼내서 반복합니다.

### 기본 문법
```python
# 리스트 순회
fruits = ["사과", "바나나", "포도"]
for fruit in fruits:
    print(fruit)
# 사과
# 바나나
# 포도

# range() 사용
for i in range(5):
    print(i)
# 0, 1, 2, 3, 4
```

### 실전 문제 5개

**Q1. [빈칸]**
```python
____ i in [1, 2, 3]:
    print(i)
```
A: `for`

**Q2. [빈칸]**
```python
for i ____ range(5):
    print(i)
```
A: `in`

**Q3. [결과예측]**
```python
for i in range(3):
    print(i)
```
출력 결과는?
A: `0`, `1`, `2` (각 줄에)

**Q4. [결과예측]**
```python
sum = 0
for i in [1, 2, 3, 4, 5]:
    sum = sum + i
print(sum)
```
출력 결과는?
A: `15`

**Q5. [디버깅]**
```python
for i in range(5)
    print(i)
```
오류 수정:
A: `for i in range(5):` (콜론 추가)

---

## Day 14: range() 완벽 이해

### 개념 설명
range()는 숫자 범위를 생성합니다.

### 사용법
```python
# range(끝) - 0부터 끝-1까지
range(5)        # 0, 1, 2, 3, 4

# range(시작, 끝) - 시작부터 끝-1까지
range(1, 5)     # 1, 2, 3, 4

# range(시작, 끝, 간격)
range(0, 10, 2) # 0, 2, 4, 6, 8
range(5, 0, -1) # 5, 4, 3, 2, 1
```

### 핵심: 끝 숫자 미포함!
```python
for i in range(1, 5):
    print(i)
# 1, 2, 3, 4 (5 없음!)
```

### 실전 문제 5개

**Q1. [결과예측]**
```python
for i in range(3):
    print(i, end=" ")
```
출력 결과는?
A: `0 1 2`

**Q2. [결과예측]**
```python
for i in range(1, 6):
    print(i, end=" ")
```
출력 결과는?
A: `1 2 3 4 5`

**Q3. [빈칸]**
```python
for i in ____:
    print(i)
# 2, 4, 6, 8 출력
```
A: `range(2, 10, 2)`

**Q4. [결과예측]**
```python
print(list(range(5, 0, -1)))
```
출력 결과는?
A: `[5, 4, 3, 2, 1]`

**Q5. [결과예측]**
```python
count = 0
for i in range(1, 11):
    count = count + 1
print(count)
```
출력 결과는?
A: `10`

---

# 📕 3주차: 문자열과 실전 대비

---

## Day 15: 문자열 슬라이싱

### 개념 설명
문자열의 일부분을 추출합니다.

### 문법
```python
s = "Hello"
# 인덱스: 01234

print(s[0])      # H
print(s[1:4])    # ell (1,2,3번 - 4 미포함!)
print(s[:3])     # Hel (처음~2번)
print(s[2:])     # llo (2번~끝)
print(s[-1])     # o (마지막)
print(s[::-1])   # olleH (역순)
```

### 실전 문제 5개

**Q1. [결과예측]**
```python
s = "Python"
print(s[0:3])
```
출력 결과는?
A: `Pyt`

**Q2. [결과예측]**
```python
s = "Hello"
print(s[1:4])
```
출력 결과는?
A: `ell`

**Q3. [빈칸]**
```python
s = "Programming"
print(s[____])  # "gram" 출력
```
A: `3:7` 또는 `[3:7]`

**Q4. [결과예측]**
```python
s = "ABCDE"
print(s[-2:])
```
출력 결과는?
A: `DE`

**Q5. [결과예측]**
```python
s = "Hello"
print(s[::-1])
```
출력 결과는?
A: `olleH`

---

## Day 16: 문자열 메서드 - upper, lower, strip

### 주요 메서드
```python
s = "  Hello World  "

# 대소문자 변환
print(s.upper())    # "  HELLO WORLD  "
print(s.lower())    # "  hello world  "

# 공백 제거
print(s.strip())    # "Hello World"
print(s.lstrip())   # "Hello World  "
print(s.rstrip())   # "  Hello World"

# 문자 개수
print(s.count("l")) # 3

# 찾기
print(s.find("World"))  # 8 (시작 인덱스)
print(s.find("xxx"))    # -1 (없으면)
```

### 실전 문제 5개

**Q1. [빈칸]**
```python
s = "hello"
print(s.____())  # "HELLO" 출력
```
A: `upper`

**Q2. [결과예측]**
```python
s = "PYTHON"
print(s.lower())
```
출력 결과는?
A: `python`

**Q3. [빈칸]**
```python
s = "  공백제거  "
print(s.____())  # "공백제거" 출력
```
A: `strip`

**Q4. [결과예측]**
```python
s = "banana"
print(s.count("a"))
```
출력 결과는?
A: `3`

**Q5. [결과예측]**
```python
s = "Hello"
print(s.find("ll"))
```
출력 결과는?
A: `2`

---

## Day 17: 문자열 메서드 - replace, split, join

### 주요 메서드
```python
# replace: 치환
s = "Hello World"
print(s.replace("World", "Python"))  # "Hello Python"
print(s.replace("l", "L"))           # "HeLLo WorLd"

# split: 분리 → 리스트
s = "a,b,c,d"
print(s.split(","))     # ['a', 'b', 'c', 'd']

s = "Hello World"
print(s.split())        # ['Hello', 'World'] (공백 기준)

# join: 리스트 → 문자열
a = ['a', 'b', 'c']
print("-".join(a))      # "a-b-c"
print("".join(a))       # "abc"
```

### 실전 문제 5개

**Q1. [빈칸]**
```python
s = "apple"
print(s.____("a", "A"))  # "Apple" 출력
```
A: `replace`

**Q2. [결과예측]**
```python
s = "1-2-3-4-5"
print(s.split("-"))
```
출력 결과는?
A: `['1', '2', '3', '4', '5']`

**Q3. [빈칸]**
```python
a = ['Hello', 'World']
print(" ".______(a))  # "Hello World" 출력
```
A: `join`

**Q4. [결과예측]**
```python
s = "aaa"
print(s.replace("a", "b"))
```
출력 결과는?
A: `bbb`

**Q5. [결과예측]**
```python
s = "Hello World Python"
words = s.split()
print(len(words))
```
출력 결과는?
A: `3`

---

## Day 18: while문과 break, continue

### 기본 문법
```python
# while문
x = 0
while x < 5:
    print(x)
    x = x + 1
# 0, 1, 2, 3, 4

# break: 반복 중단
for i in range(10):
    if i == 5:
        break
    print(i)
# 0, 1, 2, 3, 4

# continue: 이번만 건너뛰기
for i in range(5):
    if i == 2:
        continue
    print(i)
# 0, 1, 3, 4 (2 제외)
```

### 실전 문제 5개

**Q1. [빈칸]**
```python
x = 0
____ x < 3:
    print(x)
    x = x + 1
```
A: `while`

**Q2. [결과예측]**
```python
for i in range(5):
    if i == 3:
        break
    print(i, end=" ")
```
출력 결과는?
A: `0 1 2`

**Q3. [결과예측]**
```python
for i in range(5):
    if i == 2:
        continue
    print(i, end=" ")
```
출력 결과는?
A: `0 1 3 4`

**Q4. [빈칸]**
```python
for i in range(10):
    if i == 5:
        ____
    print(i)
# 0, 1, 2, 3, 4만 출력
```
A: `break`

**Q5. [디버깅] 무한루프**
```python
x = 0
while x < 5:
    print(x)
    # x 증가 없음!
```
수정:
A: `x = x + 1` 추가

---

## Day 19: len(), sum(), max(), min()

### 내장 함수
```python
a = [3, 1, 4, 1, 5, 9, 2, 6]

print(len(a))    # 8 (길이)
print(sum(a))    # 31 (합계)
print(max(a))    # 9 (최댓값)
print(min(a))    # 1 (최솟값)

# 문자열에도 사용
s = "Hello"
print(len(s))    # 5
```

### 실전 문제 5개

**Q1. [결과예측]**
```python
a = [1, 2, 3, 4, 5]
print(sum(a))
```
출력 결과는?
A: `15`

**Q2. [빈칸]**
```python
a = [10, 20, 30]
print(____(a))  # 3 출력
```
A: `len`

**Q3. [결과예측]**
```python
a = [5, 2, 8, 1, 9]
print(max(a) - min(a))
```
출력 결과는?
A: `8` (9 - 1)

**Q4. [결과예측]**
```python
s = "Python"
print(len(s))
```
출력 결과는?
A: `6`

**Q5. [빈칸]**
```python
a = [10, 50, 30, 20, 40]
print(____(a))  # 10 출력
```
A: `min`

---

## Day 20: 함수 정의와 호출

### 기본 문법
```python
# 함수 정의
def greet(name):
    print("안녕, " + name)

# 함수 호출
greet("철수")    # 안녕, 철수

# return 값 반환
def add(a, b):
    return a + b

result = add(3, 5)
print(result)    # 8
```

### 실전 문제 5개

**Q1. [빈칸]**
```python
____ multiply(x, y):
    return x * y
```
A: `def`

**Q2. [빈칸]**
```python
def square(n):
    ____ n * n

print(square(5))  # 25 출력
```
A: `return`

**Q3. [결과예측]**
```python
def hello():
    print("Hello")

hello()
hello()
```
출력 결과는?
A: `Hello` (2번)

**Q4. [결과예측]**
```python
def add(a, b):
    return a + b

x = add(10, 20)
y = add(x, 30)
print(y)
```
출력 결과는?
A: `60`

**Q5. [디버깅]**
```python
def greet(name)
    print("Hello", name)
```
오류 수정:
A: `def greet(name):` (콜론 추가)

---

## Day 21: 최종 모의고사

### PCCE 10대 함정 총정리

| 번호 | 함정 | 올바른 이해 |
|-----|------|------------|
| 1 | input()은 항상 str | int() 변환 필수 |
| 2 | / 나눗셈은 float | 10/2 = 5.0 |
| 3 | 인덱스 0부터 | 첫 번째 = [0] |
| 4 | range() 끝 미포함 | range(5) = 0~4 |
| 5 | = 대입, == 비교 | if x == 5: |
| 6 | 콜론(:) 필수 | if, for, while, def 뒤 |
| 7 | 들여쓰기 4칸 | 탭 or 스페이스 4칸 |
| 8 | 슬라이싱 끝 미포함 | [0:3] = 0,1,2번 |
| 9 | True/False 대문자 | true(X) True(O) |
| 10 | int(3.9) = 3 | 버림! 반올림 아님 |

---

### 실전 모의고사 (10문제)

**Q1. [빈칸]**
```python
____("Hello, PCCE!")
```
A: `print`

---

**Q2. [빈칸]**
```python
name = ____("이름을 입력하세요: ")
```
A: `input`

---

**Q3. [빈칸]**
```python
x = ____(input("숫자: "))
print(x + 10)
```
A: `int`

---

**Q4. [결과예측]**
```python
print(10 / 4)
```
출력 결과: ____
A: `2.5`

---

**Q5. [결과예측]**
```python
a = [10, 20, 30, 40, 50]
print(a[2])
```
출력 결과: ____
A: `30`

---

**Q6. [빈칸]**
```python
____ i in range(5):
    print(i)
```
A: `for`

---

**Q7. [결과예측]**
```python
for i in range(1, 4):
    print(i, end=" ")
```
출력 결과: ____
A: `1 2 3`

---

**Q8. [결과예측]**
```python
s = "Python"
print(s[0:3])
```
출력 결과: ____
A: `Pyt`

---

**Q9. [디버깅]**
```python
x = 10
if x = 10:
    print("10입니다")
```
오류 수정: ____
A: `if x == 10:`

---

**Q10. [빈칸]**
```python
a = [1, 2, 3]
a.____(4)
print(a)  # [1, 2, 3, 4]
```
A: `append`

---

### 채점 기준
- 각 문제 100점 x 10문제 = 1000점
- 700점 이상 = 합격
- 7문제 맞추면 합격!

### 시험 전략
1. **빈칸 먼저** (6문제, 쉬움)
2. **결과예측** (2문제, / 나눗셈과 range 주의)
3. **디버깅** (2문제, 콜론과 == 체크)

---

# 합격을 축하합니다! 🎉
