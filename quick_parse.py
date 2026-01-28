from datetime import datetime
import logging
import json
import os
import sys
import asyncio
from typing import Any, Optional
from dotenv import find_dotenv, load_dotenv

# Add the parent directory to the Python path to import the sample_helper module
sys.path.append(os.path.join(os.path.dirname(os.getcwd()), 'python'))
from content_understanding_client import AzureContentUnderstandingClient
from extension.document_processor import DocumentProcessor
from extension.sample_helper import save_json_to_file 
from azure.identity import DefaultAzureCredential

load_dotenv(find_dotenv())
logging.basicConfig(level=logging.INFO)

# For authentication, you can use either token-based auth or subscription key; only one is required
AZURE_AI_ENDPOINT = os.getenv("AZURE_AI_ENDPOINT")
# IMPORTANT: Replace with your actual subscription key or set it in your ".env" file if not using token authentication
AZURE_AI_API_KEY = os.getenv("AZURE_AI_API_KEY")
API_VERSION = "2025-11-01"

# Create token provider for Azure AD authentication
def token_provider():
    credential = DefaultAzureCredential()
    token = credential.get_token("https://cognitiveservices.azure.com/.default")
    return token.token

# Create the Content Understanding client
try:
    client = AzureContentUnderstandingClient(
        endpoint=AZURE_AI_ENDPOINT,
        api_version=API_VERSION,
        subscription_key=AZURE_AI_API_KEY,
        token_provider=token_provider if not AZURE_AI_API_KEY else None,
        x_ms_useragent="azure-ai-content-understanding-python-sample-ga"    # The user agent is used for tracking sample usage and does not provide identity information. You can change this if you want to opt out of tracking.
    )
    credential_type = "Subscription Key" if AZURE_AI_API_KEY else "Azure AD Token"
    print(f"✅ Client created successfully")
    print(f"   Endpoint: {AZURE_AI_ENDPOINT}")
    print(f"   Credential: {credential_type}")
    print(f"   API Version: {API_VERSION}")
except Exception as e:
    credential_type = "Subscription Key" if AZURE_AI_API_KEY else "Azure AD Token"
    print(f"❌ Failed to create client")
    print(f"   Endpoint: {AZURE_AI_ENDPOINT}")
    print(f"   Credential: {credential_type}")
    print(f"   Error: {e}")
    raise

try:
    processor = DocumentProcessor(client)
    print("✅ DocumentProcessor created successfully")
except Exception as e:
    print(f"❌ Failed to create DocumentProcessor: {e}")
    raise





sample_file_path = './data/invoice.pdf'
invoice_analyzer_id = "prebuilt-invoice"

print(f"🔍 Analyzing {sample_file_path} with {invoice_analyzer_id}...")

analysis_response = client.begin_analyze_binary(
    analyzer_id=invoice_analyzer_id,
    file_location=sample_file_path,
)

# Wait for analysis completion
print(f"⏳ Waiting for document analysis to complete...")
analysis_result = client.poll_result(analysis_response)
print(f"✅ Document analysis completed successfully!")



# Display comprehensive results
if analysis_result and "result" in analysis_result:
    result = analysis_result["result"]
    contents = result.get("contents", [])
    
    if contents:
        first_content = contents[0]
        
        # Display extracted fields
        fields = first_content.get("fields", {})
        print("📊 Extracted Fields:")
        print("-" * 80)
        if fields:
            for field_name, field_value in fields.items():
                field_type = field_value.get("type")
                if field_type == "string":
                    print(f"{field_name}: {field_value.get('valueString')}")
                elif field_type == "number":
                    print(f"{field_name}: {field_value.get('valueNumber')}")
                elif field_type == "date":
                    print(f"{field_name}: {field_value.get('valueDate')}")
                elif field_type == "array":
                    print(f"{field_name} (array with {len(field_value.get('valueArray', []))} items):")
                    for idx, item in enumerate(field_value.get('valueArray', []), 1):
                        if item.get('type') == 'object':
                            print(f"  Item {idx}:")
                            for key, val in item.get('valueObject', {}).items():
                                if val.get('type') == 'string':
                                    print(f"    {key}: {val.get('valueString')}")
                                elif val.get('type') == 'number':
                                    print(f"    {key}: {val.get('valueNumber')}")
                                # Display confidence and source for nested fields
                                if val.get('confidence') is not None:
                                    print(f"      Confidence: {val.get('confidence'):.3f}")
                                if val.get('source'):
                                    print(f"      Bounding Box: {val.get('source')}")
                elif field_type == "object":
                    print(f"{field_name}: {field_value.get('valueObject')}")
                
                # Display confidence and bounding box for the field
                confidence = field_value.get('confidence')
                if confidence is not None:
                    print(f"  Confidence: {confidence:.3f}")
                source = field_value.get('source')
                if source:
                    print(f"  Bounding Box: {source}")
                print()
        else:
            print("No fields extracted")
        print()
        
        # Display content metadata
        print("📋 Content Metadata:")
        print("-" * 80)
        print(f"Kind: {first_content.get('kind')}")
        if first_content.get("kind") == "document":
            start_page = first_content.get("startPageNumber", 0)
            end_page = first_content.get("endPageNumber", 0)
            print(f"Pages: {start_page} - {end_page}")
            print(f"Total pages: {end_page - start_page + 1}")
        print()
    
    # Save full result to file
    saved_file_path = save_json_to_file(analysis_result, filename_prefix="prebuilt_invoice_analysis_result")
    print(f"💾 Full analysis result saved. Review the complete JSON at: {saved_file_path}")
else:
    print("No analysis result available")
