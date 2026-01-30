# -*- coding: utf-8 -*-
"""
OS Content Generator - Part 1
Updates os.json with high-quality Korean content for 11 topics
"""

import json

# File path
OS_JSON_PATH = r"c:\tools\codemaster-next-main\codemaster-next-main\codemaster-next-main\src\data\contents\os.json"

def get_os_intro_content():
    """01_기초/os-intro - 운영체제란?"""
    return {
        "id": "01_기초/os-intro",
        "title": "운영체제란?",
        "category": "os",
        "subCategory": "01_기초",
        "language": "C",
        "description": "운영체제의 개념과 역할을 이해합니다.",
        "isPlaceholder": False,
        "sections": [
            {
                "type": "concept",
                "title": "🎯 운영체제 완전 정복",
                "content": "**한 줄 요약**: 운영체제(OS)는 하드웨어와 소프트웨어 사이에서 자원을 관리하고 사용자에게 편리한 환경을 제공하는 시스템 소프트웨어입니다.\n\n**초등학생도 이해할 비유 - 레스토랑 총괄 매니저**\n\n레스토랑을 상상해보세요:\n- 주방(CPU) - 요리를 만드는 곳\n- 냉장고(메모리) - 재료를 보관하는 곳\n- 손님(사용자 프로그램) - 음식을 주문하는 사람\n- 웨이터(입출력 장치) - 주문을 전달하고 음식을 가져다주는 역할\n\n**총괄 매니저(운영체제)의 역할:**\n1. 주방 시간 배분 - 어떤 요리를 먼저 만들지 결정\n2. 재료 관리 - 냉장고 공간을 효율적으로 사용\n3. 웨이터 조율 - 누가 어느 테이블을 담당할지 배정\n4. 손님 관리 - 대기 순서, 예약 관리\n\n**왜 알아야 하는가?**\n- 프로그램이 어떻게 실행되는지 이해\n- 성능 최적화의 기본 원리 파악\n- 시스템 레벨 문제 해결 능력 향상\n- 면접 단골 질문 (프로세스, 메모리, 스케줄링)"
            },
            {
                "type": "code",
                "title": "💻 동작 원리",
                "language": "text",
                "code": "┌─────────────────────────────────────────────────┐\n│                  사용자 영역                      │\n│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │\n│  │  Chrome  │  │   Word   │  │  게임    │       │\n│  └──────────┘  └──────────┘  └──────────┘       │\n├─────────────────────────────────────────────────┤\n│                 시스템 콜 인터페이스              │\n├─────────────────────────────────────────────────┤\n│              운영체제 (커널)                     │\n│  ┌─────────┐ ┌─────────┐ ┌─────────┐           │\n│  │프로세스 │ │ 메모리  │ │파일시스템│           │\n│  │  관리   │ │  관리   │ │  관리   │           │\n│  └─────────┘ └─────────┘ └─────────┘           │\n├─────────────────────────────────────────────────┤\n│                하드웨어                          │\n│    CPU      메모리      디스크      네트워크     │\n└─────────────────────────────────────────────────┘\n\n운영체제의 핵심 기능:\n1. 프로세스 관리: CPU 시간 분배, 프로세스 생성/종료\n2. 메모리 관리: RAM 할당/해제, 가상 메모리\n3. 파일 시스템: 파일 저장, 디렉토리 관리\n4. I/O 관리: 키보드, 마우스, 디스크 제어\n5. 보안: 사용자 인증, 접근 권한 관리"
            },
            {
                "type": "code",
                "title": "🔧 실무 활용",
                "language": "java",
                "code": "// Java에서 OS 정보 확인하기\npublic class OSInfo {\n    public static void main(String[] args) {\n        // 운영체제 정보\n        System.out.println(\"OS: \" + System.getProperty(\"os.name\"));\n        System.out.println(\"Version: \" + System.getProperty(\"os.version\"));\n        System.out.println(\"Architecture: \" + System.getProperty(\"os.arch\"));\n        \n        // 런타임 정보 (JVM이 OS로부터 할당받은 자원)\n        Runtime runtime = Runtime.getRuntime();\n        System.out.println(\"Available Processors: \" + runtime.availableProcessors());\n        System.out.println(\"Max Memory: \" + runtime.maxMemory() / 1024 / 1024 + \"MB\");\n        System.out.println(\"Total Memory: \" + runtime.totalMemory() / 1024 / 1024 + \"MB\");\n        System.out.println(\"Free Memory: \" + runtime.freeMemory() / 1024 / 1024 + \"MB\");\n    }\n}\n\n// Spring Boot에서 OS 레벨 모니터링\n@Component\npublic class SystemMonitor {\n    \n    private final OperatingSystemMXBean osBean = \n        ManagementFactory.getOperatingSystemMXBean();\n    \n    @Scheduled(fixedRate = 60000) // 1분마다 체크\n    public void monitorSystem() {\n        double cpuLoad = osBean.getSystemLoadAverage();\n        if (cpuLoad > 0.8) {\n            log.warn(\"High CPU usage: {}%\", cpuLoad * 100);\n            // 알림 발송 또는 스케일 아웃 트리거\n        }\n    }\n}"
            },
            {
                "type": "tip",
                "title": "💡 체크리스트 & 면접",
                "content": "**핵심 개념 정리표**\n| 구분 | 내용 |\n|------|------|\n| 정의 | 하드웨어를 관리하고 응용 프로그램에 서비스를 제공하는 시스템 소프트웨어 |\n| 핵심 역할 | 자원 관리, 사용자 인터페이스 제공 |\n| 주요 기능 | 프로세스/메모리/파일/I-O 관리 |\n| 대표 예시 | Windows, Linux, macOS, Android, iOS |\n\n**면접 질문**\n\n[주니어]\nQ: 운영체제의 역할은 무엇인가요?\nA: 하드웨어 자원(CPU, 메모리, 디스크)을 효율적으로 관리하고, 응용 프로그램이 하드웨어를 쉽게 사용할 수 있도록 추상화된 인터페이스를 제공합니다. 또한 여러 프로그램이 동시에 실행될 때 충돌 없이 자원을 공유할 수 있게 합니다.\n\n[시니어]\nQ: 커널 모드와 사용자 모드를 분리하는 이유는?\nA: 보안과 안정성을 위해서입니다. 사용자 프로그램이 직접 하드웨어에 접근하면 시스템 전체가 불안정해질 수 있습니다. 커널 모드에서만 하드웨어 접근이 가능하게 하고, 사용자 프로그램은 시스템 콜을 통해 간접적으로 요청함으로써 OS가 요청을 검증하고 안전하게 처리할 수 있습니다."
            }
        ]
    }

def get_os_structure_content():
    """01_기초/os-structure - OS 구조"""
    return {
        "id": "01_기초/os-structure",
        "title": "OS 구조",
        "category": "os",
        "subCategory": "01_기초",
        "language": "C",
        "description": "커널, 쉘, 사용자 영역으로 구성된 OS 구조를 이해합니다.",
        "isPlaceholder": False,
        "sections": [
            {
                "type": "concept",
                "title": "🎯 OS 구조 완전 정복",
                "content": "**한 줄 요약**: OS는 커널(핵심), 쉘(명령 해석기), 사용자 영역(응용 프로그램)의 계층 구조로 이루어져 있습니다.\n\n**초등학생도 이해할 비유 - 회사 조직도**\n\n회사를 상상해보세요:\n- 사장실(커널) - 회사의 핵심 의사결정, 모든 자원 관리\n- 비서실(쉘) - 외부 요청을 사장에게 전달, 결과 통보\n- 각 부서(사용자 영역) - 실제 업무 수행, 비서실 통해 사장에게 보고\n\n**계층별 역할:**\n1. 커널(Kernel) - OS의 핵심, 하드웨어 직접 제어\n2. 쉘(Shell) - 사용자 명령을 커널에 전달하는 인터페이스\n3. 사용자 영역 - 응용 프로그램이 실행되는 공간\n\n**왜 계층 구조인가?**\n- 보안: 일반 프로그램이 하드웨어 직접 접근 차단\n- 안정성: 한 프로그램 오류가 전체 시스템에 영향 X\n- 유지보수: 각 계층 독립적 수정 가능"
            },
            {
                "type": "code",
                "title": "💻 동작 원리",
                "language": "text",
                "code": "OS 구조 다이어그램:\n\n┌─────────────────────────────────────────────────────┐\n│              사용자 영역 (User Space)               │\n│  ┌─────────────────────────────────────────────┐   │\n│  │    응용 프로그램 (Chrome, VSCode, 게임)      │   │\n│  └─────────────────────────────────────────────┘   │\n│  ┌─────────────────────────────────────────────┐   │\n│  │    쉘 (Shell) - bash, zsh, PowerShell       │   │\n│  │    GUI 쉘 - Windows Explorer, GNOME         │   │\n│  └─────────────────────────────────────────────┘   │\n├─────────────────────────────────────────────────────┤\n│              시스템 콜 인터페이스                    │\n│         (User Mode ↔ Kernel Mode 경계)             │\n├─────────────────────────────────────────────────────┤\n│              커널 영역 (Kernel Space)               │\n│  ┌──────────┐ ┌──────────┐ ┌──────────┐            │\n│  │ 프로세스 │ │  메모리  │ │   파일   │            │\n│  │   관리   │ │   관리   │ │  시스템  │            │\n│  └──────────┘ └──────────┘ └──────────┘            │\n│  ┌──────────┐ ┌──────────┐                         │\n│  │  디바이스│ │  네트워크│                         │\n│  │  드라이버│ │   스택   │                         │\n│  └──────────┘ └──────────┘                         │\n├─────────────────────────────────────────────────────┤\n│                   하드웨어                          │\n│        CPU / RAM / Disk / NIC / GPU                │\n└─────────────────────────────────────────────────────┘\n\n커널 유형:\n1. 모놀리식 커널: 모든 기능이 커널에 (Linux)\n2. 마이크로 커널: 최소 기능만 커널에 (Minix)\n3. 하이브리드 커널: 두 방식 혼합 (Windows NT)"
            },
            {
                "type": "code",
                "title": "🔧 실무 활용",
                "language": "bash",
                "code": "# Linux에서 쉘 확인 및 사용\n$ echo $SHELL\n/bin/bash\n\n# 현재 커널 버전 확인\n$ uname -r\n5.15.0-generic\n\n# 시스템 콜 추적 (strace)\n$ strace -c ls\n% time     calls  syscall\n------ --------- ----------------\n 45.00        12  write\n 30.00         5  read\n 15.00         3  openat\n 10.00         2  close\n\n# Java에서 쉘 명령 실행\npublic class ShellExecutor {\n    public static String executeCommand(String command) {\n        try {\n            ProcessBuilder pb = new ProcessBuilder();\n            // OS에 따라 쉘 선택\n            if (System.getProperty(\"os.name\").toLowerCase().contains(\"win\")) {\n                pb.command(\"cmd\", \"/c\", command);\n            } else {\n                pb.command(\"sh\", \"-c\", command);\n            }\n            \n            Process process = pb.start();\n            BufferedReader reader = new BufferedReader(\n                new InputStreamReader(process.getInputStream()));\n            \n            StringBuilder output = new StringBuilder();\n            String line;\n            while ((line = reader.readLine()) != null) {\n                output.append(line).append(\"\\n\");\n            }\n            return output.toString();\n        } catch (IOException e) {\n            return \"Error: \" + e.getMessage();\n        }\n    }\n}"
            },
            {
                "type": "tip",
                "title": "💡 체크리스트 & 면접",
                "content": "**핵심 개념 정리표**\n| 계층 | 역할 | 예시 |\n|------|------|------|\n| 사용자 영역 | 응용 프로그램 실행 | Chrome, VSCode |\n| 쉘 | 명령 해석, 커널과 통신 | bash, PowerShell |\n| 커널 | 자원 관리, 하드웨어 제어 | 프로세스/메모리 관리 |\n\n**커널 유형 비교**\n| 유형 | 장점 | 단점 | 예시 |\n|------|------|------|------|\n| 모놀리식 | 성능 우수 | 유지보수 어려움 | Linux |\n| 마이크로 | 안정성, 유연성 | 성능 오버헤드 | Minix |\n| 하이브리드 | 균형 | 복잡성 | Windows |\n\n**면접 질문**\n\n[주니어]\nQ: 커널과 쉘의 차이점은?\nA: 커널은 OS의 핵심으로 하드웨어를 직접 제어하고 자원을 관리합니다. 쉘은 사용자와 커널 사이의 인터페이스로, 사용자의 명령을 해석하여 커널에 전달하고 결과를 보여줍니다.\n\n[시니어]\nQ: 모놀리식 커널과 마이크로 커널의 트레이드오프는?\nA: 모놀리식은 모든 서비스가 커널 공간에서 실행되어 성능이 좋지만, 하나의 버그가 전체 시스템을 망칠 수 있습니다. 마이크로는 최소 기능만 커널에 두고 나머지는 사용자 공간에서 실행해 안정성이 높지만, IPC 오버헤드로 성능이 떨어집니다. Linux는 모놀리식이지만 모듈을 통해 유연성을 확보했습니다."
            }
        ]
    }

