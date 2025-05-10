import os
import uvicorn

if __name__ == "__main__":
    print("🔁 Starting server...")
    port = int(os.environ.get("PORT", 10000))
    print(f"🌐 Launching on port {port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port)
