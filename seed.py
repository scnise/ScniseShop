import asyncio
from sqlalchemy import select
from database import async_session_maker, Item, init_db

async def seed_data():
    await init_db()
    
    async with async_session_maker() as session:
        result = await session.execute(select(Item))
        existing_items = result.scalars().all()
        
        if existing_items:
            print("База данных уже содержит товары.")
            return

        items = [
            Item(
                name="Discord Nitro 1 Месяц", 
                price=349.0, 
                description="Активация подписки Discord Nitro на 30 дней. Без слета."
            ),
            Item(
                name="Telegram Premium 1 Год", 
                price=1999.0, 
                description="Подписка Telegram Premium на 12 месяцев в виде подарка."
            ),
            Item(
                name="Spotify Premium 3 Месяца", 
                price=450.0, 
                description="Индивидуальная подписка Spotify для вашего аккаунта."
            )
        ]
        
        session.add_all(items)
        await session.commit()
        print("Тестовые товары успешно добавлены в базу данных ScniseShop!")

if __name__ == "__main__":
    asyncio.run(seed_data())