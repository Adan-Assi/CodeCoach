from fastapi import FastAPI

# "Initialize FastAPI app": creates the web server. 
app = FastAPI()

# "Create /analyze route": defines a POST endpoint at /analyze (receive requests here).
@app.get("/analyze")
async def root(): # Example: handles GET requests to the /analyze endpoint
    return {"message": "Hello World"}