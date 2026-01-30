package com.example.msa.service;

import com.example.msa.dto.LoginRequestDto;
import com.example.msa.dto.LoginResponseDto;
import com.example.msa.dto.UserRequestDto;
import com.example.msa.dto.UserResponseDto;
import com.example.msa.entity.User;
import com.example.msa.exception.CustomException;
import com.example.msa.exception.ErrorCode;
import com.example.msa.repository.UserRepository;
import com.example.msa.security.JwtTokenProvider;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@Transactional
public class UserService {

    private static final Logger log = LoggerFactory.getLogger(UserService.class);

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtTokenProvider jwtTokenProvider;
    private final AuthenticationManager authenticationManager;

    public UserService(UserRepository userRepository,
                       PasswordEncoder passwordEncoder,
                       JwtTokenProvider jwtTokenProvider,
                       AuthenticationManager authenticationManager) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtTokenProvider = jwtTokenProvider;
        this.authenticationManager = authenticationManager;
    }

    // 회원가입
    public UserResponseDto register(UserRequestDto request) {
        log.info("Registering new user: {}", request.getUsername());

        // 중복 체크
        if (userRepository.existsByUsername(request.getUsername())) {
            throw new CustomException(ErrorCode.DUPLICATE_USERNAME);
        }

        if (userRepository.existsByEmail(request.getEmail())) {
            throw new CustomException(ErrorCode.DUPLICATE_EMAIL);
        }

        // 사용자 생성
        User user = new User();
        user.setUsername(request.getUsername());
        user.setEmail(request.getEmail());
        user.setPassword(passwordEncoder.encode(request.getPassword()));
        user.setRole(User.Role.USER);
        user.setIsActive(true);

        User savedUser = userRepository.save(user);
        log.info("User registered successfully: {}", savedUser.getUsername());

        return UserResponseDto.fromEntity(savedUser);
    }

    // 로그인
    public LoginResponseDto login(LoginRequestDto request) {
        log.info("Login attempt for user: {}", request.getUsername());

        // 인증
        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(
                        request.getUsername(),
                        request.getPassword()
                )
        );

        SecurityContextHolder.getContext().setAuthentication(authentication);

        // JWT 토큰 생성
        String token = jwtTokenProvider.generateToken(authentication);

        // 사용자 정보 조회
        User user = userRepository.findByUsername(request.getUsername())
                .orElseThrow(() -> new CustomException(ErrorCode.USER_NOT_FOUND));

        log.info("User logged in successfully: {}", user.getUsername());

        LoginResponseDto response = new LoginResponseDto();
        response.setAccessToken(token);
        response.setExpiresIn(jwtTokenProvider.getExpirationSeconds());
        response.setUser(UserResponseDto.fromEntity(user));

        return response;
    }

    // 전체 사용자 조회
    @Transactional(readOnly = true)
    public List<UserResponseDto> getAllUsers() {
        log.info("Fetching all users");
        return userRepository.findAll().stream()
                .map(UserResponseDto::fromEntity)
                .collect(Collectors.toList());
    }

    // ID로 사용자 조회
    @Transactional(readOnly = true)
    public UserResponseDto getUserById(Long id) {
        log.info("Fetching user by id: {}", id);
        User user = userRepository.findById(id)
                .orElseThrow(() -> new CustomException(ErrorCode.USER_NOT_FOUND));
        return UserResponseDto.fromEntity(user);
    }

    // 사용자 정보 수정 (본인만)
    public UserResponseDto updateUser(Long id, UserRequestDto request, String currentUsername) {
        log.info("Updating user: {}", id);

        User user = userRepository.findById(id)
                .orElseThrow(() -> new CustomException(ErrorCode.USER_NOT_FOUND));

        // 본인 확인
        if (!user.getUsername().equals(currentUsername)) {
            throw new CustomException(ErrorCode.ACCESS_DENIED, "본인의 정보만 수정할 수 있습니다");
        }

        // 사용자명 변경 시 중복 체크
        if (request.getUsername() != null && !request.getUsername().equals(user.getUsername())) {
            if (userRepository.existsByUsername(request.getUsername())) {
                throw new CustomException(ErrorCode.DUPLICATE_USERNAME);
            }
            user.setUsername(request.getUsername());
        }

        // 이메일 변경 시 중복 체크
        if (request.getEmail() != null && !request.getEmail().equals(user.getEmail())) {
            if (userRepository.existsByEmail(request.getEmail())) {
                throw new CustomException(ErrorCode.DUPLICATE_EMAIL);
            }
            user.setEmail(request.getEmail());
        }

        // 비밀번호 변경
        if (request.getPassword() != null && !request.getPassword().isEmpty()) {
            user.setPassword(passwordEncoder.encode(request.getPassword()));
        }

        User updatedUser = userRepository.save(user);
        log.info("User updated successfully: {}", updatedUser.getUsername());

        return UserResponseDto.fromEntity(updatedUser);
    }

    // 사용자 삭제 (본인만)
    public void deleteUser(Long id, String currentUsername) {
        log.info("Deleting user: {}", id);

        User user = userRepository.findById(id)
                .orElseThrow(() -> new CustomException(ErrorCode.USER_NOT_FOUND));

        // 본인 확인
        if (!user.getUsername().equals(currentUsername)) {
            throw new CustomException(ErrorCode.ACCESS_DENIED, "본인의 계정만 삭제할 수 있습니다");
        }

        userRepository.delete(user);
        log.info("User deleted successfully: {}", id);
    }

    // 현재 로그인한 사용자 정보 조회
    @Transactional(readOnly = true)
    public UserResponseDto getCurrentUser(String username) {
        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> new CustomException(ErrorCode.USER_NOT_FOUND));
        return UserResponseDto.fromEntity(user);
    }
}
