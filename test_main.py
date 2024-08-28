import pytest
from fastapi.testclient import TestClient
from main import app
import json
import os

client = TestClient(app)

@pytest.mark.parametrize("file_name, expected_status_code, expected_response", [
    ("input_invoices.json", 200, {
        "certainMatch": [
            {"invoiceId": "OZC001", "hash": "8f14e45fceea167a5a36dedd4bea2543"},
            {"invoiceId": "ABL002", "hash": "6f1ed002ab5595859014ebf0951522d9"},
            {"invoiceId": "TPG102", "hash": "25f9e794323b453885f5181f1b624d0b"}
        ],
        "potentiallyMatched": [
            {"invoiceId": "OZC001", "hash": "8f14e45fceea167a5a36dedd4bea2543", "confidence": 90, "warning": "Vendor name is not an exact match."},
            {"invoiceId": "ABL002", "hash": "6f1ed002ab5595859014ebf0951522d9", "confidence": 50, "warning": "Vendor name is not an exact match. Date does not match"},
            {"invoiceId": "TPG102", "hash": "25f9e794323b453885f5181f1b624d0b", "confidence": 95, "warning": "Vendor name is not an exact match."}
        ],
        "unmatched": [
            {"hash": "2f1ed002ab5595859014ebf0951522d3"}
        ]
    }),

])
def test_match_invoices(file_name, expected_status_code, expected_response):
    # Check if the file exists
    assert os.path.exists(file_name), f"File {file_name} does not exist"

    with open(file_name) as f:
        input_data = json.load(f)
    
    response = client.post("/match_invoices/", json=input_data)
    
    assert response.status_code == expected_status_code
    
    actual_response = response.json()
    assert actual_response == expected_response, f"Expected: {expected_response}, but got: {actual_response}"
