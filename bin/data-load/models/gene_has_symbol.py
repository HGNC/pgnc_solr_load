from database import db
from enum import Enum
from enum_types.nomenclature import NomenclatureEnum
from enum_types.basic_status import BasicStatusEnum
import sqlalchemy as sa

class GeneHasSymbol(db.Model):
    __tablename__ = 'gene_has_symbol'

    gene_id = db.Column(db.BigInteger(), primary_key=True)
    symbol_id = db.Column(db.BigInteger(), nullable=False)
    type = db.Column(sa.Enum(NomenclatureEnum, name='nomenclature_type'), nullable=False)
    creator_id = db.Column(db.BigInteger(), nullable=False)
    creation_date = db.Column(db.DateTime(), nullable=False)
    editor_id = db.Column(db.BigInteger(), nullable=True)
    mod_date = db.Column(db.DateTime(), nullable=True)
    withdrawn_date = db.Column(db.DateTime(), nullable=True)
    status = db.Column(sa.Enum(BasicStatusEnum, name='basic_status'), nullable=False)

    @classmethod
    async def create_ghs(cls, gene_id: int, symbol_id: int, type: str, creator_id: int, status: str):
        return cls.create(gene_id=gene_id, symbol_id=symbol_id, type=type, creator_id=creator_id, status=status)
