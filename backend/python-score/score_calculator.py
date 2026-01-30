#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
점수 계산 및 등급 산출 시스템
실행: python score_calculator.py
"""

def calculate_grade(score: float) -> dict:
    """
    점수를 기반으로 등급을 계산합니다.
    
    Args:
        score: 0-100 사이의 점수
        
    Returns:
        등급 정보가 담긴 딕셔너리
    """
    if not 0 <= score <= 100:
        raise ValueError("점수는 0-100 사이여야 합니다.")
    
    grade_table = [
        (95, 'A+', '최우수', '🏆', 4.5),
        (90, 'A', '우수', '🥇', 4.0),
        (85, 'B+', '우량', '🥈', 3.5),
        (80, 'B', '양호', '🥉', 3.0),
        (75, 'C+', '보통+', '📗', 2.5),
        (70, 'C', '보통', '📘', 2.0),
        (65, 'D+', '미흡+', '📙', 1.5),
        (60, 'D', '미흡', '📕', 1.0),
        (0, 'F', '불합격', '❌', 0.0),
    ]
    
    for min_score, grade, description, emoji, gpa in grade_table:
        if score >= min_score:
            return {
                'score': score,
                'grade': grade,
                'description': description,
                'emoji': emoji,
                'gpa': gpa,
                'passed': grade != 'F',
                'message': f"{emoji} {score}점 - {grade}등급 ({description})"
            }
    
    return {'score': score, 'grade': 'F', 'description': '불합격', 'emoji': '❌', 'gpa': 0.0, 'passed': False}


def calculate_average(scores: list) -> dict:
    """여러 과목의 평균 점수와 등급을 계산합니다."""
    if not scores:
        raise ValueError("점수 목록이 비어있습니다.")
    
    total = sum(scores)
    average = total / len(scores)
    grade_info = calculate_grade(average)
    
    return {
        'scores': scores,
        'total': total,
        'average': round(average, 2),
        'subject_count': len(scores),
        **grade_info
    }


def calculate_weighted_score(scores: dict, weights: dict) -> dict:
    """가중치를 적용한 점수를 계산합니다."""
    if set(scores.keys()) != set(weights.keys()):
        raise ValueError("점수와 가중치의 과목이 일치하지 않습니다.")
    
    if abs(sum(weights.values()) - 1.0) > 0.001:
        raise ValueError("가중치의 합은 1.0이어야 합니다.")
    
    weighted_total = sum(scores[subject] * weights[subject] for subject in scores)
    grade_info = calculate_grade(weighted_total)
    
    details = []
    for subject, score in scores.items():
        weight = weights[subject]
        weighted = score * weight
        details.append({
            'subject': subject,
            'score': score,
            'weight': f"{weight*100:.0f}%",
            'weighted_score': round(weighted, 2)
        })
    
    return {
        'details': details,
        'weighted_total': round(weighted_total, 2),
        **grade_info
    }


def print_report(result: dict):
    """결과 리포트를 출력합니다."""
    print("\n" + "="*50)
    print("📊 성적 계산 결과")
    print("="*50)
    
    if 'details' in result:
        print("\n[과목별 점수]")
        for d in result['details']:
            print(f"  • {d['subject']}: {d['score']}점 (가중치: {d['weight']}) → {d['weighted_score']}점")
        print(f"\n[가중 평균]: {result['weighted_total']}점")
    elif 'scores' in result:
        print(f"\n[입력 점수]: {result['scores']}")
        print(f"[총점]: {result['total']}점")
        print(f"[평균]: {result['average']}점")
    
    print(f"\n{result['message']}")
    print(f"[합격 여부]: {'✅ 합격' if result['passed'] else '❌ 불합격'}")
    print("="*50 + "\n")


if __name__ == "__main__":
    print("\n🐍 Python 점수 계산 시스템\n")
    
    # 1. 단일 점수 계산
    print("1️⃣ 단일 점수 계산")
    score = 87
    result = calculate_grade(score)
    print(f"   {result['message']}")
    
    # 2. 평균 점수 계산
    print("\n2️⃣ 평균 점수 계산")
    scores = [85, 90, 78, 92, 88]
    result = calculate_average(scores)
    print_report(result)
    
    # 3. 가중치 적용 계산
    print("3️⃣ 가중치 적용 계산")
    subject_scores = {
        '중간고사': 85,
        '기말고사': 90,
        '과제': 95,
        '출석': 100
    }
    weights = {
        '중간고사': 0.3,
        '기말고사': 0.4,
        '과제': 0.2,
        '출석': 0.1
    }
    result = calculate_weighted_score(subject_scores, weights)
    print_report(result)
    
    # 4. 사용자 입력
    print("4️⃣ 직접 점수 입력해보기")
    try:
        user_score = float(input("   점수를 입력하세요 (0-100): "))
        result = calculate_grade(user_score)
        print(f"   {result['message']}")
    except ValueError as e:
        print(f"   ❌ 오류: {e}")
    except EOFError:
        print("   (입력 건너뜀)")