def get_kernel_content():
    """01_기초/kernel - 커널"""
    return {
        "id": "01_기초/kernel",
        "title": "커널",
        "category": "os",
        "subCategory": "01_기초",
        "language": "C",
        "description": "하드웨어와 소프트웨어를 연결하는 커널의 역할을 이해합니다.",
        "isPlaceholder": False,
        "sections": [
            {
                "type": "concept",
                "title": "🎯 커널 완전 정복",
                "content": "**한 줄 요약**: 커널(Kernel)은 OS의 핵심으로, 하드웨어와 소프트웨어 사이에서 자원을 관리하고 중재하는 역할을 합니다.\n\n**초등학생도 이해할 비유 - 공항 관제탑**\n\n공항을 상상해보세요:\n- 활주로(CPU) - 비행기가 이착륙하는 곳\n- 주기장(메모리) - 비행기가 대기하는 곳\n- 비행기(프로그램) - 목적지로 가려는 운송 수단\n- 관제탑(커널) - 모든 것을 조율하는 중앙 통제실\n\n**관제탑(커널)의 역할:**\n1. 이착륙 순서 결정 - CPU 스케줄링\n2. 주기장 배정 - 메모리 할당\n3. 비행기 간 충돌 방지 - 프로세스 격리\n4. 긴급 상황 처리 - 인터럽트 처리\n\n**왜 알아야 하는가?**\n- 시스템 성능 병목 이해\n- 커널 파라미터 튜닝 필요시\n- 컨테이너(Docker) 원리 이해\n- 시스템 프로그래밍의 기초"
            },
            {
                "type": "code",
                "title": "💻 동작 원리",
                "language": "text",
                "code": "커널의 주요 구성 요소:\n\n┌─────────────────────────────────────────────────────┐\n│                     커널 (Kernel)                   │\n├─────────────────────────────────────────────────────┤\n│  ┌─────────────────────────────────────────────┐   │\n│  │          프로세스 관리 (Scheduler)           │   │\n│  │  - 프로세스 생성/종료                        │   │\n│  │  - CPU 시간 분배                             │   │\n│  │  - 컨텍스트 스위칭                           │   │\n│  └─────────────────────────────────────────────┘   │\n│  ┌─────────────────────────────────────────────┐   │\n│  │          메모리 관리 (Memory Manager)        │   │\n│  │  - 가상 메모리                               │   │\n│  │  - 페이징/스와핑                             │   │\n│  │  - 메모리 보호                               │   │\n│  └─────────────────────────────────────────────┘   │\n│  ┌─────────────────────────────────────────────┐   │\n│  │          파일 시스템 (VFS)                   │   │\n│  │  - 파일 읽기/쓰기                            │   │\n│  │  - 디렉토리 관리                             │   │\n│  │  - 권한 관리                                 │   │\n│  └─────────────────────────────────────────────┘   │\n│  ┌─────────────────────────────────────────────┐   │\n│  │          디바이스 드라이버                    │   │\n│  │  - 하드웨어 추상화                           │   │\n│  │  - I/O 요청 처리                             │   │\n│  └─────────────────────────────────────────────┘   │\n│  ┌─────────────────────────────────────────────┐   │\n│  │          네트워크 스택                        │   │\n│  │  - TCP/IP 프로토콜                           │   │\n│  │  - 소켓 관리                                 │   │\n│  └─────────────────────────────────────────────┘   │\n└─────────────────────────────────────────────────────┘\n\n사용자 모드 vs 커널 모드:\n\n  User Mode          System Call         Kernel Mode\n ┌──────────┐            │              ┌──────────┐\n │ 응용     │ ──────────►│──────────────► 하드웨어 │\n │ 프로그램 │            │  권한 상승    │ 직접접근 │\n └──────────┘            │              └──────────┘\n   Ring 3                              Ring 0"
            },
            {
                "type": "code",
                "title": "🔧 실무 활용",
                "language": "bash",
                "code": "# Linux 커널 정보 확인\n$ uname -a\nLinux server 5.15.0-generic x86_64 GNU/Linux\n\n# 커널 파라미터 확인\n$ sysctl -a | head -10\nkernel.hostname = myserver\nkernel.pid_max = 4194304\nvm.swappiness = 60\n\n# 커널 파라미터 튜닝 (성능 최적화)\n$ sudo sysctl -w net.core.somaxconn=65535  # 소켓 대기열\n$ sudo sysctl -w vm.swappiness=10          # 스왑 사용 줄이기\n$ sudo sysctl -w net.ipv4.tcp_max_syn_backlog=65535\n\n# /etc/sysctl.conf에 영구 설정\nnet.core.somaxconn = 65535\nvm.swappiness = 10\nnet.ipv4.tcp_fin_timeout = 30\n\n# Java 애플리케이션에서 커널 튜닝이 필요한 경우\n# Spring Boot에서 대용량 트래픽 처리시\n\n// application.yml\nserver:\n  tomcat:\n    accept-count: 1000      # OS 레벨 backlog\n    max-connections: 10000  # 최대 연결 수\n    threads:\n      max: 200\n      min-spare: 10\n\n# Docker에서 커널 공유 확인\n$ docker run -it ubuntu uname -r\n5.15.0-generic  # 호스트와 동일한 커널 사용!"
            },
            {
                "type": "tip",
                "title": "💡 체크리스트 & 면접",
                "content": "**핵심 개념 정리표**\n| 구성요소 | 역할 | 관련 명령어 |\n|----------|------|-------------|\n| 프로세스 관리 | CPU 스케줄링, 생성/종료 | ps, top, kill |\n| 메모리 관리 | 가상 메모리, 페이징 | free, vmstat |\n| 파일 시스템 | 파일 I/O, 권한 | ls, chmod |\n| 디바이스 드라이버 | 하드웨어 제어 | lsmod, modprobe |\n| 네트워크 스택 | TCP/IP 처리 | netstat, ss |\n\n**User Mode vs Kernel Mode**\n| 구분 | User Mode | Kernel Mode |\n|------|-----------|-------------|\n| 권한 | 제한적 (Ring 3) | 전체 (Ring 0) |\n| 메모리 | 가상 주소만 | 물리 주소 접근 |\n| 하드웨어 | 접근 불가 | 직접 제어 |\n| 전환 | 시스템 콜로 | 인터럽트 발생시 |\n\n**면접 질문**\n\n[주니어]\nQ: 커널의 주요 역할 4가지를 설명해주세요.\nA: 1) 프로세스 관리 - CPU 시간 분배와 스케줄링, 2) 메모리 관리 - 가상 메모리와 페이징, 3) 파일 시스템 - 파일 I/O와 권한 관리, 4) 디바이스 관리 - 하드웨어 드라이버 제어입니다.\n\n[시니어]\nQ: 컨테이너가 VM보다 가벼운 이유를 커널 관점에서 설명해주세요.\nA: VM은 각각 독립된 Guest OS와 커널을 가져 무겁지만, 컨테이너는 호스트 OS의 커널을 공유합니다. 컨테이너는 namespace로 프로세스를 격리하고, cgroups로 자원을 제한하여 커널 레벨에서 가벼운 격리를 구현합니다. 따라서 부팅 시간이 빠르고 메모리 효율이 높습니다."
            }
        ]
    }

