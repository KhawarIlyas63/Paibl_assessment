# Invoice Matching API

## Overview

This project provides a FastAPI application for matching invoices based on their file hashes. It includes functionality to:

- Match invoices from incoming data with a predefined list.
- Identify certain matches, potential matches, and unmatched records.
- Run automated tests using `pytest`.

## Features

- **Invoice Matching**: Compares invoice file hashes and provides match details including confidence and warnings.
- **Testing**: Automated tests using `pytest` to ensure API correctness.

## Setup

### Prerequisites

- Python 3.8 or higher
- `pip` for installing dependencies

### Installation

1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd <repository-directory>

2. Create a virtual environment (recommended):
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the dependencies:
pip install -r requirements.txt

4. To start the FastAPI server, run:
uvicorn main:app --reload