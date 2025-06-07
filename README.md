# 2 Idiots 1 Keyboard

A collaborative, turn-based web code editor inspired by [ThePrimeagen's video](https://youtu.be/ycTOEWqjeHI?si=eQd7W7zinHl9Fn_A) — but much dumber and simpler!

## What is this?

This is a minimal multiplayer code editor where only one person can type at a time. After each keystroke (or special action), the turn passes to the next connected user. It's a fun, chaotic way to write code together, based on the concept from ThePrimeagen's video.

## Features
- Turn-based editing: Only one user can type at a time, then the turn rotates.
- Vim-like keybindings for navigation and editing (in the browser).
- Real-time updates for all connected users.
- Simple UI with copy/load from clipboard.

## How to Run

### 1. Install dependencies

```powershell
pip install -r requirements.txt
```


### 2. Start the server (with global access)

You can start everything (including a public tunnel) with the provided `start.bat`:

```powershell
start.bat
```

This will:
- Open VS Code in the project folder
- Start the FastAPI server on port 8000
- Start an [ngrok](https://ngrok.com/) TCP tunnel on port 8000 so others can access your server globally

> **Note:** You need to have [ngrok](https://ngrok.com/download) installed and available in your PATH.

Alternatively, you can run the server manually:

```powershell
python server.py
```

### 3. Open in your browser

Go to [http://localhost:8000](http://localhost:8000) in your browser.

To share with others globally, use the forwarding address provided by ngrok (shown in the ngrok terminal window, e.g., `tcp://0.tcp.ngrok.io:XXXXX`).
Open the same URL in another browser window or device to play with a friend.

## How to Play
- Type a character, press Backspace, Enter, or Tab — after each action, your turn ends and the next person can type.
- Use Vim-like navigation in normal mode (press `Esc` to enter normal mode, `i` to go back to insert mode).
- Use the "Copy All" and "Load from Clipboard" buttons to quickly share or load code.

## Requirements
- Python 3.8+
- [FastAPI](https://fastapi.tiangolo.com/), [Uvicorn](https://www.uvicorn.org/)

Install dependencies with `pip install -r requirements.txt`.

## Credits
- Dumbed down and reimplemented from [ThePrimeagen's 2 Idiots 1 Keyboard video](https://youtu.be/ycTOEWqjeHI?si=eQd7W7zinHl9Fn_A).
- Tailwind CSS CDN for styling.

## License
MIT (do whatever you want, but don't blame me if you lose friends playing this)
