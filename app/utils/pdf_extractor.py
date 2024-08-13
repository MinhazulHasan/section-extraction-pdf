from pdfminer.high_level import extract_text
import re
import io

def extract_pdf_sections(pdf_contents: bytes) -> dict:
    # Extract text from the PDF
    pdf_stream = io.BytesIO(pdf_contents)
    extracted_text = extract_text(pdf_stream)

    pattern = r'^.*[Pp]age\s*-\s*\d+\s*of\s*\d+.*$\n?'
    extracted_text = re.sub(pattern, '', extracted_text, flags=re.MULTILINE)
    extracted_text = extracted_text.strip()

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
