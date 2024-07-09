import re
import math
from collections import Counter
import os
import tempfile
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
    print(f"Potential Base64 strings found: {len(potential_b64_strings)}")
    
    b64_strings = []
    for s in potential_b64_strings:
        e = entropy(s)
        is_b64 = is_likely_base64(s)
        print(f"String: {s[:30]}... Length: {len(s)}, Entropy: {e:.2f}, Is Base64: {is_b64}")
        if is_b64 and ((3.0 < e < 5) or len(s) >= blob_threshold):
            b64_strings.append(s)
    
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

# Test function
def test_base64_detector():
    with tempfile.TemporaryDirectory() as tmpdirname:
        file1 = os.path.join(tmpdirname, "file1.txt")
        with open(file1, 'w') as f:
            f.write("This is a normal text file with no Base64 encoding.")
        
        file2 = os.path.join(tmpdirname, "file2.txt")
        with open(file2, 'w') as f:
            f.write("This file has a small Base64 string: SGVsbG8gV29ybGQh")
        
        file3 = os.path.join(tmpdirname, "file3.txt")
        with open(file3, 'w') as f:
            f.write(base64.b64encode(b"A" * 1000).decode('utf-8'))
        
        file4 = os.path.join(tmpdirname, "file4.txt")
        with open(file4, 'w') as f:
            f.write("SGVsbG8gV29ybGQh\n" * 15)
        
        for file in [file1, file2, file3, file4]:
            print(f"\nAnalyzing {os.path.basename(file)}:")
            result = analyze_base64(file, min_length=10, string_count_threshold=5)
            for key, value in result.items():
                print(f"  {key}: {value}")

if __name__ == "__main__":
    test_base64_detector()
