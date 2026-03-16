from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import os
import logging

logging.basicConfig(level=logging.INFO,
                    format= "%(asctime)s [%(levelname)s] %(message)s")


load_dotenv()
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}
class Database:
    def __init__(self, config=DB_CONFIG):
        self.config = config
        self.connection = None
    def get_connection(self):
        try:
            connection = psycopg2.connect(**self.config)
            logging.info("Database connection successful")
            return connection
        except Exception as e:
            logging.error(f"Database connection error: {e}")
            raise
    def get_crypto_currencies(self,like=None):
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    if like:
                        conditions = []
                        params = []

                        for string in like:
                            conditions.append("name LIKE %s")
                            params.append(f"%{string}%")

                        query = f"""
                            SELECT id, name
                            FROM crypto_currency
                            WHERE {' OR '.join(conditions)}
                        """

                        cursor.execute(query, params)
                    else:
                        cursor.execute("SELECT id, name FROM crypto_currency")
                    rows = cursor.fetchall()
                    return {row["name"]: row["id"] for row in rows}
        except Exception as e:
            logging.error(f"Error fetching crypto currencies: {e}")
            raise
    def get_currencies(self, like=None):
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    if like:
                        conditions = []
                        params = []
                        for string in like:
                            conditions.append("name like %s")
                            params.append(f"%{string}%")
                        query = f"""
                            SELECT id, name
                            FROM currency
                            WHERE {' OR '.join(conditions)}
                        """
                        cursor.execute(query, params)
                    else:
                        cursor.execute("SELECT id, name FROM currency")
                    rows = cursor.fetchall()
                    return {row["name"]: row["id"] for row in rows}
        except Exception as e:
            logging.error(f"Error fetching currencies: {e}")
            raise
    def insert_price_data(self, price_data):
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    insert_query = sql.SQL("""
                        INSERT INTO prices (coin_id, currency_id, price, last_updated_at, created_at)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (coin_id, currency_id, last_updated_at) DO NOTHING
                    """)
                    for data in price_data:
                        cursor.execute(insert_query, (
                            data.coin_id,
                            data.currency_id,
                            data.price,
                            data.last_updated_at,
                            data.created_at
                        ))
                conn.commit()
            logging.info("Price data inserted successfully")
        except Exception as e:
            logging.error(f"Error inserting price data: {e}")
            raise
    def insert_price_data_bulk(self, transformed_data): # transformed_data is a list of PriceSchema instances
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    query = """
                    INSERT INTO prices (
                        coin_id,
                        currency_id,
                        price,
                        last_updated_at,
                        created_at
                    )
                    VALUES (%(coin_id)s, %(currency_id)s, %(price)s, %(last_updated_at)s, %(created_at)s)
                    ON CONFLICT (coin_id, currency_id, last_updated_at) DO NOTHING
                    """
                    records = [p.model_dump() for p in transformed_data]
                    cursor.executemany(query, records)
                conn.commit()
            logging.info("Bulk price data inserted successfully")
        except Exception as e:
            logging.error(f"Error inserting bulk price data: {e}")
            raise


if __name__ == "__main__":
    db = Database()
    crypto_currencies = db.get_crypto_currencies()
    currencies = db.get_currencies()
    print("Crypto Currencies:", crypto_currencies)
    print("Currencies:", currencies)