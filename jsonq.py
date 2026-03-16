#!/usr/bin/env python3
"""jsonq - Query and transform JSON from CLI."""
import json, sys, argparse, re

def query(data, path):
    if not path or path == '.': return data
    parts = re.findall(r'\w+|\[\d+\]|\[\*\]|\[\?\(.+?\)\]', path.lstrip('.'))
    current = [data]
    for part in parts:
        next_vals = []
        for val in current:
            if part == '[*]':
                if isinstance(val, list): next_vals.extend(val)
                elif isinstance(val, dict): next_vals.extend(val.values())
            elif part.startswith('[') and part.endswith(']'):
                idx_str = part[1:-1]
                if idx_str.isdigit() or (idx_str.startswith('-') and idx_str[1:].isdigit()):
                    try: next_vals.append(val[int(idx_str)])
                    except: pass
            else:
                if isinstance(val, dict) and part in val:
                    next_vals.append(val[part])
                elif isinstance(val, list):
                    next_vals.extend(item.get(part) for item in val if isinstance(item, dict) and part in item)
        current = next_vals
    return current[0] if len(current) == 1 else current

def main():
    p = argparse.ArgumentParser(description='JSON query tool')
    p.add_argument('expression', nargs='?', default='.', help='Query expression')
    p.add_argument('-f', '--file', help='JSON file (default: stdin)')
    p.add_argument('-r', '--raw', action='store_true', help='Raw string output')
    p.add_argument('-c', '--compact', action='store_true', help='Compact output')
    p.add_argument('--keys', action='store_true', help='Show keys')
    p.add_argument('--type', action='store_true', help='Show type')
    p.add_argument('--length', action='store_true', help='Show length')
    p.add_argument('--flatten', action='store_true', help='Flatten nested')
    args = p.parse_args()

    if args.file:
        with open(args.file) as f: data = json.load(f)
    else:
        data = json.load(sys.stdin)

    result = query(data, args.expression)

    if args.keys:
        if isinstance(result, dict): print('\n'.join(result.keys()))
        return
    if args.type:
        print(type(result).__name__); return
    if args.length:
        print(len(result) if hasattr(result, '__len__') else 1); return
    if args.flatten and isinstance(result, list):
        flat = []
        def _flatten(v):
            if isinstance(v, list):
                for i in v: _flatten(i)
            else: flat.append(v)
        _flatten(result)
        result = flat

    if args.raw and isinstance(result, str):
        print(result)
    else:
        indent = None if args.compact else 2
        print(json.dumps(result, indent=indent, ensure_ascii=False, default=str))

if __name__ == '__main__':
    main()
