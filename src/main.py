import asyncio
from fastapi import FastAPI
from fastapi.responses import FileResponse
import pandas as pd
import datetime
import uvicorn


from src.db.models import Transaction, init_db, TransactionCreate
from src.routers import auth_cookies



app = FastAPI(title="My App")

app.include_router(auth_cookies.router)

@app.post("/transactions")
async def create_transaction(transaction: TransactionCreate):
    await add_transaction(**transaction.dict())
    return {"ok": True}


@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/export")
async def export_excel():
    async with async_session() as session:
        result = await session.execute(
            "Select date, type, amount, category FROM transactions"
        )
        transactions = result.fetchall()
        transactions_list = [
            {"Дата": row[0], "Тип": row[1], "Количество": row[2], "Категория": row[3]}
            for row in transactions
        ]
        df = pd.DataFrame(transactions_list)

        file_path = "отчёт.xlsx"

        df.to_excel(file_path, index=False)

        return FileResponse(
            file_path,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            filename="отчёт.xlsx"
        )

async def add_transaction(user_id: int, type, date, amount, category):
    async with async_session() as session:
        transaction = Transaction(
            user_id=user_id,
            date=date,
            type=type,
            amount=amount,
            category=category,
        )
        session.add(transaction)
        
        await session.commit()
        session.execute
    async with async_session() as session:
        result = await session.execute(
            select(Transaction).where(Transaction.user_id == user_id)
        )
        transactions = result.scalars().all()


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
    
