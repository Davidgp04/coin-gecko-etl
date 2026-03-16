def load_price_data(db, transformed_data):
    db.insert_price_data_bulk(transformed_data)
    