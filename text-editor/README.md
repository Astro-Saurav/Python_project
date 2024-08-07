# Python Text Editor

A feature-rich Python-based text editor developed with Tkinter. This editor provides essential text editing functionalities, customizable themes, and file encryption.

![image](https://github.com/user-attachments/assets/0769aac9-5b49-449f-bf60-72549fb9ade1)

## Features

-  Basic Text Editing: Includes Cut, Copy, Paste, Undo, Redo, and more.
-  File Encryption: Password-protect your files.
-  Theme Customization: Change background color, text color, cursor color, and opacity.
-  Word Wrap: Toggle word wrap mode on or off.
-  Zoom: Adjust text size with zoom in and zoom out.
-  Find and Replace: Search for and replace text within the document.
-  Date/Time Insertion: Easily insert the current date and time into your document.

## Installation
[Download exe](https://github.com/Astro-Saurav/Python_project/releases/tag/v0.1)

Ensure you have Python installed on your system. This project requires the cryptography library, which you can install via pip:

```bash 
pip install cryptography
```
1. **Clone the Repository**
```bash
git clone  https://github.com/Astro-Saurav/Python_project/tree/main/text-editor
cd text-editor
```
2. **Run the Application**
Copy code
```bash
python texteditor.py
```

## Using the Editor

-  New File: File > New
-  Open File: File > Open
-  Save File: File > Save or File > Save As
-  Set/Remove Password: File > Set Password or File > Remove Password
-  Change Theme: Use the Theme menu to adjust colors and opacity.
-  Zoom In/Out: Adjust font size via the View menu.
-  Theme Customization
-  Customize the following theme settings:
-  Background Color: Change the background color of the text area.
-  Text Color: Change the color of the text.
-  Cursor Color: Adjust the cursor color.
-  Opacity: Set the window opacity.
-  These settings are saved in a theme_settings.json file and will be applied the next time the editor is opened.

## File Encryption
You can encrypt files with a password. When saving a file with a password, the content is encrypted using the cryptography library. To open an encrypted file, you must enter the correct password.

## Contributing
Contributions are welcome! Please open issues or submit pull requests if you have suggestions or improvements.

## License
This project is licensed under the MIT [License](https://github.com/Astro-Saurav/Python_project/blob/bfa6151f1ee8ad34db80a5ef62855c0aa9c8f519/text-editor/License). See the LICENSE file for details.

## Contact
For questions or support, please open an issue on the repository or contact me via [email](0501saurav@gmail.com).
