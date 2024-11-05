# IntelliText 🚀

[![PyPI version](https://badge.fury.io/py/intellitext.svg)](https://badge.fury.io/py/intellitext)
[![Python Versions](https://img.shields.io/pypi/pyversions/intellitext.svg)](https://pypi.org/project/intellitext/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

IntelliText is a powerful, customizable keyboard macro and text expansion tool that helps you automate repetitive typing tasks and execute custom actions. It's designed to boost your productivity by allowing you to create shortcuts for frequently used text, commands, and actions.

## ✨ Features

#### 📝 Word Macros
- Quick text expansion using the `!` prefix
- Support for multiple text variants with random selection
- Perfect for email templates, code snippets, and common phrases

#### ⚡ Action Macros
- Execute commands and scripts using the `#` prefix
- Built-in clipboard integration
- Run system commands directly from your keyboard

#### 🔌 Extension System
- Create custom extensions to extend functionality
- Simple plugin architecture
- Support for various output types

#### 🎲 Shuffle System
- Randomly select from multiple text variants
- Perfect for adding variety to automated responses
- Configurable per macro

## 🚀 Quick Start

### Installation

```bash
pip install intellitext
```
---
    
## Example
![Example GIF](https://i.imgur.com/kTLNyHA.gif)

## 💻 Platform Compatibility

| Platform | Support |
|----------|---------|
| Windows  | ✅       |
| macOS    | ❌       |
| Linux    | ❌       |

> ⚠️
Currently IntelliText only works on windows,
macOS and Linux are not yet supported, although they will be added in the near future 

IntelliText has been tested on Windows 11 and Python 3.12 and 3.13.


---

### Basic Usage

1. IntelliText will create a it_macros.json file in `~/.intellitext/` you can edit it to your liking:

```json
{
    "macros": {
        "word": {
            "!hello": "Hello World!",
            "!greet": "Hi there,How are you?,Hello friend!",
            "!sig": "Best regards,\nYour Name"
        },
        "action": {
            "#cb": "",
            "#rnp": "notepad.exe"
        }
    },
    "macro_settings": {
        "shuffle": {
            "enabled": true,
            "shuffle_macros": ["!greet"]
        },
        "extension_setting": {
            "enabled": true,
            "extensions": []
        }
    }
}
```

2. Run from Terminal:
```cmd
intellitext.py
```


3. Run IntelliText in Python:

```python
from intellitext import IntelliText

intellitext = IntelliText()
intellitext.run()
```

## 📖 Usage Guide

### Word Macros
- Type `!` followed by your macro name
- Example: `!hello` expands to "Hello, World!"
- For multiple variants, separate with commas in the config
- Enable shuffle in settings to randomize between variants

### Action Macros
- `#cb` - Paste clipboard content
- `#r[program]` - Run a program `#rvsc` (Run vscode)
- `#ite` - Exit IntelliText
- Custom actions can be added in the config

## 🔎 Extensions
An Extension will only run when the macro starts with @ and ends with $

```json
{
    "extension_setting": {
        "enabled": true,
        "extensions": [
            {
                "@date": "date_formatter.py",
                "type": "print",
                "cmd": "python",
                "args": ["--format", "yyyy-MM-dd"]
            }
        ]
    }
}
```

For example:
`@date$` 

This will run the date extension with the predefined arguments in the it_macros.json file.

The argument priority is with the inline args passed to the extension when typing the macro.

This means that this macro: `@date --format yy-mm-dd$` 
will run with the arguments passed to the macro, and not the ones defined in the `it_macros.json`


In this case, `@date` is what triggers the extension.
The value of `@date` is the script or program that will run.
IntelliText will try to look for the script/program name in the `~/.intellitext/extensions` folder,
if it's not found there, it will try to use at as in absolute path.
The extension will not run if the file is not found.

---


## ⚙️ Configuration

### Configuration File Structure
```json
{
    "macros": {
        "word": {
            "!macro_name": "replacement_text"
        },
        "action": {
            "#action_name": "command_or_program"
        }
    },
    "macro_settings": {
        "shuffle": {
            "enabled": boolean,
            "shuffle_macros": ["macro_names"]
        },
        "extension_setting": {
            "enabled": boolean,
            "extensions": []
        }
    }
}
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [pynput](https://github.com/moses-palmer/pynput)

## 📞 Support

- Create an issue for bug reports or feature requests
- Check existing issues before creating new ones
- Email support: cloner.bl12@gmail.com

---

⭐ Star us on GitHub — it helps!