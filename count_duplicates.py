import json
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

filepath = r"c:\tools\codemaster-next-main\codemaster-next-main\codemaster-next-main\src\data\contents\algorithm.json"

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 70)
print("ALGORITHM.JSON 중복 분석")
print("=" * 70)

# 각 항목별 description, concept, code 추출
items_info = []

for key, item in data.items():
    desc = item.get('description', '')
    concept = ''
    code = ''

    for section in item.get('sections', []):
        if section.get('type') == 'concept':
            concept = section.get('content', '')
        elif section.get('type') == 'code':
            code = section.get('code', '')

    items_info.append({
        'key': key,
        'title': item.get('title', ''),
        'desc': desc,
        'concept': concept,
        'code': code[:100] if code else ''  # 코드 앞 100자
    })

# 중복 그룹화
desc_groups = defaultdict(list)
code_groups = defaultdict(list)

for item in items_info:
    desc_groups[item['desc']].append(item['key'])
    if item['code']:
        code_groups[item['code']].append(item['key'])

print(f"\n총 항목 수: {len(items_info)}개")

# Description 중복
print(f"\n{'='*70}")
print("DESCRIPTION 중복 현황")
print("=" * 70)

for desc, keys in sorted(desc_groups.items(), key=lambda x: -len(x[1])):
    if len(keys) > 1:
        print(f"\n[{len(keys)}개 중복] \"{desc[:50]}...\"")
        for k in keys:
            print(f"  - {k}")

# Code 중복
print(f"\n{'='*70}")
print("CODE 중복 현황")
print("=" * 70)

for code, keys in sorted(code_groups.items(), key=lambda x: -len(x[1])):
    if len(keys) > 1:
        code_preview = code.replace('\r\n', ' ').replace('\n', ' ')[:40]
        print(f"\n[{len(keys)}개 중복] \"{code_preview}...\"")
        for k in keys:
            print(f"  - {k}")

# 요약
print(f"\n{'='*70}")
print("요약")
print("=" * 70)

unique_descs = len([k for k, v in desc_groups.items() if len(v) == 1])
dup_descs = len(items_info) - unique_descs

unique_codes = len([k for k, v in code_groups.items() if len(v) == 1])
dup_codes = len([i for i in items_info if i['code']]) - unique_codes

print(f"Description: {unique_descs}개 고유 / {dup_descs}개 중복")
print(f"Code: {unique_codes}개 고유 / {dup_codes}개 중복")

# 완전히 동일한 콘텐츠 (desc + code 모두 같음)
full_dup = defaultdict(list)
for item in items_info:
    key = (item['desc'], item['code'])
    full_dup[key].append(item['key'])

total_full_dup = sum(len(v) for k, v in full_dup.items() if len(v) > 1)
print(f"\n완전 중복 (description + code 모두 동일): {total_full_dup}개")
