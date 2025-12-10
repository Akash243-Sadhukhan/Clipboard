# Python Clipboard Manager

A lightweight, cross-platform clipboard manager built with Python and Kivy. It runs in the background, tracking your clipboard history and providing global hotkeys to manage it.

## Features
- **History Tracking**: Automatically saves copied text to a history list.
- **Global Hotkeys**:
  - `Ctrl+C`: Copies text and adds it to the internal history.
  - `Ctrl+V`: Opes the history popup.
  - `Ctrl+Shift+C`: Stops the background listener.
- **UI**: Minimalist overlay UI powered by Kivy.
- **Multithreading**: Uses a custom `EventBus` to handle background monitoring without freezing the UI.

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate it:
   - Windows: `.\venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python clipboard_manager/main.py
```

### Note on Windows
On Windows, global hotkey listening often requires **Administrator privileges**.
- If the hotkeys (`Ctrl+C` / `Ctrl+V`) do not trigger the app, restart your terminal or IDE as Administrator and run the script again.

## Debugging
The application generates a `thread_dump.log` file in the root directory. This file updates every 2 seconds with a snapshot of all running threads, which is useful for debugging deadlocks or stuck threads.