def get_system_call_content():
    """01_기초/system-call - 시스템 콜"""
    return {
        "id": "01_기초/system-call",
        "title": "시스템 콜",
        "category": "os",
        "subCategory": "01_기초",
        "language": "C",
        "description": "사용자 프로그램이 커널에 서비스를 요청하는 시스템 콜을 이해합니다.",
        "isPlaceholder": False,
        "sections": [
            {
                "type": "concept",
                "title": "🎯 시스템 콜 완전 정복",
                "content": "**한 줄 요약**: 시스템 콜(System Call)은 사용자 프로그램이 커널의 서비스(파일 I/O, 프로세스 생성 등)를 요청하는 유일한 방법입니다.\n\n**초등학생도 이해할 비유 - 은행 창구**\n\n은행을 상상해보세요:\n- 고객(사용자 프로그램) - 돈을 입출금하고 싶은 사람\n- 금고(하드웨어 자원) - 실제 돈이 보관된 곳\n- 은행 직원(커널) - 금고에 접근할 수 있는 유일한 사람\n- 창구(시스템 콜) - 고객이 직원에게 요청하는 공식 통로\n\n**고객이 직접 금고에 들어갈 수 없는 이유:**\n1. 보안 - 아무나 금고에 접근하면 위험\n2. 관리 - 기록 없이 돈이 오가면 혼란\n3. 안정성 - 규칙 없이 접근하면 사고 발생\n\n**주요 시스템 콜 종류:**\n- 프로세스: fork(), exec(), exit(), wait()\n- 파일: open(), read(), write(), close()\n- 메모리: mmap(), brk()\n- 통신: socket(), send(), recv()"
            },
            {
                "type": "code",
                "title": "💻 동작 원리",
                "language": "text",
                "code": "시스템 콜 동작 과정:\n\n  User Mode                              Kernel Mode\n ┌──────────────┐                     ┌──────────────┐\n │ printf(\"Hi\") │                     │              │\n │      │       │                     │              │\n │      ▼       │                     │              │\n │ write() 호출 │ ──── Trap ────────► │  시스템 콜   │\n │              │     (인터럽트)      │   핸들러     │\n │              │                     │      │       │\n │              │                     │      ▼       │\n │              │                     │  sys_write() │\n │              │                     │      │       │\n │              │                     │      ▼       │\n │              │ ◄─── Return ─────── │  하드웨어    │\n │   결과 수신  │                     │   I/O 수행   │\n └──────────────┘                     └──────────────┘\n\n상세 흐름:\n1. 사용자 프로그램이 라이브러리 함수 호출 (printf)\n2. 라이브러리가 시스템 콜 번호를 레지스터에 저장\n3. 소프트웨어 인터럽트(trap) 발생 → 커널 모드 전환\n4. 커널의 시스템 콜 핸들러가 번호 확인\n5. 해당 커널 함수 실행 (sys_write)\n6. 결과를 레지스터에 저장\n7. 사용자 모드로 복귀\n\n시스템 콜 번호 예시 (Linux x86_64):\n┌────────┬────────────┬──────────────────┐\n│ 번호   │ 시스템콜   │ 설명             │\n├────────┼────────────┼──────────────────┤\n│ 0      │ read       │ 파일 읽기        │\n│ 1      │ write      │ 파일 쓰기        │\n│ 2      │ open       │ 파일 열기        │\n│ 3      │ close      │ 파일 닫기        │\n│ 57     │ fork       │ 프로세스 생성    │\n│ 59     │ execve     │ 프로그램 실행    │\n│ 60     │ exit       │ 프로세스 종료    │\n└────────┴────────────┴──────────────────┘"
            },
            {
                "type": "code",
                "title": "🔧 실무 활용",
                "language": "c",
                "code": "// C언어에서 시스템 콜 직접 사용\n#include <unistd.h>\n#include <fcntl.h>\n#include <sys/types.h>\n\nint main() {\n    // 파일 시스템 콜\n    int fd = open(\"test.txt\", O_RDONLY);  // 시스템 콜\n    char buffer[100];\n    read(fd, buffer, 100);                 // 시스템 콜\n    close(fd);                             // 시스템 콜\n    \n    // 프로세스 시스템 콜\n    pid_t pid = fork();                    // 시스템 콜\n    if (pid == 0) {\n        // 자식 프로세스\n        execl(\"/bin/ls\", \"ls\", \"-la\", NULL);  // 시스템 콜\n    } else {\n        // 부모 프로세스\n        wait(NULL);                        // 시스템 콜\n    }\n    return 0;\n}\n\n// Java에서 시스템 콜 (JNI 또는 라이브러리 통해 간접 호출)\nimport java.io.*;\n\npublic class SystemCallExample {\n    public static void main(String[] args) throws Exception {\n        // FileInputStream 내부에서 open(), read() 시스템 콜 발생\n        FileInputStream fis = new FileInputStream(\"test.txt\");\n        byte[] buffer = new byte[100];\n        fis.read(buffer);  // 내부적으로 read() 시스템 콜\n        fis.close();       // 내부적으로 close() 시스템 콜\n        \n        // ProcessBuilder로 fork+exec 시스템 콜\n        ProcessBuilder pb = new ProcessBuilder(\"ls\", \"-la\");\n        Process p = pb.start();  // 내부적으로 fork(), exec()\n        p.waitFor();             // 내부적으로 wait()\n    }\n}\n\n// strace로 시스템 콜 추적\n// $ strace -f java SystemCallExample\n// openat(AT_FDCWD, \"test.txt\", O_RDONLY) = 3\n// read(3, \"hello world\", 100) = 11\n// close(3) = 0"
            },
            {
                "type": "tip",
                "title": "💡 체크리스트 & 면접",
                "content": "**주요 시스템 콜 분류**\n| 분류 | 시스템 콜 | 설명 |\n|------|----------|------|\n| 프로세스 | fork() | 프로세스 복제 생성 |\n| 프로세스 | exec() | 새 프로그램 실행 |\n| 프로세스 | exit() | 프로세스 종료 |\n| 파일 | open() | 파일 열기 |\n| 파일 | read()/write() | 파일 읽기/쓰기 |\n| 메모리 | mmap() | 메모리 매핑 |\n| 통신 | socket() | 소켓 생성 |\n\n**시스템 콜 vs 라이브러리 함수**\n| 구분 | 시스템 콜 | 라이브러리 함수 |\n|------|----------|----------------|\n| 실행 위치 | 커널 모드 | 사용자 모드 |\n| 오버헤드 | 큼 (모드 전환) | 작음 |\n| 예시 | read(), write() | printf(), malloc() |\n| 번호 | 고유 번호 있음 | 없음 |\n\n**면접 질문**\n\n[주니어]\nQ: 시스템 콜이 필요한 이유는?\nA: 사용자 프로그램은 보안상 하드웨어에 직접 접근할 수 없습니다. 파일 읽기, 네트워크 통신 등 하드웨어 자원이 필요할 때 시스템 콜을 통해 커널에 요청해야 합니다. 커널은 요청을 검증하고 안전하게 처리한 후 결과를 반환합니다.\n\n[시니어]\nQ: 시스템 콜의 오버헤드를 줄이는 방법은?\nA: 1) 버퍼링 - 여러 번의 I/O를 모아서 한 번의 시스템 콜로 처리 (BufferedReader), 2) mmap - 파일을 메모리에 매핑하여 read/write 콜 감소, 3) io_uring - Linux 5.1+에서 비동기 I/O로 시스템 콜 배치 처리, 4) vDSO - 자주 사용되는 콜(gettimeofday)을 사용자 공간에서 처리."
            }
        ]
    }

