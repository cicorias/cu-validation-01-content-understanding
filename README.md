# Azure Content Understanding - Validation Repository

This repository validates and demonstrates the usage of the Azure Content Understanding Python client that has been made pip-installable.

## Purpose

This repository was created to validate the Azure Content Understanding Python client from [@Azure-Samples/azure-ai-content-understanding-python](https://github.com/Azure-Samples/azure-ai-content-understanding-python), specifically to test the improvements made in [PR #133](https://github.com/Azure-Samples/azure-ai-content-understanding-python/pull/133) that make the client easier to use and install with `pip`.

## Installation

The Azure Content Understanding Python client can now be installed directly using pip from the GitHub repository:

```bash
pip install "git+https://github.com/Azure-Samples/azure-ai-content-understanding-python.git@make-pip-install-friendly"
```

Alternatively, you can use the provided `vmake.sh` script which creates a virtual environment and installs the client. Note that this script may reference a specific fork or branch for development/testing purposes:

```bash
./vmake.sh
```

## Features

This repository includes:

- **quick_parse.py**: A Python script demonstrating how to use the Azure Content Understanding client to analyze documents (e.g., invoices) using prebuilt analyzers
- **notebooks/**: Jupyter notebooks with field extraction examples and other demonstrations

## Usage

### Prerequisites

- Python 3.8 or later
- Azure AI Services endpoint and API key (or Azure AD authentication)
- Sample document files (e.g., PDF invoices) for testing placed in a `data/` directory
- Set up your environment variables in a `.env` file:
  ```
  AZURE_AI_ENDPOINT=<your-endpoint>
  AZURE_AI_API_KEY=<your-api-key>
  ```

### Running the Quick Parse Example

Before running the script, ensure you have a sample document (e.g., `./data/invoice.pdf`) available for analysis. You can use your own invoice PDF or other supported document formats.

```bash
python quick_parse.py
```

This script demonstrates:
- Creating an Azure Content Understanding client
- Analyzing documents using prebuilt analyzers (e.g., invoice analyzer)
- Extracting fields and metadata from documents
- Saving analysis results to JSON files

**Note**: The script expects a file at `./data/invoice.pdf`. You can either create a `data/` directory with your sample files or modify the `sample_file_path` variable in the script to point to your document.

### Using the Notebooks

Navigate to the `notebooks/` directory and open the Jupyter notebooks to explore interactive examples:

```bash
cd notebooks
jupyter notebook field_extraction.ipynb
```

## Related Resources

- [Azure Content Understanding Python Client Repository](https://github.com/Azure-Samples/azure-ai-content-understanding-python)
- [PR #133 - Make client pip-installable](https://github.com/Azure-Samples/azure-ai-content-understanding-python/pull/133)

## License

This project follows the licensing of the original Azure Content Understanding Python samples repository.
