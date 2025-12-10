# Fixed Issues Report

This document tracks the issues identified and resolved during the recent development session.

## 1. Setup
- **Admin Privileges (Windows)**: The application was configured to `sys.exit(1)` immediately if not running as Administrator.
    - **Fix**: Modified `main.py` to print a warning but allow the application to proceed. This allows testing basic functionality without restarting the IDE/Terminal.

## 2. GUI (Kivy)
- **Blank Screen**: The application launched with a completely black window because `ClipboardGUI.build()` returned an empty `FloatLayout`.
    - **Fix**: Added a `Label` to the layout displaying the application status and hotkey instructions.

## 3. Core Logic & Hotkeys
- **Hotkey Shadowing**: `Ctrl+C` was detecting before `Ctrl+Shift+C` because `{ctrl, c}` is a subset of `{ctrl, shift, c}`.
    - **Fix**: Reordered logic in `HotkeyListener.check_key` to check for the more specific `Ctrl+Shift+C` first.
- **Incorrect Paste Behavior**: Pressing `Ctrl+V` was triggering `trigger_copy()` (simulating Ctrl+C), causing the user to lose their clipboard tracking or re-copy data.
    - **Fix**: Updated `_handle_hotkey` in `app.py` to only capture clipboard on `Ctrl+C`. `Ctrl+V` now strictly opens the history popup.
- **Windows Key Codes**: On Windows, `pynput` returns ASCII control codes (e.g., `\x03` for C, `\x16` for V) when Control is held, instead of the characters 'c' or 'v'.
    - **Fix**: Updated `HotkeyListener._normalize_key` to detect these control codes and map them back to their standard character representations (a-z).

## 4. Code Quality
- **Inheritance Error**: `HistoryManager` inherited from `threading.Thread` but was never started or used as a thread.
    - **Fix**: Removed the unnecessary inheritance.
