## Base64 Detector

The Base64 Detector is a Python script designed to identify Base64 encoded content within files. I employ several strategies to accurately detect Base64 strings while also attempting to minimize false positives.

Features:
1. **Regex Pattern Matching**: Uses regular expressions to identify potential Base64 strings.
2. **Entropy Calculation**: Computes the entropy of potential Base64 strings to filter out low-complexity data.
3. **Base64 Validation**: Attempts to decode potential Base64 strings to confirm their validity.
4. **Large Blob Detection**: Identifies large chunks of Base64 encoded data.
5. **Multiple String Detection**: Counts the number of Base64 strings in a file.

The script provides four main outputs:
- `has_any_base64`: Indicates if any Base64 content was found.
- `has_large_blob`: Indicates if a large Base64 encoded blob was detected.
- `string_count`: The number of Base64 strings found.
- `has_lots_of_strings`: Indicates if the file contains many Base64 strings.

Usage:
```
python base64-detector-script.py /full/path/to/file
```

## Test Script

The test script is designed to validate and demonstrate the functionality of the Base64 detector. It creates a set of test files with various Base64 encoding scenarios and runs the Detector on each file.

Components:
1. **Test File Generation**: Creates four test files:
   - A file with no Base64 content
   - A file with a small Base64 string
   - A file with a large Base64 blob
   - A file with multiple Base64 strings
2. **Detector Invocation**: Runs the Base64 Detector on each test file.
3. **Result Output**: Displays detailed results for each test case, including entropy values and string lengths.

The test script helps in:
- Verifying the Detector's accuracy across different scenarios
- Fine-tuning detection parameters
- Demonstrating the Detector's capabilities

Usage:
```
python base64-detector-test-script.py /full/path/to/file
```

Both scripts together provide a workable solution for identifying Base64 encoded content in files, useful for various applications such as malware analysis, data processing, and file integrity checking.