def get_process_memory_content():
    """02_프로세스/process-memory - 프로세스 메모리 구조"""
    return {
        "id": "02_프로세스/process-memory",
        "title": "프로세스 메모리 구조",
        "category": "os",
        "subCategory": "02_프로세스",
        "language": "C",
        "description": "Code, Data, Heap, Stack 영역으로 구성된 프로세스 메모리 구조를 이해합니다.",
        "isPlaceholder": False,
        "sections": [
            {
                "type": "concept",
                "title": "🎯 프로세스 메모리 구조 완전 정복",
                "content": "**한 줄 요약**: 프로세스 메모리는 Code(코드), Data(전역변수), Heap(동적할당), Stack(지역변수) 4개 영역으로 구성됩니다.\n\n**초등학생도 이해할 비유 - 책상 정리**\n\n공부하는 책상을 상상해보세요:\n- 교과서 선반(Code) - 읽기만 하는 책들, 변경 불가\n- 필통(Data) - 항상 있는 문구류, 프로그램 시작부터 끝까지\n- 서랍(Heap) - 필요할 때 꺼내고 다 쓰면 정리\n- 책상 위(Stack) - 지금 하는 과목 노트, 과목 바뀌면 치움\n\n**각 영역의 특징:**\n1. Code - 실행할 기계어 코드, 읽기 전용\n2. Data - 전역/정적 변수, 프로그램 시작시 할당\n3. Heap - malloc/new로 동적 할당, 개발자가 관리\n4. Stack - 지역변수/매개변수, 함수 호출시 자동 관리\n\n**왜 알아야 하는가?**\n- 메모리 누수(Memory Leak) 이해와 방지\n- StackOverflow 에러 원인 파악\n- 효율적인 메모리 사용 설계\n- JVM 메모리 튜닝의 기초"
            },
            {
                "type": "code",
                "title": "💻 동작 원리",
                "language": "text",
                "code": "프로세스 메모리 레이아웃:\n\n    높은 주소\n    ┌─────────────────────────────────┐\n    │         커널 영역               │ ← 사용자 접근 불가\n    ├─────────────────────────────────┤\n    │                                 │\n    │         Stack 영역              │ ← 아래로 성장 ↓\n    │   (지역변수, 매개변수, 복귀주소) │\n    │                                 │\n    ├ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┤\n    │              ↓                  │\n    │         빈 공간                 │\n    │              ↑                  │\n    ├ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┤\n    │                                 │\n    │         Heap 영역               │ ← 위로 성장 ↑\n    │   (동적 할당: malloc, new)      │\n    │                                 │\n    ├─────────────────────────────────┤\n    │         BSS 영역                │ ← 초기화 안 된 전역변수\n    ├─────────────────────────────────┤\n    │         Data 영역               │ ← 초기화된 전역/정적 변수\n    ├─────────────────────────────────┤\n    │         Code(Text) 영역         │ ← 실행 코드 (읽기 전용)\n    └─────────────────────────────────┘\n    낮은 주소\n\n각 영역 크기 (Linux 기준):\n- Stack: 기본 8MB (ulimit -s로 확인)\n- Heap: 가용 메모리까지 확장 가능\n- 전체: 32bit = 4GB, 64bit = 128TB (가상 주소 공간)"
            },
            {
                "type": "code",
                "title": "🔧 실무 활용",
                "language": "c",
                "code": "// C언어로 각 메모리 영역 확인\n#include <stdio.h>\n#include <stdlib.h>\n\nint global_init = 100;      // Data 영역 (초기화된 전역)\nint global_uninit;          // BSS 영역 (초기화 안 된 전역)\n\nvoid function(int param) {  // param: Stack\n    int local = 10;         // Stack 영역\n    int *heap = malloc(sizeof(int) * 10);  // Heap 영역\n    \n    printf(\"Code 영역: %p\\n\", (void*)function);\n    printf(\"Data 영역: %p\\n\", (void*)&global_init);\n    printf(\"BSS 영역:  %p\\n\", (void*)&global_uninit);\n    printf(\"Heap 영역: %p\\n\", (void*)heap);\n    printf(\"Stack 영역: %p\\n\", (void*)&local);\n    \n    free(heap);  // Heap 해제 필수!\n}\n\n// Java에서의 메모리 구조\npublic class MemoryExample {\n    static int staticVar = 100;     // Method Area (Data)\n    int instanceVar = 10;           // Heap (객체와 함께)\n    \n    public void method(int param) { // param: Stack\n        int localVar = 5;           // Stack\n        Object obj = new Object();  // 참조는 Stack, 객체는 Heap\n        \n        // Java는 GC가 Heap을 자동 관리\n    }\n}\n\n// JVM 메모리 설정 (Spring Boot)\njava -Xms512m \\       # Heap 초기 크기\n     -Xmx2g \\         # Heap 최대 크기\n     -Xss1m \\         # Stack 크기 (스레드당)\n     -XX:MetaspaceSize=256m \\  # Method Area\n     -jar app.jar"
            },
            {
                "type": "tip",
                "title": "💡 체크리스트 & 면접",
                "content": "**메모리 영역 비교표**\n| 영역 | 저장 내용 | 크기 결정 | 관리 주체 |\n|------|----------|----------|----------|\n| Code | 실행 코드 | 컴파일 시 | OS |\n| Data | 전역/정적 변수 | 컴파일 시 | OS |\n| Heap | 동적 할당 | 런타임 | 개발자/GC |\n| Stack | 지역변수, 매개변수 | 런타임 | OS(자동) |\n\n**주요 에러와 원인**\n| 에러 | 원인 | 해결책 |\n|------|------|--------|\n| StackOverflow | 재귀 과다, 큰 배열 | 재귀 최적화, Heap 사용 |\n| OutOfMemory | Heap 부족, 메모리 누수 | 힙 증가, 누수 수정 |\n| Segmentation Fault | 잘못된 주소 접근 | 포인터 검증 |\n\n**면접 질문**\n\n[주니어]\nQ: Stack과 Heap의 차이점은?\nA: Stack은 함수 호출시 자동으로 할당/해제되며 LIFO 구조입니다. 지역변수, 매개변수가 저장되고 크기가 제한적입니다. Heap은 개발자가 명시적으로 할당/해제하며 크기가 유동적입니다. Java에서는 객체가 Heap에 생성되고 GC가 관리합니다.\n\n[시니어]\nQ: JVM 메모리 튜닝시 고려사항은?\nA: 1) Heap 크기 - Xms와 Xmx를 동일하게 설정하여 리사이징 오버헤드 방지, 2) GC 선택 - G1GC(균형), ZGC(저지연)등 워크로드에 맞게 선택, 3) Metaspace - 클래스 많으면 증가, 4) Stack - 스레드 많으면 줄여서 메모리 절약. 항상 모니터링하며 조정해야 합니다."
            }
        ]
    }

def get_pcb_content():
    """02_프로세스/pcb - PCB"""
    return {
        "id": "02_프로세스/pcb",
        "title": "PCB (Process Control Block)",
        "category": "os",
        "subCategory": "02_프로세스",
        "language": "C",
        "description": "프로세스의 모든 정보를 담고 있는 PCB를 이해합니다.",
        "isPlaceholder": False,
        "sections": [
            {
                "type": "concept",
                "title": "🎯 PCB 완전 정복",
                "content": "**한 줄 요약**: PCB(Process Control Block)는 각 프로세스의 정보(상태, 레지스터, 메모리 등)를 저장하는 커널의 자료구조입니다.\n\n**초등학생도 이해할 비유 - 학생 생활기록부**\n\n학교를 상상해보세요:\n- 학생(프로세스) - 각각 고유한 특성을 가진 존재\n- 생활기록부(PCB) - 학생의 모든 정보가 기록된 문서\n- 담임선생님(OS) - 생활기록부를 관리하는 사람\n\n**생활기록부(PCB)에 기록된 정보:**\n1. 학번(PID) - 학생 고유 식별 번호\n2. 현재 상태 - 수업중/쉬는시간/급식중\n3. 시간표(프로그램 카운터) - 지금 어떤 수업인지\n4. 성적(레지스터) - 현재까지의 학습 상태\n5. 교실 배치(메모리 정보) - 어디에 앉아있는지\n\n**왜 알아야 하는가?**\n- 컨텍스트 스위칭 원리 이해\n- 프로세스 관리 방식 파악\n- 멀티태스킹 동작 원리\n- ps, top 명령어 결과 해석"
            },
            {
                "type": "code",
                "title": "💻 동작 원리",
                "language": "text",
                "code": "PCB 구조:\n\n┌─────────────────────────────────────────────────┐\n│              PCB (Process Control Block)        │\n├─────────────────────────────────────────────────┤\n│  PID (Process ID)          : 1234               │\n│  프로세스 상태              : Running            │\n│  프로그램 카운터 (PC)       : 0x00401000         │\n│  CPU 레지스터              : EAX, EBX, ESP...    │\n│  CPU 스케줄링 정보         : 우선순위 20         │\n│  메모리 관리 정보          : 페이지 테이블 주소   │\n│  계정 정보                 : 사용자 ID, CPU 시간  │\n│  I/O 상태 정보             : 열린 파일 목록       │\n│  부모/자식 프로세스 정보    : PPID, Child PIDs    │\n└─────────────────────────────────────────────────┘\n\n컨텍스트 스위칭과 PCB:\n\n  Process A          OS Kernel          Process B\n ┌─────────┐      ┌─────────────┐      ┌─────────┐\n │ Running │      │             │      │ Ready   │\n │    │    │      │  PCB List   │      │         │\n │    ▼    │      │ ┌─────────┐ │      │         │\n │ 인터럽트 ├─────►│ │ PCB_A   │ │      │         │\n │         │ save │ │ 상태저장 │ │      │         │\n │         │      │ └─────────┘ │      │         │\n │         │      │ ┌─────────┐ │      │         │\n │         │      │ │ PCB_B   │ │◄─────┤         │\n │         │      │ │ 상태복원 │ │restore        │\n │         │      │ └─────────┘ │      │    │    │\n │ Ready   │      │             │      │    ▼    │\n │         │      │             │      │ Running │\n └─────────┘      └─────────────┘      └─────────┘\n\nLinux의 task_struct (실제 PCB):\n- 약 1.7KB 크기의 구조체\n- 300개 이상의 필드 포함\n- include/linux/sched.h에 정의"
            },
            {
                "type": "code",
                "title": "🔧 실무 활용",
                "language": "c",
                "code": "// Linux에서 PCB 정보 확인\n// /proc/[pid]/ 디렉토리에서 프로세스 정보 확인 가능\n\n// C언어 - 프로세스 정보 읽기\n#include <stdio.h>\n#include <stdlib.h>\n#include <unistd.h>\n\nint main() {\n    pid_t pid = getpid();\n    printf(\"Current PID: %d\\n\", pid);\n    \n    // /proc/self/status 읽기\n    char path[256];\n    sprintf(path, \"/proc/%d/status\", pid);\n    \n    FILE *f = fopen(path, \"r\");\n    char line[256];\n    while (fgets(line, sizeof(line), f)) {\n        printf(\"%s\", line);\n    }\n    fclose(f);\n    return 0;\n}\n\n// Java에서 프로세스 정보 확인\npublic class ProcessInfo {\n    public static void main(String[] args) {\n        // 현재 프로세스 정보\n        ProcessHandle current = ProcessHandle.current();\n        System.out.println(\"PID: \" + current.pid());\n        \n        ProcessHandle.Info info = current.info();\n        System.out.println(\"Command: \" + info.command().orElse(\"N/A\"));\n        System.out.println(\"User: \" + info.user().orElse(\"N/A\"));\n        System.out.println(\"Start Time: \" + info.startInstant().orElse(null));\n        System.out.println(\"CPU Time: \" + info.totalCpuDuration().orElse(null));\n        \n        // 모든 프로세스 조회\n        ProcessHandle.allProcesses()\n            .filter(p -> p.info().command().isPresent())\n            .limit(10)\n            .forEach(p -> System.out.println(\n                p.pid() + \": \" + p.info().command().get()));\n    }\n}\n\n// 터미널 명령어\n$ cat /proc/1234/status    # 특정 PID의 PCB 정보\n$ ps aux                    # 모든 프로세스 정보\n$ top -p 1234               # 특정 프로세스 모니터링"
            },
            {
                "type": "tip",
                "title": "💡 체크리스트 & 면접",
                "content": "**PCB 주요 필드**\n| 필드 | 설명 | 용도 |\n|------|------|------|\n| PID | 프로세스 고유 ID | 프로세스 식별 |\n| State | 상태 (Running/Ready 등) | 스케줄링 |\n| PC | 다음 실행 명령어 주소 | 실행 위치 복원 |\n| Registers | CPU 레지스터 값 | 컨텍스트 복원 |\n| Memory | 페이지 테이블, 한계 레지스터 | 메모리 보호 |\n| I/O | 열린 파일, 디바이스 | 자원 관리 |\n\n**/proc/[pid]/ 주요 파일**\n| 파일 | 내용 |\n|------|------|\n| status | PID, 상태, 메모리 사용량 |\n| cmdline | 실행 명령어 |\n| fd/ | 열린 파일 디스크립터 |\n| maps | 메모리 매핑 정보 |\n| stat | CPU 사용 통계 |\n\n**면접 질문**\n\n[주니어]\nQ: PCB에는 어떤 정보가 저장되나요?\nA: PCB에는 프로세스 식별자(PID), 프로세스 상태, 프로그램 카운터(다음 실행할 명령어 주소), CPU 레지스터 값, 메모리 관리 정보(페이지 테이블), 스케줄링 정보(우선순위), I/O 상태 정보(열린 파일 목록) 등이 저장됩니다.\n\n[시니어]\nQ: 컨텍스트 스위칭 비용을 줄이는 방법은?\nA: 1) 스레드 사용 - 같은 프로세스 내 스레드는 메모리 공간을 공유하므로 PCB 전체가 아닌 스택/레지스터만 전환, 2) 코루틴/경량 스레드 - 사용자 레벨에서 전환하여 커널 개입 최소화, 3) CPU 친화성(affinity) 설정 - 캐시 미스 감소, 4) 스케줄러 튜닝 - 타임 슬라이스 조정으로 불필요한 스위칭 감소."
            }
        ]
    }

