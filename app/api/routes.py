from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.utils.pdf_extractor import extract_pdf_sections
from app.utils.table_extractor import extract_pdf_tables
import os
import pandas as pd
from app.utils.models import ExtractedSections, ExtractedTables

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
async def get_pdf_tables(file: UploadFile = File(...)) -> ExtractedTables:
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

        # Map cost category descriptions to the required JSON keys
        json_response = {
            "PRIIPsKIDEntryCostDescription": None,
            "PRIIPsKIDExitCostDescription": None,
            "PRIIPsKIDOngoingCostsDescription": None,
            "PRIIPsKIDTransactionCostsDescription": None,
            "PRIIPsKIDPerformanceFeesDescription": None
        }

        # Mapping of categories to keys
        category_key_map = {
            "Entry costs": "PRIIPsKIDEntryCostDescription",
            "Exit costs": "PRIIPsKIDExitCostDescription",
            "Ongoing costs taken each year": "PRIIPsKIDOngoingCostsDescription",
            "Transaction costs": "PRIIPsKIDTransactionCostsDescription",
            "Performance fees": "PRIIPsKIDPerformanceFeesDescription"
        }

        # Iterate through each element
        for item in extracted_tables["data"]:
            # Ensure each item is a list with at least two elements
            if isinstance(item, list) and len(item) >= 2:
                category = item[0]
                description = item[1]
                # Get the corresponding key from the category_key_map
                key = category_key_map.get(category)
                # Update json_response if the key exists in the map
                if key:
                    json_response[key] = description

        return JSONResponse(content=json_response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    