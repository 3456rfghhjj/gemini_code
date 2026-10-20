# Gemini Code Assistant

macOS desktop GUI app using Google Gemini API to analyze, fix, and refactor Python scripts.

## Description

Gemini Code Assistant is a desktop tool designed for macOS users working in Python (such as in Thonny). Built with Python, Tkinter, and the Google Gemini API, it lets you load local Python files, describe changes or fixes in plain text, and review refactored code without opening a web browser.

## Features

- **Direct file loading:** Pick any local .py file to load its contents instantly into the code viewer.
- **Non-blocking UI:** Threaded background execution ensures macOS remains smooth without spinning beach balls during API calls.
- **High-contrast visual layout:** Dark forest green background (`#2E4A34`) with light, clear text (`#E6F0E8`) designed to reduce eye strain.
- **Large native typography:** Uses Menlo for source code readability and macOS system UI fonts for controls.
- **Powered by Google GenAI:** Employs `gemini-3.8-flash` for code analysis and updates.

## Requirements

- macOS
- Python 3.10 or newer
- Google Gemini API key

## Installation

1. Clone or download this repository:
```bash
git clone https://github.com/3456rightdj/gemini_code.git 
cd gemini_code
```
2. install dependencies

```bash

pip install google-genai
```
3. Set your Gemini API key in your environment:

```bash
export GEMINI_API_KEY="your_actual_api_key_here"
```

4. Run the application:

```bash
python main.py
```
## Usage

1. Click Open .py File to select a Python script from your computer, or paste code directly into the top window.
2. Type your instruction in the middle input field (e.g., "fix errors", "add docstrings", or "optimize loops").
3. Click Run with Gemini.
4. Review the returned code and explanation in the bottom window.
