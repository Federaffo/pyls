import json
import argparse
from pprint import pprint
import datetime



def main(all = False, long = False, reversed = False, time_ordered = False, filter = ""):
    out = ""
    with open("structure.json") as file:
        filesystem = json.load(file)
    
    sub_items = filesystem.get("contents")

    if time_ordered:
        sub_items.sort(key=lambda x: x.get("time_modified"))

    if reversed:
        sub_items = sub_items[::-1]

    for x in sub_items:

        if not x.get("contents",None) and filter == "dir":
            continue

        if x.get("contents",None) and filter == "file":
            continue

        item_name = x.get("name")
        item_size = x.get("size")
        item_modified = datetime.datetime.utcfromtimestamp(x.get("time_modified")).strftime('%b %d %H:%M')
        item_permissions = x.get("permissions")

        if   all or item_name[0] != '.':
            if long:
                out += f"{item_permissions} {item_size:>5} {item_modified} {item_name}\n"
            else:
                out += f"{item_name} "
    
    print(out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some parameters.')
    parser.add_argument('-A', action='store_true', help='Show all files')
    parser.add_argument('-l', action='store_true', help='use a long listing format')
    parser.add_argument('-r', action='store_true', help='reverse the order of the list')
    parser.add_argument('-t', action='store_true', help='sort by time modified')
    parser.add_argument('--filter', type=str, help='Filter by file or directory name')
    args = parser.parse_args()
    if args.filter and  args.filter not in ("dir", "file"):
        raise ValueError(f"{args.filter} is not a valid filter criteria. Available filters are 'dir' and 'file'")

    
    main(all = args.A, long = args.l, reversed = args.r, time_ordered = args.t, filter = args.filter)