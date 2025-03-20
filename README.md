# PDF 2 Pocketmod

A command-line app to convert a normal pdf page to a pocketmod page (8 pages in one page).

## Usage

pdf2pocketmod create input.pdf -o output.pdf -s start_page

Options:
  -o, --output PATH
  -s, --start-page INTEGER  The page to start from.


## Installation

If you want to install the package as a cli tool systemwide, you can use the following command:

`uv pip install -e . --system`

The `-e` flag installs the package in editable mode, which means that changes to the source code will be immediately reflected in the installed package.

The `--system` flag installs the package in the system-wide Python environment, which means that the package will be available to all users on the system.