def get_process_state_content():
    """02_프로세스/process-state - 프로세스 상태"""
    return {
        "id": "02_프로세스/process-state",
        "title": "프로세스 상태",
        "category": "os",
        "subCategory": "02_프로세스",
        "language": "C",
        "description": "New, Ready, Running, Waiting, Terminated 5가지 프로세스 상태를 이해합니다.",
        "isPlaceholder": False,
        "sections": [
            {
                "type": "concept",
                "title": "🎯 프로세스 상태 완전 정복",
                "content": "**한 줄 요약**: 프로세스는 생성(New), 준비(Ready), 실행(Running), 대기(Waiting), 종료(Terminated) 5가지 상태를 거치며 생명주기를 가집니다.\n\n**초등학생도 이해할 비유 - 놀이공원 롤러코스터**\n\n롤러코스터를 상상해보세요:\n- 티켓 구매(New) - 탑승 자격 획득\n- 대기줄(Ready) - 탑승 순서 기다림\n- 탑승중(Running) - 실제로 롤러코스터 타는 중\n- 화장실(Waiting) - 급한 일 처리하고 다시 대기줄로\n- 하차(Terminated) - 탑승 완료, 퇴장\n\n**각 상태 설명:**\n1. New - 프로세스 생성 중, PCB 할당\n2. Ready - CPU 할당 대기 중, Ready Queue에서 대기\n3. Running - CPU에서 실행 중 (동시에 1개만)\n4. Waiting(Blocked) - I/O 완료 등 이벤트 대기\n5. Terminated - 실행 완료, 자원 반납 중\n\n**왜 알아야 하는가?**\n- 프로세스 스케줄링 이해\n- top/ps 명령어 상태 해석\n- 성능 병목 분석 (D 상태 프로세스 등)\n- 멀티태스킹 원리 파악"
            },
            {
                "type": "code",
                "title": "💻 동작 원리",
                "language": "text",
                "code": "프로세스 상태 전이 다이어그램:\n\n                        ┌───────────────────────┐\n                        │                       │\n                        ▼                       │\n    ┌─────┐  admit   ┌───────┐  dispatch  ┌─────────┐\n    │ New │ ───────► │ Ready │ ─────────► │ Running │\n    └─────┘          └───────┘            └─────────┘\n                        ▲  ▲                  │ │ │\n                        │  │   timeout/       │ │ │\n                        │  │   preempt        │ │ │\n                        │  └──────────────────┘ │ │\n                        │                       │ │\n                        │   I/O or event        │ │  exit\n                        │    complete           │ │\n                        │                       │ │\n                     ┌─────────┐   I/O or      │ │   ┌────────────┐\n                     │ Waiting │ ◄── event ────┘ └──►│ Terminated │\n                     │(Blocked)│     wait            └────────────┘\n                     └─────────┘\n\n상태 전이 조건:\n1. New → Ready     : 프로세스 생성 완료 (admit)\n2. Ready → Running : CPU 스케줄러가 선택 (dispatch)\n3. Running → Ready : 타임아웃, 더 높은 우선순위 등장 (preempt)\n4. Running → Waiting: I/O 요청, 이벤트 대기 (I/O wait)\n5. Waiting → Ready : I/O 완료, 이벤트 발생 (I/O complete)\n6. Running → Terminated: 프로세스 종료 (exit)\n\nLinux 프로세스 상태 코드:\n┌──────┬─────────────┬─────────────────────────────┐\n│ 코드 │ 상태        │ 설명                        │\n├──────┼─────────────┼─────────────────────────────┤\n│ R    │ Running     │ 실행 중 또는 Ready Queue    │\n│ S    │ Sleeping    │ 인터럽트 가능한 대기        │\n│ D    │ Disk Sleep  │ 인터럽트 불가 대기 (I/O)    │\n│ Z    │ Zombie      │ 종료되었지만 부모가 수습 안함│\n│ T    │ Stopped     │ 시그널로 중지됨             │\n└──────┴─────────────┴─────────────────────────────┘"
            },
            {
                "type": "code",
                "title": "🔧 실무 활용",
                "language": "bash",
                "code": "# Linux에서 프로세스 상태 확인\n$ ps aux\nUSER  PID %CPU %MEM  STAT COMMAND\nroot    1  0.0  0.1  Ss   /sbin/init\nroot  123  0.5  2.0  R    java -jar app.jar\nroot  456  0.0  0.1  S    sleep 100\nroot  789  0.0  0.0  D    dd if=/dev/sda  # 디스크 I/O 대기\nroot  999  0.0  0.0  Z    <defunct>       # 좀비 프로세스\n\n# 상태별 프로세스 수 확인\n$ ps -eo stat | sort | uniq -c\n    150 S    # Sleeping\n     10 R    # Running\n      2 D    # Disk Sleep (주의 필요!)\n      1 Z    # Zombie (정리 필요)\n\n# Java에서 스레드 상태 확인\npublic class ThreadStateDemo {\n    public static void main(String[] args) throws Exception {\n        Thread thread = new Thread(() -> {\n            try {\n                Thread.sleep(10000);  // TIMED_WAITING 상태\n            } catch (InterruptedException e) {}\n        });\n        \n        System.out.println(thread.getState());  // NEW\n        thread.start();\n        System.out.println(thread.getState());  // RUNNABLE\n        Thread.sleep(100);\n        System.out.println(thread.getState());  // TIMED_WAITING\n        thread.join();\n        System.out.println(thread.getState());  // TERMINATED\n    }\n}\n\n// Java Thread 상태:\n// NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, TERMINATED\n\n# 좀비 프로세스 정리\n$ ps aux | grep Z        # 좀비 프로세스 찾기\n$ kill -SIGCHLD <PPID>   # 부모에게 SIGCHLD 전송\n$ kill -9 <PPID>         # 부모 강제 종료 (최후 수단)"
            },
            {
                "type": "tip",
                "title": "💡 체크리스트 & 면접",
                "content": "**프로세스 5가지 상태**\n| 상태 | 설명 | Linux 코드 |\n|------|------|------------|\n| New | 프로세스 생성 중 | - |\n| Ready | CPU 대기 중 | R |\n| Running | CPU에서 실행 중 | R |\n| Waiting | I/O 등 이벤트 대기 | S, D |\n| Terminated | 종료됨 | Z (좀비) |\n\n**주의해야 할 상태**\n| 상태 | 문제점 | 해결책 |\n|------|--------|--------|\n| D (Disk Sleep) | 많으면 I/O 병목 | 디스크 성능 확인 |\n| Z (Zombie) | 자원 누수 | 부모 프로세스 수정 |\n| 과다한 R | CPU 부족 | 스케일 아웃 |\n\n**면접 질문**\n\n[주니어]\nQ: 프로세스 상태 5가지와 전이 조건을 설명해주세요.\nA: New(생성)에서 Ready(준비)로 전이하고, 스케줄러가 선택하면 Running(실행)이 됩니다. 실행 중 I/O 요청시 Waiting(대기)으로, 타임아웃시 Ready로 돌아갑니다. 실행 완료시 Terminated(종료)가 됩니다.\n\n[시니어]\nQ: 좀비 프로세스가 발생하는 원인과 해결책은?\nA: 자식 프로세스가 종료되었지만 부모가 wait()를 호출하지 않아 PCB가 남아있는 상태입니다. 해결책: 1) 부모 프로세스에서 wait()/waitpid() 호출, 2) SIGCHLD 시그널 핸들러 등록, 3) 부모를 double fork로 init에 입양시키기. 좀비 자체는 자원을 많이 안 쓰지만, PID 고갈 가능성이 있습니다."
            }
        ]
    }

