package com.codemaster.ai.config;

import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import io.swagger.v3.oas.models.security.SecurityRequirement;
import io.swagger.v3.oas.models.security.SecurityScheme;
import io.swagger.v3.oas.models.servers.Server;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

@Configuration
public class SwaggerConfig {

    @Bean
    public OpenAPI openAPI() {
        final String securitySchemeName = "bearerAuth";

        return new OpenAPI()
                .info(new Info()
                        .title("CodeMaster MSA API")
                        .description("코드마스터 MSA 프로젝트 API 문서\n\n" +
                                "## 인증\n" +
                                "Bearer JWT 토큰을 사용합니다.\n" +
                                "1. `/api/auth/login`으로 로그인하여 토큰을 발급받습니다.\n" +
                                "2. 발급받은 토큰을 `Authorization: Bearer {token}` 헤더에 포함합니다.\n\n" +
                                "## 테스트 계정\n" +
                                "- Username: `admin`\n" +
                                "- Password: `admin123`")
                        .version("1.0.0")
                        .contact(new Contact()
                                .name("CodeMaster Team")
                                .email("support@codemaster.local")
                                .url("https://github.com/codemaster"))
                        .license(new License()
                                .name("MIT License")
                                .url("https://opensource.org/licenses/MIT")))
                .servers(List.of(
                        new Server().url("http://localhost:8080").description("Development Server"),
                        new Server().url("http://api.codemaster.local").description("Production Server")
                ))
                .addSecurityItem(new SecurityRequirement().addList(securitySchemeName))
                .components(new Components()
                        .addSecuritySchemes(securitySchemeName,
                                new SecurityScheme()
                                        .name(securitySchemeName)
                                        .type(SecurityScheme.Type.HTTP)
                                        .scheme("bearer")
                                        .bearerFormat("JWT")
                                        .description("JWT 인증 토큰을 입력하세요")));
    }
}
