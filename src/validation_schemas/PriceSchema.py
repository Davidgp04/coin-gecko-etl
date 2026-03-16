from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, timezone
from decimal import Decimal
class PriceSchema(BaseModel):
    coin_id: int = Field(..., description="ID of the cryptocurrency")
    currency_id: int = Field(..., description="ID of the currency")
    price: Decimal = Field(..., max_digits=20, decimal_places=10, min_value=0, description="Price of the cryptocurrency in the specified currency")
    last_updated_at: datetime = Field(..., description="Timestamp of the last update for this price data")
    created_at: datetime = Field(default_factory=lambda:datetime.now(timezone.utc), description="Timestamp of when the price data was created in the database")
    model_config = ConfigDict(from_attributes=True)