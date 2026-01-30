package com.example.msa.config;

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
        return new OpenAPI()
                .info(new Info()
                        .title("MSA User CRUD API")
                        .description("Spring Boot 기반 사용자 관리 RESTful API\n\n" +
                                "## 기능\n" +
                                "- 회원가입/로그인 (JWT 토큰 발급)\n" +
                                "- 사용자 CRUD (인증 필요)\n" +
                                "- BCrypt 비밀번호 암호화\n\n" +
                                "## 인증\n" +
                                "1. `/api/auth/login`으로 로그인하여 토큰 발급\n" +
                                "2. 요청 헤더에 `Authorization: Bearer {token}` 추가")
                        .version("1.0.0")
                        .contact(new Contact()
                                .name("API Support")
                                .email("support@example.com"))
                        .license(new License()
                                .name("MIT License")
                                .url("https://opensource.org/licenses/MIT")))
                .servers(List.of(
                        new Server().url("http://localhost:8080").description("Local Server"),
                        new Server().url("http://localhost:8081").description("Dev Server")
                ))
                .components(new Components()
                        .addSecuritySchemes("bearerAuth", new SecurityScheme()
                                .type(SecurityScheme.Type.HTTP)
                                .scheme("bearer")
                                .bearerFormat("JWT")
                                .description("JWT 인증 토큰")))
                .addSecurityItem(new SecurityRequirement().addList("bearerAuth"));
    }
}
