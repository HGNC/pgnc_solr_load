from database import db

class Symbol(db.Model):
    __tablename__ = 'symbol'

    id = db.Column(db.BigInteger(), primary_key=True)
    symbol = db.Column(db.String(45), nullable=False)

    @classmethod
    async def create_symbol(cls, symbol: str) -> 'Symbol':
        """Async factory method for creating a new user."""
        symbol_coroutine = await cls.create(symbol=symbol)  # Async database insert
        return symbol_coroutine
