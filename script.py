from src.etl.extract.extract import get_price_data
from src.etl.transform.transform import transform_price_data
from src.db.database_connection import Database
from src.etl.load.load import load_price_data

if __name__ == "__main__":
    db=Database()
    crypto_currencies = db.get_crypto_currencies()
    currencies = db.get_currencies()
    response_dict = get_price_data(currencies=list(currencies.keys()), crypto_currencies=list(crypto_currencies.keys()))
    transformed_data = transform_price_data(response_dict, crypto_currencies, currencies)
    for data in transformed_data:
        print(data)
    load_price_data(db, transformed_data)
