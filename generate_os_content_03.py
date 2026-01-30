import json

# Load existing os.json
with open('src/data/contents/os.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Define new content for 7 topics

# ============================================
# 04_메모리 (4개)
# ============================================

data["04_메모리/memory-structure"] = {
    "id": "04_메모리/memory-structure",
    "title": "메모리 구조",
    "category": "os",
    "subCategory": "04_메모리",
    "language": "C",
    "description": "물리 메모리와 논리 메모리의 구조와 차이점을 이해합니다.",
    "isPlaceholder": False,
    "sections": [
        {
            "type": "concept",
            "title": "메모리 구조 개념",
            "content": "메모리 구조는 프로그램이 실행될 때 데이터가 저장되는 방식을 정의합니다.\n\n**한 줄 요약**: 물리 메모리는 실제 RAM, 논리 메모리는 프로세스가 보는 가상의 주소 공간입니다.\n\n**도서관 비유**:\n- 물리 메모리 = 도서관의 실제 책장 (고정된 물리적 위치)\n- 논리 메모리 = 도서 목록 카드 (책의 논리적 분류 번호)\n- 사서(MMU) = 목록 번호를 실제 책장 위치로 변환\n\n**핵심 개념**:\n1. **물리 메모리 (Physical Memory)**\n   - 실제 RAM 하드웨어\n   - 물리 주소로 직접 접근\n   - 크기가 고정됨\n\n2. **논리 메모리 (Logical Memory)**\n   - 프로세스가 인식하는 주소 공간\n   - 가상 주소 사용\n   - 각 프로세스마다 독립적\n\n3. **주소 변환**\n   - MMU(Memory Management Unit)가 담당\n   - 논리 주소 -> 물리 주소 매핑\n   - 페이지 테이블 활용"
        },
        {
            "type": "code",
            "title": "메모리 레이아웃 다이어그램",
            "language": "text",
            "code": "[ 프로세스 메모리 레이아웃 ]\n\n높은 주소 (0xFFFFFFFF)\n+------------------+\n|      Stack       | <- 지역변수, 함수 호출 정보\n|        |         |    (아래로 성장)\n|        v         |\n+------------------+\n|                  |\n|   빈 공간        | <- Stack과 Heap 사이 여유 공간\n|                  |\n+------------------+\n|        ^         |\n|        |         |    (위로 성장)\n|       Heap       | <- 동적 할당 메모리 (malloc)\n+------------------+\n|       BSS        | <- 초기화되지 않은 전역변수\n+------------------+\n|       Data       | <- 초기화된 전역변수\n+------------------+\n|       Text       | <- 프로그램 코드 (Read-Only)\n+------------------+\n낮은 주소 (0x00000000)\n\n[ 주소 변환 과정 ]\n\n논리 주소        MMU           물리 주소\n0x0040 -----> [페이지 테이블] -----> 0x7040\n\n+--------+--------+     +--------+--------+\n| 페이지 | 오프셋 |     | 프레임 | 오프셋 |\n| 번호   |        | --> | 번호   |        |\n+--------+--------+     +--------+--------+\n   4        40             7        40"
        },
        {
            "type": "code",
            "title": "C 메모리 영역 확인",
            "language": "c",
            "code": "#include <stdio.h>\n#include <stdlib.h>\n\n// Data 영역 - 초기화된 전역변수\nint global_init = 100;\n\n// BSS 영역 - 초기화되지 않은 전역변수\nint global_uninit;\n\nvoid memory_layout_demo() {\n    // Stack 영역 - 지역변수\n    int local_var = 50;\n    \n    // Heap 영역 - 동적 할당\n    int *heap_ptr = (int*)malloc(sizeof(int) * 10);\n    \n    printf(\"=== 메모리 레이아웃 ===\");\n    printf(\"Text (코드): %p\", (void*)memory_layout_demo);\n    printf(\"Data (초기화): %p\", (void*)&global_init);\n    printf(\"BSS (미초기화): %p\", (void*)&global_uninit);\n    printf(\"Heap (동적): %p\", (void*)heap_ptr);\n    printf(\"Stack (지역): %p\", (void*)&local_var);\n    \n    free(heap_ptr);\n}\n\nint main() {\n    memory_layout_demo();\n    return 0;\n}"
        },
        {
            "type": "tip",
            "title": "면접 대비 정리",
            "content": "**물리 vs 논리 메모리 비교표**:\n| 구분 | 물리 메모리 | 논리 메모리 |\n|------|------------|------------|\n| 정의 | 실제 RAM | 가상 주소 공간 |\n| 주소 | 물리 주소 | 가상 주소 |\n| 크기 | RAM 용량 | 프로세스별 독립 |\n| 관리 | 하드웨어 | OS + MMU |\n| 접근 | 직접 접근 | 주소 변환 필요 |\n\n**면접 빈출 질문**:\n\nQ1: 논리 주소와 물리 주소의 차이점은?\nA: 논리 주소는 프로세스가 사용하는 가상 주소이고, 물리 주소는 실제 RAM의 위치입니다. MMU가 논리->물리 변환을 수행합니다.\n\nQ2: 프로세스 메모리 레이아웃을 설명하세요.\nA: 낮은 주소부터 Text(코드), Data(초기화된 전역), BSS(미초기화 전역), Heap(동적할당, 위로 성장), Stack(지역변수, 아래로 성장) 순서입니다.\n\nQ3: Stack과 Heap의 차이점은?\nA: Stack은 컴파일 타임에 크기 결정, LIFO, 자동 해제. Heap은 런타임 동적 할당, 수동 해제 필요.\n\n**핵심 키워드**: MMU, 페이지 테이블, 주소 바인딩, 메모리 보호"
        }
    ]
}

data["04_메모리/stack-heap"] = {
    "id": "04_메모리/stack-heap",
    "title": "스택 vs 힙",
    "category": "os",
    "subCategory": "04_메모리",
    "language": "C",
    "description": "스택과 힙의 정적/동적 메모리 할당 방식을 비교합니다.",
    "isPlaceholder": False,
    "sections": [
        {
            "type": "concept",
            "title": "스택과 힙 개념",
            "content": "스택과 힙은 프로그램 실행 중 데이터를 저장하는 두 가지 핵심 메모리 영역입니다.\n\n**한 줄 요약**: 스택은 자동 관리되는 빠른 메모리, 힙은 수동 관리되는 유연한 메모리입니다.\n\n**아파트 비유**:\n- 스택 = 호텔 방 (체크인/아웃 자동, 정해진 크기, 빠른 배정)\n- 힙 = 임대 아파트 (계약 필요, 원하는 크기, 직접 관리)\n\n**스택 (Stack)**:\n- 함수 호출 시 자동 할당\n- LIFO (Last In First Out) 구조\n- 함수 종료 시 자동 해제\n- 크기 제한 있음 (보통 1-8MB)\n- 매우 빠른 할당/해제\n\n**힙 (Heap)**:\n- malloc/new로 명시적 할당\n- 프로그래머가 직접 관리\n- free/delete로 명시적 해제\n- 큰 데이터 저장 가능\n- 상대적으로 느린 할당/해제"
        },
        {
            "type": "code",
            "title": "스택/힙 메모리 다이어그램",
            "language": "text",
            "code": "[ 스택 메모리 동작 ]\n\nfunc_a() 호출     func_b() 호출     func_b() 반환     func_a() 반환\n+----------+     +----------+     +----------+     +----------+\n|          |     | func_b() |     |          |     |          |\n+----------+     +----------+     +----------+     +----------+\n| func_a() |     | func_a() |     | func_a() |     |          |\n+----------+     +----------+     +----------+     +----------+\n|  main()  |     |  main()  |     |  main()  |     |  main()  |\n+----------+     +----------+     +----------+     +----------+\n\n[ 힙 메모리 동작 ]\n\nmalloc(100)      malloc(200)      free(ptr1)       malloc(50)\n+----------+     +----------+     +----------+     +----------+\n|  100B    |     |  100B    |     |  (빈공간) |     |  50B     |\n+----------+     +----------+     +----------+     +----------+\n|          |     |  200B    |     |  200B    |     |  200B    |\n+----------+     +----------+     +----------+     +----------+\n  ptr1             ptr1,ptr2         ptr2           ptr3,ptr2\n\n[ 스택 프레임 구조 ]\n\n+-----------------------+\n| 반환 주소 (Return Addr)|  <- 함수 종료 후 돌아갈 위치\n+-----------------------+\n| 이전 프레임 포인터     |  <- 호출자의 스택 프레임\n+-----------------------+\n| 지역 변수 1           |\n+-----------------------+\n| 지역 변수 2           |\n+-----------------------+\n| 매개변수              |  <- 함수 인자\n+-----------------------+"
        },
        {
            "type": "code",
            "title": "C/Java 스택-힙 비교",
            "language": "c",
            "code": "// === C 언어 스택 vs 힙 ===\n#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n\nvoid stack_example() {\n    // 스택 할당 - 자동 관리\n    int stack_arr[100];      // 컴파일 타임에 크기 결정\n    int stack_var = 42;      // 함수 종료 시 자동 해제\n    \n    printf(\"Stack 변수 주소: %p\", &stack_var);\n}\n\nvoid heap_example() {\n    // 힙 할당 - 수동 관리\n    int *heap_arr = (int*)malloc(100 * sizeof(int));\n    \n    if (heap_arr == NULL) {\n        printf(\"메모리 할당 실패!\");\n        return;\n    }\n    \n    // 사용\n    heap_arr[0] = 42;\n    printf(\"Heap 변수 주소: %p\", heap_arr);\n    \n    // 반드시 해제 필요!\n    free(heap_arr);\n    heap_arr = NULL;  // Dangling pointer 방지\n}\n\n// 스택 오버플로우 예시 (위험!)\nvoid stack_overflow() {\n    int huge_array[10000000];  // 스택 초과 가능!\n}\n\n// 메모리 누수 예시 (잘못된 코드)\nvoid memory_leak() {\n    int *ptr = (int*)malloc(sizeof(int));\n    // free(ptr); 누락 -> 메모리 누수!\n}"
        },
        {
            "type": "tip",
            "title": "면접 대비 정리",
            "content": "**스택 vs 힙 비교표**:\n| 구분 | 스택 (Stack) | 힙 (Heap) |\n|------|-------------|----------|\n| 할당 | 자동 (컴파일) | 수동 (런타임) |\n| 해제 | 자동 | 수동 (free/delete) |\n| 속도 | 매우 빠름 | 상대적 느림 |\n| 크기 | 제한적 (1-8MB) | 큰 메모리 가능 |\n| 성장 | 아래로 성장 | 위로 성장 |\n| 에러 | Stack Overflow | Memory Leak |\n| 구조 | LIFO | 비순차적 |\n\n**면접 빈출 질문**:\n\nQ1: 스택과 힙의 차이점을 설명하세요.\nA: 스택은 함수 호출 시 자동 할당/해제되며 빠르지만 크기 제한이 있습니다. 힙은 동적 할당으로 큰 데이터를 저장할 수 있지만 수동 관리가 필요합니다.\n\nQ2: 스택 오버플로우는 왜 발생하나요?\nA: 스택 크기를 초과하는 큰 지역 변수나 무한 재귀 호출로 발생합니다.\n\nQ3: 메모리 누수(Memory Leak)란?\nA: 힙에 할당한 메모리를 해제하지 않아 사용 불가능한 메모리가 누적되는 현상입니다.\n\nQ4: Java에서 Stack과 Heap의 차이는?\nA: 기본형은 Stack, 객체는 Heap에 저장됩니다. GC가 Heap 메모리를 자동 관리합니다.\n\n**핵심 키워드**: LIFO, malloc/free, Stack Overflow, Memory Leak, GC"
        }
    ]
}

data["04_메모리/virtual-memory"] = {
    "id": "04_메모리/virtual-memory",
    "title": "가상 메모리",
    "category": "os",
    "subCategory": "04_메모리",
    "language": "C",
    "description": "가상 메모리를 통해 실제 RAM보다 큰 메모리를 사용하는 원리를 이해합니다.",
    "isPlaceholder": False,
    "sections": [
        {
            "type": "concept",
            "title": "가상 메모리 개념",
            "content": "가상 메모리는 물리 메모리보다 큰 주소 공간을 프로세스에 제공하는 메모리 관리 기법입니다.\n\n**한 줄 요약**: 디스크를 RAM의 확장처럼 사용하여 물리 메모리 한계를 극복합니다.\n\n**도서관 비유**:\n- 물리 메모리 = 열람실 책상 (제한된 공간)\n- 가상 메모리 = 전체 도서관 장서 (훨씬 큰 저장소)\n- 필요한 책만 책상에 가져옴 (요구 페이징)\n- 다 읽은 책은 다시 서가로 (페이지 교체)\n\n**핵심 원리**:\n1. **주소 공간 분리**: 프로세스마다 독립적인 가상 주소 공간\n2. **요구 페이징 (Demand Paging)**: 필요할 때만 메모리에 적재\n3. **페이지 교체**: 메모리 부족 시 사용 안 하는 페이지를 디스크로\n4. **스왑 영역**: 디스크의 가상 메모리 저장 공간\n\n**장점**:\n- 물리 메모리보다 큰 프로그램 실행 가능\n- 프로세스 간 메모리 보호\n- 메모리 효율적 사용\n- 공유 메모리 구현 용이"
        },
        {
            "type": "code",
            "title": "가상 메모리 구조 다이어그램",
            "language": "text",
            "code": "[ 가상 메모리 개념도 ]\n\n프로세스 A          프로세스 B          물리 메모리       디스크(Swap)\n가상 주소공간       가상 주소공간\n+----------+       +----------+       +----------+     +----------+\n| Page 0   |--+    | Page 0   |--+    | Frame 0  |<----| Page X   |\n+----------+  |    +----------+  |    +----------+     +----------+\n| Page 1   |--|---\\| Page 1   |  |    | Frame 1  |<-+  | Page Y   |\n+----------+  |    +----------+  |    +----------+  |  +----------+\n| Page 2   |  +----| Page 2   |--+---\\| Frame 2  |  |  | Page Z   |\n+----------+       +----------+      /+----------+  |  +----------+\n| Page 3   |----------------------+ | | Frame 3  |--+\n+----------+       +----------+   | | +----------+\n                                  +-+->\n\n[ 주소 변환 과정 ]\n\n가상 주소 (32bit 예시)\n+------------+------------+\n| 페이지번호 |   오프셋   |\n|   (20bit)  |  (12bit)   |   4KB 페이지\n+------------+------------+\n      |             |\n      v             |\n+------------+      |\n|페이지테이블|      |\n| 0 -> F3   |      |\n| 1 -> F7   |      |\n| 2 -> DISK |      |      Page Fault!\n| 3 -> F1   |      |\n+------------+      |\n      |             |\n      v             v\n+------------+------------+\n| 프레임번호 |   오프셋   |\n+------------+------------+\n      물리 주소"
        },
        {
            "type": "code",
            "title": "가상 메모리 시스템 콜",
            "language": "c",
            "code": "// === 가상 메모리 관련 시스템 콜 ===\n#include <stdio.h>\n#include <stdlib.h>\n#include <sys/mman.h>\n#include <unistd.h>\n\n// mmap: 가상 메모리 영역 매핑\nvoid mmap_example() {\n    size_t size = 4096;  // 1 페이지\n    \n    // 익명 메모리 매핑\n    void *addr = mmap(NULL, size,\n                      PROT_READ | PROT_WRITE,\n                      MAP_PRIVATE | MAP_ANONYMOUS,\n                      -1, 0);\n    \n    if (addr == MAP_FAILED) {\n        perror(\"mmap failed\");\n        return;\n    }\n    \n    // 메모리 사용\n    int *ptr = (int*)addr;\n    ptr[0] = 42;\n    \n    // 매핑 해제\n    munmap(addr, size);\n}\n\n// 메모리 정보 확인 (Linux)\nvoid check_memory_info() {\n    // /proc/self/maps에서 가상 메모리 매핑 확인\n    printf(\"가상 메모리 매핑 정보:\");\n    system(\"cat /proc/self/maps | head -10\");\n    \n    // 메모리 사용량 확인\n    printf(\"메모리 사용량:\");\n    system(\"free -h\");\n}\n\n// 대용량 메모리 할당 테스트\nvoid large_allocation_test() {\n    // 물리 메모리보다 큰 할당 시도\n    size_t huge_size = 1024UL * 1024 * 1024;  // 1GB\n    \n    void *huge_mem = malloc(huge_size);\n    if (huge_mem) {\n        printf(\"1GB 할당 성공 (가상 메모리 사용)\");\n        // 실제 접근 전까지 물리 메모리 미할당\n        free(huge_mem);\n    }\n}"
        },
        {
            "type": "tip",
            "title": "면접 대비 정리",
            "content": "**가상 메모리 핵심 개념**:\n| 용어 | 설명 |\n|------|------|\n| 가상 주소 | 프로세스가 사용하는 논리적 주소 |\n| 물리 주소 | 실제 RAM의 주소 |\n| 페이지 | 가상 메모리의 고정 크기 블록 (보통 4KB) |\n| 프레임 | 물리 메모리의 고정 크기 블록 |\n| 페이지 테이블 | 가상->물리 주소 매핑 테이블 |\n| TLB | 페이지 테이블 캐시 (빠른 변환) |\n| Page Fault | 페이지가 메모리에 없을 때 발생 |\n| Swap | 디스크의 가상 메모리 영역 |\n\n**면접 빈출 질문**:\n\nQ1: 가상 메모리란 무엇인가요?\nA: 디스크를 RAM의 확장으로 사용하여 물리 메모리보다 큰 주소 공간을 프로세스에 제공하는 기법입니다.\n\nQ2: Page Fault가 발생하면 어떤 일이 일어나나요?\nA: 1) CPU가 트랩 발생 2) OS가 페이지 위치 확인 3) 디스크에서 페이지 로드 4) 페이지 테이블 갱신 5) 명령어 재실행\n\nQ3: TLB(Translation Lookaside Buffer)의 역할은?\nA: 최근 사용된 페이지 테이블 항목을 캐싱하여 주소 변환 속도를 높입니다.\n\nQ4: 스래싱(Thrashing)이란?\nA: 페이지 부재가 과도하게 발생하여 실제 작업보다 페이지 교체에 더 많은 시간을 소비하는 현상입니다.\n\n**핵심 키워드**: 요구 페이징, Page Fault, TLB, Swap, 스래싱"
        }
    ]
}

data["04_메모리/paging"] = {
    "id": "04_메모리/paging",
    "title": "페이징",
    "category": "os",
    "subCategory": "04_메모리",
    "language": "C",
    "description": "고정 크기 블록으로 메모리를 관리하는 페이징 기법을 학습합니다.",
    "isPlaceholder": False,
    "sections": [
        {
            "type": "concept",
            "title": "페이징 개념",
            "content": "페이징은 메모리를 고정 크기 블록(페이지/프레임)으로 나누어 관리하는 기법입니다.\n\n**한 줄 요약**: 메모리를 동일한 크기의 블록으로 나눠 외부 단편화를 해결합니다.\n\n**아파트 비유**:\n- 페이지 = 이사할 짐 박스 (모두 같은 크기)\n- 프레임 = 아파트 방 (모두 같은 크기)\n- 페이지 테이블 = 짐 박스가 어느 방에 있는지 기록\n- 연속된 방이 필요 없음 (외부 단편화 없음)\n\n**핵심 구성요소**:\n1. **페이지 (Page)**: 가상 메모리의 고정 크기 블록\n2. **프레임 (Frame)**: 물리 메모리의 고정 크기 블록\n3. **페이지 테이블**: 페이지->프레임 매핑 정보\n4. **페이지 크기**: 보통 4KB (2^12 bytes)\n\n**장점**:\n- 외부 단편화 완전 해결\n- 메모리 할당이 단순\n- 공유 메모리 구현 용이\n\n**단점**:\n- 내부 단편화 발생 가능\n- 페이지 테이블 메모리 오버헤드"
        },
        {
            "type": "code",
            "title": "페이징 주소 변환 다이어그램",
            "language": "text",
            "code": "[ 페이징 시스템 구조 ]\n\n논리 주소 (32bit, 4KB 페이지)\n+------------------+------------------+\n|  페이지 번호     |     오프셋       |\n|    (20 bit)      |    (12 bit)      |\n+------------------+------------------+\n         |                  |\n         v                  |\n   +----------+             |\n   |페이지    |             |\n   |테이블    |             |\n   +----------+             |\n   | 0 | F5  |             |\n   +----------+             |\n   | 1 | F2  | <--+        |\n   +----------+    |        |\n   | 2 | F8  |    |        |\n   +----------+    |        |\n   | 3 | F1  |    |        |\n   +----------+    |        |\n         |         |        |\n         +---------+        |\n         v                  v\n   +------------------+------------------+\n   |  프레임 번호     |     오프셋       |\n   |     (F2)         |    (동일)        |\n   +------------------+------------------+\n                물리 주소\n\n[ 주소 변환 예시 ]\n\n논리 주소: 8196 (0x2004)\n페이지 크기: 4KB (4096)\n\n페이지 번호 = 8196 / 4096 = 2\n오프셋 = 8196 % 4096 = 4\n\n페이지 테이블[2] = 프레임 5\n\n물리 주소 = (5 * 4096) + 4 = 20484\n\n[ 다단계 페이지 테이블 (2-Level) ]\n\n+--------+--------+--------+\n| 디렉토리| 페이지 | 오프셋 |\n| (10bit)| (10bit)| (12bit)|\n+--------+--------+--------+\n    |        |\n    v        v\n+------+   +------+\n|Page  |-->|Page  |-->프레임\n|Dir   |   |Table |   번호\n+------+   +------+"
        },
        {
            "type": "code",
            "title": "페이징 시뮬레이션 코드",
            "language": "c",
            "code": "// === 페이징 시뮬레이션 ===\n#include <stdio.h>\n#include <stdlib.h>\n\n#define PAGE_SIZE 4096        // 4KB\n#define PAGE_BITS 12          // log2(4096)\n#define NUM_PAGES 256         // 페이지 테이블 엔트리 수\n#define NUM_FRAMES 64         // 물리 프레임 수\n\n// 페이지 테이블 엔트리\ntypedef struct {\n    int frame_number;     // 프레임 번호\n    int valid;            // 유효 비트\n    int dirty;            // 수정 비트\n    int referenced;       // 참조 비트\n} PageTableEntry;\n\nPageTableEntry page_table[NUM_PAGES];\n\n// 주소 변환 함수\nunsigned int translate_address(unsigned int logical_addr) {\n    // 페이지 번호와 오프셋 분리\n    unsigned int page_num = logical_addr >> PAGE_BITS;\n    unsigned int offset = logical_addr & (PAGE_SIZE - 1);\n    \n    printf(\"논리 주소: %u (0x%X)\", logical_addr, logical_addr);\n    printf(\"페이지 번호: %u, 오프셋: %u\", page_num, offset);\n    \n    // 페이지 테이블 조회\n    if (!page_table[page_num].valid) {\n        printf(\"Page Fault 발생! 페이지 %u\", page_num);\n        return -1;  // Page fault\n    }\n    \n    // 물리 주소 계산\n    int frame_num = page_table[page_num].frame_number;\n    unsigned int physical_addr = (frame_num << PAGE_BITS) | offset;\n    \n    printf(\"프레임 번호: %d\", frame_num);\n    printf(\"물리 주소: %u (0x%X)\", physical_addr, physical_addr);\n    \n    return physical_addr;\n}\n\n// 페이지 테이블 초기화\nvoid init_page_table() {\n    for (int i = 0; i < NUM_PAGES; i++) {\n        page_table[i].valid = 0;\n        page_table[i].frame_number = -1;\n    }\n    // 일부 페이지 매핑\n    page_table[0].frame_number = 5;  page_table[0].valid = 1;\n    page_table[1].frame_number = 2;  page_table[1].valid = 1;\n    page_table[2].frame_number = 8;  page_table[2].valid = 1;\n}\n\nint main() {\n    init_page_table();\n    translate_address(8196);  // 페이지 2, 오프셋 4\n    return 0;\n}"
        },
        {
            "type": "tip",
            "title": "면접 대비 정리",
            "content": "**페이징 vs 세그멘테이션 비교**:\n| 구분 | 페이징 | 세그멘테이션 |\n|------|--------|-------------|\n| 크기 | 고정 (4KB 등) | 가변 |\n| 단편화 | 내부 단편화 | 외부 단편화 |\n| 논리적 구분 | 없음 | 있음 (코드/데이터) |\n| 주소 변환 | 단순 | 복잡 |\n| 공유 | 페이지 단위 | 세그먼트 단위 |\n\n**페이지 테이블 엔트리 구성**:\n| 필드 | 설명 |\n|------|------|\n| 프레임 번호 | 물리 메모리 프레임 위치 |\n| 유효 비트 (V) | 메모리에 존재 여부 |\n| 수정 비트 (D) | 페이지 수정 여부 |\n| 참조 비트 (R) | 최근 접근 여부 |\n| 보호 비트 | R/W/X 권한 |\n\n**면접 빈출 질문**:\n\nQ1: 페이징이란 무엇인가요?\nA: 메모리를 고정 크기 블록(페이지/프레임)으로 나누어 비연속적으로 할당하는 기법입니다.\n\nQ2: 내부 단편화와 외부 단편화의 차이는?\nA: 내부 단편화는 할당된 블록 내부의 낭비, 외부 단편화는 블록 사이의 빈 공간 낭비입니다. 페이징은 외부 단편화를 해결하지만 내부 단편화가 발생합니다.\n\nQ3: TLB Miss 발생 시 과정을 설명하세요.\nA: 1) TLB 검색 실패 2) 페이지 테이블 접근 3) 물리 주소 획득 4) TLB 갱신 5) 메모리 접근\n\n**핵심 키워드**: 페이지/프레임, 페이지 테이블, TLB, 다단계 페이징, 내부 단편화"
        }
    ]
}

# ============================================
# 04_스케줄링 (3개)
# ============================================

data["04_스케줄링/cpu-scheduling"] = {
    "id": "04_스케줄링/cpu-scheduling",
    "title": "CPU 스케줄링",
    "category": "os",
    "subCategory": "04_스케줄링",
    "language": "C",
    "description": "CPU 자원을 프로세스에 효율적으로 배분하는 스케줄링 개념을 학습합니다.",
    "isPlaceholder": False,
    "sections": [
        {
            "type": "concept",
            "title": "CPU 스케줄링 개념",
            "content": "CPU 스케줄링은 여러 프로세스 중 어떤 프로세스에 CPU를 할당할지 결정하는 기법입니다.\n\n**한 줄 요약**: 여러 프로세스가 CPU를 공정하고 효율적으로 사용하도록 순서를 정합니다.\n\n**은행 창구 비유**:\n- CPU = 은행 창구 직원\n- 프로세스 = 대기 고객\n- 스케줄러 = 번호표 시스템\n- 목표: 고객 대기 시간 최소화, 직원 효율 최대화\n\n**스케줄링 목표**:\n1. **CPU 이용률 극대화**: CPU가 쉬지 않도록\n2. **처리량 최대화**: 단위 시간당 완료 프로세스 수\n3. **대기 시간 최소화**: Ready Queue에서 기다리는 시간\n4. **응답 시간 최소화**: 요청부터 첫 응답까지 시간\n5. **공정성**: 모든 프로세스에 적절한 CPU 시간\n\n**스케줄링 발생 시점**:\n- 프로세스가 Running -> Waiting (I/O 요청)\n- 프로세스가 Running -> Ready (인터럽트)\n- 프로세스가 Waiting -> Ready (I/O 완료)\n- 프로세스 종료"
        },
        {
            "type": "code",
            "title": "CPU 스케줄링 구조 다이어그램",
            "language": "text",
            "code": "[ CPU 스케줄링 전체 흐름 ]\n\n                    +-------------------+\n     새 프로세스 -->|   Ready Queue     |<-- I/O 완료\n                    | [P1][P2][P3][P4]  |\n                    +--------+----------+\n                             |\n                    +--------v----------+\n                    |     Scheduler     |\n                    |   (스케줄러)       |\n                    +--------+----------+\n                             |\n                    +--------v----------+\n                    |    Dispatcher     |\n                    | (컨텍스트 스위칭)  |\n                    +--------+----------+\n                             |\n                    +--------v----------+\n                    |       CPU         |\n                    |   [실행 중: P2]   |\n                    +--------+----------+\n                             |\n         +-------------------+-------------------+\n         |                   |                   |\n         v                   v                   v\n    종료 (Exit)        I/O 요청            Time Quantum\n                    (Waiting Queue)         만료 (선점)\n\n[ 스케줄링 성능 지표 ]\n\n      도착        시작        완료\n        |          |          |\n        v          v          v\n   ----[==========|##########]-----> 시간\n        |<-------->|<-------->|\n        대기 시간    실행 시간\n        |<------------------->|\n             반환 시간\n\n대기 시간 = 시작 시간 - 도착 시간\n반환 시간 = 완료 시간 - 도착 시간\n응답 시간 = 첫 응답 시간 - 도착 시간"
        },
        {
            "type": "code",
            "title": "스케줄링 시뮬레이션",
            "language": "c",
            "code": "// === CPU 스케줄링 기본 구조 ===\n#include <stdio.h>\n#include <stdlib.h>\n\n// 프로세스 구조체\ntypedef struct {\n    int pid;              // 프로세스 ID\n    int arrival_time;     // 도착 시간\n    int burst_time;       // 실행 시간 (CPU burst)\n    int remaining_time;   // 남은 실행 시간\n    int start_time;       // 시작 시간\n    int completion_time;  // 완료 시간\n    int waiting_time;     // 대기 시간\n    int turnaround_time;  // 반환 시간\n    int priority;         // 우선순위\n} Process;\n\n// 성능 지표 계산\nvoid calculate_metrics(Process *p) {\n    p->turnaround_time = p->completion_time - p->arrival_time;\n    p->waiting_time = p->turnaround_time - p->burst_time;\n}\n\n// FCFS 스케줄링 예시\nvoid fcfs_scheduling(Process processes[], int n) {\n    int current_time = 0;\n    \n    printf(\"=== FCFS 스케줄링 ===\");\n    \n    for (int i = 0; i < n; i++) {\n        // 프로세스 도착 대기\n        if (current_time < processes[i].arrival_time) {\n            current_time = processes[i].arrival_time;\n        }\n        \n        processes[i].start_time = current_time;\n        processes[i].completion_time = current_time + processes[i].burst_time;\n        current_time = processes[i].completion_time;\n        \n        calculate_metrics(&processes[i]);\n        \n        printf(\"P%d: 시작=%d, 완료=%d, 대기=%d, 반환=%d\",\n               processes[i].pid,\n               processes[i].start_time,\n               processes[i].completion_time,\n               processes[i].waiting_time,\n               processes[i].turnaround_time);\n    }\n}\n\nint main() {\n    Process p[] = {\n        {1, 0, 5, 5, 0, 0, 0, 0, 0},\n        {2, 1, 3, 3, 0, 0, 0, 0, 0},\n        {3, 2, 8, 8, 0, 0, 0, 0, 0}\n    };\n    fcfs_scheduling(p, 3);\n    return 0;\n}"
        },
        {
            "type": "tip",
            "title": "면접 대비 정리",
            "content": "**스케줄링 성능 지표 정리**:\n| 지표 | 정의 | 계산식 |\n|------|------|--------|\n| CPU 이용률 | CPU 사용 비율 | (실행시간/전체시간)*100 |\n| 처리량 | 완료 프로세스/시간 | 완료 수 / 전체 시간 |\n| 대기 시간 | Ready Queue 대기 | 시작 - 도착 |\n| 반환 시간 | 제출~완료 시간 | 완료 - 도착 |\n| 응답 시간 | 첫 응답까지 시간 | 첫 실행 - 도착 |\n\n**스케줄러 종류**:\n| 종류 | 역할 | 빈도 |\n|------|------|------|\n| 장기 스케줄러 | 어떤 프로세스를 Ready Queue에 | 드묾 |\n| 단기 스케줄러 | Ready -> Running 결정 | 매우 자주 |\n| 중기 스케줄러 | Swapping 결정 | 중간 |\n\n**면접 빈출 질문**:\n\nQ1: CPU 스케줄링이 왜 필요한가요?\nA: 다중 프로그래밍 환경에서 CPU 자원을 효율적이고 공정하게 배분하기 위해 필요합니다.\n\nQ2: 대기 시간과 반환 시간의 차이는?\nA: 대기 시간은 Ready Queue에서 기다린 시간, 반환 시간은 도착부터 완료까지의 전체 시간입니다.\n\nQ3: Dispatcher의 역할은?\nA: 스케줄러가 선택한 프로세스에게 실제로 CPU를 할당하고 컨텍스트 스위칭을 수행합니다.\n\n**핵심 키워드**: Ready Queue, Dispatcher, 대기시간, 반환시간, 처리량"
        }
    ]
}

data["04_스케줄링/preemptive"] = {
    "id": "04_스케줄링/preemptive",
    "title": "선점형 vs 비선점형",
    "category": "os",
    "subCategory": "04_스케줄링",
    "language": "C",
    "description": "선점형과 비선점형 스케줄링의 차이점과 특징을 비교합니다.",
    "isPlaceholder": False,
    "sections": [
        {
            "type": "concept",
            "title": "선점형과 비선점형 개념",
            "content": "스케줄링은 실행 중인 프로세스를 강제로 중단할 수 있는지에 따라 선점형/비선점형으로 구분됩니다.\n\n**한 줄 요약**: 선점형은 CPU를 빼앗을 수 있고, 비선점형은 자발적으로 반납할 때까지 기다립니다.\n\n**택시 비유**:\n- 비선점형 = 일반 택시 (손님이 내릴 때까지 대기)\n- 선점형 = 앰뷸런스 (긴급 환자 발생 시 택시 비켜!)\n\n**비선점형 (Non-preemptive)**:\n- 프로세스가 자발적으로 CPU 반납\n- I/O 요청 또는 종료 시에만 교체\n- 단순한 구현, 문맥 교환 적음\n- 응답 시간 보장 어려움\n- 예: FCFS, SJF (Non-preemptive)\n\n**선점형 (Preemptive)**:\n- OS가 강제로 CPU 회수 가능\n- 타임 퀀텀, 우선순위 변경 시 교체\n- 응답 시간 보장 가능\n- 문맥 교환 오버헤드 있음\n- 예: Round Robin, SRTF, 우선순위 스케줄링"
        },
        {
            "type": "code",
            "title": "선점형/비선점형 비교 다이어그램",
            "language": "text",
            "code": "[ 비선점형 스케줄링 (FCFS) ]\n\n시간:  0    5   8        16\n       |----|----|--------|\nP1     [####]               burst=5\nP2          [###]           burst=3  (도착:1, 대기:4)\nP3               [########] burst=8  (도착:2, 대기:6)\n\n-> P1이 끝날 때까지 P2, P3는 무조건 대기\n\n[ 선점형 스케줄링 (Round Robin, 퀀텀=2) ]\n\n시간:  0  2  4  5  7  9  10 12 14 16\n       |--|--|--|--|--|--|--|--|--|--|\nP1     [##]     [##]     [#]          burst=5\nP2        [##]     [#]                burst=3\nP3           [##]     [##]  [##][##]  burst=8\n\n-> 타임 퀀텀마다 강제 교체, 공정한 CPU 분배\n\n[ 선점 발생 시점 ]\n\n+------------------+------------------+\n|     비선점형      |      선점형       |\n+------------------+------------------+\n| Running->Waiting | Running->Waiting |\n| 프로세스 종료     | 프로세스 종료     |\n|                  | Running->Ready   |\n|                  | Waiting->Ready   |\n+------------------+------------------+\n\n[ SJF vs SRTF 비교 ]\n\n        도착  버스트\n  P1     0      7\n  P2     2      4\n  P3     4      1\n\nSJF (비선점):  P1[#######]P3[#]P2[####]\n시간:          0        7   8      12\n\nSRTF (선점):   P1[##]P2[##]P3[#]P2[##]P1[#####]\n시간:          0   2    4   5    7      12\n-> P2 도착 시 P1 선점, P3 도착 시 P2 선점"
        },
        {
            "type": "code",
            "title": "선점형/비선점형 구현",
            "language": "c",
            "code": "// === 선점형 vs 비선점형 스케줄링 ===\n#include <stdio.h>\n#include <stdbool.h>\n\ntypedef struct {\n    int pid;\n    int arrival;\n    int burst;\n    int remaining;\n    int completion;\n} Process;\n\n// 비선점형 SJF\nvoid sjf_nonpreemptive(Process p[], int n) {\n    int time = 0, completed = 0;\n    bool done[n];\n    for (int i = 0; i < n; i++) done[i] = false;\n    \n    printf(\"=== SJF (비선점형) ===\");\n    \n    while (completed < n) {\n        int shortest = -1;\n        int min_burst = 9999;\n        \n        // 도착한 프로세스 중 가장 짧은 것 선택\n        for (int i = 0; i < n; i++) {\n            if (!done[i] && p[i].arrival <= time && p[i].burst < min_burst) {\n                shortest = i;\n                min_burst = p[i].burst;\n            }\n        }\n        \n        if (shortest == -1) {\n            time++;\n            continue;\n        }\n        \n        // 선택된 프로세스 완료까지 실행 (비선점)\n        time += p[shortest].burst;\n        p[shortest].completion = time;\n        done[shortest] = true;\n        completed++;\n        \n        printf(\"P%d 완료: time=%d\", p[shortest].pid, time);\n    }\n}\n\n// 선점형 SRTF (Shortest Remaining Time First)\nvoid srtf_preemptive(Process p[], int n) {\n    int time = 0, completed = 0;\n    \n    printf(\"=== SRTF (선점형) ===\");\n    \n    while (completed < n) {\n        int shortest = -1;\n        int min_remaining = 9999;\n        \n        // 매 시간마다 가장 짧은 남은 시간 선택\n        for (int i = 0; i < n; i++) {\n            if (p[i].arrival <= time && p[i].remaining > 0 && p[i].remaining < min_remaining) {\n                shortest = i;\n                min_remaining = p[i].remaining;\n            }\n        }\n        \n        if (shortest == -1) {\n            time++;\n            continue;\n        }\n        \n        // 1단위 시간만 실행 (선점 가능)\n        p[shortest].remaining--;\n        time++;\n        \n        if (p[shortest].remaining == 0) {\n            p[shortest].completion = time;\n            completed++;\n            printf(\"P%d 완료: time=%d\", p[shortest].pid, time);\n        }\n    }\n}"
        },
        {
            "type": "tip",
            "title": "면접 대비 정리",
            "content": "**선점형 vs 비선점형 비교표**:\n| 구분 | 선점형 | 비선점형 |\n|------|--------|----------|\n| CPU 회수 | 강제 가능 | 자발적 반납 |\n| 응답 시간 | 보장 가능 | 보장 어려움 |\n| 문맥 교환 | 자주 발생 | 적게 발생 |\n| 구현 | 복잡 | 단순 |\n| 공정성 | 높음 | 낮음 |\n| 오버헤드 | 있음 | 적음 |\n\n**알고리즘 분류**:\n| 비선점형 | 선점형 |\n|----------|--------|\n| FCFS | Round Robin |\n| SJF | SRTF |\n| 우선순위 (Non) | 우선순위 (Pre) |\n| HRN | Multilevel Queue |\n\n**면접 빈출 질문**:\n\nQ1: 선점형과 비선점형의 차이점은?\nA: 선점형은 OS가 실행 중인 프로세스를 강제로 중단시킬 수 있고, 비선점형은 프로세스가 자발적으로 CPU를 반납해야 합니다.\n\nQ2: 언제 선점형 스케줄링을 사용하나요?\nA: 실시간 시스템, 대화형 시스템처럼 응답 시간이 중요한 경우에 사용합니다.\n\nQ3: Round Robin이 선점형인 이유는?\nA: 타임 퀀텀이 만료되면 프로세스 의지와 관계없이 강제로 CPU를 회수하기 때문입니다.\n\nQ4: SRTF의 문제점은?\nA: 긴 프로세스의 기아(Starvation) 현상이 발생할 수 있습니다.\n\n**핵심 키워드**: 선점(Preemption), 타임 퀀텀, 문맥 교환, 기아 현상, 응답 시간"
        }
    ]
}

data["04_스케줄링/scheduling-algorithm"] = {
    "id": "04_스케줄링/scheduling-algorithm",
    "title": "스케줄링 알고리즘",
    "category": "os",
    "subCategory": "04_스케줄링",
    "language": "C",
    "description": "주요 CPU 스케줄링 알고리즘의 특징과 동작 방식을 비교합니다.",
    "isPlaceholder": False,
    "sections": [
        {
            "type": "concept",
            "title": "스케줄링 알고리즘 개요",
            "content": "다양한 스케줄링 알고리즘이 각각의 목표와 환경에 맞게 사용됩니다.\n\n**한 줄 요약**: FCFS는 단순, SJF는 효율적, RR은 공정, 우선순위는 중요도 반영.\n\n**음식점 비유**:\n- FCFS = 번호표 순서대로 (먼저 온 손님 먼저)\n- SJF = 간단한 주문 먼저 (짧은 작업 먼저)\n- RR = 셀프바 순환 (조금씩 돌아가며)\n- 우선순위 = VIP 우선 (중요 손님 먼저)\n\n**주요 알고리즘**:\n\n1. **FCFS (First Come First Served)**\n   - 먼저 도착한 순서대로 처리\n   - 비선점형, 구현 단순\n   - Convoy Effect 문제\n\n2. **SJF (Shortest Job First)**\n   - 실행 시간이 짧은 순서대로\n   - 평균 대기 시간 최소화\n   - 기아(Starvation) 문제\n\n3. **Round Robin**\n   - 타임 퀀텀만큼 순환 실행\n   - 선점형, 공정한 분배\n   - 퀀텀 크기가 성능 좌우\n\n4. **Priority Scheduling**\n   - 우선순위 높은 것 먼저\n   - 기아 문제 -> Aging으로 해결"
        },
        {
            "type": "code",
            "title": "알고리즘별 동작 다이어그램",
            "language": "text",
            "code": "[ 예시 프로세스 ]\n\n프로세스  도착시간  실행시간  우선순위\n  P1        0         8        3\n  P2        1         4        1 (높음)\n  P3        2         2        2\n\n[ FCFS - 도착 순서대로 ]\n\n  0       8      12    14\n  |-------|------|-----|-->\nP1[#######]\nP2        [####]\nP3              [##]\n\n평균 대기: (0+7+10)/3 = 5.67\n\n[ SJF - 짧은 작업 먼저 ]\n\n  0       8  10    14\n  |-------|--|-----|-->\nP1[#######]\nP3        [##]         (P2보다 짧음)\nP2           [####]\n\n평균 대기: (0+6+8)/3 = 4.67\n\n[ Round Robin (퀀텀=3) ]\n\n  0   3   6   8  11  14\n  |---|---|---|---|---|-->\nP1[###]       [###]   [##]\nP2    [###]       [#]\nP3        [##]\n\n평균 대기: (6+7+4)/3 = 5.67\n공정한 응답 시간 보장\n\n[ 우선순위 스케줄링 ]\n\n  0   4   6      14\n  |---|---|------|-->\nP2[####]            (우선순위 1)\nP3    [##]          (우선순위 2)\nP1       [########] (우선순위 3)\n\n평균 대기: (6+3+0)/3 = 3"
        },
        {
            "type": "code",
            "title": "Round Robin 구현",
            "language": "c",
            "code": "// === Round Robin 스케줄링 구현 ===\n#include <stdio.h>\n#include <stdbool.h>\n\n#define TIME_QUANTUM 3\n#define MAX_PROCESS 10\n\ntypedef struct {\n    int pid;\n    int arrival;\n    int burst;\n    int remaining;\n    int completion;\n    int waiting;\n    int turnaround;\n    int response;\n    bool first_run;\n} Process;\n\nvoid round_robin(Process p[], int n) {\n    int queue[MAX_PROCESS * 10];\n    int front = 0, rear = 0;\n    int time = 0, completed = 0;\n    bool in_queue[MAX_PROCESS] = {false};\n    \n    // 초기화\n    for (int i = 0; i < n; i++) {\n        p[i].remaining = p[i].burst;\n        p[i].first_run = true;\n    }\n    \n    // 시간 0에 도착한 프로세스 큐에 추가\n    for (int i = 0; i < n; i++) {\n        if (p[i].arrival == 0) {\n            queue[rear++] = i;\n            in_queue[i] = true;\n        }\n    }\n    \n    printf(\"=== Round Robin (Quantum=%d) ===\", TIME_QUANTUM);\n    \n    while (completed < n) {\n        if (front == rear) {\n            time++;\n            // 새로 도착한 프로세스 확인\n            for (int i = 0; i < n; i++) {\n                if (!in_queue[i] && p[i].arrival <= time && p[i].remaining > 0) {\n                    queue[rear++] = i;\n                    in_queue[i] = true;\n                }\n            }\n            continue;\n        }\n        \n        int idx = queue[front++];\n        \n        // 응답 시간 기록\n        if (p[idx].first_run) {\n            p[idx].response = time - p[idx].arrival;\n            p[idx].first_run = false;\n        }\n        \n        // 타임 퀀텀 또는 남은 시간만큼 실행\n        int exec_time = (p[idx].remaining < TIME_QUANTUM) ? p[idx].remaining : TIME_QUANTUM;\n        \n        printf(\"Time %d-%d: P%d 실행\", time, time + exec_time, p[idx].pid);\n        \n        time += exec_time;\n        p[idx].remaining -= exec_time;\n        \n        // 새로 도착한 프로세스 큐에 추가\n        for (int i = 0; i < n; i++) {\n            if (!in_queue[i] && p[i].arrival <= time && p[i].remaining > 0) {\n                queue[rear++] = i;\n                in_queue[i] = true;\n            }\n        }\n        \n        if (p[idx].remaining > 0) {\n            queue[rear++] = idx;  // 다시 큐에 추가\n        } else {\n            p[idx].completion = time;\n            p[idx].turnaround = time - p[idx].arrival;\n            p[idx].waiting = p[idx].turnaround - p[idx].burst;\n            completed++;\n            printf(\"  -> P%d 완료!\", p[idx].pid);\n        }\n    }\n}"
        },
        {
            "type": "tip",
            "title": "면접 대비 정리",
            "content": "**스케줄링 알고리즘 비교표**:\n| 알고리즘 | 선점 | 장점 | 단점 | 사용처 |\n|---------|------|------|------|--------|\n| FCFS | X | 단순 | Convoy | 배치 |\n| SJF | X/O | 최적 대기 | 기아 | 배치 |\n| RR | O | 공정 | 오버헤드 | 대화형 |\n| 우선순위 | X/O | 중요도 | 기아 | 실시간 |\n| MLQ | O | 분류 처리 | 복잡 | 범용 |\n| MLFQ | O | 적응형 | 복잡 | 범용 |\n\n**주요 문제와 해결책**:\n| 문제 | 원인 | 해결책 |\n|------|------|--------|\n| Convoy Effect | 긴 프로세스 | SJF/RR 사용 |\n| Starvation | 낮은 우선순위 | Aging 기법 |\n| 잦은 문맥교환 | 작은 퀀텀 | 퀀텀 크기 조정 |\n\n**면접 빈출 질문**:\n\nQ1: Round Robin의 타임 퀀텀 크기는 어떻게 정하나요?\nA: 너무 크면 FCFS처럼 동작, 너무 작으면 문맥 교환 오버헤드 증가. 보통 10-100ms.\n\nQ2: SJF가 최적인 이유는?\nA: 짧은 작업을 먼저 처리하면 뒤따르는 작업들의 대기 시간이 줄어들어 평균 대기 시간이 최소화됩니다.\n\nQ3: Aging이란 무엇인가요?\nA: 오래 대기한 프로세스의 우선순위를 점진적으로 높여 기아 현상을 방지하는 기법입니다.\n\nQ4: MLFQ(Multilevel Feedback Queue)를 설명하세요.\nA: 여러 우선순위 큐를 두고, CPU 많이 사용하면 낮은 큐로, I/O 중심이면 높은 큐에 유지하는 적응형 알고리즘입니다.\n\n**핵심 키워드**: FCFS, SJF, RR, 우선순위, Aging, MLFQ, 타임 퀀텀"
        }
    ]
}

# Save updated os.json
with open('src/data/contents/os.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("os.json updated successfully with 7 topics!")
print("\nUpdated topics:")
print("04_메모리:")
print("  - memory-structure (메모리 구조)")
print("  - stack-heap (스택 vs 힙)")
print("  - virtual-memory (가상 메모리)")
print("  - paging (페이징)")
print("\n04_스케줄링:")
print("  - cpu-scheduling (CPU 스케줄링)")
print("  - preemptive (선점형 vs 비선점형)")
print("  - scheduling-algorithm (스케줄링 알고리즘)")
