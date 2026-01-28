# Azure Content Understanding Validation Project

A Python-based validation and demonstration project for Azure AI Content Understanding services, focusing on document analysis and field extraction capabilities.

## 🎯 Overview

This project provides tools and examples for working with Azure's Content Understanding API to analyze documents, extract structured information, and validate the service capabilities. It includes both command-line scripts and interactive Jupyter notebooks for different use cases.

## ✨ Features

- **Document Analysis**: Analyze PDF and other document formats using Azure AI Content Understanding
- **Field Extraction**: Extract structured fields from documents using prebuilt analyzers
- **Invoice Processing**: Specialized support for invoice analysis with the prebuilt-invoice analyzer
- **Interactive Notebooks**: Jupyter notebooks for exploratory analysis and testing
- **Flexible Authentication**: Support for both Azure AD token-based authentication and subscription key authentication

## 📋 Prerequisites

Before you begin, ensure you have the following:

- Python 3.7 or higher
- An Azure subscription
- An Azure AI Services resource configured with Content Understanding API access
- Azure AI endpoint URL
- Either an Azure AD credential or an API subscription key

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/cicorias/cu-validation-01-content-understanding.git
cd cu-validation-01-content-understanding
```

### 2. Set Up Virtual Environment

Use the provided script to create a virtual environment and install dependencies:

```bash
./vmake.sh
```

This script will:
- Remove any existing `.venv` directory
- Create a new Python virtual environment
- Activate the virtual environment
- Install the Azure AI Content Understanding Python client from the GitHub repository

Alternatively, you can manually set up the environment:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install "git+https://github.com/cicorias/azure-ai-content-understanding-python-1.git@make-pip-install-friendly"
```

### 3. Configure Environment Variables

Create a `.env` file in the project root with your Azure credentials:

```env
AZURE_AI_ENDPOINT=https://your-resource-name.cognitiveservices.azure.com/
AZURE_AI_API_KEY=your-subscription-key-here
```

**Note**: You can use either `AZURE_AI_API_KEY` (subscription key) or Azure AD authentication. For production environments, Azure AD token-based authentication is recommended for better security.

## 📖 Usage

### Quick Start with Command Line

The `quick_parse.py` script demonstrates invoice analysis:

```bash
python quick_parse.py
```

This script will:
1. Load your Azure credentials from the `.env` file
2. Create an Azure Content Understanding client
3. Analyze a sample invoice PDF from the `./data/invoice.pdf` path
4. Extract and display structured fields (vendor, amounts, dates, line items, etc.)
5. Save the complete analysis result to a JSON file

**Expected Output:**
- ✅ Client creation confirmation
- 🔍 Analysis progress updates
- 📊 Extracted fields with confidence scores
- 📋 Content metadata
- 💾 Path to saved JSON results

### Using Jupyter Notebooks

For interactive exploration, use the provided notebook:

```bash
# Make sure your virtual environment is activated
source .venv/bin/activate

# Start Jupyter
jupyter notebook notebooks/field_extraction.ipynb
```

The `field_extraction.ipynb` notebook provides:
- Step-by-step guidance for document analysis
- Examples of using prebuilt analyzers
- Custom field extraction demonstrations
- Interactive result visualization

## 📁 Project Structure

```
cu-validation-01-content-understanding/
├── .gitignore                          # Git ignore rules
├── cu-validation-01.code-workspace     # VS Code workspace configuration
├── vmake.sh                            # Virtual environment setup script
├── quick_parse.py                      # Command-line invoice analysis script
├── notebooks/                          # Jupyter notebooks for interactive analysis
│   └── field_extraction.ipynb          # Field extraction examples and tutorials
├── data/                               # Sample documents for testing (not in repo)
│   └── invoice.pdf                     # Sample invoice file
└── test_output/                        # Generated analysis results (not in repo)
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
from content_understanding_client import AzureContentUnderstandingClient

# Initialize client
client = AzureContentUnderstandingClient(
    endpoint=AZURE_AI_ENDPOINT,
    api_version="2025-11-01",
    subscription_key=AZURE_AI_API_KEY
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