def get_ipc_content():
    """02_프로세스/ipc - IPC"""
    return {
        "id": "02_프로세스/ipc",
        "title": "IPC (프로세스 간 통신)",
        "category": "os",
        "subCategory": "02_프로세스",
        "language": "C",
        "description": "프로세스 간 데이터를 주고받는 IPC 메커니즘을 이해합니다.",
        "isPlaceholder": False,
        "sections": [
            {
                "type": "concept",
                "title": "🎯 IPC 완전 정복",
                "content": "**한 줄 요약**: IPC(Inter-Process Communication)는 독립된 프로세스들이 데이터를 주고받는 방법으로, 파이프, 메시지 큐, 공유 메모리, 소켓 등이 있습니다.\n\n**초등학생도 이해할 비유 - 교실 간 소통**\n\n학교 교실들을 상상해보세요:\n- 각 교실(프로세스) - 독립된 공간, 서로 직접 못 들어감\n- 쪽지 전달(파이프) - 한 방향으로 쪽지 전달\n- 게시판(메시지 큐) - 메시지를 올리고 가져감\n- 공유 사물함(공유 메모리) - 같이 쓰는 공간\n- 전화(소켓) - 멀리 있어도 통신 가능\n\n**IPC가 필요한 이유:**\n1. 프로세스는 각자 독립된 메모리 공간\n2. 직접 다른 프로세스 메모리 접근 불가\n3. 협력이 필요한 작업 수행\n4. 데이터 공유 및 동기화\n\n**주요 IPC 방식:**\n- 파이프(Pipe) - 단방향, 부모-자식 간\n- 메시지 큐 - 비동기, 메시지 단위\n- 공유 메모리 - 가장 빠름, 동기화 필요\n- 소켓 - 네트워크 통신 가능"
            },
            {
                "type": "code",
                "title": "💻 동작 원리",
                "language": "text",
                "code": "IPC 방식 비교:\n\n1. 파이프 (Pipe)\n   ┌───────────┐    단방향    ┌───────────┐\n   │ Process A │ ───────────► │ Process B │\n   │  (부모)   │   fd[1]→fd[0] │  (자식)   │\n   └───────────┘              └───────────┘\n\n2. 명명된 파이프 (Named Pipe / FIFO)\n   ┌───────────┐              ┌───────────┐\n   │ Process A │ ──┐      ┌── │ Process B │\n   └───────────┘   │      │   └───────────┘\n                   ▼      ▼\n              ┌──────────────┐\n              │  /tmp/myfifo │  ← 파일시스템에 존재\n              └──────────────┘\n\n3. 메시지 큐 (Message Queue)\n   ┌───────────┐              ┌───────────┐\n   │ Process A │ ──┐      ┌── │ Process B │\n   └───────────┘   │      │   └───────────┘\n                   ▼      ▼\n              ┌──────────────┐\n              │ Message Queue│\n              │ [msg1][msg2] │  ← 커널이 관리\n              └──────────────┘\n\n4. 공유 메모리 (Shared Memory)\n   ┌───────────┐              ┌───────────┐\n   │ Process A │              │ Process B │\n   │           │              │           │\n   │  ┌─────┐  │              │  ┌─────┐  │\n   │  │ ptr │──┼──────────────┼──│ ptr │  │\n   │  └─────┘  │              │  └─────┘  │\n   └───────────┘              └───────────┘\n           │                        │\n           └────────┬───────────────┘\n                    ▼\n              ┌──────────────┐\n              │ Shared Memory│  ← 물리 메모리\n              │   Segment    │\n              └──────────────┘\n\n5. 소켓 (Socket)\n   ┌───────────┐              ┌───────────┐\n   │ Process A │ ◄──────────► │ Process B │\n   │ (Client)  │   TCP/UDP    │ (Server)  │\n   └───────────┘   네트워크    └───────────┘"
            },
            {
                "type": "code",
                "title": "🔧 실무 활용",
                "language": "c",
                "code": "// 1. 파이프 (Pipe) - C언어\n#include <unistd.h>\nint main() {\n    int fd[2];\n    pipe(fd);  // fd[0]: 읽기, fd[1]: 쓰기\n    \n    if (fork() == 0) {\n        // 자식: 읽기\n        close(fd[1]);\n        char buf[100];\n        read(fd[0], buf, sizeof(buf));\n        printf(\"Received: %s\\n\", buf);\n    } else {\n        // 부모: 쓰기\n        close(fd[0]);\n        write(fd[1], \"Hello!\", 7);\n    }\n    return 0;\n}\n\n// 2. Java에서 IPC - 소켓 방식\n// Server\nServerSocket server = new ServerSocket(8080);\nSocket client = server.accept();\nBufferedReader in = new BufferedReader(\n    new InputStreamReader(client.getInputStream()));\nString message = in.readLine();\n\n// Client\nSocket socket = new Socket(\"localhost\", 8080);\nPrintWriter out = new PrintWriter(socket.getOutputStream(), true);\nout.println(\"Hello Server!\");\n\n// 3. Spring에서 IPC - Redis Pub/Sub\n@Service\npublic class MessageService {\n    @Autowired\n    private StringRedisTemplate redisTemplate;\n    \n    // 메시지 발행 (Publisher)\n    public void publish(String channel, String message) {\n        redisTemplate.convertAndSend(channel, message);\n    }\n}\n\n@Component\npublic class MessageSubscriber implements MessageListener {\n    // 메시지 수신 (Subscriber)\n    @Override\n    public void onMessage(Message message, byte[] pattern) {\n        String body = new String(message.getBody());\n        log.info(\"Received: {}\", body);\n    }\n}\n\n// 4. 실무에서 많이 사용하는 IPC\n// - 마이크로서비스: REST API, gRPC, Message Queue (Kafka, RabbitMQ)\n// - 같은 서버: Unix Socket, Shared Memory\n// - 컨테이너 간: Docker Network, Kubernetes Service"
            },
            {
                "type": "tip",
                "title": "💡 체크리스트 & 면접",
                "content": "**IPC 방식 비교표**\n| 방식 | 속도 | 방향 | 범위 | 용도 |\n|------|------|------|------|------|\n| 파이프 | 중간 | 단방향 | 부모-자식 | 간단한 데이터 전달 |\n| 명명된 파이프 | 중간 | 단/양방향 | 같은 시스템 | 무관계 프로세스 통신 |\n| 메시지 큐 | 중간 | 양방향 | 같은 시스템 | 비동기 메시지 |\n| 공유 메모리 | 매우 빠름 | 양방향 | 같은 시스템 | 대용량 데이터 |\n| 소켓 | 느림 | 양방향 | 네트워크 | 분산 시스템 |\n\n**실무에서의 IPC 선택**\n| 상황 | 추천 방식 |\n|------|----------|\n| 마이크로서비스 | REST, gRPC, Kafka |\n| 실시간 이벤트 | WebSocket, Redis Pub/Sub |\n| 대용량 데이터 공유 | 공유 메모리, mmap |\n| 부모-자식 프로세스 | 파이프 |\n\n**면접 질문**\n\n[주니어]\nQ: IPC 방식의 종류와 각각의 특징은?\nA: 파이프는 단방향으로 부모-자식 간 통신에 사용됩니다. 메시지 큐는 비동기로 메시지를 주고받습니다. 공유 메모리는 가장 빠르지만 동기화가 필요합니다. 소켓은 네트워크를 통해 다른 시스템과도 통신할 수 있습니다.\n\n[시니어]\nQ: 마이크로서비스에서 동기 vs 비동기 통신의 트레이드오프는?\nA: 동기(REST, gRPC)는 구현이 단순하고 즉시 응답을 받지만, 서비스 간 강결합과 장애 전파 위험이 있습니다. 비동기(Kafka, RabbitMQ)는 느슨한 결합과 장애 격리가 가능하지만, 최종 일관성 모델이라 복잡도가 높습니다. 보통 조회는 동기, 명령은 비동기(CQRS)로 혼합 사용합니다."
            }
        ]
    }

def get_process_concept_content():
    """02_프로세스스레드/process-concept - 프로세스 개념"""
    return {
        "id": "02_프로세스스레드/process-concept",
        "title": "프로세스 개념",
        "category": "os",
        "subCategory": "02_프로세스스레드",
        "language": "C",
        "description": "프로세스의 기본 개념과 특징을 이해합니다.",
        "isPlaceholder": False,
        "sections": [
            {
                "type": "concept",
                "title": "🎯 프로세스 개념 완전 정복",
                "content": "**한 줄 요약**: 프로세스는 실행 중인 프로그램으로, 독립된 메모리 공간과 자원을 가진 실행 단위입니다.\n\n**초등학생도 이해할 비유 - 요리사와 레시피**\n\n주방을 상상해보세요:\n- 레시피(프로그램) - 종이에 적힌 요리 방법, 실행 전\n- 요리하는 행위(프로세스) - 레시피를 보고 실제로 요리\n- 조리대(메모리) - 재료와 도구를 놓는 공간\n- 요리사(CPU) - 실제로 요리를 수행\n\n**프로그램 vs 프로세스:**\n- 프로그램: 디스크에 저장된 정적인 코드\n- 프로세스: 메모리에 올라와 실행 중인 동적인 상태\n\n**프로세스의 특징:**\n1. 독립된 메모리 공간 (Code, Data, Heap, Stack)\n2. 최소 하나의 스레드 포함\n3. 고유한 PID (Process ID)\n4. 자원의 소유 단위 (파일, 소켓 등)\n\n**왜 알아야 하는가?**\n- 멀티프로세싱 vs 멀티스레딩 선택\n- 시스템 자원 관리 이해\n- 프로세스 간 통신(IPC) 필요성 파악"
            },
            {
                "type": "code",
                "title": "💻 동작 원리",
                "language": "text",
                "code": "프로그램에서 프로세스로:\n\n  디스크                        메모리(RAM)\n ┌──────────────┐             ┌──────────────────────┐\n │              │             │      Process A       │\n │  program.exe │    로딩     │  ┌────────────────┐  │\n │  (실행파일)  │ ──────────► │  │ Code (Text)    │  │\n │              │             │  ├────────────────┤  │\n │  - 코드      │             │  │ Data           │  │\n │  - 초기 데이터│             │  ├────────────────┤  │\n │              │             │  │ Heap           │  │\n └──────────────┘             │  ├────────────────┤  │\n                              │  │ Stack          │  │\n                              │  └────────────────┘  │\n                              │  PCB: PID=1234       │\n                              └──────────────────────┘\n\n같은 프로그램, 여러 프로세스:\n\n  Chrome.exe (1개)            Chrome 프로세스 (여러 개)\n ┌──────────────┐           ┌────────┐ ┌────────┐ ┌────────┐\n │              │    실행   │ PID:100│ │ PID:101│ │ PID:102│\n │  Chrome.exe  │ ────────► │ 탭 1   │ │ 탭 2   │ │ 탭 3   │\n │              │           │ 독립   │ │ 독립   │ │ 독립   │\n │              │           │ 메모리 │ │ 메모리 │ │ 메모리 │\n └──────────────┘           └────────┘ └────────┘ └────────┘\n\n프로세스 생성 과정:\n1. fork() 시스템 콜 → 부모 프로세스 복제\n2. exec() 시스템 콜 → 새 프로그램 코드로 교체\n\n  Parent Process              Child Process\n ┌──────────────┐   fork()   ┌──────────────┐\n │ PID: 100     │ ─────────► │ PID: 101     │\n │ Code: A      │   복사     │ Code: A      │\n │ Data: {...}  │            │ Data: {...}  │\n └──────────────┘            └──────────────┘\n                                    │\n                               exec()\n                                    ▼\n                             ┌──────────────┐\n                             │ PID: 101     │\n                             │ Code: B      │ ← 새 프로그램\n                             │ Data: {...}  │\n                             └──────────────┘"
            },
            {
                "type": "code",
                "title": "🔧 실무 활용",
                "language": "c",
                "code": "// C언어 - 프로세스 생성\n#include <stdio.h>\n#include <unistd.h>\n#include <sys/wait.h>\n\nint main() {\n    printf(\"Parent PID: %d\\n\", getpid());\n    \n    pid_t pid = fork();  // 프로세스 복제\n    \n    if (pid < 0) {\n        perror(\"fork failed\");\n        return 1;\n    } else if (pid == 0) {\n        // 자식 프로세스\n        printf(\"Child PID: %d, Parent: %d\\n\", getpid(), getppid());\n        execl(\"/bin/ls\", \"ls\", \"-la\", NULL);  // 새 프로그램 실행\n    } else {\n        // 부모 프로세스\n        printf(\"Created child with PID: %d\\n\", pid);\n        wait(NULL);  // 자식 종료 대기\n        printf(\"Child finished\\n\");\n    }\n    return 0;\n}\n\n// Java - 프로세스 생성\npublic class ProcessExample {\n    public static void main(String[] args) throws Exception {\n        // ProcessBuilder로 새 프로세스 생성\n        ProcessBuilder pb = new ProcessBuilder(\"notepad.exe\", \"test.txt\");\n        pb.directory(new File(\"C:/temp\"));\n        pb.environment().put(\"MY_VAR\", \"value\");\n        \n        Process process = pb.start();  // 프로세스 시작\n        \n        // 프로세스 출력 읽기\n        BufferedReader reader = new BufferedReader(\n            new InputStreamReader(process.getInputStream()));\n        String line;\n        while ((line = reader.readLine()) != null) {\n            System.out.println(line);\n        }\n        \n        int exitCode = process.waitFor();  // 종료 대기\n        System.out.println(\"Exit code: \" + exitCode);\n    }\n}\n\n// Spring에서 외부 프로세스 실행\n@Service\npublic class CommandService {\n    public String executeCommand(String command) {\n        try {\n            Process process = Runtime.getRuntime().exec(command);\n            // ... 결과 처리\n        } catch (IOException e) {\n            log.error(\"Command execution failed\", e);\n        }\n    }\n}"
            },
            {
                "type": "tip",
                "title": "💡 체크리스트 & 면접",
                "content": "**프로그램 vs 프로세스 비교**\n| 구분 | 프로그램 | 프로세스 |\n|------|----------|----------|\n| 상태 | 정적 | 동적 |\n| 저장 위치 | 디스크 | 메모리 |\n| 자원 소유 | X | O (메모리, 파일 등) |\n| 생명주기 | 없음 | 있음 (생성-종료) |\n| 개수 | 1개 | 여러 개 가능 |\n\n**프로세스 생성 시스템 콜**\n| 시스템 콜 | 역할 | 특징 |\n|----------|------|------|\n| fork() | 프로세스 복제 | 부모와 동일한 복사본 |\n| exec() | 프로그램 교체 | 코드/데이터 새로 로드 |\n| wait() | 자식 종료 대기 | 좀비 방지 |\n| exit() | 프로세스 종료 | 자원 반납 |\n\n**면접 질문**\n\n[주니어]\nQ: 프로그램과 프로세스의 차이점은?\nA: 프로그램은 디스크에 저장된 정적인 실행 파일이고, 프로세스는 그 프로그램이 메모리에 로드되어 실행 중인 동적인 상태입니다. 하나의 프로그램에서 여러 프로세스가 생성될 수 있습니다.\n\n[시니어]\nQ: fork()가 Copy-on-Write를 사용하는 이유는?\nA: fork() 시 자식 프로세스의 전체 메모리를 즉시 복사하면 비효율적입니다. 대신 부모와 자식이 같은 물리 페이지를 공유하고, 둘 중 하나가 수정할 때만 해당 페이지를 복사합니다. 이로써 fork() 직후 exec()하는 일반적인 패턴에서 불필요한 복사를 피할 수 있습니다."
            }
        ]
    }

