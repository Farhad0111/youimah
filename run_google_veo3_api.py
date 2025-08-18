import uvicorn

if __name__ == "__main__":
    print("Starting Google Veo3 API server on port 8044...")
    uvicorn.run("google_veo3_api:app", host="0.0.0.0", port=8044, reload=True)
