from enum import Enum
from database import db
from enum_types.gene_status import GeneStatusEnum
import sqlalchemy as sa

class Gene(db.Model):
    __tablename__ = 'gene'

    id = db.Column(db.BigInteger(), primary_key=True)
    taxon_id = db.Column(db.BigInteger(), nullable=False)
    creator_id = db.Column(db.BigInteger(), nullable=False)
    creation_date = db.Column(db.DateTime(), nullable=False)
    editor_id = db.Column(db.BigInteger(), nullable=True)
    mod_date = db.Column(db.DateTime(), nullable=True)
    withdrawn_date = db.Column(db.DateTime(), nullable=True)
    status = db.Column(sa.Enum(GeneStatusEnum, name='gene_status'), nullable=False)
    primary_id = db.Column(db.String(16), nullable=True)
    primary_id_source = db.Column(db.String(50), nullable=True)

    @classmethod
    async def get_gene_by_primary(cls, primary: str) -> 'Gene':
        query = cls.query.where(cls.primary_id == primary)
        return await query.gino.first()
