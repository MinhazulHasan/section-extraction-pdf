from pdfminer.high_level import extract_text
import re
import os
import json
import pandas as pd


# Path to the uploaded PDF file
pdf_file = "PRIIPS_KIDIE0005895655_en-GB_en-GB.pdf"
pdf_path = os.path.join("pdf", pdf_file)
json_path = os.path.join("output", pdf_file.replace(".pdf", ".json"))
csv_path = os.path.join("output", pdf_file.replace(".pdf", ".csv"))

# Extract text from the PDF
extracted_text = extract_text(pdf_path)

# Print the first 2000 characters to understand the structure
# print(extracted_text)


# Define the text to analyze (from the PDF)
text = extracted_text

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

# print(patterns["Risks and Returns"])
# see the extracted text
# print(re.search(patterns["Risks and Returns"], text, re.DOTALL).group(1).strip())

# Extract the sections
extracted_sections = {section: re.search(pattern, text, re.DOTALL).group(1).strip()
                      if re.search(pattern, text, re.DOTALL) else "Section not found"
                      for section, pattern in patterns.items()}

# Save the extracted sections to a JSON file
with open(json_path, "w") as file:
    json.dump(extracted_sections, file, indent=4)

# Convert the dictionary to a DataFrame
df = pd.DataFrame(list(extracted_sections.items()), columns=['Section', 'Content'])

# Create an CSV file from the DataFrame
df.to_csv(csv_path, index=False)
