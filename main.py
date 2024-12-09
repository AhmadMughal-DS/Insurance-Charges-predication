from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import boto3

# Initialize FastAPI
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific domains (e.g., ["http://localhost:3000"]) in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (e.g., POST, GET)
    allow_headers=["*"],  # Allows all headers
)

# Initialize SageMaker client
sagemaker_client = boto3.client("sagemaker-runtime", region_name="your region name")

# SageMaker endpoint name
ENDPOINT_NAME = "your endpoint name"

# Define the input schema
class PredictionRequest(BaseModel):
    age: int
    sex: str  # "male" or "female"
    bmi: float
    children: int
    smoker: str  # "yes" or "no"
    region: str  # "northeast", "northwest", "southeast", "southwest"

import json

@app.post("/predict")
async def predict(request: PredictionRequest):
    try:
        # Debug log: Input data
        print(f"Received request: {request}")

        # Map categorical values to numerical
        sex_map = {"male": 0, "female": 1}
        smoker_map = {"no": 0, "yes": 1}
        region_map = {
            "northeast": (0, 0, 0),
            "northwest": (1, 0, 0),
            "southeast": (0, 1, 0),
            "southwest": (0, 0, 1),
        }

        # Convert categorical inputs
        sex = sex_map.get(request.sex.lower())
        smoker = smoker_map.get(request.smoker.lower())
        region_northwest, region_southeast, region_southwest = region_map.get(request.region.lower(), (None, None, None))

        # Debug log: Converted values
        print(f"Converted values - Sex: {sex}, Smoker: {smoker}, Region: {region_northwest, region_southeast, region_southwest}")

        # Ensure all values are valid
        if None in [sex, smoker, region_northwest, region_southeast, region_southwest]:
            raise ValueError("Invalid categorical value provided.")

        # Create payload for SageMaker
        payload = (
            f"{request.age},{sex},{request.bmi},{request.children},{smoker},"
            f"{region_northwest},{region_southeast},{region_southwest}"
        )

        # Debug log: Payload
        print(f"Payload sent to SageMaker: {payload}")

        # Invoke SageMaker endpoint
        response = sagemaker_client.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType="text/csv",
            Body=payload,
        )

        # Decode the response and parse JSON
        response_body = response["Body"].read().decode("utf-8")
        print(f"SageMaker response: {response_body}")

        # Extract the score from the JSON response
        response_data = json.loads(response_body)
        prediction_score = response_data["predictions"][0]["score"]

        # Return the prediction score
        return {"prediction": prediction_score}

    except Exception as e:
        # Log the error
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error invoking endpoint: {str(e)}")

