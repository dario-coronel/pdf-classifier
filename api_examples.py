"""
API Usage Examples for PDF Classifier
Demonstrates how to interact with the API endpoints
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000"

def example_get_statistics():
    """Example: Get system statistics"""
    print("\n=== Get Statistics ===")
    
    response = requests.get(f"{BASE_URL}/api/statistics")
    data = response.json()
    
    if data['success']:
        stats = data['statistics']
        print(f"Total documents: {stats['total']}")
        print(f"Pending: {stats['pending']}")
        print(f"Validated: {stats['validated']}")
        print(f"\nBy type:")
        for doc_type, count in stats['by_type'].items():
            print(f"  {doc_type}: {count}")
    else:
        print(f"Error: {data.get('error')}")

def example_process_documents():
    """Example: Process pending documents"""
    print("\n=== Process Documents ===")
    
    response = requests.post(f"{BASE_URL}/api/process")
    data = response.json()
    
    if data['success']:
        print(f"✓ {data['message']}")
        print(f"Processed document IDs: {data['document_ids']}")
    else:
        print(f"✗ Error: {data.get('error')}")

def example_get_documents():
    """Example: Get documents with filters"""
    print("\n=== Get Documents (Filtered) ===")
    
    # Example filters
    params = {
        'type': 'Factura',
        'status': 'classified',
        'limit': 10
    }
    
    response = requests.get(f"{BASE_URL}/api/documents", params=params)
    data = response.json()
    
    if data['success']:
        docs = data['documents']
        print(f"Found {len(docs)} documents")
        for doc in docs[:3]:  # Show first 3
            print(f"\n  ID: {doc['id']}")
            print(f"  File: {doc['original_filename']}")
            print(f"  Type: {doc['document_type']}")
            print(f"  Confidence: {doc['confidence_score']:.2%}")
    else:
        print(f"Error: {data.get('error')}")

def example_get_document_detail():
    """Example: Get specific document details"""
    print("\n=== Get Document Detail ===")
    
    doc_id = 1  # Change to existing document ID
    response = requests.get(f"{BASE_URL}/api/documents/{doc_id}")
    data = response.json()
    
    if data['success']:
        doc = data['document']
        print(f"Document ID: {doc['id']}")
        print(f"Filename: {doc['original_filename']}")
        print(f"Type: {doc['document_type']}")
        print(f"Status: {doc['status']}")
        print(f"CUIT: {doc.get('cuit', 'N/A')}")
        print(f"Provider: {doc.get('provider', 'N/A')}")
        print(f"Date: {doc.get('document_date', 'N/A')}")
        print(f"Amount: {doc.get('total_amount', 'N/A')}")
    else:
        print(f"Error: {data.get('error')}")

def example_validate_document():
    """Example: Validate a single document"""
    print("\n=== Validate Document ===")
    
    payload = {
        'document_id': 1,  # Change to existing document ID
        'document_type': 'Factura',
        'user': 'admin'
    }
    
    response = requests.post(
        f"{BASE_URL}/api/validate",
        json=payload
    )
    data = response.json()
    
    if data['success']:
        print(f"✓ {data['message']}")
    else:
        print(f"✗ Error: {data.get('error')}")

def example_validate_batch():
    """Example: Validate multiple documents"""
    print("\n=== Validate Batch ===")
    
    validations = [
        {
            'document_id': 1,
            'document_type': 'Factura',
            'user': 'admin'
        },
        {
            'document_id': 2,
            'document_type': 'Remito',
            'user': 'admin'
        }
    ]
    
    payload = {'validations': validations}
    
    response = requests.post(
        f"{BASE_URL}/api/validate-batch",
        json=payload
    )
    data = response.json()
    
    if data['success']:
        print(f"✓ {data['message']}")
        print(f"Validated: {data['validated_count']}/{len(validations)}")
    else:
        print(f"✗ Error: {data.get('error')}")

def example_search_by_date_range():
    """Example: Search documents by date range"""
    print("\n=== Search by Date Range ===")
    
    today = datetime.now()
    last_month = today - timedelta(days=30)
    
    params = {
        'date_from': last_month.strftime('%Y-%m-%d'),
        'date_to': today.strftime('%Y-%m-%d'),
        'limit': 50
    }
    
    response = requests.get(f"{BASE_URL}/api/documents", params=params)
    data = response.json()
    
    if data['success']:
        docs = data['documents']
        print(f"Found {len(docs)} documents in the last 30 days")
    else:
        print(f"Error: {data.get('error')}")

def example_search_by_cuit():
    """Example: Search documents by CUIT"""
    print("\n=== Search by CUIT ===")
    
    params = {
        'cuit': '20-12345678-9',
        'limit': 20
    }
    
    response = requests.get(f"{BASE_URL}/api/documents", params=params)
    data = response.json()
    
    if data['success']:
        docs = data['documents']
        print(f"Found {len(docs)} documents for CUIT: {params['cuit']}")
        for doc in docs:
            print(f"  - {doc['original_filename']} ({doc['document_type']})")
    else:
        print(f"Error: {data.get('error')}")

def example_search_by_provider():
    """Example: Search documents by provider"""
    print("\n=== Search by Provider ===")
    
    params = {
        'provider': 'EMPRESA',
        'limit': 20
    }
    
    response = requests.get(f"{BASE_URL}/api/documents", params=params)
    data = response.json()
    
    if data['success']:
        docs = data['documents']
        print(f"Found {len(docs)} documents from providers matching: {params['provider']}")
    else:
        print(f"Error: {data.get('error')}")

def example_get_document_types():
    """Example: Get all document types"""
    print("\n=== Get Document Types ===")
    
    response = requests.get(f"{BASE_URL}/api/document-types")
    data = response.json()
    
    if data['success']:
        doc_types = data['document_types']
        print(f"Available document types:")
        for dt in doc_types:
            status = "✓" if dt['is_active'] else "✗"
            print(f"  {status} {dt['name']} (ID: {dt['id']})")
    else:
        print(f"Error: {data.get('error')}")

def example_retrain_model():
    """Example: Retrain ML model"""
    print("\n=== Retrain Model ===")
    
    response = requests.post(f"{BASE_URL}/api/retrain-model")
    data = response.json()
    
    if data['success']:
        print(f"✓ {data['message']}")
    else:
        print(f"✗ Error: {data.get('error')}")

def run_all_examples():
    """Run all example functions"""
    print("=" * 60)
    print("PDF Classifier - API Usage Examples")
    print("=" * 60)
    
    try:
        # Check if server is running
        response = requests.get(BASE_URL)
        if response.status_code != 200:
            print("✗ Error: Server not responding")
            return
    except requests.exceptions.ConnectionError:
        print("✗ Error: Cannot connect to server")
        print(f"  Make sure the application is running at {BASE_URL}")
        return
    
    print("✓ Server is running\n")
    
    # Run examples
    example_get_statistics()
    example_get_document_types()
    
    # Uncomment to run these examples:
    # example_process_documents()
    # example_get_documents()
    # example_get_document_detail()
    # example_validate_document()
    # example_validate_batch()
    # example_search_by_date_range()
    # example_search_by_cuit()
    # example_search_by_provider()
    # example_retrain_model()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)

if __name__ == '__main__':
    run_all_examples()
