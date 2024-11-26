import json
import argparse
from pprint import pprint
import datetime
from typing import List, Dict, Optional

def human_readable(size: int) -> str:
    units = ["", "K", "M", "G", "T"]
    index = 0
    while size >= 1024 and index < len(units) - 1:
        size /= 1024
        index += 1
    return f"{size:.1f}{units[index]}" if size % 1 != 0 else f"{int(size)}{units[index]}"

def load_filesystem(path: str) -> Dict[str, any]:
    with open(path) as file:
        return json.load(file)

def navigate_to_path(filesystem: Dict[str, any], path: str) -> Optional[Dict[str, any]]:
    parts = path.split('/')
    for part in parts:
        if part:  # Skip empty parts
            sub_items = filesystem.get("contents", [])
            filesystem = next((item for item in sub_items if item.get("name") == part), None)
            if filesystem is None:
                print(f"error: cannot access '{path}': No such file or directory")
                return None
    return filesystem

def main(all: bool = False, long: bool = False, reversed: bool = False, 
         time_ordered: bool = False, filter: Optional[str] = "", path: str = "") -> None:
    filesystem = load_filesystem("structure.json")
    
    # Normalize the path
    if path in ["", "."]:
        path = ""
    elif path.startswith("./"):
        path = path[2:]

    filesystem = navigate_to_path(filesystem, path)
    if filesystem is None:
        return

    sub_items = filesystem.get("contents", [])

    if time_ordered:
        sub_items.sort(key=lambda x: x.get("time_modified"))

    if reversed:
        sub_items = sub_items[::-1]

    out = ""
    for x in sub_items:
        if not x.get("contents") and filter == "dir":
            continue
        if x.get("contents") and filter == "file":
            continue

        item_name = x.get("name")
        item_size = human_readable(x.get("size"))

        # Timestamp is not specified in task description
        item_modified = datetime.datetime.fromtimestamp(x.get("time_modified")).strftime('%b %d %H:%M')
        item_permissions = x.get("permissions")

        if all or item_name[0] != '.':
            if long:
                out += f"{item_permissions} {item_size:>5} {item_modified} {item_name}\n"
            else:
                out += f"{item_name} "
    
    print(out)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='List contents of a filesystem structure from a JSON file.')
    parser.add_argument('-A', action='store_true', help='Show all files')
    parser.add_argument('-l', action='store_true', help='Use a long listing format')
    parser.add_argument('-r', action='store_true', help='Reverse the order of the list')
    parser.add_argument('-t', action='store_true', help='Sort by time modified')
    parser.add_argument('--filter', type=str, choices=['dir', 'file'], help='Filter by file or directory name')
    parser.add_argument('path', type=str, nargs='?', default='', help='Path to list contents of')
    
    args = parser.parse_args()
    if args.filter and args.filter not in ("dir", "file"):
        print(f"{args.filter} is not a valid filter criteria. Available filters are 'dir' and 'file'")

    
    main(all = args.A, long = args.l, reversed = args.r, time_ordered = args.t, filter = args.filter, path = args.path)