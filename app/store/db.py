import os

import asyncpg

class DB:
    def __init__(self):
        self.conn = None

    async def connect(self) -> None:
        try:
            self.conn = await asyncpg.connect(
                host="ep-weathered-unit-a59kz001-pooler.us-east-2.aws.neon.tech",
                port=5432,
                database="neondb",
                user=os.environ.get('POSTGRES_USER'),
                password=os.environ.get('POSTGRES_PASSWORD')
            )
            print("Successfully connected to Neon database")
        except Exception as e:
            print(f"Error connecting to database: {e}")

    async def disconnect(self) -> None:
        if self.conn:
            await self.conn.close()
            print("Database connection closed")