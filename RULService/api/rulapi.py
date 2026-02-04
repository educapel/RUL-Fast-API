
import uvicorn
from fastapi import FastAPI

from RULService.RULObject import SensorInput
from RULService.Model import RULPredictor


app = FastAPI(title = 'rul')



predictor = RULPredictor()

@app.post("/rul")
def predict_rul(sensor_input: SensorInput):
    print('Datarecieved: {sensor_input}')
    print(sensor_input)
    rul = predictor.predict(sensor_input.dict())
    print(rul)
    return {"predicted_rul": round(rul, 2)}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9696)









