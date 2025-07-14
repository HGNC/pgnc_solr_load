"""
Tests for the GeneHasSymbol model
"""
import datetime

import pytest
import sqlalchemy as sa
from db.enum_types.basic_status import BasicStatusEnum  # type: ignore
from db.enum_types.nomenclature import NomenclatureEnum  # type: ignore
from db.models.base import Base  # type: ignore
from db.models.gene_has_symbol import GeneHasSymbol  # type: ignore


class TestGeneHasSymbolModel:
    """Test cases for the GeneHasSymbol model"""
    
    def test_gene_has_symbol_inheritance(self):
        """Test that GeneHasSymbol inherits from Base"""
        assert issubclass(GeneHasSymbol, Base)
    
    def test_gene_has_symbol_table_name(self):
        """Test that GeneHasSymbol has the correct table name"""
        assert GeneHasSymbol.__tablename__ == "gene_has_symbol"
    
    def test_gene_has_symbol_has_required_columns(self):
        """Test that GeneHasSymbol model has all required columns"""
        columns = GeneHasSymbol.__table__.columns
        column_names = [col.name for col in columns]
        
        expected_columns = [
            'gene_id', 'symbol_id', 'type', 'creator_id', 'creation_date',
            'editor_id', 'mod_date', 'withdrawn_date', 'status'
        ]
        
        for col in expected_columns:
            assert col in column_names, f"Column {col} not found in GeneHasSymbol model"
    
    def test_gene_has_symbol_composite_primary_key(self):
        """Test that gene_id and symbol_id form a composite primary key"""
        primary_keys = [col.name for col in GeneHasSymbol.__table__.primary_key.columns]
        assert set(primary_keys) == {'gene_id', 'symbol_id'}
        assert len(primary_keys) == 2
    
    def test_gene_has_symbol_foreign_keys(self):
        """Test that foreign key relationships are properly defined"""
        # Check gene_id foreign key
        gene_id_col = GeneHasSymbol.__table__.columns['gene_id']
        assert len(gene_id_col.foreign_keys) == 1
        fk = list(gene_id_col.foreign_keys)[0]
        assert str(fk.target_fullname) == "gene.id"
        
        # Check symbol_id foreign key
        symbol_id_col = GeneHasSymbol.__table__.columns['symbol_id']
        assert len(symbol_id_col.foreign_keys) == 1
        fk = list(symbol_id_col.foreign_keys)[0]
        assert str(fk.target_fullname) == "symbol.id"
        
        # Check creator_id foreign key
        creator_id_col = GeneHasSymbol.__table__.columns['creator_id']
        assert len(creator_id_col.foreign_keys) == 1
        fk = list(creator_id_col.foreign_keys)[0]
        assert str(fk.target_fullname) == "user.id"
        
        # Check editor_id foreign key
        editor_id_col = GeneHasSymbol.__table__.columns['editor_id']
        assert len(editor_id_col.foreign_keys) == 1
        fk = list(editor_id_col.foreign_keys)[0]
        assert str(fk.target_fullname) == "user.id"
    
    def test_gene_has_symbol_nullable_constraints(self):
        """Test that nullable constraints are correctly set"""
        columns = GeneHasSymbol.__table__.columns
        
        # Required columns (not nullable)
        required_columns = ['gene_id', 'symbol_id', 'type', 'creator_id', 'status']
        for col_name in required_columns:
            assert not columns[col_name].nullable, f"Column {col_name} should not be nullable"
        
        # Optional columns (nullable)
        optional_columns = ['editor_id', 'mod_date', 'withdrawn_date']
        for col_name in optional_columns:
            assert columns[col_name].nullable, f"Column {col_name} should be nullable"
        
        # Special case: creation_date is nullable in this model
        assert columns['creation_date'].nullable
    
    def test_gene_has_symbol_column_types(self):
        """Test that column types are correctly defined"""
        columns = GeneHasSymbol.__table__.columns
        
        # Check Integer columns
        assert isinstance(columns['gene_id'].type, sa.Integer)
        assert isinstance(columns['symbol_id'].type, sa.Integer)
        assert isinstance(columns['creator_id'].type, sa.Integer)
        assert isinstance(columns['editor_id'].type, sa.Integer)
        
        # Check DateTime columns
        assert isinstance(columns['creation_date'].type, sa.DateTime)
        assert isinstance(columns['mod_date'].type, sa.DateTime)
        assert isinstance(columns['withdrawn_date'].type, sa.DateTime)
        
        # Check Enum columns
        assert isinstance(columns['type'].type, sa.Enum)
        assert isinstance(columns['status'].type, sa.Enum)
    
    def test_gene_has_symbol_enum_columns(self):
        """Test that enum columns use correct enum types"""
        columns = GeneHasSymbol.__table__.columns
        
        # Check type column uses NomenclatureEnum
        type_col = columns['type']
        assert isinstance(type_col.type, sa.Enum)
        assert type_col.type.enum_class == NomenclatureEnum
        
        # Check status column uses BasicStatusEnum
        status_col = columns['status']
        assert isinstance(status_col.type, sa.Enum)
        assert status_col.type.enum_class == BasicStatusEnum
    
    def test_gene_has_symbol_default_values(self):
        """Test that default values are properly set"""
        creation_date_col = GeneHasSymbol.__table__.columns['creation_date']
        assert creation_date_col.server_default is not None
    
    def test_gene_has_symbol_relationships_exist(self):
        """Test that relationships are defined"""
        # Check that relationship attributes exist
        assert hasattr(GeneHasSymbol, 'gene')
        assert hasattr(GeneHasSymbol, 'symbol')
        assert hasattr(GeneHasSymbol, 'creator')
        assert hasattr(GeneHasSymbol, 'editor')
    
    def test_gene_has_symbol_instantiation(self):
        """Test that GeneHasSymbol can be instantiated"""
        gene_has_symbol = GeneHasSymbol()
        assert isinstance(gene_has_symbol, GeneHasSymbol)
        assert isinstance(gene_has_symbol, Base)
    
    def test_gene_has_symbol_creation_with_required_fields(self):
        """Test creating a gene_has_symbol with required fields"""
        gene_has_symbol = GeneHasSymbol()
        gene_has_symbol.gene_id = 123
        gene_has_symbol.symbol_id = 456
        gene_has_symbol.type = NomenclatureEnum.approved
        gene_has_symbol.creator_id = 1
        gene_has_symbol.status = BasicStatusEnum.public
        
        assert gene_has_symbol.gene_id == 123
        assert gene_has_symbol.symbol_id == 456
        assert gene_has_symbol.type == NomenclatureEnum.approved
        assert gene_has_symbol.creator_id == 1
        assert gene_has_symbol.status == BasicStatusEnum.public
    
    @pytest.mark.parametrize("nomenclature_type", [
        NomenclatureEnum.approved,
        NomenclatureEnum.alias,
        NomenclatureEnum.previous
    ])
    def test_gene_has_symbol_nomenclature_enum_values(self, nomenclature_type):
        """Test that all NomenclatureEnum values can be assigned"""
        gene_has_symbol = GeneHasSymbol()
        gene_has_symbol.type = nomenclature_type
        assert gene_has_symbol.type == nomenclature_type
    
    @pytest.mark.parametrize("status", [
        BasicStatusEnum.public,
        BasicStatusEnum.internal,
        BasicStatusEnum.withdrawn
    ])
    def test_gene_has_symbol_status_enum_values(self, status):
        """Test that all BasicStatusEnum values can be assigned"""
        gene_has_symbol = GeneHasSymbol()
        gene_has_symbol.status = status
        assert gene_has_symbol.status == status
    
    def test_gene_has_symbol_optional_fields(self):
        """Test that optional fields can be None"""
        gene_has_symbol = GeneHasSymbol()
        
        # These should be able to be None
        assert gene_has_symbol.editor_id is None
        assert gene_has_symbol.mod_date is None
        assert gene_has_symbol.withdrawn_date is None
        assert gene_has_symbol.creation_date is None  # This is nullable in this model
    
    def test_gene_has_symbol_datetime_fields(self):
        """Test that datetime fields can be set"""
        gene_has_symbol = GeneHasSymbol()
        test_date = datetime.datetime(2025, 7, 14, 12, 0, 0)
        
        gene_has_symbol.creation_date = test_date
        gene_has_symbol.mod_date = test_date
        gene_has_symbol.withdrawn_date = test_date
        
        assert gene_has_symbol.creation_date == test_date
        assert gene_has_symbol.mod_date == test_date
        assert gene_has_symbol.withdrawn_date == test_date
