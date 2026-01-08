from fastapi import FastAPI, UploadFile, Query
from datetime import datetime
import uvicorn

# Imports from your local files
from emissions import normalize_and_calculate
from extract import mock_extract_data

app = FastAPI()
upload_history = [] 

@app.post("/process")
async def process_document(file: UploadFile, batch_name: str = Query("Default Batch")):
    # 1. Extraction logic
    data = await mock_extract_data(file.filename)
    
    # 2. Calculation logic
    total_co2 = normalize_and_calculate(data['quantity'], data['unit'], data['fuel_type'])
    
    # 3. Create the record (MATCHING THE FRONTEND KEYS)
    record = {
        "id": len(upload_history) + 1,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "supplier": data['supplier'],
        "fuel_type": data['fuel_type'],
        "total_emissions_kgco2e": total_co2, # Fixed key name
        "batch": batch_name,
        "extracted_data": data  # Keeps compatibility with your audit view
    }
    
    upload_history.append(record)
    return record

@app.get("/history")
async def get_history():
    return upload_history

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)