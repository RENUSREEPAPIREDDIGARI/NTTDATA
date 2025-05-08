from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from typing import Optional
import os
from datetime import datetime
from data_processor import DataProcessor
from data_validator import DataValidator
from query_processor import QueryProcessor

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components with sample data
SAMPLE_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "sample_oee_data.xlsx")
data_processor = DataProcessor(SAMPLE_DATA_PATH) if os.path.exists(SAMPLE_DATA_PATH) else None
query_processor = QueryProcessor()

class Query(BaseModel):
    device_id: Optional[str] = None
    location: Optional[str] = None
    month: Optional[str] = None
    message: str

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save the uploaded file
        file_path = f"data/{file.filename}"
        os.makedirs("data", exist_ok=True)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Validate the data
        df = pd.read_excel(file_path)
        is_valid, validation_results = DataValidator.validate_data(df)
        
        if not is_valid:
            error_message = DataValidator.get_validation_message(validation_results)
            raise HTTPException(status_code=400, detail=error_message)
        
        # Initialize data processor with the uploaded file
        global data_processor
        data_processor = DataProcessor(file_path)
        
        return {"message": "File uploaded and validated successfully", "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/query")
async def process_query(query: Query):
    try:
        if data_processor is None:
            raise HTTPException(status_code=400, detail="Please upload data file first")
        
        # Process natural language query
        extracted_params = query_processor.process_query(query.message)
        
        # Use extracted parameters or provided ones
        device_id = extracted_params['device_id'] or query.device_id
        location = extracted_params['location'] or query.location
        month = extracted_params['month'] or query.month
        
        # Calculate OEE
        oee_data = data_processor.calculate_oee(
            device_id=device_id,
            location=location,
            month=month
        )
        
        # Generate natural language response
        response_message = query_processor.generate_response(query.message, oee_data)
        
        return {
            **oee_data,
            "message": response_message
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/filters")
async def get_filters():
    try:
        if data_processor is None:
            raise HTTPException(status_code=400, detail="Please upload data file first")
        
        return data_processor.get_available_filters()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"} 