import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

filepath = 'src/data/contents/javascript.json'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

print("Original file size:", len(content))

# The issue: [..."HELLO\"] should be [...\"HELLO\"]
# In the raw JSON string, the opening quote of HELLO is not escaped

# Fix: Replace [..."HELLO with [...\"HELLO
# This needs to handle the case where the opening quote is not escaped

# Let's look for patterns where we have spread operator followed by unescaped quote
# The pattern [..."HELLO\"] in JSON should be [...\"HELLO\"]

# Actually looking at the error context:
# 'const arr1 = [..."HELLO\\"];  // [\\"H\\",'
# The issue is the first quote in "HELLO is not escaped but the closing one is

fixed_content = content.replace('[..."HELLO\\"]', '[...\\"HELLO\\"]')

if fixed_content != content:
    print("Fix applied: [...\"HELLO\\\"] -> [...\\\"HELLO\\\"]")

    # Verify the fix
    try:
        json.loads(fixed_content)
        print("JSON is now valid!")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print("File saved successfully!")
    except json.JSONDecodeError as e:
        print(f"Still has error: {e}")
        print("Looking for more issues...")

        # Show context around new error
        pos = e.pos
        start = max(0, pos - 50)
        end = min(len(fixed_content), pos + 50)
        print(f"Context: {repr(fixed_content[start:end])}")
else:
    print("Pattern not found, trying alternative approach...")

    # Try to find any unescaped quotes in spread patterns
    # Look for [..." where the quote should be escaped
    pattern = r'\[\.\.\."([^"\\])'
    matches = list(re.finditer(pattern, content))
    print(f"Found {len(matches)} potential issues")

    for m in matches:
        start = max(0, m.start() - 10)
        end = min(len(content), m.end() + 20)
        print(f"At {m.start()}: {repr(content[start:end])}")
