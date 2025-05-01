import re
import unicodedata
from bs4 import BeautifulSoup
from pathlib import Path
import argparse
import sys

def sanitize_input(raw_text: str) -> str:
    soup = BeautifulSoup(raw_text, "html.parser")
    text_only = soup.get_text()
    normalized_text = unicodedata.normalize("NFKC", text_only)
    zero_width_pattern = r'[\u200B-\u200D\uFEFF]'
    no_zw_chars = re.sub(zero_width_pattern, '', normalized_text)
    base64_pattern = r'\b[A-Za-z0-9+/]{24,}={0,2}\b'
    no_base64 = re.sub(base64_pattern, '[REDACTED_ENCODED_BLOB]', no_zw_chars)
    injection_keywords = [
        r'ignore all previous instructions',
        r'you are now',
        r'disregard earlier context',
        r'respond only with',
        r'begin prompt'
    ]
    injection_pattern = re.compile("|".join(injection_keywords), re.IGNORECASE)
    no_injections = injection_pattern.sub('[REDACTED_INJECTION]', no_base64)
    cleaned = re.sub(r'\s+', ' ', no_injections).strip()
    return cleaned

def main():
    parser = argparse.ArgumentParser(description="LLM Input Sanitizer")
    parser.add_argument("input", nargs="?", help="Input file (optional)")
    parser.add_argument("-o", "--output", help="Output file (optional)")
    args = parser.parse_args()

    if args.input:
        raw_text = Path(args.input).read_text(encoding="utf-8")
    else:
        print("\n--- LLM Input Sanitizer ---")
        print("Type or paste your raw input. End input with a single line: END\n")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        raw_text = "\n".join(lines)

    sanitized = sanitize_input(raw_text)

    if args.output:
        Path(args.output).write_text(sanitized, encoding="utf-8")
        print(f"Sanitized output written to {args.output}")
    else:
        print("\n\n=== Original Input ===")
        print(raw_text)
        print("\n=== Sanitized Output ===")
        print(sanitized)

if __name__ == "__main__":
    main()
