"""
Tests for the Symbol model
"""
import pytest
import sqlalchemy as sa
from db.models.base import Base  # type: ignore
from db.models.symbol import Symbol  # type: ignore


class TestSymbolModel:
    """Test cases for the Symbol model"""
    
    def test_symbol_inheritance(self):
        """Test that Symbol inherits from Base"""
        assert issubclass(Symbol, Base)
    
    def test_symbol_table_name(self):
        """Test that Symbol has the correct table name"""
        assert Symbol.__tablename__ == "symbol"
    
    def test_symbol_has_required_columns(self):
        """Test that Symbol model has all required columns"""
        columns = Symbol.__table__.columns
        column_names = [col.name for col in columns]
        
        expected_columns = ['id', 'symbol']
        
        for col in expected_columns:
            assert col in column_names, f"Column {col} not found in Symbol model"
    
    def test_symbol_primary_key(self):
        """Test that id is the primary key"""
        primary_keys = [col.name for col in Symbol.__table__.primary_key.columns]
        assert primary_keys == ['id']
        assert Symbol.__table__.columns['id'].type.python_type is int
    
    def test_symbol_column_types(self):
        """Test that column types are correctly defined"""
        columns = Symbol.__table__.columns
        
        # Check BigInteger for id
        assert isinstance(columns['id'].type, sa.BigInteger)
        
        # Check String for symbol
        assert isinstance(columns['symbol'].type, sa.String)
        assert columns['symbol'].type.length == 45
    
    def test_symbol_nullable_constraints(self):
        """Test that nullable constraints are correctly set"""
        columns = Symbol.__table__.columns
        
        # Both columns should be required (not nullable)
        assert not columns['id'].nullable
        assert not columns['symbol'].nullable
    
    def test_symbol_relationships_exist(self):
        """Test that relationships are defined"""
        # Check that relationship attributes exist
        assert hasattr(Symbol, 'symbol_has_genes')
    
    def test_symbol_repr(self):
        """Test that __repr__ method works correctly"""
        # Create a mock symbol instance
        symbol = Symbol()
        symbol.id = 123
        symbol.symbol = "TEST_SYMBOL"
        
        repr_str = repr(symbol)
        
        # Check that key information is in the repr
        assert "Symbol(" in repr_str
        assert "id=123" in repr_str
        assert "symbol='TEST_SYMBOL'" in repr_str
    
    def test_symbol_instantiation(self):
        """Test that Symbol can be instantiated"""
        symbol = Symbol()
        assert isinstance(symbol, Symbol)
        assert isinstance(symbol, Base)
    
    def test_symbol_creation_with_fields(self):
        """Test creating a symbol with fields"""
        symbol = Symbol()
        symbol.symbol = "BRCA1"
        
        assert symbol.symbol == "BRCA1"
    
    @pytest.mark.parametrize("symbol_value", [
        "BRCA1",
        "TP53", 
        "EGFR",
        "PIK3CA",
        "KRAS",
        "A1BG",
        "A2M"
    ])
    def test_symbol_various_values(self, symbol_value):
        """Test that various symbol values can be assigned"""
        symbol = Symbol()
        symbol.symbol = symbol_value
        assert symbol.symbol == symbol_value
    
    def test_symbol_string_length_constraint(self):
        """Test that symbol field respects length constraints"""
        symbol = Symbol()
        
        # Test with maximum length (45 characters)
        max_length_symbol = "A" * 45
        symbol.symbol = max_length_symbol
        assert symbol.symbol == max_length_symbol
        assert len(symbol.symbol) == 45
    
    def test_symbol_empty_string(self):
        """Test that symbol can be set to empty string"""
        symbol = Symbol()
        symbol.symbol = ""
        assert symbol.symbol == ""
