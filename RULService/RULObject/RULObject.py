from pydantic import BaseModel, confloat



SensorValue = confloat(ge=0.0, le=1)

class SensorInput(BaseModel):
    s_1: SensorValue
    s_2: SensorValue
    s_3: SensorValue
    s_4: SensorValue
    s_5: SensorValue
    s_6: SensorValue
    s_7: SensorValue
    s_8: SensorValue
    s_9: SensorValue
    s_10: SensorValue
    s_11: SensorValue
    s_12: SensorValue
    s_13: SensorValue
    s_14: SensorValue
    s_15: SensorValue
    s_16: SensorValue
    s_17: SensorValue
    s_18: SensorValue
    s_19: SensorValue
    s_20: SensorValue
    s_21: SensorValue


