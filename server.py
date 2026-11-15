from mcp.server.fastmcp import FastMCP
import os, requests, base64

mcp = FastMCP("moss-tts")
API_KEY = os.environ.get("MOSS_API_KEY", "sk-392844447ce638e2a76d29da71c80eeaa00d5da9ff7ab216")
VOICE_ID = os.environ.get("MOSS_VOICE_ID", "187b0c9b-612c-4019-98fe-c7bb59eb8074")

@mcp.tool()
def speak(text: str) -> str:
    resp = requests.post(
        "https://api.mosi.cn/v1/audio/speech",
        json={
            "model": "moss-tts",
            "input": text,
            "voice_id": VOICE_ID,
            "response_format": "mp3",
            "delivery_method": "audio"
        },
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        timeout=30
    )
    if resp.status_code != 200:
        return f"Error {resp.status_code}"
    audio_b64 = base64.b64encode(resp.content).decode()
    return f"data:audio/mp3;base64,{audio_b64}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http",
    host="0.0.0.0", port=8080)
