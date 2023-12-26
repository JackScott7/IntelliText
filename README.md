# IntelliText

IntelliText listens to keyboard input and performs actions based on the input. It is designed to support word and action macros triggered by specific characters.

- Word Macros: Words or phrases triggered by the '!' character.
- Action Macros: Special actions triggered by the '#' character.

The script reads macro definitions from a `macros.json` file, allowing users to customize and extend the available macros. For example, The only predefined action macro for now, is `#cb` that copies the clipboard content and types it (although the clipboard content should be only text).

## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/JackScott7/IntelliText.git
    ```

2. Install the required Python packages:

    ```bash
    pip install pynput pyperclip
    ```

3. Run the script:

    ```bash
    python intellitext.py
    ```

## Usage
~~### Action Macros are not implemented at the moment, tho they will be added in the future. Only the predefined `#cb` works for now.~~

✅ Action Macros are now implemented, you can now define your own action macros in the `macros.json` file.
For now, only run actions are supported, for example `#rsomeexe` will run the `some.exe` executable.

1. Define your word and action macros in the `macros.json` file.

   Example `macros.json`:

    ```json
    {
      "macros": {
        "word": {
          "!greet": "Hello, how are you?",
          "!name": "John Doe",
          "!lang": "C#,Python,Rust,Go"
        },
        "action": {
          "#cb": "",
          "#rsomeexe": "path\\to\\some.exe"
        }
      },
      "macro_settings": {
        "shuffle": {
          "enabled": "true",
          "shuffle_macros": [
            "!lang"
          ]
        }
      }
    }
    ```

2. Launch the script by running:

    ```bash
    python intellitext.py
    ```

3. The Macro Shuffle setting can be set to `true` or `false`, depending on if you want to shuffle the word macros that you defined, for example `!lang` that is seperated by commas, everytime `!lang` is detected it randomly selects or shuffles from the word macro list.
4. Type your macros during keyboard input to trigger predefined words or actions.

## Example
![Example GIF](https://i.imgur.com/kTLNyHA.gif)