def get_thread_concept_content():
    """02_프로세스스레드/thread-concept - 스레드 개념"""
    return {
        "id": "02_프로세스스레드/thread-concept",
        "title": "스레드 개념",
        "category": "os",
        "subCategory": "02_프로세스스레드",
        "language": "C",
        "description": "프로세스 내 실행 흐름인 스레드의 개념과 특징을 이해합니다.",
        "isPlaceholder": False,
        "sections": [
            {
                "type": "concept",
                "title": "🎯 스레드 개념 완전 정복",
                "content": "**한 줄 요약**: 스레드는 프로세스 내에서 실행되는 가벼운 실행 단위로, 같은 프로세스의 스레드들은 메모리(Code, Data, Heap)를 공유합니다.\n\n**초등학생도 이해할 비유 - 같은 주방의 요리사들**\n\n레스토랑 주방을 상상해보세요:\n- 주방(프로세스) - 요리하는 공간 전체\n- 요리사들(스레드) - 같은 주방에서 일하는 사람들\n- 냉장고/조리대(공유 메모리) - 모든 요리사가 함께 사용\n- 개인 도마(Stack) - 각 요리사의 개인 작업 공간\n\n**스레드의 특징:**\n1. 프로세스 내 실행 흐름\n2. Code, Data, Heap 영역 공유\n3. 각자 독립적인 Stack과 레지스터\n4. 같은 프로세스 내 스레드끼리 빠른 통신\n\n**왜 스레드를 사용하는가?**\n- 병렬 처리로 성능 향상\n- 프로세스보다 생성/전환 비용 저렴\n- 메모리 공유로 통신 간편\n- 응답성 향상 (UI + 백그라운드 작업)"
            },
            {
                "type": "code",
                "title": "💻 동작 원리",
                "language": "text",
                "code": "프로세스 vs 스레드 메모리 구조:\n\n  멀티프로세스                    멀티스레드\n ┌─────────────┐                ┌─────────────────────────┐\n │ Process A   │                │       Process           │\n │ ┌─────────┐ │                │ ┌─────────────────────┐ │\n │ │  Code   │ │                │ │       Code          │ │\n │ ├─────────┤ │                │ ├─────────────────────┤ │\n │ │  Data   │ │                │ │       Data          │ │\n │ ├─────────┤ │                │ ├─────────────────────┤ │\n │ │  Heap   │ │                │ │       Heap          │ │\n │ ├─────────┤ │                │ ├─────────────────────┤ │\n │ │  Stack  │ │                │ │ Stack A │ Stack B   │ │\n │ └─────────┘ │                │ └─────────┴───────────┘ │\n └─────────────┘                │  Thread A   Thread B    │\n ┌─────────────┐                └─────────────────────────┘\n │ Process B   │                  ▲ 메모리 공유\n │ ┌─────────┐ │\n │ │  Code   │ │\n │ ├─────────┤ │\n │ │  Data   │ │  ← 완전히 분리\n │ ├─────────┤ │\n │ │  Heap   │ │\n │ ├─────────┤ │\n │ │  Stack  │ │\n │ └─────────┘ │\n └─────────────┘\n\n스레드별 독립/공유 영역:\n┌─────────────────────────────────────────────────┐\n│              프로세스 메모리                     │\n├─────────────────────────────────────────────────┤\n│ [공유]                                          │\n│  - Code: 실행 코드                              │\n│  - Data: 전역/정적 변수                         │\n│  - Heap: 동적 할당 메모리                       │\n│  - 파일 디스크립터, 시그널 핸들러               │\n├─────────────────────────────────────────────────┤\n│ [스레드별 독립]                                 │\n│  - Stack: 지역변수, 함수 호출 정보              │\n│  - PC(Program Counter): 다음 실행 명령어        │\n│  - 레지스터 집합                                │\n│  - 스레드 ID (TID)                              │\n└─────────────────────────────────────────────────┘"
            },
            {
                "type": "code",
                "title": "🔧 실무 활용",
                "language": "java",
                "code": "// Java 스레드 생성 방법 1: Thread 상속\nclass MyThread extends Thread {\n    @Override\n    public void run() {\n        System.out.println(\"Thread: \" + Thread.currentThread().getName());\n    }\n}\n\n// 방법 2: Runnable 구현 (권장)\nclass MyRunnable implements Runnable {\n    @Override\n    public void run() {\n        System.out.println(\"Runnable: \" + Thread.currentThread().getName());\n    }\n}\n\n// 방법 3: Lambda (Java 8+)\nThread thread = new Thread(() -> {\n    System.out.println(\"Lambda Thread\");\n});\n\n// 스레드 실행\npublic class ThreadExample {\n    public static void main(String[] args) {\n        // 스레드 생성 및 시작\n        Thread t1 = new MyThread();\n        Thread t2 = new Thread(new MyRunnable());\n        Thread t3 = new Thread(() -> System.out.println(\"Lambda\"));\n        \n        t1.start();  // run()이 아닌 start() 호출!\n        t2.start();\n        t3.start();\n        \n        // 스레드 종료 대기\n        try {\n            t1.join();\n            t2.join();\n            t3.join();\n        } catch (InterruptedException e) {\n            Thread.currentThread().interrupt();\n        }\n    }\n}\n\n// Spring에서 비동기 처리\n@Service\npublic class AsyncService {\n    \n    @Async  // 별도 스레드에서 실행\n    public CompletableFuture<String> asyncMethod() {\n        // 시간이 오래 걸리는 작업\n        return CompletableFuture.completedFuture(\"Done\");\n    }\n}\n\n// 스레드 풀 사용 (권장)\n@Configuration\n@EnableAsync\npublic class AsyncConfig {\n    @Bean\n    public Executor taskExecutor() {\n        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();\n        executor.setCorePoolSize(10);\n        executor.setMaxPoolSize(50);\n        executor.setQueueCapacity(100);\n        executor.setThreadNamePrefix(\"Async-\");\n        executor.initialize();\n        return executor;\n    }\n}"
            },
            {
                "type": "tip",
                "title": "💡 체크리스트 & 면접",
                "content": "**스레드 공유/독립 영역**\n| 영역 | 공유 여부 | 설명 |\n|------|----------|------|\n| Code | 공유 | 실행 코드 |\n| Data | 공유 | 전역/정적 변수 |\n| Heap | 공유 | 동적 할당 객체 |\n| Stack | 독립 | 지역변수, 매개변수 |\n| PC/레지스터 | 독립 | 실행 위치, CPU 상태 |\n\n**스레드 장단점**\n| 장점 | 단점 |\n|------|------|\n| 생성 비용 낮음 | 동기화 필요 |\n| 컨텍스트 스위칭 빠름 | 하나가 죽으면 전체 영향 |\n| 메모리 공유로 통신 쉬움 | 디버깅 어려움 |\n| 응답성 향상 | 공유 자원 경쟁 |\n\n**면접 질문**\n\n[주니어]\nQ: 스레드가 공유하는 자원과 독립적인 자원은?\nA: Code, Data, Heap 영역과 파일 디스크립터는 공유합니다. 반면 Stack, Program Counter, 레지스터는 각 스레드가 독립적으로 가집니다. 이로 인해 스레드 간 통신은 쉽지만 동기화가 필요합니다.\n\n[시니어]\nQ: 사용자 수준 스레드와 커널 수준 스레드의 차이는?\nA: 사용자 수준 스레드는 라이브러리가 관리하여 커널이 모르므로 전환이 빠르지만, 하나가 블로킹되면 전체가 멈춥니다. 커널 수준 스레드는 OS가 직접 관리하여 블로킹 시에도 다른 스레드가 실행되지만, 전환 비용이 큽니다. Java의 스레드는 1:1 모델로 커널 스레드와 매핑됩니다."
            }
        ]
    }

