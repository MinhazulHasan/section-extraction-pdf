from pdfminer.high_level import extract_text
import re
import io


def clean_extracted_text(text: str) -> str:
    # Remove page numbers or similar structured text
    pattern = r'^.*[Pp]age\s*-\s*\d+\s*of\s*\d+.*$\n?'
    text = re.sub(pattern, '', text, flags=re.MULTILINE)

    # 1. Remove extra newlines
    text = re.sub(r'\n+', '\n', text)
    
    # 2. Replace tabs with single space
    text = re.sub(r'\t+', ' ', text)
    
    # 3. Remove special characters (keeping alphanumeric, space, and newline)
    text = re.sub(r'[^a-zA-Z0-9\s\n]', '', text)

    # Additional cleanup
    text = re.sub(r' +', ' ', text)  # Remove multiple spaces
    text = text.strip()

    return text



def extract_pdf_sections(pdf_contents: bytes) -> dict:
    # Extract text from the PDF
    pdf_stream = io.BytesIO(pdf_contents)
    extracted_text = extract_text(pdf_stream)
    extracted_text = clean_extracted_text(extracted_text)

    # Define patterns for each section using regular expressions
    patterns = {
        "PRIIPSKIDTypeOption": r"Type:\s*(.*?)\s*(?=\bTerm\b)",
        "PRIIPsKIDTerm": r"Term:\s*(.*?)\s*(?=\b(Objective|Objectives)\b)",
        "PRIIPsKIDObjective": r"Objective[s]?:\s*(.*?)\s*(?=\b(Intended investor|Dealing Frequency|Fund Currency|Investment Policy)\b|\bWhat are the risks\b)",
        "PRIIPsKIDTargetMarket": r"Intended\s*(?:investor|Investor|Retail\s*Investor):\s*(.*?)\s*(?=\b(What are the risks|Purchase and Repurchase|Risk Indicator)\b)",
        "PRIIPsKIDOtherRisks": r"What are the risks and what could I get in return\?\s*(.*?)\s*(?=\bWhat happens if\b)",
        "PRIIPsKIDUnableToPayOut": r"What happens if.*?\s*(.*?)\s*(?=\bWhat are the costs\b)",
        "PRIIPsKIDTakeMoneyOutEarly": r"How long should I hold it and can I take money out early\?\s*(.*?)\s*(?=\bHow can I complain\b)",
        "PRIIPsKIDComplaints": r"How can I complain\?\s*(.*?)\s*(?=\bOther relevant information\b)",
        "PRIIPsKIDOtherInfoEU": r"Other relevant information\s*(.*)"
    }

    # Extract the sections
    extracted_sections = {section: re.search(pattern, extracted_text, re.DOTALL).group(1).strip()
                          if re.search(pattern, extracted_text, re.DOTALL) else "Section not found"
                          for section, pattern in patterns.items()}

    return extracted_sections
