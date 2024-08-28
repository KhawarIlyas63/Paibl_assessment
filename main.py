from typing import List, Dict
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Invoice(BaseModel):
    filehash: str
    vendorName: str
    invoiceDate: str
    amountPayable: str

class Invoices(BaseModel):
    invoices: List[Invoice]

# Known data for matching
certain_match = [
    { "invoiceId": "SW322", "hash": "5d41402abc4b2a76b9719d911017c592" },
    { "invoiceId": "ABC121", "hash": "098f6bcd4621d373cade4e832627b4f6" },
    { "invoiceId": "EA413", "hash": "e4da3b7fbbce2345d7772b0674a318d5" },
    { "invoiceId": "ABL002", "hash": "7b774effe4a349c6dd82ad4f4f21d34c" },
    { "invoiceId": "IPI523", "hash": "098f6bcd4621d373cade4e832627b4f6" }
]

potentially_matched = [
    {"invoiceId": "OZC001", "hash": "8f14e45fceea167a5a36dedd4bea2543", "confidence": 90, "warning": "Vendor name is not an exact match."},
    {"invoiceId": "ABL002", "hash": "6f1ed002ab5595859014ebf0951522d9", "confidence": 50, "warning": "Vendor name is not an exact match. Date does not match"},
    {"invoiceId": "TPG102", "hash": "25f9e794323b453885f5181f1b624d0b", "confidence": 95, "warning": "Vendor name is not an exact match."}
]

unmatched = [{ "hash": "2f1ed002ab5595859014ebf0951522d3" }]

@app.post("/match_invoices/")
def match_invoices_endpoint(invoices: Invoices):
    """API endpoint to match invoices."""
    result = {
        "certainMatch": [],
        "potentiallyMatched": [],
        "unmatched": []
    }

    # Convert lists to dictionaries for quick lookup
    certain_match_dict = {entry["hash"]: entry["invoiceId"] for entry in certain_match}
    potentially_matched_dict = {
        entry["hash"]: {
            "invoiceId": entry["invoiceId"],
            "confidence": entry["confidence"],
            "warning": entry["warning"]
        }
        for entry in potentially_matched
    }

    # Set to keep track of all processed hashes
    processed_hashes = set()

    for invoice in invoices.invoices:
        filehash = invoice.filehash

        if filehash in certain_match_dict:
            result["certainMatch"].append({
                "invoiceId": certain_match_dict[filehash],
                "hash": filehash
            })
            processed_hashes.add(filehash)
        elif filehash in potentially_matched_dict:
            result["potentiallyMatched"].append({
                "invoiceId": potentially_matched_dict[filehash]["invoiceId"],
                "hash": filehash,
                "confidence": potentially_matched_dict[filehash]["confidence"],
                "warning": potentially_matched_dict[filehash]["warning"]
            })
            processed_hashes.add(filehash)
        else:
            result["unmatched"].append({"hash": filehash})

    # Ensure that unmatched hashes are those not in any processed set
    for invoice in invoices.invoices:
        if invoice.filehash not in processed_hashes:
            result["unmatched"].append({"hash": invoice.filehash})

    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
