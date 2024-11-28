# Filesystem Structure Viewer

This project provides a command-line tool to list the contents of a filesystem structure from a JSON file.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/repository.git
   cd repository
   ```

2. **Install dependencies:**
   Make sure you have Python installed. You can install the required packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare the JSON file:**
   Create a `structure.json` file in the root directory of the project. This file should contain the filesystem structure you want to view.

## Usage

Run the script using Python with the following command:

```bash
python pyls.py -A -l -t
```

### Options

- `-A`: Show all files, including hidden ones.
- `-l`: Use a long listing format.
- `-r`: Reverse the order of the list.
- `-t`: Sort by time modified.
- `--filter <dir|file>`: Filter the output to show only directories or files.
- `path`: (Optional) Specify the path to list contents of. If not provided, it defaults to the root.

### Example

To list all files in a long format, sorted by time modified, you can run:

```bash
python pyls.py -A -l -t
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.