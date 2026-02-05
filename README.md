# RUL-Fast-API

A FastAPI-based service for predicting the Remaining Useful Life (RUL) of turbofan engines using machine learning.

## What is RUL Prediction?

Remaining Useful Life (RUL) prediction estimates how many more cycles a machine (in this case, a turbofan engine) can operate before requiring maintenance or replacement. This service uses 21 sensor readings from an engine to predict its remaining operational cycles.

## Features

- RESTful API for RUL predictions
- Input validation using Pydantic
- Pre-trained Linear Regression model
- Docker support for easy deployment
- Automatic API documentation (Swagger UI)

## Project Structure

```
RUL-Fast-API/
├── RULService/               # Main application package
│   ├── api/                  # FastAPI endpoints
│   │   └── rulapi.py        # Main API application
│   ├── Model/               # ML model logic
│   │   └── rul.py           # RULPredictor class
│   ├── RULObject/           # Data validation schemas
│   │   └── RULObject.py     # SensorInput Pydantic model
│   └── Test/                # Test files
│       └── test.py          # API test script
├── Models/                   # Trained ML models
│   └── lr_rul_pipeline.joblib
├── Scripts/                  # Training scripts
│   ├── Train.py             # Model training
│   └── Predict.py           # Standalone prediction
├── CMAPSSData/              # CMAPSS dataset
├── Dockerfile               # Docker configuration
├── pyproject.toml           # Project dependencies (uv)
└── README.md                # This file
```

## Requirements

- Python 3.13+
- Dependencies managed with `uv`

### Core Dependencies

- FastAPI
- Uvicorn
- Scikit-learn
- Pandas
- Joblib

## Installation

### Option 1: Local Setup with UV

1. **Clone the repository**
```bash
git clone <repository-url>
cd RUL-Fast-API
```

2. **Install UV (if not already installed)**
```bash
pip install uv
```

3. **Install dependencies**
```bash
uv sync
```

4. **Activate virtual environment**
```bash
source .venv/bin/activate
```

### Option 2: Docker Setup

Just have Docker installed on your machine.

## Usage

### Running Locally

**Start the server:**
```bash
# From project root
uvicorn RULService.api.rulapi:app --host 0.0.0.0 --port 9696 --reload
```

**Access the API:**
- **API**: http://localhost:9696
- **Interactive docs (Swagger UI)**: http://localhost:9696/docs
- **ReDoc**: http://localhost:9696/redoc

### Running with Docker

**1. Build the Docker image:**
```bash
docker build -t rulprediction .
```

**2. Run the container:**
```bash
docker run -d -p 9696:9696 --name rul-api rulprediction
```

**3. Check logs:**
```bash
docker logs rul-api
```

**4. Stop the container:**
```bash
docker stop rul-api
```

**5. Remove the container:**
```bash
docker rm rul-api
```

## API Endpoints

### POST /rul

Predict the remaining useful life of an engine.

**Request:**
```bash
curl -X POST http://localhost:9696/rul \
  -H "Content-Type: application/json" \
  -d '{
    "s_1": 0.0,
    "s_2": 0.421876,
    "s_3": 0.512349,
    "s_4": 0.0,
    "s_5": 1.0,
    "s_6": 0.492156,
    "s_7": 0.334521,
    "s_8": 0.198765,
    "s_9": 0.0,
    "s_10": 0.389234,
    "s_11": 0.578912,
    "s_12": 0.312456,
    "s_13": 0.167890,
    "s_14": 0.456123,
    "s_15": 0.0,
    "s_16": 0.423567,
    "s_17": 0.0,
    "s_18": 0.0,
    "s_19": 0.467823,
    "s_20": 0.534219,
    "s_21": 0.601234
  }'
```

**Response:**
```json
{
  "predicted_rul": 123.45
}
```

### Sensor Inputs

The API expects 21 sensor readings (s_1 to s_21) representing:

