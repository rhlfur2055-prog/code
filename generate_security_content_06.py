#!/usr/bin/env python3
"""
Generate Security Content 06 - Updates security.json with practical security content
Topics: spring-security, sensitive-data, logging-security, input-validation,
        password-policy, security-header, interview-security, index
"""

import json
import os

def get_security_content():
    """Returns the security content to update"""

    return {
        "06_실무/spring-security": {
            "id": "06_실무/spring-security",
            "title": "Spring Security 완벽 가이드",
            "category": "security",
            "subCategory": "06_실무",
            "language": "Java",
            "description": "Spring Security의 핵심 개념부터 JWT 인증, OAuth2까지 실무에 필요한 모든 보안 설정을 학습합니다.",
            "isPlaceholder": False,
            "sections": [
                {
                    "type": "concept",
                    "title": "Spring Security 핵심 개념",
                    "content": "## Spring Security란?\n\n> Spring 기반 애플리케이션의 인증(Authentication)과 인가(Authorization)를 담당하는 보안 프레임워크\n\n---\n\n## 핵심 구성요소\n\n```\n[요청] -> [Security Filter Chain] -> [Controller]\n              |\n    +-------------------+\n    | Authentication    | - 인증 (누구인가?)\n    | Authorization     | - 인가 (권한이 있는가?)\n    | Session Management| - 세션 관리\n    | CSRF Protection   | - CSRF 방어\n    +-------------------+\n```\n\n### SecurityFilterChain 동작 순서\n\n1. **SecurityContextPersistenceFilter**: 세션에서 인증 정보 복원\n2. **UsernamePasswordAuthenticationFilter**: 로그인 처리\n3. **ExceptionTranslationFilter**: 보안 예외 처리\n4. **FilterSecurityInterceptor**: 최종 인가 결정\n\n---\n\n## 인증 vs 인가\n\n| 구분 | 인증 (Authentication) | 인가 (Authorization) |\n|------|----------------------|---------------------|\n| 질문 | 누구인가? | 권한이 있는가? |\n| 시점 | 로그인 시 | 리소스 접근 시 |\n| 실패 | 401 Unauthorized | 403 Forbidden |\n| 예시 | ID/PW 검증 | ADMIN만 접근 허용 |"
                },
                {
                    "type": "code",
                    "title": "Spring Security 6.x 설정",
                    "language": "java",
                    "content": "```java\n@Configuration\n@EnableWebSecurity\n@EnableMethodSecurity(prePostEnabled = true)\npublic class SecurityConfig {\n\n    @Bean\n    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {\n        http\n            // 1. CSRF 설정 (REST API는 비활성화)\n            .csrf(csrf -> csrf.disable())\n            \n            // 2. 세션 정책 (JWT 사용 시 STATELESS)\n            .sessionManagement(session -> session\n                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)\n            )\n            \n            // 3. 경로별 권한 설정\n            .authorizeHttpRequests(auth -> auth\n                .requestMatchers(\"/api/auth/**\").permitAll()\n                .requestMatchers(\"/api/public/**\").permitAll()\n                .requestMatchers(\"/api/admin/**\").hasRole(\"ADMIN\")\n                .requestMatchers(\"/api/user/**\").hasAnyRole(\"USER\", \"ADMIN\")\n                .anyRequest().authenticated()\n            )\n            \n            // 4. JWT 필터 추가\n            .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class)\n            \n            // 5. 예외 처리\n            .exceptionHandling(ex -> ex\n                .authenticationEntryPoint(jwtAuthEntryPoint)\n                .accessDeniedHandler(customAccessDeniedHandler)\n            );\n\n        return http.build();\n    }\n\n    @Bean\n    public PasswordEncoder passwordEncoder() {\n        return new BCryptPasswordEncoder(12);\n    }\n\n    @Bean\n    public AuthenticationManager authManager(AuthenticationConfiguration config) throws Exception {\n        return config.getAuthenticationManager();\n    }\n}\n```"
                },
                {
                    "type": "code",
                    "title": "JWT 인증 필터 구현",
                    "language": "java",
                    "content": "```java\n@Component\n@RequiredArgsConstructor\npublic class JwtAuthenticationFilter extends OncePerRequestFilter {\n\n    private final JwtTokenProvider jwtProvider;\n    private final UserDetailsService userDetailsService;\n\n    @Override\n    protected void doFilterInternal(HttpServletRequest request,\n            HttpServletResponse response, FilterChain filterChain)\n            throws ServletException, IOException {\n        \n        String token = extractToken(request);\n        \n        if (token != null && jwtProvider.validateToken(token)) {\n            String username = jwtProvider.getUsername(token);\n            UserDetails userDetails = userDetailsService.loadUserByUsername(username);\n            \n            UsernamePasswordAuthenticationToken auth =\n                new UsernamePasswordAuthenticationToken(\n                    userDetails, null, userDetails.getAuthorities());\n            \n            SecurityContextHolder.getContext().setAuthentication(auth);\n        }\n        \n        filterChain.doFilter(request, response);\n    }\n\n    private String extractToken(HttpServletRequest request) {\n        String header = request.getHeader(\"Authorization\");\n        if (header != null && header.startsWith(\"Bearer \")) {\n            return header.substring(7);\n        }\n        return null;\n    }\n}\n\n// JWT 토큰 제공자\n@Component\npublic class JwtTokenProvider {\n    @Value(\"${jwt.secret}\")\n    private String secretKey;\n    \n    @Value(\"${jwt.expiration}\")\n    private long validityInMs;\n\n    public String createToken(String username, List<String> roles) {\n        Claims claims = Jwts.claims().setSubject(username);\n        claims.put(\"roles\", roles);\n        \n        Date now = new Date();\n        Date validity = new Date(now.getTime() + validityInMs);\n        \n        return Jwts.builder()\n            .setClaims(claims)\n            .setIssuedAt(now)\n            .setExpiration(validity)\n            .signWith(SignatureAlgorithm.HS256, secretKey)\n            .compact();\n    }\n}\n```"
                },
                {
                    "type": "tip",
                    "title": "Spring Security 실무 체크리스트",
                    "content": "## 필수 보안 설정 체크리스트\n\n```\n[ ] HTTPS 강제 (http.requiresChannel().anyRequest().requiresSecure())\n[ ] CSRF 토큰 적용 (SPA는 Cookie 기반 토큰)\n[ ] 세션 고정 공격 방지 (sessionFixation().newSession())\n[ ] 동시 세션 제한 (maximumSessions(1))\n[ ] Remember-Me 보안 (persistentTokenRepository 사용)\n[ ] 로그인 실패 횟수 제한 (Account Lockout)\n[ ] 보안 헤더 설정 (X-Frame-Options, CSP 등)\n```\n\n## 메서드 레벨 보안\n\n```java\n@PreAuthorize(\"hasRole('ADMIN')\")\npublic void deleteUser(Long id) { }\n\n@PreAuthorize(\"#userId == authentication.principal.id\")\npublic User getUser(Long userId) { }\n\n@PostAuthorize(\"returnObject.owner == authentication.name\")\npublic Document getDocument(Long id) { }\n```\n\n## 자주 하는 실수\n\n| 실수 | 올바른 방법 |\n|------|------------|\n| 모든 경로 permitAll() | 화이트리스트 방식 사용 |\n| CSRF 무조건 비활성화 | REST API만 비활성화 |\n| 비밀번호 평문 저장 | BCrypt 해시 사용 |\n| JWT 만료시간 없음 | 적절한 만료시간 설정 |"
                }
            ]
        },

        "06_실무/sensitive-data": {
            "id": "06_실무/sensitive-data",
            "title": "민감 정보 관리 (API 키, 환경변수)",
            "category": "security",
            "subCategory": "06_실무",
            "language": "Java",
            "description": "API 키, 데이터베이스 비밀번호 등 민감 정보를 안전하게 관리하는 방법을 학습합니다.",
            "isPlaceholder": False,
            "sections": [
                {
                    "type": "concept",
                    "title": "민감 정보 관리 원칙",
                    "content": "## 민감 정보란?\n\n> 노출 시 보안 사고로 이어질 수 있는 모든 데이터\n\n---\n\n## 민감 정보 종류\n\n```\n[인증 정보]\n- API Keys (AWS, GCP, 외부 서비스)\n- Database 비밀번호\n- OAuth Client Secret\n- JWT Secret Key\n\n[개인정보]\n- 주민등록번호, 신용카드 번호\n- 비밀번호 (해시 전)\n- 개인 식별 정보 (PII)\n\n[인프라 정보]\n- 서버 IP, 포트\n- 내부 API 엔드포인트\n- 인증서, 개인키\n```\n\n---\n\n## 절대 하면 안 되는 것\n\n| 금지 | 이유 |\n|------|------|\n| 소스코드에 하드코딩 | Git에 노출됨 |\n| .env 파일 Git 커밋 | 이력에 영구 저장 |\n| 로그에 비밀번호 출력 | 로그 수집 시 노출 |\n| Slack/이메일로 공유 | 중간자 공격 가능 |\n| 주석에 비밀번호 기록 | 코드 리뷰 시 노출 |"
                },
                {
                    "type": "code",
                    "title": "환경변수 및 설정 관리",
                    "language": "java",
                    "content": "```java\n// application.yml - 환경별 설정\nspring:\n  profiles:\n    active: ${SPRING_PROFILES_ACTIVE:local}\n\n---\nspring:\n  config:\n    activate:\n      on-profile: local\n  datasource:\n    url: jdbc:h2:mem:testdb\n\n---\nspring:\n  config:\n    activate:\n      on-profile: prod\n  datasource:\n    url: ${DB_URL}\n    username: ${DB_USERNAME}\n    password: ${DB_PASSWORD}\n\njwt:\n  secret: ${JWT_SECRET}\n  expiration: 86400000\n\naws:\n  access-key: ${AWS_ACCESS_KEY_ID}\n  secret-key: ${AWS_SECRET_ACCESS_KEY}\n```\n\n```java\n// 환경변수 주입\n@Configuration\n@ConfigurationProperties(prefix = \"aws\")\n@Validated\npublic class AwsProperties {\n    @NotBlank\n    private String accessKey;\n    \n    @NotBlank\n    private String secretKey;\n    \n    // getters, setters\n}\n\n// 사용\n@Service\n@RequiredArgsConstructor\npublic class S3Service {\n    private final AwsProperties awsProps;\n    \n    public void upload() {\n        // awsProps.getAccessKey() 사용\n    }\n}\n```"
                },
                {
                    "type": "code",
                    "title": "Vault / Secret Manager 연동",
                    "language": "java",
                    "content": "```java\n// HashiCorp Vault 연동 (Spring Cloud Vault)\n// build.gradle\nimplementation 'org.springframework.cloud:spring-cloud-starter-vault-config'\n\n// bootstrap.yml\nspring:\n  cloud:\n    vault:\n      uri: https://vault.company.com\n      token: ${VAULT_TOKEN}\n      kv:\n        enabled: true\n        backend: secret\n        default-context: myapp\n\n// AWS Secrets Manager 연동\n@Configuration\npublic class SecretsManagerConfig {\n    \n    public String getSecret(String secretName) {\n        AWSSecretsManager client = AWSSecretsManagerClientBuilder.standard()\n            .withRegion(Regions.AP_NORTHEAST_2)\n            .build();\n        \n        GetSecretValueRequest request = new GetSecretValueRequest()\n            .withSecretId(secretName);\n        \n        GetSecretValueResult result = client.getSecretValue(request);\n        return result.getSecretString();\n    }\n}\n\n// Docker 환경 - docker-compose.yml\nservices:\n  app:\n    environment:\n      - DB_PASSWORD_FILE=/run/secrets/db_password\n    secrets:\n      - db_password\n\nsecrets:\n  db_password:\n    file: ./secrets/db_password.txt\n```"
                },
                {
                    "type": "tip",
                    "title": "Git에서 민감 정보 제거",
                    "content": "## .gitignore 필수 항목\n\n```\n# 환경 설정\n.env\n.env.local\n.env.*.local\napplication-local.yml\napplication-prod.yml\n\n# 키/인증서\n*.pem\n*.key\n*.p12\n*.jks\n\n# IDE 설정\n.idea/\n*.iml\n```\n\n## 실수로 커밋한 경우 대처법\n\n```bash\n# 1. 즉시 키 무효화 (가장 중요!)\n# AWS Console에서 Access Key 삭제 후 재발급\n\n# 2. Git 히스토리에서 제거\ngit filter-branch --force --index-filter \\\n  \"git rm --cached --ignore-unmatch secrets.yml\" \\\n  --prune-empty --tag-name-filter cat -- --all\n\n# 3. 강제 푸시\ngit push origin --force --all\n\n# 4. BFG Repo-Cleaner (더 빠름)\nbfg --delete-files secrets.yml\nbfg --replace-text passwords.txt\n```\n\n## 감사 로그 남기기\n\n```java\n@Aspect\n@Component\npublic class SensitiveDataAudit {\n    @Around(\"@annotation(SensitiveAccess)\")\n    public Object audit(ProceedingJoinPoint pjp) {\n        String user = SecurityContextHolder.getContext()\n            .getAuthentication().getName();\n        log.info(\"[SENSITIVE ACCESS] User: {}, Method: {}\",\n            user, pjp.getSignature().getName());\n        return pjp.proceed();\n    }\n}\n```"
                }
            ]
        },

        "06_실무/logging-security": {
            "id": "06_실무/logging-security",
            "title": "보안 로깅 전략",
            "category": "security",
            "subCategory": "06_실무",
            "language": "Java",
            "description": "보안 이벤트 로깅, 민감 정보 마스킹, 침입 탐지를 위한 로깅 전략을 학습합니다.",
            "isPlaceholder": False,
            "sections": [
                {
                    "type": "concept",
                    "title": "보안 로깅 원칙",
                    "content": "## 왜 보안 로깅이 중요한가?\n\n> OWASP Top 10 A09: Security Logging and Monitoring Failures\n> 로깅 부재 시 침입 탐지 및 사후 분석 불가능\n\n---\n\n## 필수 로깅 이벤트\n\n```\n[인증 관련]\n- 로그인 성공/실패\n- 비밀번호 변경\n- 로그아웃\n- 세션 만료\n\n[권한 관련]\n- 권한 변경\n- 접근 거부 (403)\n- 관리자 작업\n\n[데이터 관련]\n- 민감 정보 조회\n- 대량 데이터 다운로드\n- 데이터 수정/삭제\n\n[시스템 관련]\n- 설정 변경\n- 비정상 트래픽\n- 오류 패턴\n```\n\n---\n\n## 로그 레벨 가이드\n\n| 레벨 | 용도 | 예시 |\n|------|------|------|\n| ERROR | 보안 사고 | 인증 우회 시도 |\n| WARN | 의심 행위 | 로그인 5회 실패 |\n| INFO | 정상 이벤트 | 로그인 성공 |\n| DEBUG | 개발용 | 상세 요청 정보 |"
                },
                {
                    "type": "code",
                    "title": "보안 이벤트 로깅 구현",
                    "language": "java",
                    "content": "```java\n@Slf4j\n@Component\npublic class SecurityEventLogger {\n\n    // 구조화된 로그 포맷\n    public void logSecurityEvent(SecurityEvent event) {\n        MDC.put(\"eventType\", event.getType());\n        MDC.put(\"userId\", event.getUserId());\n        MDC.put(\"ip\", event.getIpAddress());\n        MDC.put(\"timestamp\", Instant.now().toString());\n        \n        log.info(\"[SECURITY] {} - User: {}, IP: {}, Details: {}\",\n            event.getType(),\n            event.getUserId(),\n            event.getIpAddress(),\n            event.getDetails());\n        \n        MDC.clear();\n    }\n\n    // 로그인 실패 추적\n    public void logLoginFailure(String username, String ip, String reason) {\n        log.warn(\"[AUTH FAILURE] User: {}, IP: {}, Reason: {}, Attempts: {}\",\n            username, ip, reason, getFailedAttempts(username));\n        \n        if (getFailedAttempts(username) >= 5) {\n            log.error(\"[BRUTE FORCE ALERT] User: {}, IP: {} - Account locked\",\n                username, ip);\n            alertSecurityTeam(username, ip);\n        }\n    }\n\n    // 권한 상승 시도 감지\n    public void logPrivilegeEscalation(String user, String resource) {\n        log.error(\"[PRIVILEGE ESCALATION] User: {} attempted to access: {}\",\n            user, resource);\n    }\n}\n\n// AOP 기반 자동 로깅\n@Aspect\n@Component\n@Slf4j\npublic class SecurityAuditAspect {\n\n    @AfterReturning(\"@annotation(PreAuthorize)\")\n    public void logAuthorizedAccess(JoinPoint jp) {\n        String user = getCurrentUser();\n        String method = jp.getSignature().toShortString();\n        log.info(\"[ACCESS GRANTED] User: {}, Method: {}\", user, method);\n    }\n\n    @AfterThrowing(pointcut = \"@annotation(PreAuthorize)\", throwing = \"ex\")\n    public void logAccessDenied(JoinPoint jp, AccessDeniedException ex) {\n        String user = getCurrentUser();\n        String method = jp.getSignature().toShortString();\n        log.warn(\"[ACCESS DENIED] User: {}, Method: {}\", user, method);\n    }\n}\n```"
                },
                {
                    "type": "code",
                    "title": "민감 정보 마스킹",
                    "language": "java",
                    "content": "```java\n// Logback 마스킹 패턴\n// logback-spring.xml\n<configuration>\n    <conversionRule conversionWord=\"mask\" \n        converterClass=\"com.example.MaskingConverter\"/>\n    \n    <appender name=\"CONSOLE\" class=\"ch.qos.logback.core.ConsoleAppender\">\n        <encoder>\n            <pattern>%d{HH:mm:ss} %-5level %mask(%msg)%n</pattern>\n        </encoder>\n    </appender>\n</configuration>\n\n// 마스킹 컨버터 구현\npublic class MaskingConverter extends MessageConverter {\n    private static final Pattern CARD_PATTERN = \n        Pattern.compile(\"(\\\\d{4})-?(\\\\d{4})-?(\\\\d{4})-?(\\\\d{4})\");\n    private static final Pattern SSN_PATTERN = \n        Pattern.compile(\"(\\\\d{6})-?(\\\\d{7})\");\n    private static final Pattern PASSWORD_PATTERN = \n        Pattern.compile(\"(password|pwd|passwd)[=:]\\\\s*([^\\\\s,}]+)\", Pattern.CASE_INSENSITIVE);\n\n    @Override\n    public String convert(ILoggingEvent event) {\n        String message = event.getFormattedMessage();\n        \n        // 카드번호 마스킹: 1234-5678-9012-3456 -> 1234-****-****-3456\n        message = CARD_PATTERN.matcher(message)\n            .replaceAll(\"$1-****-****-$4\");\n        \n        // 주민번호 마스킹: 900101-1234567 -> 900101-*******\n        message = SSN_PATTERN.matcher(message)\n            .replaceAll(\"$1-*******\");\n        \n        // 비밀번호 마스킹: password=secret -> password=*****\n        message = PASSWORD_PATTERN.matcher(message)\n            .replaceAll(\"$1=*****\");\n        \n        return message;\n    }\n}\n\n// 요청/응답 마스킹 필터\n@Component\npublic class SensitiveDataFilter extends OncePerRequestFilter {\n    \n    private final Set<String> sensitiveFields = Set.of(\n        \"password\", \"cardNumber\", \"ssn\", \"secret\");\n\n    @Override\n    protected void doFilterInternal(HttpServletRequest request,\n            HttpServletResponse response, FilterChain chain) {\n        ContentCachingRequestWrapper wrappedRequest = \n            new ContentCachingRequestWrapper(request);\n        chain.doFilter(wrappedRequest, response);\n        \n        String body = maskSensitiveData(wrappedRequest.getContentAsString());\n        log.debug(\"Request: {}\", body);\n    }\n}\n```"
                },
                {
                    "type": "tip",
                    "title": "로그 분석 및 알림",
                    "content": "## ELK Stack 연동\n\n```yaml\n# logback-spring.xml - JSON 포맷\n<appender name=\"LOGSTASH\" class=\"net.logstash.logback.appender.LogstashTcpSocketAppender\">\n    <destination>logstash:5000</destination>\n    <encoder class=\"net.logstash.logback.encoder.LogstashEncoder\">\n        <includeMdc>true</includeMdc>\n        <customFields>{\"app\":\"my-service\"}</customFields>\n    </encoder>\n</appender>\n```\n\n## 실시간 알림 설정\n\n```java\n@Component\npublic class SecurityAlertService {\n    \n    @Async\n    public void sendAlert(SecurityEvent event) {\n        if (event.getSeverity() >= Severity.HIGH) {\n            slackNotifier.send(\"#security-alerts\", \n                formatAlert(event));\n            emailService.sendToSecurityTeam(event);\n        }\n    }\n}\n```\n\n## 로그 보존 정책\n\n| 로그 유형 | 보존 기간 | 이유 |\n|----------|----------|------|\n| 인증 로그 | 1년 | 감사 추적 |\n| 접근 로그 | 6개월 | 법적 요구사항 |\n| 에러 로그 | 3개월 | 문제 분석 |\n| 디버그 로그 | 7일 | 디스크 용량 |\n\n## 로그 무결성 보장\n\n```bash\n# 로그 파일 해시 생성\nsha256sum /var/log/app/*.log > /var/log/checksums/$(date +%Y%m%d).sha256\n\n# 중앙 로그 서버 전송 (변조 방지)\nrsyslog -> 중앙 서버 (WORM 스토리지)\n```"
                }
            ]
        },

        "04_실무/input-validation": {
            "id": "04_실무/input-validation",
            "title": "입력값 검증",
            "category": "security",
            "subCategory": "04_실무",
            "language": "Java",
            "description": "SQL Injection, XSS 등을 방지하기 위한 입력값 검증 기법을 학습합니다.",
            "isPlaceholder": False,
            "sections": [
                {
                    "type": "concept",
                    "title": "입력값 검증 원칙",
                    "content": "## 핵심 원칙\n\n> **Never Trust User Input** - 모든 사용자 입력은 악의적이라고 가정\n\n---\n\n## 검증 위치\n\n```\n[클라이언트]     [서버]         [DB]\n    |\n   UX용          필수!          최종 방어\n   (우회 가능)   (화이트리스트)  (Prepared Statement)\n```\n\n**3중 방어 전략:**\n1. 프론트엔드: 사용자 경험 (우회 가능)\n2. 백엔드: 필수 검증 (핵심)\n3. 데이터베이스: 최종 방어선\n\n---\n\n## 검증 유형\n\n| 유형 | 설명 | 예시 |\n|------|------|------|\n| 형식 검증 | 타입, 길이, 패턴 | 이메일 정규식 |\n| 범위 검증 | 최소/최대값 | 나이 1-150 |\n| 비즈니스 검증 | 도메인 규칙 | 재고보다 많이 주문 불가 |\n| 인코딩 검증 | 특수문자 처리 | HTML 이스케이프 |\n\n---\n\n## 화이트리스트 vs 블랙리스트\n\n```\n화이트리스트 (권장): 허용된 것만 통과\n  예: [a-zA-Z0-9] 문자만 허용\n\n블랙리스트 (비권장): 금지된 것만 차단\n  예: <script> 태그만 차단 -> <SCRIPT> 우회 가능\n```"
                },
                {
                    "type": "code",
                    "title": "Bean Validation 활용",
                    "language": "java",
                    "content": "```java\n// DTO with Validation\npublic class UserCreateRequest {\n\n    @NotBlank(message = \"이메일은 필수입니다\")\n    @Email(message = \"올바른 이메일 형식이 아닙니다\")\n    @Size(max = 100, message = \"이메일은 100자 이하\")\n    private String email;\n\n    @NotBlank(message = \"비밀번호는 필수입니다\")\n    @Size(min = 8, max = 20, message = \"비밀번호는 8-20자\")\n    @Pattern(regexp = \"^(?=.*[A-Z])(?=.*[a-z])(?=.*\\\\d)(?=.*[@#$%]).+$\",\n             message = \"대/소문자, 숫자, 특수문자 포함 필수\")\n    private String password;\n\n    @NotBlank(message = \"이름은 필수입니다\")\n    @Size(min = 2, max = 50)\n    @Pattern(regexp = \"^[가-힣a-zA-Z]+$\", message = \"한글/영문만 허용\")\n    private String name;\n\n    @NotNull(message = \"나이는 필수입니다\")\n    @Min(value = 1, message = \"나이는 1세 이상\")\n    @Max(value = 150, message = \"나이는 150세 이하\")\n    private Integer age;\n\n    @Pattern(regexp = \"^01[016789]\\\\d{7,8}$\", message = \"올바른 전화번호 형식\")\n    private String phone;\n}\n\n// Controller에서 검증\n@RestController\n@Validated\npublic class UserController {\n\n    @PostMapping(\"/users\")\n    public ResponseEntity<?> createUser(@Valid @RequestBody UserCreateRequest request) {\n        // @Valid 통과 시 여기 도달\n        return ResponseEntity.ok(userService.create(request));\n    }\n}\n\n// 전역 예외 처리\n@RestControllerAdvice\npublic class ValidationExceptionHandler {\n\n    @ExceptionHandler(MethodArgumentNotValidException.class)\n    public ResponseEntity<ErrorResponse> handleValidation(MethodArgumentNotValidException ex) {\n        List<String> errors = ex.getBindingResult()\n            .getFieldErrors()\n            .stream()\n            .map(e -> e.getField() + \": \" + e.getDefaultMessage())\n            .collect(Collectors.toList());\n        \n        return ResponseEntity.badRequest()\n            .body(new ErrorResponse(\"VALIDATION_ERROR\", errors));\n    }\n}\n```"
                },
                {
                    "type": "code",
                    "title": "XSS 및 SQL Injection 방지",
                    "language": "java",
                    "content": "```java\n// XSS 방지 - HTML 이스케이프\n@Component\npublic class XssFilter implements Filter {\n\n    @Override\n    public void doFilter(ServletRequest request, ServletResponse response,\n            FilterChain chain) throws IOException, ServletException {\n        chain.doFilter(new XssRequestWrapper((HttpServletRequest) request), response);\n    }\n}\n\npublic class XssRequestWrapper extends HttpServletRequestWrapper {\n    \n    @Override\n    public String getParameter(String name) {\n        String value = super.getParameter(name);\n        return sanitize(value);\n    }\n\n    private String sanitize(String value) {\n        if (value == null) return null;\n        // OWASP Java Encoder 사용\n        return Encode.forHtml(value);\n    }\n}\n\n// SQL Injection 방지 - PreparedStatement\n@Repository\npublic class UserRepository {\n\n    // 절대 금지: 문자열 연결\n    public User findByIdUnsafe(String id) {\n        String sql = \"SELECT * FROM users WHERE id = '\" + id + \"'\";  // 취약!\n    }\n\n    // 안전: PreparedStatement\n    public User findById(String id) {\n        String sql = \"SELECT * FROM users WHERE id = ?\";\n        return jdbcTemplate.queryForObject(sql, userMapper, id);\n    }\n\n    // 안전: JPA (자동 파라미터 바인딩)\n    @Query(\"SELECT u FROM User u WHERE u.email = :email\")\n    Optional<User> findByEmail(@Param(\"email\") String email);\n}\n\n// 커스텀 검증 어노테이션\n@Target({ElementType.FIELD})\n@Retention(RetentionPolicy.RUNTIME)\n@Constraint(validatedBy = NoScriptValidator.class)\npublic @interface NoScript {\n    String message() default \"스크립트 태그는 허용되지 않습니다\";\n    Class<?>[] groups() default {};\n    Class<? extends Payload>[] payload() default {};\n}\n\npublic class NoScriptValidator implements ConstraintValidator<NoScript, String> {\n    private static final Pattern SCRIPT_PATTERN = \n        Pattern.compile(\"<script.*?>.*?</script>\", Pattern.CASE_INSENSITIVE | Pattern.DOTALL);\n\n    @Override\n    public boolean isValid(String value, ConstraintValidatorContext ctx) {\n        if (value == null) return true;\n        return !SCRIPT_PATTERN.matcher(value).find();\n    }\n}\n```"
                },
                {
                    "type": "tip",
                    "title": "입력값 검증 체크리스트",
                    "content": "## 필수 검증 항목\n\n```\n[ ] 모든 입력 필드에 길이 제한\n[ ] 숫자 필드에 범위 제한\n[ ] 이메일/전화번호 형식 검증\n[ ] 파일 업로드: 확장자, 크기, MIME 타입\n[ ] URL 파라미터 검증\n[ ] Hidden 필드도 서버에서 검증\n```\n\n## 파일 업로드 보안\n\n```java\n@PostMapping(\"/upload\")\npublic String upload(@RequestParam MultipartFile file) {\n    // 1. 확장자 화이트리스트\n    String ext = getExtension(file.getOriginalFilename());\n    if (!ALLOWED_EXT.contains(ext.toLowerCase())) {\n        throw new InvalidFileException();\n    }\n    \n    // 2. MIME 타입 검증 (확장자 위조 방지)\n    String mime = tika.detect(file.getInputStream());\n    if (!ALLOWED_MIME.contains(mime)) {\n        throw new InvalidFileException();\n    }\n    \n    // 3. 파일 크기 제한\n    if (file.getSize() > MAX_SIZE) {\n        throw new FileTooLargeException();\n    }\n    \n    // 4. 저장 시 파일명 변경 (경로 조작 방지)\n    String savedName = UUID.randomUUID() + \".\" + ext;\n}\n```\n\n## 자주 놓치는 검증\n\n| 항목 | 공격 | 방어 |\n|------|------|------|\n| Redirect URL | Open Redirect | 화이트리스트 도메인 |\n| 정렬 컬럼 | SQL Injection | Enum으로 제한 |\n| 페이지 번호 | 정수 오버플로우 | 범위 검증 |\n| JSON 깊이 | DoS | 최대 깊이 제한 |"
                }
            ]
        },

        "04_실무/password-policy": {
            "id": "04_실무/password-policy",
            "title": "비밀번호 정책",
            "category": "security",
            "subCategory": "04_실무",
            "language": "Java",
            "description": "안전한 비밀번호 정책 수립과 해시 저장, 비밀번호 관리 베스트 프랙티스를 학습합니다.",
            "isPlaceholder": False,
            "sections": [
                {
                    "type": "concept",
                    "title": "비밀번호 보안 원칙",
                    "content": "## 비밀번호 저장 원칙\n\n> **절대 평문 저장 금지** - 단방향 해시 + Salt 필수\n\n---\n\n## 해시 알고리즘 비교\n\n```\n[사용 금지]\n- MD5: 해시 충돌, GPU 공격에 취약\n- SHA-1: 충돌 발견됨 (2017년)\n- SHA-256 (without salt): Rainbow Table 공격\n\n[권장]\n- BCrypt: 기본 선택 (work factor 조절 가능)\n- Argon2: 최신 표준 (메모리 하드)\n- PBKDF2: NIST 권장 (반복 횟수 조절)\n```\n\n---\n\n## BCrypt 동작 원리\n\n```\n비밀번호: \"mypassword\"\n          |\n    +-----+-----+\n    |           |\n   Salt     Work Factor\n(랜덤 생성)   (10~12)\n    |           |\n    +-----+-----+\n          |\n     BCrypt 해시\n          |\n$2a$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.XQJZQlHH5B1J2q\n ^^  ^^  ^^^^^^^^^^^^^^^^^^^^^^^^  ^^^^^^^^^^^^^^^^^^^^^^^^\n알고  WF     Salt (22자)              Hash (31자)\n리즘\n```\n\n---\n\n## 비밀번호 정책 권장사항\n\n| 항목 | 최소 요구사항 | 권장 |\n|------|-------------|------|\n| 길이 | 8자 이상 | 12자 이상 |\n| 복잡도 | 대/소/숫자/특수 | 패스프레이즈 |\n| 만료 | 90일 | 미적용 (NIST 2023) |\n| 이력 | 최근 5개 불가 | 최근 10개 |\n| 잠금 | 5회 실패 | 5회 후 15분 잠금 |"
                },
                {
                    "type": "code",
                    "title": "비밀번호 해시 및 검증",
                    "language": "java",
                    "content": "```java\n// Spring Security BCrypt\n@Configuration\npublic class SecurityConfig {\n\n    @Bean\n    public PasswordEncoder passwordEncoder() {\n        // Work factor 12 (기본 10, 높을수록 느림/안전)\n        return new BCryptPasswordEncoder(12);\n    }\n}\n\n@Service\n@RequiredArgsConstructor\npublic class UserService {\n\n    private final PasswordEncoder passwordEncoder;\n    private final UserRepository userRepository;\n\n    public void register(UserCreateRequest request) {\n        // 1. 비밀번호 정책 검증\n        validatePasswordPolicy(request.getPassword());\n        \n        // 2. 비밀번호 해시\n        String hashedPassword = passwordEncoder.encode(request.getPassword());\n        \n        // 3. 저장 (해시된 비밀번호)\n        User user = User.builder()\n            .email(request.getEmail())\n            .password(hashedPassword)  // $2a$12$xxx...\n            .build();\n        \n        userRepository.save(user);\n    }\n\n    public boolean authenticate(String email, String rawPassword) {\n        User user = userRepository.findByEmail(email)\n            .orElseThrow(() -> new AuthException(\"인증 실패\"));\n        \n        // BCrypt 내부에서 salt 추출 후 검증\n        if (!passwordEncoder.matches(rawPassword, user.getPassword())) {\n            handleFailedLogin(user);\n            throw new AuthException(\"인증 실패\");\n        }\n        \n        resetFailedAttempts(user);\n        return true;\n    }\n}\n\n// Argon2 사용 (더 강력)\n@Bean\npublic PasswordEncoder passwordEncoder() {\n    return new Argon2PasswordEncoder(\n        16,   // salt length\n        32,   // hash length  \n        1,    // parallelism\n        65536, // memory (KB)\n        3     // iterations\n    );\n}\n```"
                },
                {
                    "type": "code",
                    "title": "비밀번호 정책 구현",
                    "language": "java",
                    "content": "```java\n// 커스텀 비밀번호 검증기\n@Component\npublic class PasswordPolicyValidator {\n\n    private static final int MIN_LENGTH = 8;\n    private static final int MAX_LENGTH = 128;\n    \n    // 취약 비밀번호 목록 (상위 10000개)\n    private final Set<String> weakPasswords;\n\n    public PasswordPolicyValidator() {\n        this.weakPasswords = loadWeakPasswords();\n    }\n\n    public void validate(String password) {\n        List<String> errors = new ArrayList<>();\n\n        // 1. 길이 검사\n        if (password.length() < MIN_LENGTH) {\n            errors.add(\"최소 \" + MIN_LENGTH + \"자 이상\");\n        }\n        if (password.length() > MAX_LENGTH) {\n            errors.add(\"최대 \" + MAX_LENGTH + \"자 이하\");\n        }\n\n        // 2. 복잡도 검사\n        if (!password.matches(\".*[A-Z].*\")) {\n            errors.add(\"대문자 포함 필수\");\n        }\n        if (!password.matches(\".*[a-z].*\")) {\n            errors.add(\"소문자 포함 필수\");\n        }\n        if (!password.matches(\".*\\\\d.*\")) {\n            errors.add(\"숫자 포함 필수\");\n        }\n        if (!password.matches(\".*[@#$%^&+=!].*\")) {\n            errors.add(\"특수문자 포함 필수\");\n        }\n\n        // 3. 취약 비밀번호 검사\n        if (weakPasswords.contains(password.toLowerCase())) {\n            errors.add(\"취약한 비밀번호입니다\");\n        }\n\n        // 4. 연속/반복 문자 검사\n        if (hasSequentialChars(password)) {\n            errors.add(\"연속 문자 3개 이상 금지 (abc, 123)\");\n        }\n        if (hasRepeatedChars(password)) {\n            errors.add(\"동일 문자 3개 이상 반복 금지\");\n        }\n\n        if (!errors.isEmpty()) {\n            throw new PasswordPolicyException(errors);\n        }\n    }\n\n    // 비밀번호 이력 검사\n    public void checkPasswordHistory(User user, String newPassword) {\n        List<String> history = user.getPasswordHistory();\n        for (String oldHash : history) {\n            if (passwordEncoder.matches(newPassword, oldHash)) {\n                throw new PasswordPolicyException(\"최근 사용한 비밀번호는 재사용 불가\");\n            }\n        }\n    }\n}\n```"
                },
                {
                    "type": "tip",
                    "title": "비밀번호 보안 베스트 프랙티스",
                    "content": "## 비밀번호 변경 플로우\n\n```\n1. 현재 비밀번호 확인\n2. 새 비밀번호 정책 검증\n3. 이력 검사 (최근 N개 불가)\n4. 새 비밀번호 해시 저장\n5. 이전 해시를 이력에 추가\n6. 모든 세션 무효화 (선택)\n7. 변경 알림 이메일 발송\n```\n\n## 비밀번호 찾기 보안\n\n```java\n// 안전한 비밀번호 재설정\npublic void requestPasswordReset(String email) {\n    // 1. 이메일 존재 여부 노출 금지\n    // (항상 같은 메시지 반환)\n    \n    // 2. 토큰 생성 (랜덤, 일회용, 만료시간)\n    String token = generateSecureToken();\n    \n    // 3. 토큰 저장 (해시 저장!)\n    resetTokenRepository.save(new ResetToken(\n        hashToken(token),\n        email,\n        Instant.now().plus(1, ChronoUnit.HOURS)\n    ));\n    \n    // 4. 이메일 발송 (Rate Limit 적용)\n    emailService.sendResetLink(email, token);\n}\n```\n\n## NIST 2023 권장사항\n\n| 기존 방식 | 새 권장사항 |\n|----------|------------|\n| 주기적 변경 강제 | 유출 시에만 변경 |\n| 복잡도 규칙 | 길이 우선 (12자+) |\n| 힌트 질문 | 사용 금지 |\n| SMS 인증 | TOTP/앱 인증 권장 |\n\n## MFA 적용 우선순위\n\n1. 하드웨어 키 (YubiKey)\n2. TOTP 앱 (Google Authenticator)\n3. 푸시 알림\n4. SMS (최후의 수단)"
                }
            ]
        },

        "04_실무/security-header": {
            "id": "04_실무/security-header",
            "title": "보안 헤더 설정 (HTTP Security Headers)",
            "category": "security",
            "subCategory": "04_실무",
            "language": "Java",
            "description": "XSS, Clickjacking, MIME Sniffing 등을 방지하는 HTTP 보안 헤더 설정을 학습합니다.",
            "isPlaceholder": False,
            "sections": [
                {
                    "type": "concept",
                    "title": "HTTP 보안 헤더 개요",
                    "content": "## 왜 보안 헤더가 중요한가?\n\n> 브라우저에게 보안 정책을 전달하여 클라이언트 측 공격 방어\n\n---\n\n## 필수 보안 헤더\n\n```\n[XSS 방어]\n- Content-Security-Policy (CSP)\n- X-XSS-Protection (deprecated, CSP 대체)\n\n[Clickjacking 방어]\n- X-Frame-Options\n- CSP frame-ancestors\n\n[MIME Sniffing 방어]\n- X-Content-Type-Options\n\n[HTTPS 강제]\n- Strict-Transport-Security (HSTS)\n\n[정보 노출 방지]\n- X-Powered-By 제거\n- Server 헤더 최소화\n```\n\n---\n\n## 헤더별 역할\n\n| 헤더 | 방어 대상 | 설명 |\n|------|----------|------|\n| CSP | XSS | 허용 리소스 출처 정의 |\n| X-Frame-Options | Clickjacking | iframe 삽입 제어 |\n| X-Content-Type-Options | MIME Sniffing | 브라우저 타입 추론 방지 |\n| HSTS | 다운그레이드 | HTTPS 강제 |\n| Referrer-Policy | 정보 유출 | Referer 헤더 제어 |"
                },
                {
                    "type": "code",
                    "title": "Spring Security 보안 헤더 설정",
                    "language": "java",
                    "content": "```java\n@Configuration\n@EnableWebSecurity\npublic class SecurityHeaderConfig {\n\n    @Bean\n    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {\n        http\n            .headers(headers -> headers\n                // 1. Content-Security-Policy\n                .contentSecurityPolicy(csp -> csp\n                    .policyDirectives(\n                        \"default-src 'self'; \" +\n                        \"script-src 'self' 'nonce-{random}'; \" +\n                        \"style-src 'self' 'unsafe-inline'; \" +\n                        \"img-src 'self' data: https:; \" +\n                        \"font-src 'self' https://fonts.gstatic.com; \" +\n                        \"connect-src 'self' https://api.example.com; \" +\n                        \"frame-ancestors 'none'; \" +\n                        \"form-action 'self';\"\n                    )\n                )\n                \n                // 2. X-Frame-Options (Clickjacking 방지)\n                .frameOptions(frame -> frame.deny())\n                \n                // 3. X-Content-Type-Options (MIME Sniffing 방지)\n                .contentTypeOptions(content -> {})  // nosniff 자동 적용\n                \n                // 4. HSTS (HTTPS 강제)\n                .httpStrictTransportSecurity(hsts -> hsts\n                    .maxAgeInSeconds(31536000)  // 1년\n                    .includeSubDomains(true)\n                    .preload(true)\n                )\n                \n                // 5. Referrer-Policy\n                .referrerPolicy(referrer -> referrer\n                    .policy(ReferrerPolicyHeaderWriter.ReferrerPolicy.STRICT_ORIGIN_WHEN_CROSS_ORIGIN)\n                )\n                \n                // 6. Permissions-Policy (카메라, 마이크 등 제어)\n                .permissionsPolicy(permissions -> permissions\n                    .policy(\"camera=(), microphone=(), geolocation=()\")\n                )\n            );\n\n        return http.build();\n    }\n}\n\n// Server 헤더 제거 (application.yml)\nserver:\n  server-header: \"\"  # 빈 값으로 설정\n\n// X-Powered-By 제거 (Tomcat)\nserver:\n  tomcat:\n    additional-tld-skip-patterns: \"*.jar\"\n```"
                },
                {
                    "type": "code",
                    "title": "CSP 상세 설정 및 Nginx 설정",
                    "language": "java",
                    "content": "```java\n// CSP Nonce 동적 생성\n@Component\npublic class CspNonceFilter extends OncePerRequestFilter {\n\n    @Override\n    protected void doFilterInternal(HttpServletRequest request,\n            HttpServletResponse response, FilterChain chain) {\n        \n        // 랜덤 nonce 생성\n        String nonce = Base64.getEncoder().encodeToString(\n            SecureRandom.getInstanceStrong().generateSeed(16)\n        );\n        \n        request.setAttribute(\"cspNonce\", nonce);\n        \n        // CSP 헤더에 nonce 포함\n        String csp = String.format(\n            \"default-src 'self'; script-src 'self' 'nonce-%s';\", nonce);\n        response.setHeader(\"Content-Security-Policy\", csp);\n        \n        chain.doFilter(request, response);\n    }\n}\n\n// Thymeleaf 템플릿에서 nonce 사용\n// <script th:attr=\"nonce=${cspNonce}\">...</script>\n```\n\n```nginx\n# Nginx 보안 헤더 설정\nserver {\n    listen 443 ssl http2;\n    \n    # 보안 헤더\n    add_header X-Frame-Options \"DENY\" always;\n    add_header X-Content-Type-Options \"nosniff\" always;\n    add_header X-XSS-Protection \"1; mode=block\" always;\n    add_header Referrer-Policy \"strict-origin-when-cross-origin\" always;\n    \n    # HSTS (HTTPS 강제)\n    add_header Strict-Transport-Security \"max-age=31536000; includeSubDomains; preload\" always;\n    \n    # CSP\n    add_header Content-Security-Policy \"default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';\" always;\n    \n    # 정보 노출 방지\n    server_tokens off;\n    \n    # 쿠키 보안\n    proxy_cookie_path / \"/; Secure; HttpOnly; SameSite=Strict\";\n}\n```"
                },
                {
                    "type": "tip",
                    "title": "보안 헤더 테스트 및 체크리스트",
                    "content": "## 보안 헤더 테스트 도구\n\n```bash\n# curl로 헤더 확인\ncurl -I https://your-site.com\n\n# 온라인 도구\n- securityheaders.com (A+ 목표)\n- observatory.mozilla.org\n- hstspreload.org (HSTS 등록)\n```\n\n## 필수 체크리스트\n\n```\n[ ] Content-Security-Policy 설정\n[ ] X-Frame-Options: DENY\n[ ] X-Content-Type-Options: nosniff\n[ ] HSTS: max-age=31536000\n[ ] Referrer-Policy 설정\n[ ] X-Powered-By 제거\n[ ] Server 헤더 최소화\n```\n\n## CSP 디버깅\n\n```javascript\n// CSP 위반 리포트 수신\nContent-Security-Policy-Report-Only: default-src 'self'; report-uri /csp-report\n\n// 서버에서 리포트 수신\n@PostMapping(\"/csp-report\")\npublic void handleCspReport(@RequestBody String report) {\n    log.warn(\"CSP Violation: {}\", report);\n}\n```\n\n## 헤더 설정 시 주의사항\n\n| 상황 | 주의점 |\n|------|--------|\n| CSP 적용 | 점진적 적용 (Report-Only 먼저) |\n| HSTS 적용 | 롤백 어려움 (max-age 짧게 시작) |\n| iframe 사용 | frame-ancestors로 허용 도메인 지정 |\n| CDN 사용 | CSP에 CDN 도메인 추가 |"
                }
            ]
        },

        "05_면접/interview-security": {
            "id": "05_면접/interview-security",
            "title": "보안 면접 총정리",
            "category": "security",
            "subCategory": "05_면접",
            "language": "Java",
            "description": "주니어/시니어 보안 면접 질문과 모범 답변, 실무 시나리오 질문을 정리합니다.",
            "isPlaceholder": False,
            "sections": [
                {
                    "type": "concept",
                    "title": "주니어 면접 질문 10선",
                    "content": "## Q1. OWASP Top 10이 무엇인가요?\n\n**A:** OWASP(Open Web Application Security Project)에서 발표하는 웹 애플리케이션 보안 취약점 Top 10입니다. 2-3년마다 업데이트되며, 2021년 기준 1위는 Broken Access Control입니다.\n\n---\n\n## Q2. SQL Injection이 무엇이고 어떻게 방어하나요?\n\n**A:** 사용자 입력에 SQL 구문을 삽입하여 DB를 조작하는 공격입니다. 방어법은:\n- PreparedStatement 사용 (파라미터 바인딩)\n- ORM 프레임워크 사용 (JPA, MyBatis)\n- 입력값 검증 (화이트리스트)\n\n---\n\n## Q3. XSS(Cross-Site Scripting)란?\n\n**A:** 악성 스크립트를 웹 페이지에 삽입하는 공격입니다.\n- Stored XSS: DB에 저장된 스크립트 실행\n- Reflected XSS: URL 파라미터 통해 실행\n- 방어: 입력값 이스케이프, CSP 헤더, HttpOnly 쿠키\n\n---\n\n## Q4. CSRF란 무엇인가요?\n\n**A:** 사용자가 로그인한 상태에서 악성 사이트가 요청을 위조하는 공격입니다.\n- 방어: CSRF 토큰, SameSite 쿠키, Referer 검증\n\n---\n\n## Q5. 비밀번호를 왜 해시로 저장하나요?\n\n**A:** 평문 저장 시 DB 유출로 전체 비밀번호 노출됩니다.\n- BCrypt, Argon2 등 단방향 해시 사용\n- Salt를 추가하여 Rainbow Table 공격 방어\n- Work factor로 무차별 대입 공격 지연"
                },
                {
                    "type": "concept",
                    "title": "주니어 면접 질문 (계속)",
                    "content": "## Q6. HTTPS와 HTTP의 차이점은?\n\n**A:**\n- HTTPS: TLS/SSL로 암호화된 통신\n- 중간자 공격(MITM) 방지\n- 데이터 무결성 보장\n- SEO 순위, 브라우저 경고 관련\n\n---\n\n## Q7. 세션과 토큰 인증의 차이점은?\n\n**A:**\n| 항목 | 세션 | 토큰(JWT) |\n|------|------|----------|\n| 저장 위치 | 서버 | 클라이언트 |\n| 확장성 | 서버 메모리 부담 | Stateless |\n| 탈취 대응 | 서버에서 삭제 가능 | 만료까지 유효 |\n\n---\n\n## Q8. 인증(Authentication)과 인가(Authorization)의 차이?\n\n**A:**\n- 인증: 누구인지 확인 (로그인)\n- 인가: 권한이 있는지 확인 (관리자 페이지 접근)\n- 인증 실패: 401, 인가 실패: 403\n\n---\n\n## Q9. CORS란 무엇인가요?\n\n**A:** Cross-Origin Resource Sharing. 브라우저가 다른 도메인 요청을 제한하는 정책입니다.\n- 서버에서 Access-Control-Allow-Origin 헤더로 허용\n- Preflight 요청 (OPTIONS)으로 사전 확인\n\n---\n\n## Q10. API 키를 소스코드에 하드코딩하면 안 되는 이유?\n\n**A:**\n- Git 히스토리에 영구 저장\n- 코드 리뷰, 로그에서 노출\n- 대안: 환경변수, Vault, Secret Manager"
                },
                {
                    "type": "concept",
                    "title": "시니어 면접 질문 10선",
                    "content": "## Q1. Zero Trust 보안 모델을 설명하세요.\n\n**A:** \"Never Trust, Always Verify\" 원칙으로, 네트워크 위치와 관계없이 모든 요청을 검증합니다.\n- 마이크로 세그멘테이션\n- 지속적 인증/인가\n- 최소 권한 원칙\n- 구현: BeyondCorp, SASE\n\n---\n\n## Q2. JWT 토큰의 보안 취약점과 대응 방안은?\n\n**A:**\n- 탈취 시 만료까지 유효 -> Access/Refresh 토큰 분리, 짧은 만료시간\n- 서명 알고리즘 변조 -> 알고리즘 화이트리스트\n- Claim 변조 -> 서명 검증 필수\n- 토큰 크기 -> Redis 블랙리스트로 폐기\n\n---\n\n## Q3. 마이크로서비스 환경에서 인증/인가를 어떻게 구현하나요?\n\n**A:**\n- API Gateway: 중앙 인증\n- Service Mesh: mTLS, 서비스 간 인증\n- OAuth2 + JWT: 토큰 기반 인가\n- 옵션: Istio, Envoy, Spring Cloud Gateway\n\n---\n\n## Q4. OWASP Top 10 2021에서 A01이 Broken Access Control인 이유는?\n\n**A:**\n- 2017년 5위에서 1위로 상승\n- MSA 확산으로 API 엔드포인트 증가\n- 권한 체크 로직 분산으로 누락 빈번\n- 자동화 도구로 IDOR 취약점 탐지 용이"
                },
                {
                    "type": "concept",
                    "title": "시니어 면접 질문 (계속)",
                    "content": "## Q5. DevSecOps 파이프라인을 어떻게 구성하나요?\n\n**A:**\n```\nCode -> SAST(정적분석) -> Build -> Container Scan\n  -> DAST(동적분석) -> Deploy -> RASP(런타임)\n```\n- 도구: SonarQube, OWASP ZAP, Trivy, Snyk\n- Shift-Left: 개발 초기에 보안 검사\n\n---\n\n## Q6. Rate Limiting과 DDoS 방어 전략은?\n\n**A:**\n- Rate Limiting: Token Bucket, Sliding Window\n- L7 DDoS: WAF, Cloudflare, AWS Shield\n- L4 DDoS: ISP 협조, Anycast\n- 캐싱, CDN으로 Origin 보호\n\n---\n\n## Q7. Secrets Management 베스트 프랙티스는?\n\n**A:**\n- 코드와 시크릿 분리 (12-Factor App)\n- HashiCorp Vault, AWS Secrets Manager\n- 자동 로테이션\n- 최소 권한 접근, 감사 로그\n\n---\n\n## Q8. Security Logging 전략을 설명하세요.\n\n**A:**\n- 로깅 대상: 인증, 권한변경, 민감 데이터 접근\n- 민감정보 마스킹 필수\n- 중앙 로그 서버 (ELK, Splunk)\n- 실시간 알림 (SIEM)\n- 무결성 보장 (WORM 스토리지)\n\n---\n\n## Q9. 보안 사고 대응 절차(Incident Response)는?\n\n**A:**\n1. 탐지 및 분석\n2. 격리 (영향 범위 제한)\n3. 제거 (악성코드, 취약점 패치)\n4. 복구 (시스템 정상화)\n5. 사후 분석 (RCA, 재발 방지)\n\n---\n\n## Q10. 암호화 알고리즘 선택 기준은?\n\n**A:**\n- 대칭키: AES-256-GCM (성능)\n- 비대칭키: RSA-2048, ECDSA (키 교환)\n- 해시: SHA-256 (무결성), BCrypt/Argon2 (비밀번호)\n- TLS 1.3 사용, 취약 알고리즘(MD5, SHA-1, DES) 제거"
                },
                {
                    "type": "tip",
                    "title": "실무 시나리오 질문",
                    "content": "## 시나리오 1: 비밀번호 유출 대응\n\n**Q:** DB 유출로 사용자 비밀번호가 노출되었습니다. 어떻게 대응하나요?\n\n**A:**\n1. 즉시 전체 사용자 비밀번호 리셋 강제\n2. 세션 전체 무효화\n3. 영향 범위 파악 (해시 알고리즘 확인)\n4. 사용자 통보 및 비밀번호 변경 안내\n5. 유출 경로 분석 및 패치\n6. 로그 분석으로 악용 여부 확인\n\n---\n\n## 시나리오 2: 서비스 DDoS 공격\n\n**Q:** 갑자기 트래픽이 10배 증가하고 서비스가 느려졌습니다.\n\n**A:**\n1. CDN/WAF에서 Rate Limiting 강화\n2. 공격 IP 대역 식별 및 차단\n3. Origin 서버 Auto Scaling\n4. ISP에 Upstream 차단 요청\n5. 정상 트래픽 구분 (Captcha 등)\n\n---\n\n## 시나리오 3: 내부자 위협\n\n**Q:** 퇴사 예정자가 민감 정보를 대량 다운로드한 것으로 의심됩니다.\n\n**A:**\n1. 감사 로그 분석 (접근 이력, 다운로드 기록)\n2. 계정 즉시 비활성화\n3. 관련 시스템 접근 권한 회수\n4. DLP(Data Loss Prevention) 로그 확인\n5. 법무팀/HR 협조하여 대응\n\n---\n\n## 면접 팁\n\n- **주니어:** 개념 설명 + 간단한 방어 코드\n- **시니어:** 아키텍처 레벨 + 트레이드오프 논의\n- **공통:** \"해본 경험\"을 구체적으로 설명"
                }
            ]
        },

        "index": {
            "id": "index",
            "title": "보안 학습 로드맵",
            "category": "security",
            "subCategory": None,
            "language": "Text",
            "description": "백엔드 개발자를 위한 보안 학습 로드맵과 필수 개념, 실습 프로젝트를 안내합니다.",
            "isPlaceholder": False,
            "sections": [
                {
                    "type": "concept",
                    "title": "7가지 필수 보안 개념",
                    "content": "## 학습 순서\n\n```\n[기초 단계 - 1~2주]\n1. CIA Triad (기밀성, 무결성, 가용성)\n   - 보안의 3대 원칙 이해\n   - 각 원칙이 위반되는 사례 분석\n\n2. OWASP Top 10\n   - 웹 취약점 Top 10 숙지\n   - 각 취약점의 공격/방어 방법\n\n[중급 단계 - 2~3주]\n3. 인증/인가 (Authentication/Authorization)\n   - 세션 vs JWT\n   - OAuth 2.0, OIDC\n   - RBAC, ABAC 권한 모델\n\n4. 암호화 기초\n   - 대칭키 vs 비대칭키\n   - 해시 함수 (BCrypt, SHA)\n   - TLS/HTTPS 동작 원리\n\n[실무 단계 - 3~4주]\n5. 입력값 검증\n   - SQL Injection 방어\n   - XSS 방어\n   - 파일 업로드 보안\n\n6. 보안 헤더 & 설정\n   - CSP, CORS, HSTS\n   - 쿠키 보안 (HttpOnly, Secure, SameSite)\n\n7. 보안 로깅 & 모니터링\n   - 감사 로그 설계\n   - 민감 정보 마스킹\n   - 이상 탐지\n```"
                },
                {
                    "type": "concept",
                    "title": "각 토픽 요약",
                    "content": "## 토픽별 핵심 요약\n\n| 토픽 | 핵심 내용 | 난이도 |\n|------|----------|--------|\n| CIA Triad | 기밀성-무결성-가용성 원칙 | 초급 |\n| OWASP Top 10 | 웹 취약점 TOP 10 | 초급 |\n| SQL Injection | PreparedStatement로 방어 | 초급 |\n| XSS | 입력 이스케이프, CSP | 초급 |\n| CSRF | 토큰, SameSite 쿠키 | 중급 |\n| JWT | Access/Refresh 토큰 설계 | 중급 |\n| OAuth 2.0 | 인증 플로우 4가지 | 중급 |\n| BCrypt | 비밀번호 해시, Salt | 중급 |\n| HTTPS/TLS | 인증서, 핸드셰이크 | 중급 |\n| Spring Security | 필터 체인, 권한 설정 | 고급 |\n| 보안 헤더 | CSP, HSTS, X-Frame-Options | 고급 |\n| 보안 로깅 | 감사 로그, 마스킹 | 고급 |\n\n---\n\n## 학습 우선순위\n\n```\n[필수] OWASP Top 10 -> 입력값 검증 -> 인증/인가\n[권장] 암호화 기초 -> 보안 헤더 -> Spring Security\n[심화] 보안 로깅 -> DevSecOps -> 침투 테스트\n```"
                },
                {
                    "type": "concept",
                    "title": "실습 프로젝트 제안",
                    "content": "## 프로젝트 1: 취약 사이트 만들고 해킹하기\n\n**목표:** OWASP Top 10 취약점 직접 체험\n\n```\n[구현할 취약점]\n- SQL Injection 가능한 로그인\n- XSS 가능한 게시판\n- CSRF 취약한 비밀번호 변경\n- 권한 체크 없는 관리자 페이지\n\n[해킹 후 패치]\n- 각 취약점 패치 코드 작성\n- 보안 테스트로 검증\n```\n\n---\n\n## 프로젝트 2: Spring Security 적용\n\n**목표:** 실무 수준의 인증/인가 구현\n\n```\n[구현 기능]\n- JWT 기반 인증 (Access + Refresh)\n- Role 기반 권한 관리\n- OAuth2 소셜 로그인 (Google, Kakao)\n- 비밀번호 정책 적용\n- 로그인 실패 횟수 제한\n```\n\n---\n\n## 프로젝트 3: 보안 강화 API 서버\n\n**목표:** 실무 체크리스트 완전 적용\n\n```\n[체크리스트]\n- 모든 보안 헤더 적용\n- 입력값 검증 100%\n- 보안 로깅 구현\n- Rate Limiting 적용\n- HTTPS 강제\n- 취약점 스캔 통과\n```"
                },
                {
                    "type": "tip",
                    "title": "취약점 스캔 도구 소개",
                    "content": "## SAST (정적 분석 도구)\n\n```\n[무료]\n- SonarQube Community: 코드 품질 + 보안\n- SpotBugs + FindSecBugs: Java 보안 버그\n- Semgrep: 패턴 기반 분석\n\n[유료]\n- Checkmarx: 엔터프라이즈 SAST\n- Fortify: 종합 보안 분석\n```\n\n---\n\n## DAST (동적 분석 도구)\n\n```\n[무료]\n- OWASP ZAP: 자동 스캔, 프록시\n- Nikto: 웹 서버 스캐너\n- SQLMap: SQL Injection 자동화\n\n[유료]\n- Burp Suite Pro: 침투 테스트 필수\n- Acunetix: 자동 웹 스캐너\n```\n\n---\n\n## 의존성 취약점 스캔\n\n```\n# OWASP Dependency-Check\n./gradlew dependencyCheckAnalyze\n\n# Snyk (무료 티어 있음)\nsnyk test\n\n# GitHub Dependabot\n자동으로 취약 라이브러리 PR 생성\n```\n\n---\n\n## 실습 환경\n\n```\n[취약 앱 실습]\n- OWASP WebGoat: 학습용 취약 앱\n- OWASP Juice Shop: 현실적 취약 쇼핑몰\n- DVWA: Damn Vulnerable Web App\n- PortSwigger Academy: 무료 온라인 실습\n\n[CTF (Capture The Flag)]\n- HackTheBox: 실전 해킹 플랫폼\n- TryHackMe: 초보자 친화적\n```\n\n---\n\n## 자격증 로드맵\n\n```\n[입문]\n- CompTIA Security+\n\n[중급]\n- CEH (Certified Ethical Hacker)\n- CISA (정보시스템감사사)\n\n[고급]\n- OSCP (Offensive Security)\n- CISSP (정보보안전문가)\n```"
                }
            ]
        }
    }


def update_security_json():
    """Update security.json with new content"""

    json_path = r"c:\tools\codemaster-next-main\codemaster-next-main\codemaster-next-main\src\data\contents\security.json"

    # Read existing JSON
    print(f"Reading {json_path}...")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Get new content
    new_content = get_security_content()

    # Update each topic
    updated_topics = []
    for topic_id, topic_data in new_content.items():
        if topic_id in data:
            data[topic_id] = topic_data
            updated_topics.append(topic_id)
            print(f"Updated: {topic_id}")
        else:
            print(f"Topic not found, adding: {topic_id}")
            data[topic_id] = topic_data
            updated_topics.append(topic_id)

    # Write updated JSON
    print(f"\nWriting updated content to {json_path}...")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nSuccessfully updated {len(updated_topics)} topics:")
    for topic in updated_topics:
        print(f"  - {topic}")

    return updated_topics


if __name__ == "__main__":
    print("=" * 60)
    print("Security Content Generator 06")
    print("=" * 60)

    updated = update_security_json()

    print("\n" + "=" * 60)
    print("Complete!")
    print("=" * 60)
