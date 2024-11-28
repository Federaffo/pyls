import json
import argparse
import os
import datetime
from typing import List, Dict, Optional


def human_readable(size: int) -> str:
    """Convert byte size to a human-readable format."""
    units = ["", "K", "M", "G", "T"]
    index = 0
    while size >= 1024 and index < len(units) - 1:
        size /= 1024
        index += 1
    return f"{size:.1f}{units[index]}" if size % 1 != 0 else f"{int(size)}{units[index]}"


def load_filesystem(path: str) -> Dict[str, any]:
    """Load the filesystem structure from a JSON file."""
    with open(path) as file:
        return json.load(file)


def navigate_to_path(filesystem: Dict[str, any], path: str) -> Optional[Dict[str, any]]:
    """Navigate to a specific path within the filesystem structure."""
    if path in ("", "."):
        return filesystem
    
    parts = path.strip('./').split('/')
    for part in parts:
        sub_items = filesystem.get("contents", [])
        filesystem = next((item for item in sub_items if item.get("name") == part), None)
        if filesystem is None:
            print(f"error: cannot access '{path}': No such file or directory")
            return None
    return filesystem


def sort_items(sub_items: List[Dict[str, any]], time_ordered: bool, reversed: bool) -> List[Dict[str, any]]:
    """Sort items based on the specified criteria."""
    if time_ordered:
        sub_items.sort(key=lambda x: x.get("time_modified"))
    if reversed:
        sub_items.reverse()
    return sub_items


def format_item(item: Dict[str, any], long: bool) -> str:
    """Format a single item for output."""
    name = item.get("name")
    size = human_readable(item.get("size"))
    modified_time = datetime.datetime.fromtimestamp(item.get("time_modified")).strftime('%b %d %H:%M')
    permissions = item.get("permissions")
    
    if long:
        return f"{permissions} {size:>5} {modified_time} {name}"
    return name


def filter_items(sub_items: List[Dict[str, any]], filter: Optional[str], all: bool) -> List[Dict[str, any]]:
    """Filter items based on the provided filter criteria."""

    if not all:
        sub_items = [x for x in sub_items if x.get("name")[0] != '.']

    if filter == "dir":
        return [x for x in sub_items if x.get("contents")]
    elif filter == "file":
        return [x for x in sub_items if not x.get("contents")]
    return sub_items

def get_output_separator(long: bool) -> str:
    if long:
        return '\n'
    
    return ' '

def main(all: bool = False, long: bool = False, reversed: bool = False,
         time_ordered: bool = False, filter: Optional[str] = "", path: str = "") -> None:
    """Main function to list the filesystem contents."""
    filesystem = load_filesystem("structure.json")
    filesystem = navigate_to_path(filesystem, path)
    
    if filesystem is None:
        return
    
    sub_items = filesystem.get("contents", None)
    if sub_items is None and path:
        sub_items = [filesystem]

    sub_items = sort_items(sub_items, time_ordered, reversed)
    sub_items = filter_items(sub_items, filter,  all)
    
    separator = get_output_separator(long=long)
    output = separator.join(format_item(x, long) for x in sub_items)

    print(output)


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

    main(all=args.A, long=args.l, reversed=args.r, time_ordered=args.t, filter=args.filter, path=args.path)
