import re
import math
from collections import Counter
import base64

def analyze_base64(file_path, min_length=20, blob_threshold=1000, string_count_threshold=10):
    with open(file_path, 'rb') as file:
        content = file.read().decode('utf-8', errors='ignore')
    
    def entropy(s):
        p, lns = Counter(s), float(len(s))
        return -sum(count/lns * math.log(count/lns, 2) for count in p.values())
    
    def is_likely_base64(s):
        if len(s) % 4 != 0:
            return False
        try:
            base64.b64decode(s, validate=True)
            return True
        except Exception:
            return False
    
    potential_b64_strings = re.findall(r'[A-Za-z0-9+/]{%d,}={0,2}' % min_length, content)
    
    b64_strings = [s for s in potential_b64_strings if is_likely_base64(s) and 
                   ((3.0 < entropy(s) < 5) or len(s) >= blob_threshold)]
    
    has_any_b64 = len(b64_strings) > 0
    has_large_blob = any(len(s) >= blob_threshold for s in b64_strings)
    string_count = len(b64_strings)
    has_lots_of_strings = string_count > string_count_threshold
    
    return {
        "has_any_base64": has_any_b64,
        "has_large_blob": has_large_blob,
        "string_count": string_count,
        "has_lots_of_strings": has_lots_of_strings
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python base64_detector.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    result = analyze_base64(file_path)
    
    print("Base64 Detection Results:")
    for key, value in result.items():
        print(f"  {key}: {value}")
