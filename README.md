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

#### Option 1: Azure AD Token Authentication (Recommended for Production)

```python
from azure.identity import DefaultAzureCredential

def token_provider():
    credential = DefaultAzureCredential()
    token = credential.get_token("https://cognitiveservices.azure.com/.default")
    return token.token

client = AzureContentUnderstandingClient(
    endpoint=AZURE_AI_ENDPOINT,
    api_version="2025-11-01",
    token_provider=token_provider
)
```

#### Option 2: Subscription Key Authentication

```python
client = AzureContentUnderstandingClient(
    endpoint=AZURE_AI_ENDPOINT,
    api_version="2025-11-01",
    subscription_key=AZURE_AI_API_KEY
)
```

### Supported Analyzers

The project currently uses the `prebuilt-invoice` analyzer, but Azure Content Understanding supports many prebuilt analyzers including:

- `prebuilt-invoice` - Invoice processing
- `prebuilt-receipt` - Receipt analysis
- `prebuilt-id-document` - Identity document extraction
- `prebuilt-business-card` - Business card parsing
- And many more...

## 📝 Example: Analyzing an Invoice

```python
# Note: content_understanding_client is installed via the pip install command
# from the GitHub repository as described in the Installation section
from content_understanding_client import AzureContentUnderstandingClient
from azure.identity import DefaultAzureCredential

# Token provider for Azure AD authentication (optional)
def token_provider():
    credential = DefaultAzureCredential()
    token = credential.get_token("https://cognitiveservices.azure.com/.default")
    return token.token

# Initialize client (automatically selects authentication method)
# Uses token provider if AZURE_AI_API_KEY is not set, otherwise uses subscription key
client = AzureContentUnderstandingClient(
    endpoint=AZURE_AI_ENDPOINT,
    api_version="2025-11-01",
    subscription_key=AZURE_AI_API_KEY,  # Optional: omit to use token provider
    token_provider=token_provider if not AZURE_AI_API_KEY else None
)

# Analyze invoice
analysis_response = client.begin_analyze_binary(
    analyzer_id="prebuilt-invoice",
    file_location="./data/invoice.pdf"
)

# Wait for results
analysis_result = client.poll_result(analysis_response)

# Access extracted fields
if analysis_result and "result" in analysis_result:
    result = analysis_result["result"]
    contents = result.get("contents", [])
    fields = contents[0].get("fields", {})
    
    # Get invoice details
    vendor_name = fields.get("VendorName", {}).get("valueString")
    invoice_total = fields.get("InvoiceTotal", {}).get("valueNumber")
    invoice_date = fields.get("InvoiceDate", {}).get("valueDate")
```

## 🤝 Contributing

Contributions are welcome! Here are some ways you can contribute:

1. **Report Bugs**: Open an issue describing the bug and how to reproduce it
2. **Suggest Features**: Share ideas for new features or improvements
3. **Submit Pull Requests**: Fix bugs or add features with a PR
4. **Improve Documentation**: Help make the docs better

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Test your changes thoroughly
5. Commit your changes: `git commit -am 'Add some feature'`
6. Push to the branch: `git push origin feature/your-feature-name`
7. Submit a pull request

## 📚 Additional Resources

- [Azure AI Content Understanding Documentation](https://learn.microsoft.com/azure/ai-services/document-intelligence/)
- [Azure AI Services](https://azure.microsoft.com/services/cognitive-services/)
- [Azure SDK for Python](https://github.com/Azure/azure-sdk-for-python)

## ⚠️ Important Notes

- **Data Directory**: The `data/` directory is git-ignored. You need to provide your own sample documents for testing.
- **Test Output**: Analysis results are saved to `test_output/` which is also git-ignored.
- **API Costs**: Be aware that using Azure AI Content Understanding API incurs costs based on your usage.
- **Security**: Never commit your `.env` file or API keys to version control.

## 📄 License

This project is for validation and demonstration purposes. Please check the repository for license information.

## 🙋 Support

For issues and questions:
- Check existing [GitHub Issues](https://github.com/cicorias/cu-validation-01-content-understanding/issues)
- Open a new issue if you encounter a problem
- Review Azure AI documentation for API-specific questions

---

**Note**: This is a validation project for Azure AI Content Understanding services. The implementation is subject to change as the service evolves.
