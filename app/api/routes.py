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
        extracted_sections = extract_pdf_sections(contents)

        # Save CSV
        df = pd.DataFrame(list(extracted_sections.items()), columns=['Section', 'Content'])
        os.makedirs('output', exist_ok=True)
        csv_path = os.path.join('output', f"{file.filename.replace('.pdf', '.csv')}")
        df.to_csv(csv_path, index=False)

        return JSONResponse(content=extracted_sections)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.post("/get_pdf_tables/")
async def get_pdf_tables(file: UploadFile = File(...)):
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail='Only PDF files are allowed.')
    try:
        contents = await file.read()
        extracted_tables_df = extract_pdf_tables(contents)

        # Check if the DataFrame is empty
        if extracted_tables_df.empty:
            raise HTTPException(status_code=404, detail="No tables found in the PDF")

        # Save the DataFrame to an CSV file
        os.makedirs('output_tables', exist_ok=True)
        table_csv_path = os.path.join('output_tables', f"{file.filename.replace('.pdf', '.csv')}")
        extracted_tables_df.to_csv(table_csv_path, index=False)

        # make the Panda DataFrame to a list of dictionaries
        extracted_tables = extracted_tables_df.to_dict(orient='split')
        return JSONResponse(content=extracted_tables)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    