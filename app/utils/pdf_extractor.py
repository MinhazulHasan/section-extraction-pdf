from pdfminer.high_level import extract_text
import re
import io

def extract_pdf_sections(pdf_contents: bytes) -> dict:
    # Extract text from the PDF
    pdf_stream = io.BytesIO(pdf_contents)
    extracted_text = extract_text(pdf_stream)

    # Define patterns for each section using regular expressions
    patterns = {
        "Type": r"Type:\s*(.*?)\s*(?=\bTerm\b)",
        "Term": r"Term:\s*(.*?)\s*(?=\b(Objective|Objectives)\b)",
        "Objective": r"Objective[s]?:\s*(.*?)\s*(?=\b(Intended investor|Dealing Frequency)\b|\bWhat are the risks\b)",
        "Intended Investor": r"Intended\s*(?:investor|Retail\s*Investor):\s*(.*?)\s*(?=\bWhat are the risks\b)",
        "Risks and Returns": r"What are the risks and what could I get in return\?\s*(.*?)\s*(?=\bWhat happens if\b)",
        "Payment Issues": r"What happens if.*?\s*(.*?)\s*(?=\bHow long should I hold it\b)",
        "Holding Period": r"How long should I hold it and can I take money out early\?\s*(.*?)\s*(?=\bHow can I complain\b)",
        "Complaints": r"How can I complain\?\s*(.*?)\s*(?=\bOther relevant information\b)",
        "Other Information": r"Other relevant information\s*(.*)"
    }

    # Extract the sections
    extracted_sections = {section: re.search(pattern, extracted_text, re.DOTALL).group(1).strip()
                          if re.search(pattern, extracted_text, re.DOTALL) else "Section not found"
                          for section, pattern in patterns.items()}

    return extracted_sections
