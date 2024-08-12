import pdfplumber
import io
from typing import List, Dict
import pandas as pd


def extract_pdf_tables(pdf_contents: bytes) -> List[Dict]:
    pdf_stream = io.BytesIO(pdf_contents)
    expected_df = pd.DataFrame()

    with pdfplumber.open(pdf_stream) as pdf:
        for i, page in enumerate(pdf.pages):
            # Extract tables from the page
            tables = page.extract_tables()

            # Iterate through the tables
            for j, table in enumerate(tables):
                # Convert the table to a DataFrame
                df = pd.DataFrame(table[1:], columns=table[0])
                
                # Check if the DataFrame is not empty
                if not df.empty:
                    # Check if the first row first column contains the text "Entry costs"
                    if df.head(1).apply(lambda row: row.str.contains("Entry costs", case=False, na=False).any(), axis=1).values[0]:
                        # keep the df to expected_df
                        expected_df = df
                        break

    return expected_df