1. `s_1`: Fan inlet temperature (°R)
2. `s_2`: LPC outlet temperature (°R)
3. `s_3`: HPC outlet temperature (°R)
4. `s_4`: LPT outlet temperature (°R)
5. `s_5`: Fan inlet pressure (psia)
6. `s_6`: Bypass-duct pressure (psia)
7. `s_7`: HPC outlet pressure (psia)
8. `s_8`: Physical fan speed (rpm)
9. `s_9`: Physical core speed (rpm)
10. `s_10`: Engine pressure ratio (P50/P2)
11. `s_11`: HPC outlet static pressure (psia)
12. `s_12`: Ratio of fuel flow to Ps30 (pps/psia)
13. `s_13`: Corrected fan speed (rpm)
14. `s_14`: Corrected core speed (rpm)
15. `s_15`: Bypass ratio
16. `s_16`: Burner fuel-air ratio
17. `s_17`: Bleed enthalpy
18. `s_18`: Required fan speed
19. `s_19`: Required fan conversion speed
20. `s_20`: High-pressure turbine cool air flow
21. `s_21`: Low-pressure turbine cool air flow

## Testing

### Run the test script:

```bash
python RULService/Test/test.py
```

**Expected output:**
```
Predicted RUL: 123.45 cycles
```

### Using Python requests:

```python
import requests

url = 'http://localhost:9696/rul'

sample_data = {
    "s_1": 0.0,
    "s_2": 0.421876,
    # ... all 21 sensors
    "s_21": 0.601234
}

response = requests.post(url, json=sample_data)
result = response.json()
print(f"Predicted RUL: {result['predicted_rul']} cycles")
```

## Model Information

- **Algorithm**: Linear Regression with MinMaxScaler
- **Training Data**: CMAPSS FD001 dataset (turbofan engine degradation simulation)
- **Features**: 21 sensor readings
- **Output**: Remaining useful life in cycles
- **Model File**: `Models/lr_rul_pipeline.joblib`

## Training the Model

To retrain the model with new data:

```bash
python Scripts/Train.py
```

This will:
1. Load the CMAPSS dataset
2. Preprocess and scale features
3. Train a Linear Regression model
4. Save the pipeline to `Models/lr_rul_pipeline.joblib`

## Development

### Project Dependencies

Dependencies are managed in `pyproject.toml`:

```toml
[project]
dependencies = [
    "fastapi>=0.128.0",
    "scikit-learn>=1.8.0",
    "uvicorn>=0.40.0",
    "pandas>=2.0.0",
    "joblib>=1.3.0",
]

[dependency-groups]
dev = [
    "requests>=2.32.5",
]
```

### Adding Dependencies

```bash
# Add a new dependency
uv add <package-name>

# Add a dev dependency
uv add --dev <package-name>

# Sync dependencies
uv sync
```

### Code Structure

- **API Layer** (`RULService/api/`): Handles HTTP requests/responses
- **Model Layer** (`RULService/Model/`): ML model loading and prediction logic
- **Validation Layer** (`RULService/RULObject/`): Input data validation using Pydantic

## Docker Commands Reference

```bash
# Build image
docker build -t rulprediction .

# Run container
docker run -d -p 9696:9696 --name rul-api rulprediction

# View logs
docker logs rul-api
docker logs -f rul-api  # Follow logs

# Manage container
docker stop rul-api
docker start rul-api
docker restart rul-api
docker rm rul-api

# Enter container
docker exec -it rul-api bash

# Clean up
docker system prune -a
```

## Troubleshooting

### Port Already in Use

If port 9696 is already allocated:

```bash
# Find what's using the port
lsof -i :9696

# Kill the process
kill -9 <PID>

# Or use a different port
docker run -d -p 8080:9696 --name rul-api rulprediction
```

### Module Not Found Errors

Make sure you're running from the project root and have activated the virtual environment:

```bash
cd /path/to/RUL-Fast-API
source .venv/bin/activate
```

### Docker Build Fails

Try rebuilding without cache:

```bash
docker build --no-cache -t rulprediction .
```

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:9696/docs
- **ReDoc**: http://localhost:9696/redoc

These provide:
- Interactive API testing
- Request/response schemas
- Example requests
- Try-it-out functionality

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request


## Dataset

This project uses the CMAPSS (Commercial Modular Aero-Propulsion System Simulation) dataset from NASA's Prognostics Data Repository for training the RUL prediction model.




