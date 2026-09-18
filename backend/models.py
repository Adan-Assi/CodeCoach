from pydantic import BaseModel, Field

# Pydantic model defining the expected structure of the (input) request sent to /analyze.
# FastAPI validates incoming JSON against this model before running the endpoint.
class AnalyzeRequest(BaseModel):
    # The code snippet to be analyzed, with validation for length,
    # (1-8000 characters; design choice.)
    code: str = Field(min_length=1, max_length=8000)

    # Optional field for specifying the programming language of the code snippet,
    # str | None needs Python 3.10 or newer.
    language: str | None = None

# Pydantic model defining the exact structure of the response returned by /analyze,
# (This acts as a strict contract for what the API sends back to the frontend.)
# FastAPI uses this model to automatically validate and serialize the output into JSON.
class AnalyzeResponse(BaseModel):
    explanation: str # human-readable explanation of the analyzed code
    time_complexity: str
    space_complexity: str
    suggestions: list[str] # list of improvement tips for the code
