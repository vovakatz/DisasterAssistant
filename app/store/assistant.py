from app.store.db import DB

class AssistantStore:
    async def save_q_and_a(self, thread_id, question, answer: str):
        db = DB()
        try:
            await db.connect()
            await db.conn.execute("INSERT INTO q_and_a(thread_id, question, answer) VALUES($1, $2, $3)", thread_id, question, answer)
            await db.disconnect()
        except Exception as e:
            print(f"Error saving Q&A: {e}")
        finally:
            await db.disconnect()