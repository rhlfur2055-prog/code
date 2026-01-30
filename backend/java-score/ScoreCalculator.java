import java.util.*;
import java.io.*;

/**
 * 점수 계산 및 등급 산출 시스템
 * 컴파일: javac -encoding UTF-8 ScoreCalculator.java
 * 실행: java -Dfile.encoding=UTF-8 ScoreCalculator
 */
public class ScoreCalculator {
    
    // 등급 정보를 담는 레코드
    record GradeResult(
        double score,
        String grade,
        String description,
        String emoji,
        double gpa,
        boolean passed,
        String message
    ) {}
    
    /**
     * 점수를 기반으로 등급을 계산합니다.
     */
    public static GradeResult calculateGrade(double score) {
        if (score < 0 || score > 100) {
            throw new IllegalArgumentException("점수는 0-100 사이여야 합니다.");
        }
        
        String grade, description, emoji;
        double gpa;
        boolean passed = true;
        
        if (score >= 95) {
            grade = "A+"; description = "최우수"; emoji = "🏆"; gpa = 4.5;
        } else if (score >= 90) {
            grade = "A"; description = "우수"; emoji = "🥇"; gpa = 4.0;
        } else if (score >= 85) {
            grade = "B+"; description = "우량"; emoji = "🥈"; gpa = 3.5;
        } else if (score >= 80) {
            grade = "B"; description = "양호"; emoji = "🥉"; gpa = 3.0;
        } else if (score >= 75) {
            grade = "C+"; description = "보통+"; emoji = "📗"; gpa = 2.5;
        } else if (score >= 70) {
            grade = "C"; description = "보통"; emoji = "📘"; gpa = 2.0;
        } else if (score >= 65) {
            grade = "D+"; description = "미흡+"; emoji = "📙"; gpa = 1.5;
        } else if (score >= 60) {
            grade = "D"; description = "미흡"; emoji = "📕"; gpa = 1.0;
        } else {
            grade = "F"; description = "불합격"; emoji = "❌"; gpa = 0.0; passed = false;
        }
        
        String message = String.format("%s %.1f점 - %s등급 (%s)", emoji, score, grade, description);
        return new GradeResult(score, grade, description, emoji, gpa, passed, message);
    }
    
    /**
     * 여러 점수의 평균을 계산합니다.
     */
    public static Map<String, Object> calculateAverage(double[] scores) {
        if (scores == null || scores.length == 0) {
            throw new IllegalArgumentException("점수 배열이 비어있습니다.");
        }
        
        double total = 0;
        for (double score : scores) {
            total += score;
        }
        double average = total / scores.length;
        
        GradeResult gradeResult = calculateGrade(average);
        
        Map<String, Object> result = new HashMap<>();
        result.put("scores", scores);
        result.put("total", total);
        result.put("average", Math.round(average * 100.0) / 100.0);
        result.put("count", scores.length);
        result.put("grade", gradeResult.grade());
        result.put("description", gradeResult.description());
        result.put("emoji", gradeResult.emoji());
        result.put("gpa", gradeResult.gpa());
        result.put("passed", gradeResult.passed());
        result.put("message", gradeResult.message());
        
        return result;
    }
    
    /**
     * 결과 리포트를 출력합니다.
     */
    public static void printReport(Map<String, Object> result) {
        System.out.println("\n" + "=".repeat(50));
        System.out.println("📊 성적 계산 결과");
        System.out.println("=".repeat(50));
        
        if (result.containsKey("scores")) {
            double[] scores = (double[]) result.get("scores");
            System.out.printf("%n[입력 점수]: %s%n", Arrays.toString(scores));
            System.out.printf("[총점]: %.1f점%n", result.get("total"));
            System.out.printf("[평균]: %.2f점%n", result.get("average"));
        }
        
        System.out.println("\n" + result.get("message"));
        boolean passed = (boolean) result.get("passed");
        System.out.printf("[합격 여부]: %s%n", passed ? "✅ 합격" : "❌ 불합격");
        System.out.println("=".repeat(50) + "\n");
    }
    
    public static void main(String[] args) {
        // UTF-8 인코딩 설정
        try {
            System.setOut(new PrintStream(System.out, true, "UTF-8"));
        } catch (UnsupportedEncodingException e) {
            // 기본 인코딩 사용
        }

        Scanner scanner = new Scanner(System.in);

        System.out.println("\n☕ Java 점수 계산 시스템\n");
        
        // 1. 단일 점수 계산
        System.out.println("1️⃣ 단일 점수 계산");
        double score = 87;
        GradeResult result1 = calculateGrade(score);
        System.out.println("   " + result1.message());
        
        // 2. 평균 점수 계산
        System.out.println("\n2️⃣ 평균 점수 계산");
        double[] scores = {85, 90, 78, 92, 88};
        Map<String, Object> result2 = calculateAverage(scores);
        printReport(result2);
        
        // 3. 사용자 입력
        System.out.println("3️⃣ 직접 점수 입력해보기");
        System.out.print("   점수를 입력하세요 (0-100): ");
        try {
            if (scanner.hasNextDouble()) {
                double userScore = scanner.nextDouble();
                GradeResult userResult = calculateGrade(userScore);
                System.out.println("   " + userResult.message());
            }
        } catch (Exception e) {
            System.out.println("   ❌ 잘못된 입력입니다.");
        }
        
        scanner.close();
    }
}
