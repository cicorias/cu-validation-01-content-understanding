# Azure Content Understanding Validation

A Python-based validation and sample project for Azure AI Content Understanding API. This project demonstrates how to analyze documents using Azure's Content Understanding service with prebuilt analyzers like invoice processing.

## 🎯 Overview

This repository was created to validate the Azure Content Understanding Python client from [@Azure-Samples/azure-ai-content-understanding-python](https://github.com/Azure-Samples/azure-ai-content-understanding-python), specifically to test the improvements made in [PR #133](https://github.com/Azure-Samples/azure-ai-content-understanding-python/pull/133) that make the client easier to use and install with `pip`.

This project provides practical examples and utilities for working with Azure AI Content Understanding API, enabling you to:

- Extract structured data from documents (invoices, forms, receipts, etc.)
- Validate document processing workflows
- Understand field extraction capabilities
- Integrate Azure Content Understanding into your applications

## ✨ Features

- **Prebuilt Analyzer Support**: Leverage Azure's prebuilt analyzers (invoice, receipt, etc.)
- **Document Processing**: Analyze various document formats (PDF, images, etc.)
- **Field Extraction**: Extract structured fields with confidence scores and bounding boxes
- **Interactive Notebooks**: Jupyter notebooks for learning and experimentation
- **Authentication Flexibility**: Support for both API key and Azure AD token-based authentication

## 📋 Prerequisites

Before you begin, ensure you have:

- Python 3.8 or higher
- An Azure subscription
- An Azure AI Services resource configured with Content Understanding
- Azure credentials (Subscription Key or Azure AD authentication)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/cicorias/cu-validation-01-content-understanding.git
cd cu-validation-01-content-understanding
```

### 2. Set Up Virtual Environment

Use the provided setup script:

```bash
./vmake.sh
```

Or manually:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install "git+https://github.com/Azure-Samples/azure-ai-content-understanding-python.git@make-pip-install-friendly"
```

**Note**: The `vmake.sh` script may reference a specific fork or branch for development/testing purposes. The recommended installation method is using the Azure-Samples repository as shown above.

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
AZURE_AI_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_AI_API_KEY=your-subscription-key-here
```

**Note**: Using Azure AD authentication (DefaultAzureCredential) is recommended for production. If using token-based auth, you can omit `AZURE_AI_API_KEY`.

## 💻 Usage

### Quick Start with Python Script

The `quick_parse.py` script demonstrates invoice analysis:

```bash
python quick_parse.py
```

This script will:
1. Connect to Azure Content Understanding service
2. Analyze a sample invoice from `./data/invoice.pdf`
3. Extract structured fields (vendor, total, line items, etc.)
4. Display confidence scores and bounding boxes
5. Save the full JSON result to the output directory

**Note**: Ensure you have a sample document at `./data/invoice.pdf` before running. You can use your own invoice PDF or modify the `sample_file_path` variable in the script to point to your document.

### Using Jupyter Notebooks

For interactive exploration:

```bash
jupyter notebook notebooks/field_extraction.ipynb
```

The notebook provides:
- Step-by-step guidance on using Content Understanding API
- Examples of field extraction
- Visualization of extracted data
- Custom analyzer demonstrations

## 📁 Project Structure

```
.
├── quick_parse.py              # Quick start script for invoice analysis
├── vmake.sh                    # Virtual environment setup script
├── notebooks/
│   └── field_extraction.ipynb  # Interactive Jupyter notebook
├── data/                       # Sample documents (not in repo)
│   └── invoice.pdf
├── .env                        # Environment configuration (create this)
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## 🔧 Configuration

### Authentication Methods

**Option 1: Subscription Key** (Quick Start)
```python
AZURE_AI_API_KEY = os.getenv("AZURE_AI_API_KEY")
client = AzureContentUnderstandingClient(
    endpoint=AZURE_AI_ENDPOINT,
    subscription_key=AZURE_AI_API_KEY,
    api_version=API_VERSION
)
```

**Option 2: Azure AD Token** (Recommended for Production)
```python
from azure.identity import DefaultAzureCredential

def token_provider():
    credential = DefaultAzureCredential()
    token = credential.get_token("https://cognitiveservices.azure.com/.default")
    return token.token

client = AzureContentUnderstandingClient(
    endpoint=AZURE_AI_ENDPOINT,
    token_provider=token_provider,
    api_version=API_VERSION
)
```

### Supported Analyzers

The project uses prebuilt analyzers including:
- `prebuilt-invoice`: Extract invoice fields (vendor, total, line items, etc.)
- `prebuilt-receipt`: Extract receipt information
- `prebuilt-layout`: Extract layout and structure
- And many more...

## 📊 Output Example

When analyzing an invoice, you'll get structured output like:

```
✅ Client created successfully
   Endpoint: https://your-resource.cognitiveservices.azure.com/
   Credential: Subscription Key
   API Version: 2025-11-01

🔍 Analyzing ./data/invoice.pdf with prebuilt-invoice...
⏳ Waiting for document analysis to complete...
✅ Document analysis completed successfully!

📊 Extracted Fields:
--------------------------------------------------------------------------------
VendorName: Contoso Ltd.
  Confidence: 0.987
  Bounding Box: {...}

InvoiceTotal: 1234.56
  Confidence: 0.995
  Bounding Box: {...}

Items (array with 3 items):
  Item 1:
    Description: Product A
    Amount: 500.00
    ...
```

## 🤝 Contributing

Contributions are welcome! This is a validation and learning project, so feel free to:

- Add new examples
- Improve documentation
- Share insights about Content Understanding features
- Report issues or suggest improvements

## 📝 License

This project is provided as-is for learning and validation purposes. Please refer to Azure's terms of service for the Content Understanding API.

## 🔗 Resources

- [Azure Content Understanding Python Client Repository](https://github.com/Azure-Samples/azure-ai-content-understanding-python)
- [PR #133 - Make client pip-installable](https://github.com/Azure-Samples/azure-ai-content-understanding-python/pull/133)
- [Azure AI Content Understanding Documentation](https://learn.microsoft.com/azure/ai-services/content-understanding/)
- [Azure AI Services](https://azure.microsoft.com/services/cognitive-services/)
