from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.utils.pdf_extractor import extract_pdf_sections
from app.utils.table_extractor import extract_pdf_tables
import os
import pandas as pd
from app.utils.models import ExtractedSections

router = APIRouter()


@router.post("/get_pdf_content/")
async def get_pdf_content(file: UploadFile = File(...)) -> ExtractedSections:
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail='Only PDF files are allowed.')
    
    try:
        contents = await file.read()
        extracted_sections_dict = extract_pdf_sections(contents)
        extracted_tables_dict = extract_pdf_tables(contents, file.filename)

        # Merge the two dictionaries
        merged_dict = {**extracted_sections_dict, **extracted_tables_dict}

        # Save CSV
        # df = pd.DataFrame(list(merged_dict.items()), columns=['Section', 'Content'])
        # os.makedirs('output', exist_ok=True)
        # csv_path = os.path.join('output', f"{file.filename.replace('.pdf', '.csv')}")
        # df.to_csv(csv_path, index=False)

        return JSONResponse(content=merged_dict)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
