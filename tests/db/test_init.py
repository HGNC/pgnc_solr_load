"""
Tests for the db package initialization
"""


class TestDbInit:
    """Test cases for the main db package initialization"""
    
    def test_db_package_imports(self):
        """Test that the db package can be imported"""
        import db  # type: ignore
        assert db is not None
    
    def test_models_imported_in_db(self):
        """Test that model classes are available from db package"""
        import db  # type: ignore
        
        # Test some key model imports
        assert hasattr(db, 'Gene')
        assert hasattr(db, 'User')
        assert hasattr(db, 'Symbol')
        assert hasattr(db, 'Location')
        
        # Verify they are classes
        from inspect import isclass
        assert isclass(db.Gene)  # type: ignore
        assert isclass(db.User)  # type: ignore
        assert isclass(db.Symbol)  # type: ignore
        assert isclass(db.Location)  # type: ignore
    
    def test_insert_classes_imported_in_db(self):
        """Test that insert classes are available from db package"""
        import db  # type: ignore
        
        # Test insert class imports
        assert hasattr(db, 'GeneSymbol')
        assert hasattr(db, 'GeneName')
        assert hasattr(db, 'GeneLocation')
        assert hasattr(db, 'GeneLocusType')
        assert hasattr(db, 'GeneXref')
        
        # Verify they are classes
        from inspect import isclass
        assert isclass(db.GeneSymbol)  # type: ignore
        assert isclass(db.GeneName)  # type: ignore
        assert isclass(db.GeneLocation)  # type: ignore
        assert isclass(db.GeneLocusType)  # type: ignore
        assert isclass(db.GeneXref)  # type: ignore
    
    def test_enum_types_imported_in_db(self):
        """Test that enum types are available from db package"""
        import db  # type: ignore
        
        # Test enum imports
        assert hasattr(db, 'GeneStatusEnum')
        assert hasattr(db, 'NomenclatureEnum')
        assert hasattr(db, 'BasicStatusEnum')
        
        # Verify they are enum classes
        from enum import Enum
        assert issubclass(db.GeneStatusEnum, Enum)  # type: ignore
        assert issubclass(db.NomenclatureEnum, Enum)  # type: ignore
        assert issubclass(db.BasicStatusEnum, Enum)  # type: ignore
    
    def test_config_imported_in_db(self):
        """Test that config is available from db package"""
        import db  # type: ignore
        
        # Test config import
        assert hasattr(db, 'Config')
        
        # Verify it's a class
        from inspect import isclass
        assert isclass(db.Config)  # type: ignore
    
    def test_wildcard_imports_work(self):
        """Test that wildcard imports expose expected classes"""
        # Test what gets imported with 'from db import *'
        import db  # type: ignore
        
        # Get all public attributes (not starting with _)
        public_attrs = [attr for attr in dir(db) if not attr.startswith('_')]
        
        # Should have a reasonable number of public attributes
        assert len(public_attrs) > 20  # We have many models, enums, etc.
        
        # Check some specific expected items
        expected_items = [
            'Gene', 'User', 'Symbol', 'Location',  # Models
            'GeneSymbol', 'GeneName',  # Insert classes
            'GeneStatusEnum', 'BasicStatusEnum',  # Enums
            'Config'  # Config
        ]
        
        for item in expected_items:
            assert item in public_attrs, f"Expected {item} to be in db package"
