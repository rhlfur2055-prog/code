import json
import os
import sys
from pathlib import Path

# UTF-8 출력 설정
sys.stdout.reconfigure(encoding='utf-8')

def validate_json_file(filepath):
    """JSON 파일 유효성 검사"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            json.loads(content)
        return True, None
    except json.JSONDecodeError as e:
        return False, e

def find_json_error_location(filepath):
    """JSON 에러 위치 상세 분석"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        try:
            json.loads(content)
            return None
        except json.JSONDecodeError as e:
            pos = e.pos
            start = max(0, pos - 50)
            end = min(len(content), pos + 50)
            context = content[start:end]

            lines = content[:pos].split('\n')
            line_num = len(lines)
            col = len(lines[-1]) if lines else 0

            return {
                'file': str(filepath),
                'error': str(e),
                'line': line_num,
                'column': col,
                'position': pos,
                'context': context,
                'context_start': start
            }
    except Exception as e:
        return {'file': str(filepath), 'error': str(e)}

def main():
    contents_dir = Path(r"c:\tools\codemaster-next-main\codemaster-next-main\codemaster-next-main\src\data\contents")

    print("=" * 60)
    print("JSON Validation Check")
    print("=" * 60)

    errors = []
    valid_count = 0

    for json_file in sorted(contents_dir.glob("*.json")):
        is_valid, error = validate_json_file(json_file)

        if is_valid:
            print(f"[OK] {json_file.name}")
            valid_count += 1
        else:
            print(f"[ERROR] {json_file.name}")
            error_info = find_json_error_location(json_file)
            if error_info:
                errors.append(error_info)
                print(f"   Line: {error_info.get('line')}, Column: {error_info.get('column')}")

    print("\n" + "=" * 60)
    print(f"Valid: {valid_count}, Errors: {len(errors)}")
    print("=" * 60)

    for err in errors:
        print(f"\n--- Error Details ---")
        print(f"File: {err['file']}")
        print(f"Position: Line {err.get('line')}, Col {err.get('column')}")
        print(f"Message: {err['error']}")
        print(f"Context around error:")
        print(repr(err.get('context', '')))

if __name__ == "__main__":
    main()
