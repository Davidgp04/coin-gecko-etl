from src.validation_schemas.PriceSchema import PriceSchema
from src.db.database_connection import Database
from src.etl.extract.extract import get_price_data
def transform_price_data(response_dict, crypto_currencies: dict, currencies: dict):
    # crypto_currencies = db.get_crypto_currencies()

    # currencies = {
    #     "usd": 1,
    #     "cop": 2,}
    transformed_data = []
    for coin, data in response_dict.items():
        for currency, price in data.items():
            if currency != "last_updated_at":
                price_data = PriceSchema(
                    coin_id=crypto_currencies[coin],  # This should be replaced with actual coin_id from your database
                    currency_id=currencies[currency],  # This should be replaced with actual currency_id from your database
                    price=price,
                    last_updated_at=data["last_updated_at"]
                )
                transformed_data.append(price_data)
    return transformed_data

if __name__ == "__main__":
    response_dict = get_price_data()

    db = Database()
    transformed_data = transform_price_data(response_dict, db)
    for data in transformed_data:
        print(data)


    