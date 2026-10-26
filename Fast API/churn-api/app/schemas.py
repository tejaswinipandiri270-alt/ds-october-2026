from pydantic import BaseModel, Field, ConfigDict


class AdultCensusData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    age: int = Field(ge=17, le=100)
    workclass: str
    fnlwgt: int
    education: str
    education_num: int = Field(alias="education.num")
    marital_status: str = Field(alias="marital.status")
    occupation: str
    relationship: str
    race: str
    sex: str
    capital_gain: int = Field(alias="capital.gain", ge=0)
    capital_loss: int = Field(alias="capital.loss", ge=0)
    hours_per_week: int = Field(alias="hours.per.week", ge=1, le=100)
    native_country: str = Field(alias="native.country")