def get_process_vs_thread_content():
    """02_프로세스스레드/process-vs-thread - 프로세스 vs 스레드 비교"""
    return {
        "id": "02_프로세스스레드/process-vs-thread",
        "title": "프로세스 vs 스레드 비교",
        "category": "os",
        "subCategory": "02_프로세스스레드",
        "language": "C",
        "description": "프로세스와 스레드의 차이점을 비교하고 적절한 선택 기준을 이해합니다.",
        "isPlaceholder": False,
        "sections": [
            {
                "type": "concept",
                "title": "🎯 프로세스 vs 스레드 완전 정복",
                "content": "**한 줄 요약**: 프로세스는 독립된 메모리 공간을 가진 실행 단위이고, 스레드는 프로세스 내에서 메모리를 공유하는 가벼운 실행 단위입니다.\n\n**초등학생도 이해할 비유 - 집과 방**\n\n아파트를 상상해보세요:\n- 각 세대(프로세스) - 독립된 공간, 이웃집에 못 들어감\n- 세대 내 방들(스레드) - 거실/주방은 공유, 각자 방은 개인\n\n**프로세스 = 독립된 세대**\n- 자기만의 주방, 화장실 (독립 메모리)\n- 이웃과 소통하려면 초인종, 전화 (IPC)\n- 한 세대 문제가 다른 세대에 영향 X\n\n**스레드 = 같은 세대의 가족**\n- 거실, 주방 함께 사용 (공유 메모리)\n- 말로 바로 소통 (직접 통신)\n- 한 사람이 물 틀어놓으면 다른 사람도 영향\n\n**언제 무엇을 선택?**\n- 프로세스: 안정성 중요, 독립 실행 필요\n- 스레드: 성능 중요, 데이터 공유 필요"
            },
            {
                "type": "code",
                "title": "💻 동작 원리",
                "language": "text",
                "code": "프로세스 vs 스레드 비교 다이어그램:\n\n┌─────────── 멀티프로세스 ───────────┐  ┌─────────── 멀티스레드 ───────────┐\n│                                    │  │                                  │\n│  Process A       Process B         │  │           Process                │\n│ ┌──────────┐   ┌──────────┐       │  │ ┌──────────────────────────────┐ │\n│ │ Code     │   │ Code     │       │  │ │         Code (공유)          │ │\n│ ├──────────┤   ├──────────┤       │  │ ├──────────────────────────────┤ │\n│ │ Data     │   │ Data     │       │  │ │         Data (공유)          │ │\n│ ├──────────┤   ├──────────┤       │  │ ├──────────────────────────────┤ │\n│ │ Heap     │   │ Heap     │       │  │ │         Heap (공유)          │ │\n│ ├──────────┤   ├──────────┤       │  │ ├──────────┬───────────────────┤ │\n│ │ Stack    │   │ Stack    │       │  │ │ Stack A  │      Stack B      │ │\n│ └──────────┘   └──────────┘       │  │ └──────────┴───────────────────┘ │\n│       ↑              ↑             │  │  Thread A      Thread B          │\n│       └──── IPC ─────┘             │  │       ↑            ↑              │\n│          (파이프, 소켓)             │  │       └── 직접 접근 ─┘             │\n└────────────────────────────────────┘  └──────────────────────────────────┘\n\n비용 비교:\n┌────────────────────────────────────────────────────────────────┐\n│                    생성 비용                                    │\n├────────────────────────────────────────────────────────────────┤\n│ 프로세스: ████████████████████████████████  (메모리 복사, PCB) │\n│ 스레드:   ████████  (Stack만 할당)                              │\n└────────────────────────────────────────────────────────────────┘\n\n┌────────────────────────────────────────────────────────────────┐\n│                컨텍스트 스위칭 비용                              │\n├────────────────────────────────────────────────────────────────┤\n│ 프로세스: ████████████████████████  (전체 메모리 맵 전환)       │\n│ 스레드:   ████████  (Stack, 레지스터만)                         │\n└────────────────────────────────────────────────────────────────┘\n\n┌────────────────────────────────────────────────────────────────┐\n│                    통신 비용                                    │\n├────────────────────────────────────────────────────────────────┤\n│ 프로세스: ████████████████  (IPC 필요 - 커널 경유)              │\n│ 스레드:   ████  (공유 메모리 직접 접근)                         │\n└────────────────────────────────────────────────────────────────┘"
            },
            {
                "type": "code",
                "title": "🔧 실무 활용",
                "language": "java",
                "code": "// 멀티프로세스 예시: Chrome 브라우저\n// - 각 탭이 독립 프로세스\n// - 한 탭 크래시가 다른 탭에 영향 X\n\n// Java에서 멀티프로세스\npublic class MultiProcessExample {\n    public static void main(String[] args) throws Exception {\n        // 별도 프로세스로 실행\n        ProcessBuilder pb = new ProcessBuilder(\"java\", \"-jar\", \"worker.jar\");\n        Process worker1 = pb.start();\n        Process worker2 = pb.start();\n        // 각 워커는 독립된 JVM (힙, 스택 모두 분리)\n    }\n}\n\n// 멀티스레드 예시: 웹 서버\n// - 요청마다 스레드 할당\n// - 공유 데이터(캐시, 커넥션 풀) 활용\n\n// Java에서 멀티스레드\npublic class MultiThreadExample {\n    private static int sharedCounter = 0;  // 공유 자원\n    \n    public static void main(String[] args) {\n        // ExecutorService로 스레드 풀 관리\n        ExecutorService executor = Executors.newFixedThreadPool(10);\n        \n        for (int i = 0; i < 100; i++) {\n            executor.submit(() -> {\n                // 공유 자원 접근 시 동기화 필요!\n                synchronized (MultiThreadExample.class) {\n                    sharedCounter++;\n                }\n            });\n        }\n        \n        executor.shutdown();\n    }\n}\n\n// 실무 선택 기준\n/*\n멀티프로세스 선택:\n- 안정성이 최우선 (한 프로세스 죽어도 서비스 유지)\n- 언어가 다른 컴포넌트 연동\n- CPU 집약적 작업 (GIL 우회 - Python)\n\n멀티스레드 선택:\n- 성능이 최우선 (빠른 통신, 낮은 오버헤드)\n- 데이터 공유가 많은 경우\n- I/O 바운드 작업 (웹 서버, DB 접근)\n*/\n\n// Spring Boot: 기본적으로 멀티스레드 (톰캣 스레드 풀)\nserver:\n  tomcat:\n    threads:\n      max: 200      # 최대 스레드\n      min-spare: 10 # 최소 유지 스레드"
            },
            {
                "type": "tip",
                "title": "💡 체크리스트 & 면접",
                "content": "**프로세스 vs 스레드 종합 비교**\n| 항목 | 프로세스 | 스레드 |\n|------|----------|--------|\n| 메모리 | 독립 공간 | 공유 (Stack만 독립) |\n| 생성 비용 | 높음 | 낮음 |\n| 컨텍스트 스위칭 | 느림 | 빠름 |\n| 통신 | IPC (느림) | 공유 메모리 (빠름) |\n| 안정성 | 높음 (격리) | 낮음 (영향 전파) |\n| 동기화 | 불필요 | 필요 |\n| 디버깅 | 쉬움 | 어려움 |\n\n**실무 선택 가이드**\n| 상황 | 추천 | 이유 |\n|------|------|------|\n| 웹 서버 | 스레드 | 빠른 응답, 커넥션 풀 공유 |\n| 브라우저 탭 | 프로세스 | 탭 간 격리, 보안 |\n| CPU 집약 연산 | 프로세스 | 멀티코어 활용 |\n| I/O 바운드 | 스레드 | 대기 시간 활용 |\n\n**면접 질문**\n\n[주니어]\nQ: 프로세스와 스레드의 차이점은?\nA: 프로세스는 독립된 메모리 공간을 가져 서로 직접 접근이 불가능하고 IPC로 통신합니다. 스레드는 같은 프로세스 내에서 Code, Data, Heap을 공유하며, Stack만 독립적입니다. 스레드가 생성/전환 비용이 낮지만 동기화가 필요합니다.\n\n[시니어]\nQ: 대규모 트래픽 처리 시 멀티프로세스와 멀티스레드 중 어떤 것을 선택하겠습니까?\nA: 상황에 따라 다릅니다. 웹 서버는 멀티스레드 + 이벤트 루프(Netty, WebFlux)로 I/O 대기 시간을 활용합니다. CPU 집약적 작업은 프로세스 분리 또는 워커 스레드 풀을 사용합니다. 실제로는 둘을 조합하여 멀티프로세스(수평 확장) + 멀티스레드(프로세스 내 동시성)로 구성합니다."
            }
        ]
    }

def main():
    # Read existing os.json
    with open(OS_JSON_PATH, 'r', encoding='utf-8') as f:
        os_data = json.load(f)

    # Update with new content
    topics = [
        get_os_intro_content(),
        get_os_structure_content(),
        get_kernel_content(),
        get_system_call_content(),
        get_process_memory_content(),
        get_pcb_content(),
        get_process_state_content(),
        get_ipc_content(),
        get_process_concept_content(),
        get_thread_concept_content(),
        get_process_vs_thread_content(),
    ]

    for topic in topics:
        topic_id = topic["id"]
        os_data[topic_id] = topic
        print(f"Updated: {topic_id}")

    # Write back to os.json
    with open(OS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(os_data, f, ensure_ascii=False, indent=2)

    print(f"\nSuccessfully updated {len(topics)} topics in os.json")

if __name__ == "__main__":
    main()
