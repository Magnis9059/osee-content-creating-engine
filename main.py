import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"=== Starting OSEE Content Studio on 0.0.0.0:{port} ===", flush=True)
    print(f"ENV PORT: {os.environ.get('PORT')}", flush=True)
    uvicorn.run("app:app", host="0.0.0.0", port=port, log_level="info")
