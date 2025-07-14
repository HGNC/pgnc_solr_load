"""
Integration tests for all insert classes
"""
from datetime import datetime
from unittest.mock import Mock, patch

import pytest
from insert import (
    GeneLocation,  # type: ignore
    GeneLocusType,  # type: ignore
    GeneName,  # type: ignore
    GeneSymbol,  # type: ignore
    GeneXref,  # type: ignore
)


class TestInsertIntegration:
    """Integration tests for all insert classes"""
    
    @pytest.fixture
    def mock_session(self):
        """Create a mock database session"""
        session = Mock()
        session.add = Mock()
        session.flush = Mock()
        session.refresh = Mock()
        
        # Mock query chain for classes that need it
        query_mock = Mock()
        where_mock = Mock()
        one_mock = Mock()
        one_or_none_mock = Mock()
        
        session.query.return_value = query_mock
        query_mock.where.return_value = where_mock
        where_mock.one.return_value = one_mock
        where_mock.one_or_none.return_value = one_or_none_mock
        
        return session
    
    def test_all_insert_classes_are_available(self):
        """Test that all insert classes are available through the main module"""
        assert GeneSymbol is not None
        assert GeneName is not None
        assert GeneLocation is not None
        assert GeneLocusType is not None
        assert GeneXref is not None

    def test_all_insert_classes_have_required_methods(self):
        """Test that all insert classes have the required methods"""
        classes = [GeneSymbol, GeneName, GeneLocation, GeneLocusType, GeneXref]
        
        for cls in classes:
            # All classes should have __init__ and __repr__
            assert hasattr(cls, '__init__')
            assert hasattr(cls, '__repr__')
            
            # All classes should have their specific private methods
            if cls == GeneSymbol:
                assert hasattr(cls, '_create_symbol')
                assert hasattr(cls, '_create_gene_has_symbol')
            elif cls == GeneName:
                assert hasattr(cls, '_create_name')
                assert hasattr(cls, '_create_gene_has_name')
            elif cls == GeneLocation:
                assert hasattr(cls, '_create_gene_has_location')
            elif cls == GeneLocusType:
                assert hasattr(cls, '_create_gene_has_locus_type')
            elif cls == GeneXref:
                assert hasattr(cls, '_create_xref')
                assert hasattr(cls, '_create_gene_has_xref')

    def test_all_classes_accept_common_parameters(self, mock_session):
        """Test that all classes can be instantiated with common parameters"""
        common_params = {
            "session": mock_session,
            "gene_id": 1001,
            "creator_id": 2001,
            "status": "public"
        }
        
        # Setup mocks for classes that need additional setup
        mock_location = Mock()
        mock_location.id = 123
        mock_locus_type = Mock()
        mock_locus_type.id = 456
        mock_xref = Mock()
        mock_xref.id = 789
        
        mock_session.query().where().one.return_value = mock_location
        mock_session.query().where().one_or_none.return_value = None  # For GeneXref to create new
        
        with patch('insert.gene_symbol.Symbol'), \
             patch('insert.gene_symbol.GeneHasSymbol'), \
             patch('insert.gene_name.Name'), \
             patch('insert.gene_name.GeneHasName'), \
             patch('insert.gene_location.GeneHasLocation'), \
             patch('insert.gene_locus_type.GeneHasLocusType'), \
             patch('insert.gene_xref.Xref', return_value=mock_xref), \
             patch('insert.gene_xref.GeneHasXref'):
            
            # Test GeneSymbol
            gene_symbol = GeneSymbol(
                **common_params,
                symbol="TEST_SYMBOL",
                type="approved"
            )
            assert hasattr(gene_symbol, 'gene_id')
            assert hasattr(gene_symbol, 'creator_id')
            assert hasattr(gene_symbol, 'status')
            
            # Test GeneName
            gene_name = GeneName(
                **common_params,
                name="test name",
                type="approved"
            )
            assert hasattr(gene_name, 'gene_id')
            assert hasattr(gene_name, 'creator_id')
            assert hasattr(gene_name, 'status')
            
            # Test GeneLocation
            gene_location = GeneLocation(
                **common_params,
                location_name="1p36.33"
            )
            assert hasattr(gene_location, 'gene_id')
            assert hasattr(gene_location, 'creator_id')
            assert hasattr(gene_location, 'status')
            
            # Test GeneLocusType
            gene_locus_type = GeneLocusType(
                **common_params,
                locus_type_name="gene with protein product"
            )
            assert hasattr(gene_locus_type, 'gene_id')
            assert hasattr(gene_locus_type, 'creator_id')
            assert hasattr(gene_locus_type, 'status')
            
            # Test GeneXref
            gene_xref = GeneXref(
                **common_params,
                display_id="NM_000001",
                ext_res_id=1,
                source="RefSeq"
            )
            assert hasattr(gene_xref, 'gene_id')
            assert hasattr(gene_xref, 'creator_id')
            assert hasattr(gene_xref, 'status')

    def test_all_classes_have_creation_date_attribute(self, mock_session):
        """Test that all classes have a creation_date attribute"""
        mock_creation_date = datetime(2025, 7, 14, 12, 0, 0)
        
        # Setup common mocks
        mock_location = Mock()
        mock_location.id = 123
        mock_locus_type = Mock()
        mock_locus_type.id = 456
        
        mock_session.query().where().one.return_value = mock_location
        mock_session.query().where().one_or_none.return_value = None
        
        with patch('insert.gene_symbol.Symbol'), \
             patch('insert.gene_symbol.GeneHasSymbol') as MockGeneHasSymbol, \
             patch('insert.gene_name.Name'), \
             patch('insert.gene_name.GeneHasName') as MockGeneHasName, \
             patch('insert.gene_location.GeneHasLocation') as MockGeneHasLocation, \
             patch('insert.gene_locus_type.GeneHasLocusType') as MockGeneHasLocusType, \
             patch('insert.gene_xref.Xref'), \
             patch('insert.gene_xref.GeneHasXref') as MockGeneHasXref:
            
            # Setup mock returns with creation_date
            for mock_class in [MockGeneHasSymbol, MockGeneHasName, MockGeneHasLocation, MockGeneHasLocusType, MockGeneHasXref]:
                mock_instance = Mock()
                mock_instance.creation_date = mock_creation_date
                mock_class.return_value = mock_instance
            
            # Test that all classes have creation_date
            gene_symbol = GeneSymbol(mock_session, "TEST", 1, 1, "approved", "public")
            assert gene_symbol.creation_date == mock_creation_date
            
            gene_name = GeneName(mock_session, "test", 1, 1, "approved", "public")
            assert gene_name.creation_date == mock_creation_date
            
            gene_location = GeneLocation(mock_session, "1p36.33", 1, 1, "public")
            assert gene_location.creation_date == mock_creation_date
            
            gene_locus_type = GeneLocusType(mock_session, "gene with protein product", 1, 1, "public")
            assert gene_locus_type.creation_date == mock_creation_date
            
            gene_xref = GeneXref(mock_session, "NM_000001", 1, 1, 1, "RefSeq", "public")
            assert gene_xref.creation_date == mock_creation_date

    def test_all_classes_interact_with_session_correctly(self, mock_session):
        """Test that all classes interact with the database session correctly"""
        # Setup common mocks
        mock_location = Mock()
        mock_location.id = 123
        mock_locus_type = Mock()
        mock_locus_type.id = 456
        
        mock_session.query().where().one.return_value = mock_location
        mock_session.query().where().one_or_none.return_value = None
        
        with patch('insert.gene_symbol.Symbol'), \
             patch('insert.gene_symbol.GeneHasSymbol'), \
             patch('insert.gene_name.Name'), \
             patch('insert.gene_name.GeneHasName'), \
             patch('insert.gene_location.GeneHasLocation'), \
             patch('insert.gene_locus_type.GeneHasLocusType'), \
             patch('insert.gene_xref.Xref'), \
             patch('insert.gene_xref.GeneHasXref'):
            
            # Reset session mock
            mock_session.reset_mock()
            
            # Create instances of all classes
            GeneSymbol(mock_session, "TEST", 1, 1, "approved", "public")
            GeneName(mock_session, "test", 1, 1, "approved", "public")
            GeneLocation(mock_session, "1p36.33", 1, 1, "public")
            GeneLocusType(mock_session, "gene with protein product", 1, 1, "public")
            GeneXref(mock_session, "NM_000001", 1, 1, 1, "RefSeq", "public")
            
            # Verify that session methods were called
            assert mock_session.add.call_count > 0
            assert mock_session.flush.call_count > 0
            assert mock_session.refresh.call_count > 0

    def test_repr_methods_return_strings(self, mock_session):
        """Test that all classes have proper __repr__ methods that return strings"""
        mock_creation_date = datetime(2025, 7, 14, 12, 0, 0)
        
        # Setup common mocks
        mock_location = Mock()
        mock_location.id = 123
        mock_locus_type = Mock()
        mock_locus_type.id = 456
        
        mock_session.query().where().one.return_value = mock_location
        mock_session.query().where().one_or_none.return_value = None
        
        with patch('insert.gene_symbol.Symbol'), \
             patch('insert.gene_symbol.GeneHasSymbol') as MockGeneHasSymbol, \
             patch('insert.gene_name.Name'), \
             patch('insert.gene_name.GeneHasName') as MockGeneHasName, \
             patch('insert.gene_location.GeneHasLocation') as MockGeneHasLocation, \
             patch('insert.gene_locus_type.GeneHasLocusType') as MockGeneHasLocusType, \
             patch('insert.gene_xref.Xref'), \
             patch('insert.gene_xref.GeneHasXref') as MockGeneHasXref:
            
            # Setup mock returns
            for mock_class in [MockGeneHasSymbol, MockGeneHasName, MockGeneHasLocation, MockGeneHasLocusType, MockGeneHasXref]:
                mock_instance = Mock()
                mock_instance.creation_date = mock_creation_date
                mock_class.return_value = mock_instance
            
            # Test repr methods
            gene_symbol = GeneSymbol(mock_session, "TEST", 1, 1, "approved", "public")
            assert isinstance(repr(gene_symbol), str)
            assert "GeneSymbol" in repr(gene_symbol)
            
            gene_name = GeneName(mock_session, "test", 1, 1, "approved", "public")
            assert isinstance(repr(gene_name), str)
            assert "GeneName" in repr(gene_name)
            
            gene_location = GeneLocation(mock_session, "1p36.33", 1, 1, "public")
            assert isinstance(repr(gene_location), str)
            assert "GeneLocation" in repr(gene_location)
            
            gene_locus_type = GeneLocusType(mock_session, "gene with protein product", 1, 1, "public")
            assert isinstance(repr(gene_locus_type), str)
            assert "GeneLocusType" in repr(gene_locus_type)
            
            gene_xref = GeneXref(mock_session, "NM_000001", 1, 1, 1, "RefSeq", "public")
            assert isinstance(repr(gene_xref), str)
            assert "GeneXref" in repr(gene_xref)

    def test_classes_handle_database_errors_consistently(self, mock_session):
        """Test that all classes handle database errors consistently"""
        # Mock a database connection error - only affects classes that use query
        mock_session.query.side_effect = Exception("Database connection error")
        
        with patch('insert.gene_symbol.Symbol'), \
             patch('insert.gene_symbol.GeneHasSymbol'), \
             patch('insert.gene_name.Name'), \
             patch('insert.gene_name.GeneHasName'), \
             patch('insert.gene_location.GeneHasLocation'), \
             patch('insert.gene_locus_type.GeneHasLocusType'), \
             patch('insert.gene_xref.Xref'), \
             patch('insert.gene_xref.GeneHasXref'):
            
            # GeneLocation, GeneLocusType, and GeneXref use query to find existing records
            with pytest.raises(Exception, match="Database connection error"):
                GeneLocation(mock_session, "1p36.33", 1, 1, "public")
            
            with pytest.raises(Exception, match="Database connection error"):
                GeneLocusType(mock_session, "gene with protein product", 1, 1, "public")
                
            with pytest.raises(Exception, match="Database connection error"):
                GeneXref(mock_session, "NM_000001", 1, 1, 1, "RefSeq", "public")
            
            # GeneSymbol and GeneName don't query during initialization
            # so they should succeed even with query errors
            try:
                GeneSymbol(mock_session, "TEST", 1, 1, "approved", "public")
                GeneName(mock_session, "test", 1, 1, "approved", "public")
            except Exception as e:
                pytest.fail(f"Classes without query dependencies should not fail: {e}")

    def test_parameter_validation_consistency(self):
        """Test that all classes have consistent parameter validation"""
        classes_and_params = [
            (GeneSymbol, ["session", "symbol", "gene_id", "creator_id", "type", "status"]),
            (GeneName, ["session", "name", "gene_id", "creator_id", "type", "status"]),
            (GeneLocation, ["session", "location_name", "gene_id", "creator_id", "status"]),
            (GeneLocusType, ["session", "locus_type_name", "gene_id", "creator_id", "status"]),
            (GeneXref, ["session", "display_id", "ext_res_id", "gene_id", "creator_id", "source", "status"])
        ]
        
        for cls, expected_params in classes_and_params:
            # Get the __init__ method signature
            import inspect
            sig = inspect.signature(cls.__init__)
            actual_params = list(sig.parameters.keys())
            
            # Remove 'self' parameter for comparison
            actual_params = [p for p in actual_params if p != 'self']
            
            # Check that all expected parameters are present
            for param in expected_params:
                assert param in actual_params, f"{cls.__name__} missing parameter: {param}"
