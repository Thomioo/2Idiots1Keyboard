from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def get():
    return FileResponse("static/index.html", media_type="text/html")

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.turn_index = 0
        self.content = ""
        self.caret_offset = 0

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        await self.send_state()

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_state(self):
        for idx, conn in enumerate(self.active_connections):
            await conn.send_json({
                "content": self.content,
                "caret_offset": self.caret_offset,
                "your_turn": idx == self.turn_index
            })

    async def receive_edit(self, websocket: WebSocket, data: str):
        idx = self.active_connections.index(websocket)
        if idx != self.turn_index:
            await websocket.send_json({"error": "Not your turn!"})
            return

        import json
        msg = None
        try:
            msg = json.loads(data)
            action = msg.get("action")
            caret = msg.get("caret_offset")
        except Exception:
            action = data
            caret = None

        if action == "MOVE_CARET" and caret is not None:
            self.caret_offset = max(0, min(caret, len(self.content)))
        elif action == "DELETE_RANGE" and msg is not None:
            start = msg.get("start")
            end = msg.get("end")
            if start is not None and end is not None and 0 <= start <= end <= len(self.content):
                self.content = self.content[:start] + self.content[end:]
                self.caret_offset = start
        else:
            pos = self.caret_offset
            if action == "BACKSPACE" or (msg is None and data == "BACKSPACE"):
                if pos > 0:
                    self.content = self.content[:pos-1] + self.content[pos:]
                    self.caret_offset = pos - 1
            elif action == "ENTER" or (msg is None and data == "ENTER"):
                self.content = self.content[:pos] + "\n" + self.content[pos:]
                self.caret_offset = pos + 1
            elif action == "TAB" or (msg is None and data == "TAB"):
                self.content = self.content[:pos] + "    " + self.content[pos:]
                self.caret_offset = pos + 4
            else:
                char = action if action else data
                if isinstance(char, str) and len(char) == 1:
                    self.content = self.content[:pos] + char + self.content[pos:]
                    self.caret_offset = pos + 1
                else:
                    self.content += str(char)
                    self.caret_offset = len(self.content)

        self.turn_index = (self.turn_index + 1) % len(self.active_connections)
        await self.send_state()

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.receive_edit(websocket, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if  __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)