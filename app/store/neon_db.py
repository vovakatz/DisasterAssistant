import os
import pg8000
from typing import Optional, Dict

class NeonDatabase:
    def __init__(self):
        self.conn = None

    def connect(self) -> None:
        try:
            self.conn = pg8000.connect(
                host="ep-weathered-unit-a59kz001-pooler.us-east-2.aws.neon.tech",
                port=5432,
                database="neondb",
                user=os.environ.get('POSTGRES_USER'),
                password=os.environ.get('POSTGRES_PASSWORD')
            )
            print("Successfully connected to Neon database")
        except pg8000.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def disconnect(self) -> None:
        if self.conn:
            self.conn.close()
            print("Database connection closed")

    def add_record(self, table_name: str, data: Dict) -> bool:
        if not self.conn:
            self.connect()

        try:
            with self.conn.cursor() as cur:
                # Create the INSERT query dynamically
                columns = ', '.join(data.keys())
                values = ', '.join(['%s'] * len(data))
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"

                # Execute the query with the data values
                cur.execute(query, list(data.values()))
                self.conn.commit()
                print(f"Successfully added record to {table_name}")
                return True

        except pg8000.Error as e:
            print(f"Error adding record: {e}")
            self.conn.rollback()
            return False

        finally:
            self.disconnect()