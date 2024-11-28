import json
from unittest.mock import patch, mock_open
from pyls import  main, human_readable, list_filesystem  # Adjusted import to reflect the correct module path

# Sample data to be used in tests, based on the provided structure.json
mock_filesystem = {
    "name": "interpreter",
    "size": 4096,
    "time_modified": 1699957865,
    "permissions": "-rw-r--r--",
    "contents": [
        {"name": ".gitignore", "size": 8911, "time_modified": 1699941437, "permissions": "drwxr-xr-x"},
        {"name": "LICENSE", "size": 1071, "time_modified": 1699941437, "permissions": "drwxr-xr-x"},
        {"name": "README.md", "size": 83, "time_modified": 1699941437, "permissions": "drwxr-xr-x"},
        {
            "name": "ast",
            "size": 4096,
            "time_modified": 1699957739,
            "permissions": "-rw-r--r--",
            "contents": [
                {"name": "go.mod", "size": 225, "time_modified": 1699957780, "permissions": "-rw-r--r--"},
                {"name": "ast.go", "size": 837, "time_modified": 1699957719, "permissions": "drwxr-xr-x"}
            ]
        },
        {"name": "go.mod", "size": 60, "time_modified": 1699950073, "permissions": "drwxr-xr-x"},
        {
            "name": "lexer",
            "size": 4096,
            "time_modified": 1699955487,
            "permissions": "drwxr-xr-x",
            "contents": [
                {"name": "lexer_test.go", "size": 1729, "time_modified": 1699955126, "permissions": "drwxr-xr-x"},
                {"name": "go.mod", "size": 227, "time_modified": 1699944819, "permissions": "-rw-r--r--"},
                {"name": "lexer.go", "size": 2886, "time_modified": 1699955487, "permissions": "drwxr-xr-x"}
            ]
        },
        {"name": "main.go", "size": 74, "time_modified": 1699950453, "permissions": "-rw-r--r--"},
        {
            "name": "parser",
            "size": 4096,
            "time_modified": 1700205662,
            "permissions": "drwxr-xr-x",
            "contents": [
                {"name": "parser_test.go", "size": 1342, "time_modified": 1700205662, "permissions": "drwxr-xr-x"},
                {"name": "parser.go", "size": 1622, "time_modified": 1700202950, "permissions": "-rw-r--r--"},
                {"name": "go.mod", "size": 533, "time_modified": 1699958000, "permissions": "drwxr-xr-x"}
            ]
        },
        {
            "name": "token",
            "size": 4096,
            "time_modified": 1699954070,
            "permissions": "-rw-r--r--",
            "contents": [
                {"name": "token.go", "size": 910, "time_modified": 1699954070, "permissions": "-rw-r--r--"},
                {"name": "go.mod", "size": 66, "time_modified": 1699944730, "permissions": "drwxr-xr-x"}
            ]
        }
    ]
}

def test_main():
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_filesystem))), \
        patch("builtins.print") as mock_print:
        list_filesystem(all=False, long=False, reversed=False, time_ordered=False, filter="")
        mock_print.assert_called_once_with(
            "LICENSE README.md ast go.mod lexer main.go parser token"
        )

def test_main_all_files():
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_filesystem))), \
        patch("builtins.print") as mock_print:
        list_filesystem(all=True, long=False, reversed=False, time_ordered=False, filter="")
        mock_print.assert_called_once_with(
            ".gitignore LICENSE README.md ast go.mod lexer main.go parser token"
        )



def test_main_filter_files():
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_filesystem))), \
        patch("builtins.print") as mock_print:
        list_filesystem(all=False, long=False, reversed=False, time_ordered=False, filter="file")
        mock_print.assert_called_once_with("LICENSE README.md go.mod main.go")

def test_human_readable():
    assert human_readable(1024) == "1K"
    assert human_readable(2048) == "2K"
    assert human_readable(1048576) == "1M"
    assert human_readable(1234567890) == "1.1G"

def test_main_filter_directories():
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_filesystem))), \
        patch("builtins.print") as mock_print:
        list_filesystem(all=False, long=False, reversed=False, time_ordered=False, filter="dir")
        mock_print.assert_called_once_with("ast lexer parser token")

def test_main_long_listing():
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_filesystem))), \
        patch("builtins.print") as mock_print:
        list_filesystem(all=False, long=True, reversed=False, time_ordered=False, filter="")
        mock_print.assert_called_once_with(
            "drwxr-xr-x  1.0K Nov 14 06:57 LICENSE\n"
            "drwxr-xr-x    83 Nov 14 06:57 README.md\n"
            "-rw-r--r--    4K Nov 14 11:28 ast\n"
            "drwxr-xr-x    60 Nov 14 09:21 go.mod\n"
            "drwxr-xr-x    4K Nov 14 10:51 lexer\n"
            "-rw-r--r--    74 Nov 14 09:27 main.go\n"
            "drwxr-xr-x    4K Nov 17 08:21 parser\n"
            "-rw-r--r--    4K Nov 14 10:27 token"
        )

def test_main_reversed_order():
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_filesystem))), \
        patch("builtins.print") as mock_print:
        list_filesystem(all=False, long=False, reversed=True, time_ordered=False, filter="")
        mock_print.assert_called_once_with(
            "token parser main.go lexer go.mod ast README.md LICENSE"
        )

def test_main_time_ordered():
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_filesystem))), \
        patch("builtins.print") as mock_print:
        list_filesystem(all=False, long=False, reversed=False, time_ordered=True, filter="")
        mock_print.assert_called_once_with(
            "LICENSE README.md go.mod main.go token lexer ast parser"
        )
