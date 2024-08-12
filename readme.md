# 📄 PDF Extractor API

> Extract sections and tables from PDFs with ease!

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🚀 Quick Start

Get up and running in no time with these simple steps:

```bash
# Create a virtual environment
python -m venv extractionEnv

# Activate the virtual environment
# On Windows:
.\extractionEnv\Scripts\activate
# On macOS and Linux:
source extractionEnv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch the API
python run.py
```

## 🎯 Features

- 📊 Extract tables from PDFs
- 📝 Extract key sections from PDFs
- 🗃️ Save extracted data as CSV files
- 🌐 RESTful API powered by FastAPI

## 🛠️ API Usage

Send a POST request to `/extract-pdf` with a PDF file to extract its contents:

```bash
curl -X POST "http://localhost:8000/extract-pdf" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_pdf_file.pdf"
```

## 📁 Project Structure

```
pdf-extractor/
│
├── app/main.py        # FastAPI application
├── extractionEnv      # PDF extraction Virtual Enviroment
├── requirements.txt   # Project dependencies
├── run.py             # Script to run the application
└── README.md          # Project documentation
```

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/yourusername/pdf-extractor/issues).

## 📜 License

This project is [MIT](https://choosealicense.com/licenses/mit/) licensed.

## 🙏 Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [pdfplumber](https://github.com/jsvine/pdfplumber)
- [pdfminer.six](https://github.com/pdfminer/pdfminer.six)

---

