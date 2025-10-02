#!/usr/bin/env python3
# replace_space_with_entity.py
# Заменяет все пробелы в каждой строке на: %20"&quot;"%20
# Usage:
#   python3 replace_space_with_entity.py input.txt
# Output:
#   input.txt.obf4

import sys
from pathlib import Path

REPLACEMENT = '%20"&quot;"%20'

def transform_line(line: str) -> str:
    # заменяем все пробелы (ASCII 0x20)
    return line.replace(' ', REPLACEMENT)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 xss_bypass_swapSpaces.py input_file.txt", file=sys.stderr)
        sys.exit(2)

    in_path = Path(sys.argv[1])
    if not in_path.is_file():
        print(f"Input file not found: {in_path}", file=sys.stderr)
        sys.exit(1)

    out_path = in_path.with_name(in_path.name + ".obf4")

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
