from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# "Initialize FastAPI app": creates the web server. 
app = FastAPI()


# Define allowed origins (frontend URLs)
origins = [
    "http://localhost:3000",  # React frontend dev server
    # we can add more URLs if needed
]

# Add CORS middleware: defines what the allowed origins are permitted to do when accessing this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # allowed origins
    allow_credentials=True,  # allow cookies/auth headers
    allow_methods=["*"],     # allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],     # allow all headers
)

# "Create /analyze route": defines a POST endpoint at /analyze (receive requests here).
@app.get("/analyze")
async def root(): # Example: handles GET requests to the /analyze endpoint
    return {"message": "Hello World"}



    from fastapi import FastAPI
