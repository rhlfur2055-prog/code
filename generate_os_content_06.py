#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OS Content Generator 06
Updates os.json with high-quality Korean content for:
- 07_동기비동기/io-model
- 07_면접/interview-os
- 08_파일시스템/file-system
- 08_파일시스템/inode
- 08_파일시스템/linux-command
- index
"""

import json
import os

def get_new_content():
    """Return new content for OS topics."""

    return {
        # 07_동기비동기/io-model - I/O 모델
        "07_동기비동기/io-model": {
            "id": "07_동기비동기/io-model",
            "title": "I/O 모델",
            "category": "os",
            "subCategory": "07_동기비동기",
            "language": "C",
            "description": "Blocking I/O, Non-blocking I/O, I/O Multiplexing, Async I/O의 동작 원리와 차이점을 학습합니다.",
            "isPlaceholder": False,
            "sections": [
                {
                    "type": "concept",
                    "title": "I/O 모델의 이해",
                    "content": "I/O 모델은 프로그램이 입출력 작업을 처리하는 방식입니다.\n\n**도서관 비유로 이해하기**\n\n도서관에서 책을 빌리는 상황을 상상해보세요:\n\n1. **Blocking I/O (동기 블로킹)**\n   - 사서에게 책을 요청하고, 책이 올 때까지 카운터 앞에서 기다림\n   - 그 동안 아무것도 할 수 없음\n   - 가장 단순하지만 비효율적\n\n2. **Non-blocking I/O (동기 논블로킹)**\n   - 책을 요청하고 \"아직 없어요\"라는 답을 받으면 다른 일을 함\n   - 주기적으로 와서 \"책 왔나요?\" 확인 (polling)\n   - CPU를 낭비할 수 있음\n\n3. **I/O Multiplexing (select/poll/epoll)**\n   - 여러 책을 동시에 요청해두고, 안내 방송을 기다림\n   - \"3번 손님, 책 준비되었습니다\" 방송이 오면 가져감\n   - 하나의 스레드로 여러 I/O를 효율적으로 처리\n\n4. **Async I/O (비동기 I/O)**\n   - 책을 요청하고 집 주소를 남김\n   - 책이 준비되면 집으로 배달해줌\n   - 완전한 비동기, 가장 효율적\n\n**핵심 차이점**\n\n| 모델 | 호출 시 블록 | 완료 통보 방식 | 사용 예 |\n|------|-------------|---------------|--------|\n| Blocking | O | 직접 확인 | 전통적 소켓 |\n| Non-blocking | X | Polling | 게임 루프 |\n| Multiplexing | O (대기) | 이벤트 | 웹서버(Nginx) |\n| Async | X | 콜백/시그널 | io_uring, IOCP |"
                },
                {
                    "type": "code",
                    "title": "I/O 모델 비교 다이어그램",
                    "language": "text",
                    "code": "=== I/O 모델 비교 다이어그램 ===\n\n[1] Blocking I/O\n\n    Application          Kernel\n        |                   |\n        |--- read() ------->|\n        |    (blocked)      |<-- 데이터 대기 -->\n        |                   |<-- 데이터 복사 -->\n        |<-- return --------|  \n        |                   |\n\n[2] Non-blocking I/O\n\n    Application          Kernel\n        |                   |\n        |--- read() ------->|\n        |<-- EAGAIN --------|  (데이터 없음)\n        |--- read() ------->|\n        |<-- EAGAIN --------|  (polling 반복)\n        |--- read() ------->|\n        |<-- return data ---|  (데이터 준비됨)\n        |                   |\n\n[3] I/O Multiplexing (select/epoll)\n\n    Application          Kernel\n        |                   |\n        |--- select() ----->|  (여러 fd 감시)\n        |    (blocked)      |<-- 이벤트 대기 -->\n        |<-- fd ready ------|  (준비된 fd 알림)\n        |--- read() ------->|\n        |<-- return data ---|  (데이터 읽기)\n        |                   |\n\n[4] Async I/O (aio_read, io_uring)\n\n    Application          Kernel\n        |                   |\n        |--- aio_read() --->|  (즉시 반환)\n        |<-- return --------|  \n        |  (다른 작업 수행)  |<-- 데이터 처리 -->\n        |                   |\n        |<-- 시그널/콜백 ---|  (완료 통보)\n        |                   |"
                },
                {
                    "type": "code",
                    "title": "실무 I/O 모델 구현 예제",
                    "language": "c",
                    "code": "/* === 1. Blocking I/O === */\n#include <stdio.h>\n#include <unistd.h>\n#include <fcntl.h>\n\nvoid blocking_read() {\n    char buf[1024];\n    // read()는 데이터가 올 때까지 블록됨\n    ssize_t n = read(STDIN_FILENO, buf, sizeof(buf));\n    printf(\"Read %zd bytes\\n\", n);\n}\n\n/* === 2. Non-blocking I/O === */\n#include <errno.h>\n\nvoid nonblocking_read(int fd) {\n    char buf[1024];\n    \n    // Non-blocking 모드 설정\n    int flags = fcntl(fd, F_GETFL, 0);\n    fcntl(fd, F_SETFL, flags | O_NONBLOCK);\n    \n    while (1) {\n        ssize_t n = read(fd, buf, sizeof(buf));\n        if (n > 0) {\n            printf(\"Read %zd bytes\\n\", n);\n            break;\n        } else if (n == -1 && errno == EAGAIN) {\n            printf(\"No data yet, doing other work...\\n\");\n            usleep(100000);  // 다른 작업 수행\n        }\n    }\n}\n\n/* === 3. I/O Multiplexing (epoll) === */\n#include <sys/epoll.h>\n\n#define MAX_EVENTS 10\n\nvoid epoll_example(int server_fd) {\n    int epoll_fd = epoll_create1(0);\n    struct epoll_event ev, events[MAX_EVENTS];\n    \n    // 서버 소켓 등록\n    ev.events = EPOLLIN;\n    ev.data.fd = server_fd;\n    epoll_ctl(epoll_fd, EPOLL_CTL_ADD, server_fd, &ev);\n    \n    while (1) {\n        // 이벤트 대기 (여러 fd 동시 감시)\n        int nfds = epoll_wait(epoll_fd, events, MAX_EVENTS, -1);\n        \n        for (int i = 0; i < nfds; i++) {\n            if (events[i].data.fd == server_fd) {\n                // 새 연결 처리\n                int client_fd = accept(server_fd, NULL, NULL);\n                ev.events = EPOLLIN | EPOLLET;  // Edge Trigger\n                ev.data.fd = client_fd;\n                epoll_ctl(epoll_fd, EPOLL_CTL_ADD, client_fd, &ev);\n            } else {\n                // 클라이언트 데이터 처리\n                handle_client(events[i].data.fd);\n            }\n        }\n    }\n}\n\n/* === 4. select vs poll vs epoll 비교 === */\n/*\n+----------+-----------+------------+------------------+\n| 방식     | 시간복잡도 | fd 제한    | 커널 통신        |\n+----------+-----------+------------+------------------+\n| select   | O(n)      | 1024       | 매번 fd 복사     |\n| poll     | O(n)      | 제한 없음  | 매번 fd 복사     |\n| epoll    | O(1)      | 제한 없음  | 콜백 방식        |\n+----------+-----------+------------+------------------+\n\nepoll의 장점:\n1. Level Trigger / Edge Trigger 선택 가능\n2. 등록된 fd에 대해서만 이벤트 전달\n3. 대규모 연결에서 뛰어난 성능\n*/"
                },
                {
                    "type": "tip",
                    "title": "I/O 모델 선택 가이드 및 면접 대비",
                    "content": "**실무에서의 I/O 모델 선택**\n\n1. **Blocking I/O**\n   - 단순한 CLI 도구, 스크립트\n   - 클라이언트당 스레드 모델\n\n2. **Non-blocking + Polling**\n   - 게임 서버의 메인 루프\n   - 실시간 시스템\n\n3. **I/O Multiplexing (epoll)**\n   - 웹 서버 (Nginx, Node.js)\n   - 채팅 서버, 게임 서버\n   - C10K 문제 해결의 핵심\n\n4. **Async I/O (io_uring)**\n   - 고성능 데이터베이스\n   - 저지연 네트워크 서버\n   - Linux 5.1+ 최신 기술\n\n**면접 빈출 질문**\n\nQ1. select와 epoll의 차이점은?\n- select: O(n), fd 제한(1024), 매번 fd_set 복사\n- epoll: O(1), 제한 없음, 콜백 방식\n\nQ2. Level Trigger vs Edge Trigger?\n- LT: 데이터 있으면 계속 알림 (기본값)\n- ET: 상태 변화시에만 알림 (효율적, 복잡)\n\nQ3. Nginx가 빠른 이유는?\n- 이벤트 기반 + I/O Multiplexing\n- 단일 프로세스로 수만 연결 처리\n\nQ4. Node.js의 이벤트 루프와 epoll의 관계?\n- libuv가 OS별로 epoll(Linux), kqueue(Mac), IOCP(Windows) 사용\n\n**C10K 문제란?**\n1만 개의 동시 연결을 처리하는 문제\n- 해결책: 이벤트 기반 I/O Multiplexing\n- 현재는 C10M(천만 연결)까지 논의"
                }
            ]
        },

        # 07_면접/interview-os - OS 면접 질문 총정리
        "07_면접/interview-os": {
            "id": "07_면접/interview-os",
            "title": "OS 면접 질문 총정리",
            "category": "os",
            "subCategory": "07_면접",
            "language": "Text",
            "description": "주니어/시니어 레벨별 OS 면접 질문 25개와 모범 답변을 정리합니다.",
            "isPlaceholder": False,
            "sections": [
                {
                    "type": "concept",
                    "title": "OS 면접 준비 가이드",
                    "content": "운영체제 면접은 CS 기초를 평가하는 핵심 영역입니다.\n\n**면접 준비 전략**\n\n면접관이 보는 관점을 이해하세요:\n- 주니어: 기본 개념의 정확한 이해\n- 시니어: 깊이 있는 이해 + 실무 적용 능력\n\n**답변의 3단계 구조**\n\n1. **정의** (What): 간단명료하게 개념 설명\n2. **원리** (How): 동작 방식 설명\n3. **실무** (Why): 왜 중요한지, 어디서 사용되는지\n\n**핵심 출제 영역 (빈도순)**\n\n1. 프로세스 vs 스레드 (90%)\n2. 동기화 (Mutex, Semaphore, Deadlock) (85%)\n3. 메모리 관리 (페이징, 가상메모리) (80%)\n4. CPU 스케줄링 (70%)\n5. I/O 모델 (동기/비동기, Blocking) (65%)\n\n**면접 팁**\n- 모르면 솔직히 말하고, 아는 부분까지 설명\n- 실제 경험이나 프로젝트와 연결해서 답변\n- 그림을 그려가며 설명하면 효과적"
                },
                {
                    "type": "code",
                    "title": "주니어 면접 질문 15선 (모범 답변)",
                    "language": "text",
                    "code": "=== 주니어 OS 면접 질문 15선 ===\n\n[Q1] 프로세스와 스레드의 차이점은 무엇인가요?\n\nA: 프로세스는 실행 중인 프로그램으로 독립적인 메모리 공간(Code, Data, \nHeap, Stack)을 가집니다. 스레드는 프로세스 내의 실행 단위로, 같은 \n프로세스의 스레드들은 Code, Data, Heap을 공유하고 Stack만 별도로 \n가집니다. 따라서 스레드 간 통신이 빠르지만, 동기화 문제가 발생할 수 \n있습니다.\n\n---\n[Q2] 컨텍스트 스위칭이란 무엇인가요?\n\nA: CPU가 현재 실행 중인 프로세스/스레드에서 다른 것으로 전환할 때, \n현재 상태(레지스터, PC 등)를 PCB에 저장하고 새 프로세스의 상태를 \n복원하는 과정입니다. 오버헤드가 발생하므로, 잦은 컨텍스트 스위칭은 \n성능 저하를 유발합니다.\n\n---\n[Q3] 데드락(Deadlock)이란 무엇이고, 발생 조건은?\n\nA: 데드락은 두 개 이상의 프로세스가 서로가 가진 자원을 기다리며 \n무한히 대기하는 상태입니다.\n\n4가지 필요조건:\n1. 상호배제: 자원을 한 번에 하나만 사용\n2. 점유대기: 자원을 가진 채 다른 자원 대기\n3. 비선점: 강제로 자원을 빼앗을 수 없음\n4. 순환대기: 프로세스들이 원형으로 자원 대기\n\n---\n[Q4] Mutex와 Semaphore의 차이는?\n\nA: Mutex는 1개의 스레드만 임계영역에 접근 가능(이진 잠금), \nSemaphore는 N개의 스레드가 접근 가능합니다. Mutex는 소유권 개념이 \n있어 잠근 스레드만 해제 가능하지만, Semaphore는 다른 스레드가 \n해제할 수 있습니다.\n\n---\n[Q5] 가상 메모리란 무엇인가요?\n\nA: 물리 메모리보다 큰 메모리 공간을 사용할 수 있게 해주는 기술입니다.\n프로세스는 가상 주소를 사용하고, MMU가 물리 주소로 변환합니다. \n필요한 페이지만 물리 메모리에 올리고, 나머지는 디스크(swap)에 \n저장합니다.\n\n---\n[Q6] 페이지 폴트란?\n\nA: 접근하려는 페이지가 물리 메모리에 없을 때 발생하는 인터럽트입니다.\nOS가 디스크에서 해당 페이지를 메모리로 로드합니다. 빈번한 페이지 \n폴트는 성능을 크게 저하시킵니다(스래싱).\n\n---\n[Q7] 페이지 교체 알고리즘을 설명해주세요.\n\nA: 물리 메모리가 부족할 때 어떤 페이지를 내릴지 결정하는 알고리즘입니다.\n- FIFO: 가장 오래된 페이지 교체\n- LRU: 가장 오래 사용 안 된 페이지 교체 (실무에서 많이 사용)\n- LFU: 가장 적게 사용된 페이지 교체\n- OPT: 앞으로 가장 오래 안 쓸 페이지 (이론적 최적)\n\n---\n[Q8] 동기와 비동기의 차이는?\n\nA: 동기는 요청 후 결과가 올 때까지 기다립니다. 비동기는 요청만 하고 \n다른 작업을 수행하다가 결과가 오면 처리합니다. 비동기는 효율적이지만 \n콜백 관리가 복잡합니다.\n\n---\n[Q9] Blocking과 Non-blocking의 차이는?\n\nA: Blocking은 호출한 함수가 완료될 때까지 제어권을 반환하지 않습니다.\nNon-blocking은 즉시 제어권을 반환하고, 결과가 준비되지 않았으면 \n에러코드를 반환합니다.\n\n---\n[Q10] CPU 스케줄링 알고리즘 3가지를 설명해주세요.\n\nA: \n1. FCFS: 먼저 온 순서대로 처리 (단순, 호위효과 문제)\n2. Round Robin: 시간 할당량만큼 돌아가며 실행 (공정, 반응성 좋음)\n3. Priority: 우선순위 높은 순서로 (기아 문제 -> 에이징으로 해결)\n\n---\n[Q11] 사용자 모드와 커널 모드의 차이는?\n\nA: 사용자 모드는 제한된 명령만 실행 가능하고, 커널 모드는 모든 명령을 \n실행할 수 있습니다. 시스템 콜을 통해 커널 모드로 전환하여 하드웨어 \n접근 등 특권 작업을 수행합니다.\n\n---\n[Q12] 시스템 콜이란?\n\nA: 사용자 프로그램이 커널의 서비스를 요청하는 인터페이스입니다.\n파일 I/O(open, read, write), 프로세스 관리(fork, exec), \n메모리 관리(mmap) 등이 있습니다.\n\n---\n[Q13] 캐시 메모리란?\n\nA: CPU와 메인 메모리 사이의 고속 메모리로, 자주 사용하는 데이터를 \n저장합니다. 지역성(Locality) 원리를 활용하여 메모리 접근 속도를 \n향상시킵니다. L1, L2, L3 캐시가 있습니다.\n\n---\n[Q14] 인터럽트란?\n\nA: CPU가 현재 작업을 중단하고 긴급한 이벤트를 처리하는 메커니즘입니다.\n하드웨어 인터럽트(키보드, 타이머)와 소프트웨어 인터럽트(시스템콜, \n예외)가 있습니다.\n\n---\n[Q15] Stack과 Heap의 차이는?\n\nA: Stack은 함수 호출 시 지역변수, 매개변수가 저장되며 자동 할당/해제됩니다.\nHeap은 동적 메모리 할당 영역으로, 프로그래머가 직접 관리합니다.\nStack은 빠르지만 크기 제한이 있고, Heap은 느리지만 유연합니다."
                },
                {
                    "type": "code",
                    "title": "시니어 면접 질문 10선 (심화 답변)",
                    "language": "text",
                    "code": "=== 시니어 OS 면접 질문 10선 ===\n\n[Q1] 멀티스레드 환경에서 Race Condition을 어떻게 해결하셨나요?\n\nA: Race Condition은 여러 스레드가 공유 자원에 동시 접근할 때 발생합니다.\n\n해결 경험:\n1. Mutex/Lock: 임계영역 보호 (단순하지만 성능 저하)\n2. Atomic 연산: CAS 기반 lock-free 자료구조\n3. Thread-local 저장소: 공유 자체를 피함\n4. 불변 객체: 상태 변경 없이 새 객체 생성\n\n실무에서는 먼저 공유를 최소화하고, 필요시 적절한 수준의 동기화를 \n적용합니다. 과도한 락은 성능 병목이 되므로 프로파일링 후 최적화합니다.\n\n---\n[Q2] 메모리 릭을 디버깅한 경험을 설명해주세요.\n\nA: \n진단 과정:\n1. 증상 확인: 메모리 사용량 지속 증가, OOM 발생\n2. 도구 활용: Valgrind, AddressSanitizer, pmap\n3. 힙 덤프 분석: 어떤 객체가 증가하는지 확인\n\n해결 사례:\n- 이벤트 리스너 미해제 -> weak reference 적용\n- 캐시 무한 증가 -> LRU 캐시로 교체, TTL 설정\n- 순환 참조 -> weak_ptr 사용 또는 명시적 해제\n\n예방책:\n- RAII 패턴, 스마트 포인터 사용\n- 정적 분석 도구 CI 연동\n\n---\n[Q3] 대규모 동시 접속을 처리하기 위한 I/O 모델 선택 기준은?\n\nA: \nC10K 이상의 연결 처리 시:\n\n1. I/O Multiplexing (epoll/kqueue)\n   - 하나의 스레드로 수만 연결 처리\n   - Nginx, Redis 아키텍처\n   - Level/Edge Trigger 선택 중요\n\n2. 스레드 풀 + epoll 조합\n   - 이벤트 감지: epoll\n   - 작업 처리: 스레드 풀\n   - CPU bound 작업이 섞인 경우\n\n3. io_uring (최신)\n   - 커널-유저 공간 복사 최소화\n   - 배치 처리로 syscall 오버헤드 감소\n\n선택 기준: 연결 수, 요청 특성(CPU/IO bound), 지연시간 요구사항\n\n---\n[Q4] 데드락을 시스템 레벨에서 어떻게 탐지/해결하나요?\n\nA: \n탐지 방법:\n1. 자원 할당 그래프에서 사이클 탐지\n2. 타임아웃 기반 탐지 (실용적)\n3. 주기적 데드락 검사 스레드\n\n해결 방법:\n1. 프로세스 종료: 비용 적은 프로세스 선택\n2. 자원 선점: 롤백 후 재시작\n3. 예방: 자원 순서 정의, 한번에 모든 자원 요청\n\n실무 경험:\n- DB 트랜잭션 데드락: 순서 일관성 유지, 타임아웃 설정\n- 락 계층 정의: 항상 같은 순서로 락 획득\n\n---\n[Q5] 컨테이너(Docker)의 격리 원리를 OS 관점에서 설명해주세요.\n\nA: \n리눅스 커널 기술 활용:\n\n1. Namespace: 자원 격리\n   - PID ns: 프로세스 ID 격리\n   - Network ns: 네트워크 스택 격리\n   - Mount ns: 파일시스템 격리\n   - User ns: 사용자/그룹 ID 격리\n\n2. Cgroups: 자원 제한\n   - CPU, Memory, I/O 사용량 제한\n   - OOM 시 특정 컨테이너만 kill\n\n3. UnionFS: 레이어 파일시스템\n   - 이미지 레이어 재사용\n   - Copy-on-Write로 효율적 저장\n\nVM과 차이: 하이퍼바이저 없이 커널 공유, 더 가벼움\n\n---\n[Q6] 커널 패닉 상황을 디버깅한 경험이 있나요?\n\nA: \n진단 과정:\n1. 커널 로그 분석: dmesg, /var/log/kern.log\n2. 크래시 덤프 분석: kdump + crash 유틸리티\n3. 스택 트레이스로 원인 모듈 파악\n\n경험 사례:\n- OOM Killer 동작 -> 메모리 누수 애플리케이션 발견\n- 드라이버 버그 -> 커널 버전 업그레이드로 해결\n- 파일시스템 손상 -> fsck 후 복구\n\n예방책:\n- 커널 파라미터 튜닝 (vm.overcommit_memory)\n- 리소스 모니터링 및 알림 설정\n\n---\n[Q7] NUMA 아키텍처에서 성능 최적화 경험은?\n\nA: \nNUMA(Non-Uniform Memory Access) 이해:\n- 각 CPU가 로컬 메모리를 가짐\n- 원격 메모리 접근은 느림 (2-3배)\n\n최적화 전략:\n1. numactl로 프로세스를 특정 노드에 바인딩\n2. 메모리 할당 정책: local, interleave\n3. CPU affinity 설정\n4. 대용량 페이지(Huge Pages) 활용\n\n모니터링:\n- numastat: NUMA 히트/미스 확인\n- perf stat: 원격 메모리 접근 측정\n\n---\n[Q8] 실시간 시스템에서 스케줄링 요구사항은?\n\nA: \n실시간 시스템 분류:\n- Hard Real-time: 데드라인 필수 (항공, 의료)\n- Soft Real-time: 데드라인 권장 (멀티미디어)\n\n리눅스 실시간 스케줄링:\n1. SCHED_FIFO: 우선순위 기반, 선점 없음\n2. SCHED_RR: 우선순위 + 라운드로빈\n3. SCHED_DEADLINE: EDF 알고리즘\n\n튜닝 경험:\n- 인터럽트 처리 최적화\n- 커널 선점 활성화 (PREEMPT_RT 패치)\n- 메모리 락 (mlockall)으로 페이지 폴트 방지\n\n---\n[Q9] 파일시스템 선택 기준과 성능 특성은?\n\nA: \n주요 파일시스템 비교:\n\n1. ext4: 범용, 안정적, 저널링\n   - 대부분의 리눅스 서버\n\n2. XFS: 대용량 파일, 병렬 I/O\n   - 데이터베이스, 미디어 서버\n\n3. Btrfs: CoW, 스냅샷, 압축\n   - 백업, 개발 환경\n\n4. ZFS: 무결성, RAID, 압축\n   - 엔터프라이즈 스토리지\n\n성능 튜닝:\n- noatime 마운트 옵션\n- I/O 스케줄러 선택 (none for SSD)\n- 적절한 블록 크기 설정\n\n---\n[Q10] OS 레벨에서 보안 강화 방법은?\n\nA: \n다층 방어 전략:\n\n1. 접근 제어\n   - SELinux/AppArmor: MAC(Mandatory Access Control)\n   - 최소 권한 원칙\n\n2. 메모리 보호\n   - ASLR: 주소 공간 랜덤화\n   - DEP/NX: 실행 불가 메모리\n   - Stack Canary: 버퍼 오버플로우 방지\n\n3. 감사 및 모니터링\n   - auditd: 시스템 콜 로깅\n   - 침입 탐지 시스템\n\n4. 컨테이너 보안\n   - Seccomp: 시스템 콜 필터링\n   - 루트리스 컨테이너\n   - 이미지 취약점 스캔"
                },
                {
                    "type": "tip",
                    "title": "면접 실전 팁 및 체크리스트",
                    "content": "**면접 직전 체크리스트**\n\n[ ] 프로세스 vs 스레드 명확히 구분 가능\n[ ] 동기화 3총사 (Mutex, Semaphore, Monitor) 설명 가능\n[ ] 데드락 4조건 암기\n[ ] 가상메모리, 페이징 동작 원리 이해\n[ ] 동기/비동기, Blocking/Non-blocking 2x2 매트릭스\n[ ] 스케줄링 알고리즘 3개 이상\n\n**답변 시 피해야 할 것**\n\n1. \"잘 모르겠습니다\"만 하지 말 것\n   -> \"정확히는 모르지만, ~라고 추측합니다\"\n\n2. 외운 대로만 말하지 말 것\n   -> 실제 경험, 프로젝트와 연결\n\n3. 너무 길게 말하지 말 것\n   -> 핵심 먼저, 질문 시 상세 설명\n\n**꼬리 질문 대비**\n\nQ: 프로세스 vs 스레드 답변 후\n-> \"그럼 멀티프로세스보다 멀티스레드가 항상 좋나요?\"\nA: \"아닙니다. 스레드는 하나가 죽으면 전체가 영향받고, \n    메모리 공유로 동기화 문제가 생깁니다. \n    Chrome은 탭마다 프로세스로 안정성을 높였습니다.\"\n\n**실무 연결 예시**\n\n\"저는 프로젝트에서 Redis를 사용했는데, Redis가 싱글 스레드임에도 \n빠른 이유를 공부하면서 I/O Multiplexing(epoll)의 효율성을 \n이해하게 되었습니다.\"\n\n**추천 학습 순서**\n1. 프로세스/스레드 (기본)\n2. 동기화 (필수)\n3. 메모리 관리 (중요)\n4. 스케줄링 (이론)\n5. I/O 모델 (실무)"
                }
            ]
        },

        # 08_파일시스템/file-system - 파일 시스템 개념
        "08_파일시스템/file-system": {
            "id": "08_파일시스템/file-system",
            "title": "파일 시스템 개념",
            "category": "os",
            "subCategory": "08_파일시스템",
            "language": "Bash",
            "description": "FAT, NTFS, ext4 등 파일 시스템의 구조와 특징을 학습합니다.",
            "isPlaceholder": False,
            "sections": [
                {
                    "type": "concept",
                    "title": "파일 시스템의 이해",
                    "content": "파일 시스템은 저장 장치에서 데이터를 조직화하고 관리하는 방법입니다.\n\n**도서관 비유로 이해하기**\n\n파일 시스템을 도서관에 비유해보면:\n\n1. **하드디스크** = 도서관 건물 전체\n2. **파티션** = 각 층 (1층: 소설, 2층: 과학 등)\n3. **파일 시스템** = 책 정리 방법 (듀이십진분류법 등)\n4. **디렉토리** = 책장/서가\n5. **파일** = 책\n6. **inode** = 책의 위치 카드 (어느 서가, 몇 번째)\n\n**주요 파일 시스템 비교**\n\n| 파일시스템 | OS | 최대 파일 | 최대 볼륨 | 특징 |\n|-----------|-----|----------|----------|------|\n| FAT32 | 범용 | 4GB | 2TB | 단순, 호환성 |\n| NTFS | Windows | 16EB | 256TB | 저널링, 권한 |\n| ext4 | Linux | 16TB | 1EB | 저널링, 안정 |\n| XFS | Linux | 8EB | 8EB | 대용량 특화 |\n| APFS | macOS | 8EB | - | SSD 최적화 |\n\n**저널링(Journaling)이란?**\n\n변경 전 로그를 먼저 기록하는 방식:\n1. 트랜잭션 로그 기록\n2. 실제 데이터 기록\n3. 로그 삭제\n\n비정상 종료 시 로그로 복구 -> 데이터 무결성 보장"
                },
                {
                    "type": "code",
                    "title": "파일 시스템 구조 다이어그램",
                    "language": "text",
                    "code": "=== ext4 파일 시스템 구조 ===\n\n+----------------------------------------------------------+\n|                      Disk Partition                       |\n+----------------------------------------------------------+\n|  Boot  |  Super  | Group | Block | Inode | Inode |  Data  |\n| Block  |  Block  | Desc. | Bitmap| Bitmap| Table | Blocks |\n+--------+---------+-------+-------+-------+-------+--------+\n|  1KB   |   1KB   |  nKB  |  1 Blk| 1 Blk | n Blk |  ....  |\n+----------------------------------------------------------+\n\n[ Super Block ]\n- 파일 시스템 전체 정보\n- 블록 크기, 블록 수, inode 수\n- 마운트 횟수, 마지막 마운트 시간\n\n[ Block Group 구조 ]\n\n    Block Group 0        Block Group 1        Block Group N\n+-------------------+-------------------+-------------------+\n| Super | GDT |Data | Super | GDT |Data | Super | GDT |Data |\n| Block |     |     | Block |     |     | Block |     |     |\n+-------------------+-------------------+-------------------+\n        (백업)             (백업)             (백업)\n\n=== NTFS 구조 ===\n\n+----------------------------------------------------------+\n|  Boot  |  MFT   | MFT    | Log   | Volume | Root | Data  |\n| Sector | (Master| Mirror | File  | Info   | Dir  | Area  |\n|        |  File  |        |       |        |      |       |\n|        | Table) |        |       |        |      |       |\n+--------+--------+--------+-------+--------+------+-------+\n\n[ MFT 레코드 구조 ]\n+------------+------------+------------+------------+\n| $STANDARD_ | $FILE_NAME | $DATA      | $INDEX_    |\n| INFORMATION|            | (파일내용) | ROOT       |\n+------------+------------+------------+------------+\n\n=== FAT32 구조 ===\n\n+----------------------------------------------------------+\n|  Boot  |  FAT1  |  FAT2  |  Root    |    Data Area      |\n| Sector | (File  | (File  |Directory |    (Clusters)      |\n|        |  Alloc |  Alloc |          |                    |\n|        | Table) | Table) |          |                    |\n+--------+--------+--------+----------+--------------------+\n\n[ FAT 테이블 - 클러스터 체인 ]\n\n클러스터 2 -> 클러스터 5 -> 클러스터 8 -> EOF\n    |            |            |\n    v            v            v\n[File A]     [File A]     [File A]\n[part 1]     [part 2]     [part 3]"
                },
                {
                    "type": "code",
                    "title": "파일 시스템 실무 명령어",
                    "language": "bash",
                    "code": "# === 파일 시스템 정보 확인 ===\n\n# 마운트된 파일 시스템 확인\ndf -Th\n# Filesystem     Type      Size  Used Avail Use% Mounted on\n# /dev/sda1      ext4      100G   30G   70G  30% /\n# /dev/sdb1      xfs       500G  200G  300G  40% /data\n\n# 블록 장치 정보\nlsblk -f\n# NAME   FSTYPE LABEL UUID                                 MOUNTPOINT\n# sda                                                       \n# ├─sda1 ext4         a1b2c3d4-...                         /\n# └─sda2 swap         e5f6g7h8-...                         [SWAP]\n\n# 파일 시스템 상세 정보 (ext4)\nsudo dumpe2fs /dev/sda1 | head -30\n\n# === 파일 시스템 생성 ===\n\n# ext4 파일 시스템 생성\nsudo mkfs.ext4 /dev/sdb1\n\n# ext4 with 라벨\nsudo mkfs.ext4 -L \"DataDrive\" /dev/sdb1\n\n# XFS 파일 시스템 생성\nsudo mkfs.xfs /dev/sdc1\n\n# NTFS 파일 시스템 생성 (Linux에서)\nsudo mkfs.ntfs /dev/sdd1\n\n# === 마운트/언마운트 ===\n\n# 마운트\nsudo mount /dev/sdb1 /mnt/data\n\n# 특정 옵션으로 마운트\nsudo mount -o noatime,nodiratime /dev/sdb1 /mnt/data\n\n# UUID로 마운트 (안전한 방법)\nsudo mount UUID=a1b2c3d4-... /mnt/data\n\n# 언마운트\nsudo umount /mnt/data\n\n# 강제 언마운트 (busy 상태일 때)\nsudo umount -l /mnt/data  # lazy unmount\n\n# === /etc/fstab 설정 ===\n# 부팅 시 자동 마운트 설정\n\n# UUID=xxxx  /mnt/data  ext4  defaults,noatime  0  2\n# |          |          |     |                 |  |\n# 장치ID     마운트포인트 타입  옵션              덤프 fsck순서\n\n# fstab 테스트 (실제 마운트 없이)\nsudo mount -a --fake\n\n# === 파일 시스템 점검/복구 ===\n\n# ext4 점검 (언마운트 상태에서)\nsudo fsck.ext4 /dev/sdb1\n\n# 자동 복구\nsudo fsck.ext4 -y /dev/sdb1\n\n# XFS 점검\nsudo xfs_repair /dev/sdc1\n\n# === 파일 시스템 튜닝 ===\n\n# ext4 파라미터 조정\nsudo tune2fs -c 30 /dev/sda1      # 30회 마운트마다 fsck\nsudo tune2fs -i 180d /dev/sda1    # 180일마다 fsck\n\n# reserved blocks 조정 (기본 5%)\nsudo tune2fs -m 1 /dev/sda1       # 1%로 변경\n\n# === 디스크 사용량 분석 ===\n\n# 디렉토리별 사용량\ndu -sh /var/*\n\n# 가장 큰 파일/디렉토리 찾기\ndu -ah / 2>/dev/null | sort -rh | head -20\n\n# ncdu (시각적 디스크 사용량 분석기)\nsudo apt install ncdu\nncdu /"
                },
                {
                    "type": "tip",
                    "title": "파일 시스템 선택 가이드 및 면접 질문",
                    "content": "**용도별 파일 시스템 선택**\n\n1. **일반 서버**: ext4\n   - 안정적, 범용적, 복구 도구 풍부\n\n2. **대용량 파일 서버**: XFS\n   - 대용량 파일 처리 최적화\n   - 병렬 I/O 성능 우수\n\n3. **백업/개발**: Btrfs\n   - 스냅샷, CoW 지원\n   - 데이터 압축 기능\n\n4. **Windows 호환**: NTFS, exFAT\n   - USB: exFAT (4GB 제한 없음)\n\n5. **SSD**: ext4(discard), F2FS\n   - TRIM 지원 중요\n\n**성능 튜닝 옵션**\n\n- `noatime`: 읽기 시 시간 기록 안 함\n- `nodiratime`: 디렉토리 접근 시간 안 기록\n- `discard`: SSD TRIM 활성화\n- `data=writeback`: 메타데이터만 저널링 (성능 우선)\n\n**면접 빈출 질문**\n\nQ1. 저널링이란?\nA: 변경 전 로그를 먼저 기록하여 비정상 종료 시 복구 가능하게 하는 기술\n\nQ2. inode가 부족하면 어떻게 되나요?\nA: 디스크 공간이 있어도 새 파일 생성 불가. 작은 파일이 많으면 발생.\n\nQ3. ext4와 XFS의 차이?\nA: ext4는 범용, XFS는 대용량 파일과 병렬 I/O에 강함\n\nQ4. soft link vs hard link?\nA: soft link는 경로를 가리킴(원본 삭제시 깨짐), hard link는 같은 inode 공유\n\n**트러블슈팅 체크리스트**\n\n[ ] df와 du 결과 불일치 -> 삭제된 파일의 열린 핸들\n[ ] No space left but df shows free -> inode 부족\n[ ] Read-only filesystem -> fsck 필요, 하드웨어 확인"
                }
            ]
        },

        # 08_파일시스템/inode - 아이노드
        "08_파일시스템/inode": {
            "id": "08_파일시스템/inode",
            "title": "아이노드 (Inode)",
            "category": "os",
            "subCategory": "08_파일시스템",
            "language": "Bash",
            "description": "파일 메타데이터를 저장하는 inode의 구조와 역할을 학습합니다.",
            "isPlaceholder": False,
            "sections": [
                {
                    "type": "concept",
                    "title": "Inode의 이해",
                    "content": "Inode(Index Node)는 파일의 메타데이터를 저장하는 자료구조입니다.\n\n**도서관 목록 카드 비유**\n\n도서관에서 책을 찾을 때:\n1. 목록 카드(inode)에서 책 정보 확인\n   - 제목, 저자, 출판년도 (메타데이터)\n   - 서가 위치 (데이터 블록 주소)\n2. 서가로 가서 실제 책(데이터)을 가져옴\n\n파일 시스템에서:\n- 파일명은 디렉토리에 저장\n- 파일 속성과 위치는 inode에 저장\n- 실제 데이터는 데이터 블록에 저장\n\n**Inode에 저장되는 정보**\n\n| 필드 | 설명 |\n|------|------|\n| 파일 타입 | 일반, 디렉토리, 심볼릭링크 등 |\n| 권한 | rwxr-xr-x |\n| 소유자/그룹 | UID, GID |\n| 파일 크기 | bytes |\n| 시간 정보 | atime, mtime, ctime |\n| 링크 수 | hard link 개수 |\n| 블록 포인터 | 데이터 블록 주소 |\n\n**주의: inode에 없는 것**\n- 파일 이름 (디렉토리에 저장)\n- 파일 내용 (데이터 블록에 저장)\n\n**왜 파일명이 inode에 없을까?**\n하나의 파일에 여러 이름(hard link)을 가질 수 있기 때문"
                },
                {
                    "type": "code",
                    "title": "Inode 구조 및 블록 포인터",
                    "language": "text",
                    "code": "=== Inode 구조 (ext4 기준) ===\n\n+----------------------------------+\n|           Inode (256 bytes)      |\n+----------------------------------+\n| File Type & Permissions (2)      |  # 파일 타입 + 권한\n| Owner UID (2)                    |  # 소유자 ID\n| File Size (lower 32 bits) (4)    |  # 파일 크기 (하위)\n| Access Time (4)                  |  # 최근 접근 시간\n| Change Time (4)                  |  # inode 변경 시간\n| Modification Time (4)            |  # 내용 수정 시간\n| Deletion Time (4)                |  # 삭제 시간\n| Group GID (2)                    |  # 그룹 ID\n| Links Count (2)                  |  # 하드링크 수\n| Blocks Count (4)                 |  # 할당된 블록 수\n| Flags (4)                        |  # 플래그\n| ... OS specific ...              |\n+----------------------------------+\n|       Block Pointers (60)        |  # 데이터 블록 포인터\n+----------------------------------+\n| Generation Number (4)            |  # NFS용\n| Extended Attributes (4)          |  # 확장 속성\n| File Size (upper 32 bits) (4)    |  # 파일 크기 (상위)\n+----------------------------------+\n\n\n=== 블록 포인터 구조 (전통적 ext2/3 방식) ===\n\n                    Inode\n                +----------+\nDirect Blocks   | Block 0  |---------> [Data Block]\n(12개)          | Block 1  |---------> [Data Block]\n                |   ...    |\n                | Block 11 |---------> [Data Block]\n                +----------+\nSingle Indirect | Indirect |----+\n(1개)           +----------+    |\n                                v\n                        +---------------+\n                        | Ptr | Ptr |...|---> [Data Blocks]\n                        +---------------+\n                        (1024개 포인터)\n\nDouble Indirect +----------+\n(1개)           | 2x Indir |----+\n                +----------+    |\n                                v\n                        +---------------+\n                        | Ptr | Ptr |...|---> [Single Indirect]\n                        +---------------+         |\n                                                  v\n                                          [Data Blocks]\n\nTriple Indirect +----------+\n(1개)           | 3x Indir |---> [Double Indirect]---> ...\n                +----------+\n\n\n=== 최대 파일 크기 계산 (4KB 블록 기준) ===\n\nDirect Blocks:       12 * 4KB = 48KB\nSingle Indirect:     1024 * 4KB = 4MB  \nDouble Indirect:     1024 * 1024 * 4KB = 4GB\nTriple Indirect:     1024^3 * 4KB = 4TB\n\n총 최대 파일 크기 ≈ 4TB (실제로는 다른 제한 있음)\n\n\n=== ext4 Extent 방식 (현대적) ===\n\n전통적 블록 포인터: 블록마다 포인터 필요 (비효율적)\next4 Extent: 연속 블록을 하나의 extent로 표현\n\n+----------------------------------+\n|        Extent Header             |\n+----------------------------------+\n| Start Block | Length | Phys Addr |\n+----------------------------------+\n|    1000     |  100   | 50000     |  # 블록 1000~1099 -> 50000~50099\n+----------------------------------+\n\n장점: 대용량 파일에서 메타데이터 크게 감소"
                },
                {
                    "type": "code",
                    "title": "Inode 실무 명령어",
                    "language": "bash",
                    "code": "# === Inode 정보 확인 ===\n\n# 파일의 inode 번호 확인\nls -i filename.txt\n# 12345678 filename.txt\n\n# 상세 정보 함께 보기\nls -li\n# 12345678 -rw-r--r-- 1 user group 1024 Jan 30 10:00 file.txt\n# inode    권한       링크수 소유자 그룹 크기 시간       파일명\n\n# stat으로 상세 정보\nstat filename.txt\n#   File: filename.txt\n#   Size: 1024            Blocks: 8          IO Block: 4096   regular file\n# Device: 801h/2049d      Inode: 12345678    Links: 1\n# Access: (0644/-rw-r--r--)  Uid: ( 1000/  user)   Gid: ( 1000/  group)\n# Access: 2024-01-30 10:00:00.000000000 +0900\n# Modify: 2024-01-30 09:00:00.000000000 +0900\n# Change: 2024-01-30 09:00:00.000000000 +0900\n#  Birth: 2024-01-29 08:00:00.000000000 +0900\n\n# === Inode 사용량 확인 ===\n\n# 파일 시스템별 inode 사용량\ndf -i\n# Filesystem      Inodes   IUsed   IFree IUse% Mounted on\n# /dev/sda1      6553600  250000 6303600    4% /\n\n# 특정 디렉토리의 inode 수\nfind /var -xdev | wc -l\n\n# inode를 많이 사용하는 디렉토리 찾기\nfor d in /*; do echo \"$d: $(find $d -xdev 2>/dev/null | wc -l)\"; done | sort -t: -k2 -rn | head\n\n# === Hard Link와 Soft Link ===\n\n# Hard Link 생성 (같은 inode 공유)\nln original.txt hardlink.txt\nls -li original.txt hardlink.txt\n# 12345678 -rw-r--r-- 2 user group 1024 ... original.txt\n# 12345678 -rw-r--r-- 2 user group 1024 ... hardlink.txt\n#                   ^ 링크 수 2\n\n# Soft Link 생성 (새로운 inode, 경로 저장)\nln -s original.txt softlink.txt\nls -li original.txt softlink.txt\n# 12345678 -rw-r--r-- 1 user group 1024 ... original.txt\n# 87654321 lrwxrwxrwx 1 user group   12 ... softlink.txt -> original.txt\n\n# Hard Link vs Soft Link 동작 차이\necho \"Hello\" > original.txt\nln original.txt hard.txt\nln -s original.txt soft.txt\n\nrm original.txt\n\ncat hard.txt   # Hello (데이터 유지)\ncat soft.txt   # Error: No such file (깨진 링크)\n\n# === Inode 관련 문제 해결 ===\n\n# 문제: \"No space left on device\" but df shows free space\n# 원인: inode 부족\n\n# 진단\ndf -i /\ndf -h /\n\n# 해결: 작은 파일이 많은 디렉토리 정리\nfind /tmp -type f -mtime +30 -delete\n\n# 특정 inode 번호로 파일 찾기\nfind / -inum 12345678 2>/dev/null\n\n# 삭제된 파일이지만 프로세스가 잡고 있는 경우\nlsof +L1  # 링크 수가 0인 열린 파일\n# 해당 프로세스 재시작하면 공간 확보\n\n# === 디버깅 도구 ===\n\n# debugfs로 inode 직접 확인 (읽기 전용)\nsudo debugfs -R 'stat <12345678>' /dev/sda1\n\n# 디렉토리 내용 확인\nsudo debugfs -R 'ls -l /home/user' /dev/sda1\n\n# 삭제된 inode 목록 (복구 시)\nsudo debugfs -R 'lsdel' /dev/sda1"
                },
                {
                    "type": "tip",
                    "title": "Inode 관련 면접 질문 및 실무 팁",
                    "content": "**면접 빈출 질문**\n\nQ1. inode란 무엇인가요?\nA: 파일의 메타데이터(권한, 소유자, 크기, 블록 위치 등)를 저장하는 자료구조. 파일명은 포함하지 않음.\n\nQ2. Hard Link와 Soft Link의 차이?\nA: \n- Hard Link: 같은 inode를 가리킴, 원본 삭제해도 데이터 유지\n- Soft Link: 새 inode, 경로만 저장, 원본 삭제시 깨짐\n- Hard Link는 파티션 경계 불가, Soft Link는 가능\n\nQ3. inode가 부족하면 어떻게 되나요?\nA: 디스크 공간이 있어도 새 파일 생성 불가. 작은 파일이 매우 많을 때 발생. df -i로 확인.\n\nQ4. 왜 파일명이 inode에 없나요?\nA: 하나의 파일에 여러 이름(hard link)을 가질 수 있기 때문. 파일명은 디렉토리 엔트리에 저장.\n\n**시간 정보 구분**\n\n- atime: 마지막 접근 시간 (read)\n- mtime: 마지막 수정 시간 (write)\n- ctime: inode 변경 시간 (권한, 소유자 변경)\n\n```\ncat file.txt      # atime 변경\necho >> file.txt  # mtime 변경\nchmod 755 file.txt # ctime 변경\n```\n\n**실무 팁**\n\n1. **성능 튜닝**: noatime 마운트로 불필요한 inode 업데이트 방지\n\n2. **inode 고갈 예방**: \n   - 임시 파일 정기 정리\n   - 세션 파일을 파티션 분리\n\n3. **백업 시 주의**: \n   - Hard Link 보존 옵션 사용\n   - rsync -H (hard links 보존)\n\n4. **파일 복구**: \n   - 삭제 직후 debugfs로 inode 확인 가능\n   - 데이터 덮어쓰기 전 복구 가능성 있음"
                }
            ]
        },

        # 08_파일시스템/linux-command - 리눅스 필수 명령어
        "08_파일시스템/linux-command": {
            "id": "08_파일시스템/linux-command",
            "title": "리눅스 필수 명령어",
            "category": "os",
            "subCategory": "08_파일시스템",
            "language": "Bash",
            "description": "ls, cd, chmod, grep, ps, top 등 개발자 필수 리눅스 명령어를 학습합니다.",
            "isPlaceholder": False,
            "sections": [
                {
                    "type": "concept",
                    "title": "리눅스 명령어 기초",
                    "content": "리눅스 명령어는 개발자의 필수 도구입니다.\n\n**서랍장 비유로 이해하기**\n\n리눅스 파일 시스템을 서랍장에 비유하면:\n\n- **cd** (Change Directory): 서랍장 칸 이동\n- **ls** (List): 현재 칸의 내용물 보기\n- **pwd** (Print Working Directory): 현재 위치 확인\n- **mkdir/rmdir**: 새 칸 만들기/제거하기\n- **cp/mv/rm**: 물건 복사/이동/버리기\n\n**명령어 구조**\n\n```\ncommand [options] [arguments]\n명령어   [옵션]    [인자]\n\n예: ls -la /home\n    |  |   |\n    |  |   +-- 인자: 대상 디렉토리\n    |  +------ 옵션: long format, all files\n    +--------- 명령어: list\n```\n\n**자주 쓰는 옵션 패턴**\n\n- `-h`: human readable (사람이 읽기 쉽게)\n- `-r`: recursive (하위 디렉토리 포함)\n- `-f`: force (강제 실행)\n- `-v`: verbose (상세 출력)\n- `-i`: interactive (확인 후 실행)\n\n**핵심 명령어 분류**\n\n| 분류 | 명령어 |\n|------|--------|\n| 파일 | ls, cp, mv, rm, cat, find, grep |\n| 프로세스 | ps, top, kill, bg, fg |\n| 권한 | chmod, chown, chgrp |\n| 시스템 | df, du, free, uname |\n| 네트워크 | curl, wget, ss, netstat |"
                },
                {
                    "type": "code",
                    "title": "파일/디렉토리 명령어",
                    "language": "bash",
                    "code": "# =============================================\n# 파일 및 디렉토리 기본 명령어\n# =============================================\n\n# === ls (List) ===\nls                    # 현재 디렉토리 목록\nls -l                 # 상세 정보 (권한, 소유자, 크기, 시간)\nls -la                # 숨김 파일 포함 (.으로 시작하는 파일)\nls -lh                # 파일 크기를 KB/MB로 표시\nls -lt                # 시간순 정렬 (최신 먼저)\nls -lS                # 크기순 정렬 (큰 것 먼저)\nls -lR                # 하위 디렉토리까지 재귀적 출력\n\n# === cd (Change Directory) ===\ncd /home/user         # 절대 경로로 이동\ncd ..                 # 상위 디렉토리\ncd ~                  # 홈 디렉토리\ncd -                  # 이전 디렉토리로 돌아가기\ncd                    # 홈 디렉토리 (cd ~ 와 동일)\n\n# === 파일 조작 ===\ncp source dest        # 파일 복사\ncp -r dir1 dir2       # 디렉토리 복사 (recursive)\ncp -p file1 file2     # 권한, 시간 정보 유지\n\nmv old new            # 이름 변경/이동\nmv file.txt /tmp/     # 파일 이동\n\nrm file.txt           # 파일 삭제\nrm -r directory       # 디렉토리 삭제\nrm -rf directory      # 강제 삭제 (주의!)\nrm -i file.txt        # 확인 후 삭제\n\n# === 파일 내용 보기 ===\ncat file.txt          # 전체 출력\nhead -20 file.txt     # 처음 20줄\ntail -20 file.txt     # 마지막 20줄\ntail -f log.txt       # 실시간 로그 모니터링\nless file.txt         # 페이지 단위로 보기 (q: 종료)\n\n# === 파일 검색 ===\nfind /home -name \"*.txt\"              # 이름으로 검색\nfind /var -size +100M                 # 100MB 이상 파일\nfind . -mtime -7                      # 7일 내 수정된 파일\nfind . -type f -name \"*.log\" -delete  # 찾아서 삭제\n\n# === grep (텍스트 검색) ===\ngrep \"error\" log.txt           # 패턴 검색\ngrep -i \"error\" log.txt        # 대소문자 무시\ngrep -r \"TODO\" ./src           # 디렉토리 재귀 검색\ngrep -n \"function\" script.js   # 줄 번호 표시\ngrep -v \"debug\" log.txt        # 패턴 제외\ngrep -E \"error|warn\" log.txt   # 정규식 (OR)\n\n# 실용적인 조합\ngrep -rn \"TODO\" --include=\"*.py\"  # Python 파일에서 TODO 검색\n\n# === chmod (권한 변경) ===\n# 숫자 방식: r=4, w=2, x=1\nchmod 755 script.sh   # rwxr-xr-x (소유자 full, 그룹/기타 읽기+실행)\nchmod 644 file.txt    # rw-r--r-- (소유자 읽기쓰기, 나머지 읽기)\nchmod 600 secret.key  # rw------- (소유자만)\n\n# 심볼릭 방식\nchmod +x script.sh    # 실행 권한 추가\nchmod u+w file.txt    # 소유자에게 쓰기 권한\nchmod go-w file.txt   # 그룹/기타 쓰기 권한 제거\nchmod -R 755 dir/     # 디렉토리 재귀 적용\n\n# === chown (소유자 변경) ===\nchown user file.txt           # 소유자 변경\nchown user:group file.txt     # 소유자와 그룹 변경\nchown -R user:group dir/      # 재귀적 변경"
                },
                {
                    "type": "code",
                    "title": "프로세스/시스템 명령어",
                    "language": "bash",
                    "code": "# =============================================\n# 프로세스 관리 명령어\n# =============================================\n\n# === ps (Process Status) ===\nps                    # 현재 터미널의 프로세스\nps aux                # 모든 프로세스 상세 정보\n# USER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND\n\nps -ef                # 모든 프로세스 (다른 형식)\nps aux | grep nginx   # 특정 프로세스 찾기\nps -u username        # 특정 사용자 프로세스\n\n# === top (실시간 모니터링) ===\ntop                   # 실시간 프로세스 모니터링\n# 대화형 명령:\n#   q: 종료\n#   M: 메모리 순 정렬\n#   P: CPU 순 정렬\n#   k: 프로세스 kill\n#   1: CPU 코어별 표시\n\nhtop                  # top의 개선판 (설치 필요)\n\n# === kill (프로세스 종료) ===\nkill PID              # SIGTERM (정상 종료 요청)\nkill -9 PID           # SIGKILL (강제 종료)\nkill -15 PID          # SIGTERM (기본값)\nkillall nginx         # 이름으로 모든 프로세스 종료\npkill -f \"python app\" # 패턴 매칭으로 종료\n\n# === 백그라운드 실행 ===\ncommand &             # 백그라운드 실행\nnohup command &       # 터미널 종료해도 계속 실행\nnohup python app.py > output.log 2>&1 &\n\nCtrl+Z                # 현재 프로세스 일시 정지\nbg                    # 백그라운드로 보내기\nfg                    # 포그라운드로 가져오기\njobs                  # 백그라운드 작업 목록\n\n# =============================================\n# 시스템 정보 명령어\n# =============================================\n\n# === 디스크 사용량 ===\ndf -h                 # 파일시스템 사용량\ndf -i                 # inode 사용량\ndu -sh /var/*         # 디렉토리별 크기\ndu -sh * | sort -h    # 크기순 정렬\nncdu                  # 시각적 디스크 분석 (설치 필요)\n\n# === 메모리 ===\nfree -h               # 메모리 사용량\n# total: 전체, used: 사용중, free: 미사용, \n# buff/cache: 버퍼/캐시, available: 실제 사용 가능\n\n# === 시스템 정보 ===\nuname -a              # 커널 정보\nlsb_release -a        # 배포판 정보\nhostname              # 호스트명\nuptime                # 가동 시간, 로드 평균\nwho                   # 로그인한 사용자\n\n# === 네트워크 ===\nip addr               # IP 주소 확인\nip route              # 라우팅 테이블\nss -tuln              # 열린 포트 확인 (netstat 대체)\nss -tulnp             # 프로세스 정보 포함\n\ncurl -I https://example.com   # HTTP 헤더만\ncurl -o file.zip URL          # 파일 다운로드\nwget URL                      # 파일 다운로드\n\n# === 로그 확인 ===\njournalctl -f                 # 시스템 로그 실시간\njournalctl -u nginx           # 특정 서비스 로그\ndmesg | tail                  # 커널 메시지\n\n# === 서비스 관리 (systemd) ===\nsystemctl status nginx        # 서비스 상태\nsystemctl start nginx         # 서비스 시작\nsystemctl stop nginx          # 서비스 중지\nsystemctl restart nginx       # 재시작\nsystemctl enable nginx        # 부팅시 자동 시작\nsystemctl disable nginx       # 자동 시작 해제\nsystemctl list-units --type=service  # 모든 서비스"
                },
                {
                    "type": "tip",
                    "title": "명령어 치트시트 및 실무 조합",
                    "content": "**자주 쓰는 명령어 조합**\n\n```bash\n# 로그에서 에러 찾고 개수 세기\ngrep -c \"ERROR\" app.log\n\n# 최근 수정된 파일 10개\nfind . -type f -mmin -60 | head -10\n\n# 큰 파일 찾기\nfind / -type f -size +100M 2>/dev/null\n\n# 특정 포트 사용 프로세스\nlsof -i :8080\nss -tulnp | grep 8080\n\n# 디스크 사용량 상위 10개\ndu -ah / 2>/dev/null | sort -rh | head -10\n\n# 특정 프로세스 CPU/메모리\nps aux | grep nginx | grep -v grep\n\n# 로그 실시간 + 필터\ntail -f /var/log/app.log | grep --line-buffered \"ERROR\"\n```\n\n**단축키 & 팁**\n\n- `Ctrl+R`: 명령어 히스토리 검색\n- `!!`: 이전 명령어 반복\n- `!$`: 이전 명령의 마지막 인자\n- `Ctrl+A/E`: 줄 처음/끝으로 이동\n- `Tab`: 자동 완성\n\n**권한 숫자 외우기**\n```\n7 = rwx (4+2+1)\n6 = rw- (4+2)\n5 = r-x (4+1)\n4 = r--\n0 = ---\n\n755 = rwxr-xr-x (실행 파일)\n644 = rw-r--r-- (일반 파일)\n600 = rw------- (비밀 파일)\n```\n\n**면접 빈출 질문**\n\nQ1. 프로세스가 사용 중인 포트 확인 방법?\nA: `ss -tulnp` 또는 `lsof -i :포트번호`\n\nQ2. 좀비 프로세스란? 확인 방법?\nA: 종료되었지만 부모가 wait() 안 한 상태. `ps aux | grep Z`\n\nQ3. 디스크 풀인데 du로 확인 안 될 때?\nA: 삭제된 파일을 프로세스가 잡고 있음. `lsof +L1`로 확인\n\n**자주 실수하는 것**\n\n- `rm -rf /` 주의! (공백 실수로 `rm -rf / home` 가능)\n- `chmod 777`은 보안상 피하기\n- `kill -9`는 정상 종료 실패 후에만\n- 백그라운드 실행 시 nohup 잊지 말기"
                }
            ]
        },

        # index - OS 학습 로드맵
        "index": {
            "id": "index",
            "title": "운영체제 학습 로드맵",
            "category": "os",
            "subCategory": None,
            "language": "Text",
            "description": "운영체제의 핵심 개념을 체계적으로 학습하기 위한 가이드입니다.",
            "isPlaceholder": False,
            "sections": [
                {
                    "type": "concept",
                    "title": "운영체제 학습 가이드",
                    "content": "운영체제(OS)는 하드웨어와 소프트웨어 사이의 인터페이스입니다.\n\n**왜 OS를 배워야 할까요?**\n\n1. **면접 필수**: CS 기술 면접의 핵심 영역\n2. **성능 최적화**: 병목 현상의 원인 파악\n3. **시스템 설계**: 효율적인 아키텍처 구현\n4. **트러블슈팅**: 서버 장애 해결 능력\n\n**학습 로드맵 개요**\n\n```\n[1단계: 기초]           [2단계: 핵심]           [3단계: 심화]\n     |                       |                       |\n  OS 개념  ───────>  프로세스/스레드  ───────>  파일시스템\n  커널      ───────>  동기화/데드락   ───────>  I/O 모델\n  시스템 콜 ───────>  메모리 관리     ───────>  면접 준비\n                      스케줄링\n```\n\n**추천 학습 시간**\n- 1단계: 1-2일 (개념 이해)\n- 2단계: 1-2주 (핵심 내용)\n- 3단계: 1주 (심화 + 면접)\n\n**병행 추천 학습**\n- 리눅스 명령어 실습\n- C/시스템 프로그래밍\n- 컴퓨터 구조 기초"
                },
                {
                    "type": "code",
                    "title": "섹션별 학습 내용 요약",
                    "language": "text",
                    "code": "=== 운영체제 전체 커리큘럼 ===\n\n[01_기초] - 운영체제의 기본 개념\n+--------------------------------------------------+\n| os-intro     | OS란 무엇인가, 역할과 목적        |\n| os-structure | 모놀리식, 마이크로커널, 하이브리드 |\n| kernel       | 커널의 역할과 종류                |\n| system-call  | 사용자모드 <-> 커널모드 전환      |\n+--------------------------------------------------+\n> 실무 연관: 컨테이너(Docker)의 커널 공유 이해\n\n\n[02_프로세스스레드] - 실행의 단위\n+--------------------------------------------------+\n| process-concept   | 프로세스 정의와 생명주기     |\n| process-vs-thread | 프로세스 vs 스레드 비교      |\n| thread-concept    | 스레드의 구조와 장단점       |\n| context-switching | 컨텍스트 스위칭 오버헤드     |\n+--------------------------------------------------+\n> 실무 연관: 웹서버 아키텍처(Apache vs Nginx)\n> 면접 빈도: ★★★★★ (가장 자주 출제)\n\n\n[03_동기화] - 공유 자원 관리\n+--------------------------------------------------+\n| race-condition | 경쟁 상태와 임계 영역           |\n| mutex          | 상호배제, 락의 개념             |\n| semaphore      | 세마포어, P/V 연산              |\n| monitor        | 모니터, 조건 변수               |\n| deadlock       | 데드락 조건과 해결 방법         |\n+--------------------------------------------------+\n> 실무 연관: DB 트랜잭션, 분산 시스템 동기화\n> 면접 빈도: ★★★★★\n\n\n[04_스케줄링] - CPU 시간 분배\n+--------------------------------------------------+\n| scheduling-intro    | 스케줄링 기준과 목표       |\n| cpu-scheduling      | 선점형 vs 비선점형         |\n| scheduling-algorithm| FCFS, SJF, RR, Priority   |\n| preemptive          | 선점 스케줄링 상세         |\n+--------------------------------------------------+\n> 실무 연관: 쿠버네티스 리소스 스케줄링\n> 면접 빈도: ★★★☆☆\n\n\n[06_메모리] - 메모리 관리\n+--------------------------------------------------+\n| memory-structure  | 메모리 계층 구조            |\n| memory-allocation | 연속/불연속 할당            |\n| paging            | 페이징, 페이지 테이블       |\n| segmentation      | 세그멘테이션               |\n| virtual-memory    | 가상 메모리, Demand Paging  |\n| page-replacement  | LRU, FIFO, OPT 알고리즘    |\n| page-fault        | 페이지 폴트, 스래싱        |\n| fragmentation     | 내부/외부 단편화           |\n| cache             | 캐시 메모리, 지역성        |\n+--------------------------------------------------+\n> 실무 연관: GC 동작 이해, 메모리 릭 디버깅\n> 면접 빈도: ★★★★☆\n\n\n[07_동기비동기] - I/O 처리 방식\n+--------------------------------------------------+\n| sync-async           | 동기 vs 비동기           |\n| blocking-nonblocking | 블로킹 vs 논블로킹       |\n| sync-blocking-matrix | 4가지 조합 분석          |\n| io-model             | I/O 멀티플렉싱, Async IO |\n+--------------------------------------------------+\n> 실무 연관: Node.js, Nginx, Redis 아키텍처\n> 면접 빈도: ★★★★☆ (백엔드 필수)\n\n\n[08_파일시스템] - 저장소 관리\n+--------------------------------------------------+\n| file-system    | FAT, NTFS, ext4 비교          |\n| inode          | 아이노드, 메타데이터          |\n| linux-command  | 리눅스 필수 명령어            |\n+--------------------------------------------------+\n> 실무 연관: 서버 운영, 로그 분석, 트러블슈팅\n> 면접 빈도: ★★★☆☆\n\n\n[07_면접] - 면접 대비 총정리\n+--------------------------------------------------+\n| interview-os | 주니어 15문항 + 시니어 10문항  |\n+--------------------------------------------------+"
                },
                {
                    "type": "code",
                    "title": "추천 학습 순서",
                    "language": "text",
                    "code": "=== 레벨별 추천 학습 순서 ===\n\n[주니어 개발자 / 취업 준비생]\n\n1일차: 기초 개념\n├── os-intro (30분)\n├── os-structure (30분)\n└── system-call (30분)\n\n2-3일차: 프로세스와 스레드 ⭐중요\n├── process-concept (1시간)\n├── thread-concept (1시간)\n├── process-vs-thread (1시간) ← 면접 필수!\n└── context-switching (30분)\n\n4-5일차: 동기화 ⭐중요\n├── race-condition (30분)\n├── mutex (1시간)\n├── semaphore (1시간)\n└── deadlock (1시간) ← 면접 필수!\n\n6-7일차: 메모리 관리\n├── memory-structure (30분)\n├── paging (1시간)\n├── virtual-memory (1시간)\n└── page-replacement (1시간)\n\n8일차: I/O 모델 ⭐백엔드 필수\n├── sync-async (30분)\n├── blocking-nonblocking (30분)\n└── io-model (1시간)\n\n9-10일차: 면접 준비\n├── interview-os (2시간)\n└── 복습 및 모의 면접\n\n\n[시니어 / 심화 학습]\n\n추가 학습 추천:\n├── NUMA 아키텍처\n├── 커널 내부 구조 (리눅스 커널 소스)\n├── io_uring 최신 I/O 모델\n├── eBPF 시스템 프로그래밍\n└── 컨테이너 기술 (namespace, cgroups)\n\n\n=== 학습 팁 ===\n\n1. 실습 병행하기\n   - 리눅스 가상머신 설치\n   - 명령어 직접 타이핑\n   - 시스템 프로그래밍 실습\n\n2. 면접 질문으로 점검\n   - 각 섹션 끝의 면접 질문 확인\n   - 답을 보지 않고 설명해보기\n   - 꼬리 질문 대비\n\n3. 그림으로 이해하기\n   - 프로세스 메모리 구조 그리기\n   - 데드락 상황 시각화\n   - 페이지 테이블 손으로 계산\n\n4. 실무와 연결하기\n   - Redis가 싱글스레드인 이유?\n   - Nginx가 Apache보다 빠른 이유?\n   - Docker의 격리 원리?"
                },
                {
                    "type": "tip",
                    "title": "실무 연관성 및 학습 리소스",
                    "content": "**실무에서 OS 지식이 필요한 순간**\n\n1. **서버 장애 대응**\n   - CPU 100% -> 프로세스 분석, 스케줄링 이해\n   - 메모리 부족 -> 가상 메모리, OOM 이해\n   - 디스크 풀 -> 파일 시스템, inode 이해\n\n2. **성능 최적화**\n   - 응답 지연 -> I/O 모델, 비동기 처리\n   - 동시성 이슈 -> 동기화, 락 전략\n   - GC 튜닝 -> 메모리 구조 이해\n\n3. **시스템 설계**\n   - 멀티프로세스 vs 멀티스레드 선택\n   - 이벤트 기반 vs 스레드풀 아키텍처\n   - 캐시 전략, 버퍼 관리\n\n4. **기술 면접**\n   - CS 기초 질문의 핵심 영역\n   - 경력에 상관없이 자주 출제\n   - 깊이 있는 답변으로 차별화\n\n**추천 학습 리소스**\n\n- 책: \"Operating System Concepts\" (공룡책)\n- 책: \"리눅스 커널의 이해\"\n- 강의: KOCW 운영체제 (반효경 교수)\n- 실습: Linux From Scratch\n\n**체크리스트: 학습 완료 기준**\n\n[ ] 프로세스와 스레드의 차이를 그림으로 설명 가능\n[ ] 데드락 4가지 조건을 암기하고 해결법 설명 가능\n[ ] 가상 메모리 동작 원리 설명 가능\n[ ] 동기/비동기, 블로킹/논블로킹 조합 설명 가능\n[ ] 주요 리눅스 명령어 실무 활용 가능\n[ ] 면접 빈출 질문 20개에 답변 가능\n\n**OS 학습이 도움이 되는 기술들**\n\n- Docker/Kubernetes: 커널, namespace, cgroups\n- Redis: 싱글스레드, 이벤트루프, I/O 멀티플렉싱\n- Nginx: 비동기 이벤트 기반 아키텍처\n- Node.js: 이벤트 루프, libuv\n- JVM: 메모리 관리, GC 알고리즘"
                }
            ]
        }
    }

def update_os_json():
    """Update os.json with new content."""
    json_path = r"c:\tools\codemaster-next-main\codemaster-next-main\codemaster-next-main\src\data\contents\os.json"

    # Read existing file
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Get new content
    new_content = get_new_content()

    # Update with new content
    for key, value in new_content.items():
        data[key] = value
        print(f"Updated: {key}")

    # Write back to file
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nSuccessfully updated {len(new_content)} topics in os.json")
    print("\nUpdated topics:")
    for key in new_content.keys():
        print(f"  - {key}")

if __name__ == "__main__":
    update_os_json()
