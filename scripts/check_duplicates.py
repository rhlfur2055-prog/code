#!/usr/bin/env python3
"""
Check for duplicate content in HTML files
"""
import os
import re
import hashlib
from collections import defaultdict
from pathlib import Path

def extract_code_content(html_content):
    """Extract the code example from HTML"""
    # Find code block content
    code_match = re.search(r'<pre><code>(.*?)</code></pre>', html_content, re.DOTALL)
    if code_match:
        return code_match.group(1).strip()
    return ""

def extract_main_content(html_content):
    """Extract main content sections"""
    # Remove style and head sections
    content = re.sub(r'<style>.*?</style>', '', html_content, flags=re.DOTALL)
    content = re.sub(r'<head>.*?</head>', '', content, flags=re.DOTALL)
    # Get body content
    body_match = re.search(r'<body>(.*?)</body>', content, re.DOTALL)
    if body_match:
        return body_match.group(1).strip()
    return content

def get_content_hash(content):
    """Get hash of content"""
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def main():
    study_dir = Path(r"c:\tools\codemaster-next-main\public\study")

    # Dictionary to store files by their code content hash
    code_duplicates = defaultdict(list)
    content_duplicates = defaultdict(list)

    total_files = 0

    for html_file in study_dir.rglob("*.html"):
        if html_file.name == "index.html":
            continue

        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            total_files += 1

            # Extract and hash code content
            code_content = extract_code_content(content)
            if code_content:
                code_hash = get_content_hash(code_content)
                code_duplicates[code_hash].append(str(html_file))

        except Exception as e:
            print(f"Error reading {html_file}: {e}")

    print(f"\n{'='*60}")
    print(f"Total HTML files analyzed: {total_files}")
    print(f"{'='*60}\n")

    # Find duplicates (groups with more than 1 file)
    duplicate_groups = {k: v for k, v in code_duplicates.items() if len(v) > 1}

    print(f"Found {len(duplicate_groups)} groups of duplicate code content:\n")

    # Sort by number of duplicates (most duplicates first)
    sorted_groups = sorted(duplicate_groups.items(), key=lambda x: len(x[1]), reverse=True)

    total_duplicates = 0
    for i, (hash_val, files) in enumerate(sorted_groups[:20], 1):  # Show top 20
        print(f"\n--- Group {i}: {len(files)} files with identical code ---")
        total_duplicates += len(files)

        # Show first file's code snippet
        try:
            with open(files[0], 'r', encoding='utf-8') as f:
                content = f.read()
            code = extract_code_content(content)[:200]
            print(f"Code preview: {code}...")
        except:
            pass

        # Show file paths (shortened)
        for f in files[:5]:
            short_path = f.replace(str(study_dir), "")
            print(f"  - {short_path}")
        if len(files) > 5:
            print(f"  ... and {len(files) - 5} more files")

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  - Total files: {total_files}")
    print(f"  - Unique code content: {len(code_duplicates)}")
    print(f"  - Duplicate groups: {len(duplicate_groups)}")
    print(f"  - Files with duplicate code: {sum(len(v) for v in duplicate_groups.values())}")
    print(f"{'='*60}")

    # Write detailed report
    report_path = Path(r"c:\tools\codemaster-next-main\scripts\duplicate_report.txt")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("Duplicate Content Report\n")
        f.write("="*60 + "\n\n")

        for i, (hash_val, files) in enumerate(sorted_groups, 1):
            f.write(f"\n--- Group {i}: {len(files)} files ---\n")
            for file_path in files:
                short_path = file_path.replace(str(study_dir), "")
                f.write(f"  {short_path}\n")

    print(f"\nDetailed report saved to: {report_path}")

if __name__ == "__main__":
    main()
