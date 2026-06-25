from pydantic import BaseModel

class AnalysisStatusResponse(BaseModel):
    enabled: bool

class ToggleAnalysisRequest(BaseModel):
    enabled: bool
