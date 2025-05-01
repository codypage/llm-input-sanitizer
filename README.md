# llm-input-sanitizer

A CLI tool that sanitizes untrusted input before feeding it into an LLM context. Removes prompt injections, base64 blobs, invisible characters, and other adversarial patterns.

## Usage
```bash
python llm_input_sanitizer.py input.txt -o output.txt
```
