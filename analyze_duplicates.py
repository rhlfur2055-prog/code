import json
import sys
from pathlib import Path
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

contents_dir = Path(r"c:\tools\codemaster-next-main\codemaster-next-main\codemaster-next-main\src\data\contents")

print("=" * 80)
print("콘텐츠 중복 분석 리포트")
print("=" * 80)

# 분석 결과 저장
all_results = []

for json_file in sorted(contents_dir.glob("*.json")):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    category = json_file.stem

    # 각 항목의 description과 concept content 수집
    descriptions = defaultdict(list)
    concepts = defaultdict(list)
    codes = defaultdict(list)

    total_items = 0
    placeholder_items = 0

    for key, item in data.items():
        total_items += 1

        if item.get('isPlaceholder', False):
            placeholder_items += 1
            continue

        # description 중복 체크
        desc = item.get('description', '')
        if desc:
            descriptions[desc].append(key)

        # sections 내 concept과 code 체크
        for section in item.get('sections', []):
            if section.get('type') == 'concept':
                content = section.get('content', '')
                if content and len(content) < 200:  # 짧은 개념은 중복 가능성 높음
                    concepts[content].append(key)
            elif section.get('type') == 'code':
                code = section.get('code', '')
                if code:
                    codes[code].append(key)

    # 중복 찾기 (2개 이상 동일)
    dup_descs = {k: v for k, v in descriptions.items() if len(v) > 1}
    dup_concepts = {k: v for k, v in concepts.items() if len(v) > 1}
    dup_codes = {k: v for k, v in codes.items() if len(v) > 1}

    if dup_descs or dup_concepts or dup_codes:
        result = {
            'category': category,
            'total': total_items,
            'placeholders': placeholder_items,
            'filled': total_items - placeholder_items,
            'dup_descs': dup_descs,
            'dup_concepts': dup_concepts,
            'dup_codes': dup_codes
        }
        all_results.append(result)

# 결과 출력
print("\n")
for result in all_results:
    cat = result['category']
    print(f"\n{'='*80}")
    print(f"[{cat.upper()}] - 총 {result['total']}개 (채워진: {result['filled']}, 비어있음: {result['placeholders']})")
    print("=" * 80)

    # Description 중복
    if result['dup_descs']:
        print(f"\n  [DESCRIPTION 중복] - {len(result['dup_descs'])}개 패턴")
        for desc, items in result['dup_descs'].items():
            print(f"\n    중복 텍스트: \"{desc[:60]}...\"" if len(desc) > 60 else f"\n    중복 텍스트: \"{desc}\"")
            print(f"    영향받는 항목 ({len(items)}개):")
            for item in items[:10]:  # 최대 10개만 표시
                print(f"      - {item}")
            if len(items) > 10:
                print(f"      ... 외 {len(items) - 10}개")

    # Concept 중복
    if result['dup_concepts']:
        print(f"\n  [CONCEPT 중복] - {len(result['dup_concepts'])}개 패턴")
        for concept, items in result['dup_concepts'].items():
            print(f"\n    중복 텍스트: \"{concept[:60]}...\"" if len(concept) > 60 else f"\n    중복 텍스트: \"{concept}\"")
            print(f"    영향받는 항목 ({len(items)}개):")
            for item in items[:10]:
                print(f"      - {item}")
            if len(items) > 10:
                print(f"      ... 외 {len(items) - 10}개")

    # Code 중복
    if result['dup_codes']:
        print(f"\n  [CODE 중복] - {len(result['dup_codes'])}개 패턴")
        for code, items in result['dup_codes'].items():
            code_preview = code.replace('\r\n', ' ').replace('\n', ' ')[:50]
            print(f"\n    중복 코드: \"{code_preview}...\"")
            print(f"    영향받는 항목 ({len(items)}개):")
            for item in items[:10]:
                print(f"      - {item}")
            if len(items) > 10:
                print(f"      ... 외 {len(items) - 10}개")

# 요약
print("\n\n" + "=" * 80)
print("요약")
print("=" * 80)
total_dup_items = 0
for result in all_results:
    cat = result['category']
    dup_count = 0
    for items in result['dup_descs'].values():
        dup_count += len(items) - 1  # 원본 제외
    for items in result['dup_concepts'].values():
        dup_count += len(items) - 1
    total_dup_items += dup_count
    if dup_count > 0:
        print(f"  {cat}: {dup_count}개 항목이 중복 콘텐츠 사용")

print(f"\n  총 중복 의심 항목: {total_dup_items}개")
print("\n  원인 추정:")
print("    - 템플릿 콘텐츠가 각 항목별로 개별화되지 않음")
print("    - 동일한 기본 description/code가 모든 항목에 복사됨")
print("    - isPlaceholder: false로 표시되었지만 실제 콘텐츠 없음")
