from typing import List, Dict
from pydantic import BaseModel

class ExtractedSections(BaseModel):
    Type: str
    Term: str
    Objective: str
    Intended_Investor: str
    Risks_and_Returns: str
    Payment_Issues: str
    Holding_Period: str
    Complaints: str
    Other_Information: str
