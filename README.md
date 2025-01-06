
# Symlink Converter

A simple GUI application that helps you convert symbolic links (symlinks) to regular files while preserving the original folder structure.

## Features

- 🔄 Converts symlinks to actual files
- 📁 Preserves complete folder structure
- 📝 Logs all symlink conversions
- ⚠️ Error handling and reporting
- 🖥️ User-friendly GUI interface

## Description

This application is designed to help users who need to convert symbolic links to actual files, which can be useful when:
- Backing up data
- Sharing folders across systems
- Moving data to systems that don't support symlinks
- Creating a clean copy of a directory structure

## How to Use

1. Launch the application
2. Click "Select Source Folder" to choose the directory containing your symlinks
3. Click "Select Destination Folder" to choose where you want the converted files to be saved
4. Click "Start Conversion" to begin the process
5. Monitor the progress in the logging window
6. Review the completion message for any errors or warnings

## Requirements

- Python 3.x
- tkinter (usually comes with Python)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/symlink-converter.git

# Navigate to the directory
cd symlink-converter

# Run the application
python symlink_converter_app.py
```

## Technical Details

The application:
- Recursively scans the source directory
- Identifies symbolic links using `os.path.islink()`
- Resolves the actual file path using `os.readlink()`
- Creates a matching directory structure in the destination
- Copies actual files instead of symlinks
- Maintains regular files as-is

## Error Handling

The application handles several error cases:
- Missing source/destination folders
- Non-existent target files
- Permission issues
- Invalid symlinks

All errors are logged and displayed to the user after completion.

## Contributing

Feel free to fork this repository and submit pull requests. You can also open issues for bugs or feature requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Made with ❤️ by [Your Name]
