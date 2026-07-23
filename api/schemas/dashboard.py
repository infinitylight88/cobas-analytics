from pydantic import BaseModel
from datetime import date


class DailyWorkload(BaseModel):

    date: date
    unique_samples: int