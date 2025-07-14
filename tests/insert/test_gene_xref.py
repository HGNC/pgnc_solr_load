"""
Unit tests for GeneXref class
"""
from datetime import datetime
from unittest.mock import Mock, patch

import pytest
from insert.gene_xref import GeneXref  # type: ignore


class TestGeneXref:
    """Test cases for GeneXref class"""
    
    @pytest.fixture
    def mock_session(self):
        """Create a mock database session"""
        session = Mock()
        session.add = Mock()
        session.flush = Mock()
        session.refresh = Mock()
        
        # Mock query chain
        query_mock = Mock()
        where_mock = Mock()
        one_or_none_mock = Mock()
        
        session.query.return_value = query_mock
        query_mock.where.return_value = where_mock
        where_mock.one_or_none.return_value = one_or_none_mock
        
        return session
    
    @pytest.fixture
    def mock_xref(self):
        """Create a mock Xref instance"""
        xref = Mock()
        xref.id = 123
        xref.display_id = "NM_000001"
        xref.ext_resource_id = 1
        return xref
    
    @pytest.fixture
    def mock_gene_has_xref(self):
        """Create a mock GeneHasXref instance"""
        gene_has_xref = Mock()
        gene_has_xref.id = 456
        gene_has_xref.creation_date = datetime(2025, 7, 14, 12, 0, 0)
        return gene_has_xref
    
    @pytest.fixture
    def sample_data(self):
        """Sample data for testing"""
        return {
            "display_id": "NM_000001",
            "ext_res_id": 1,
            "gene_id": 1001,
            "creator_id": 2001,
            "source": "RefSeq",
            "status": "public"
        }
    
    @pytest.fixture
    def sample_data_hgnc(self):
        """Sample data for testing with HGNC (allows existing xref)"""
        return {
            "display_id": "HGNC:123",
            "ext_res_id": 4,  # HGNC ext_resource_id
            "gene_id": 1001,
            "creator_id": 2001,
            "source": "HGNC",
            "status": "public"
        }
    
    def test_init_creates_gene_xref_with_existing_xref(self, mock_session, mock_xref, mock_gene_has_xref, sample_data_hgnc):
        """Test that GeneXref initialization works with existing HGNC xref"""
        # Arrange
        mock_session.query().where().one_or_none.return_value = mock_xref
        
        with patch.object(GeneXref, '_create_gene_has_xref', return_value=mock_gene_has_xref) as mock_create_gene_has_xref:
            
            # Act
            gene_xref = GeneXref(
                session=mock_session,
                **sample_data_hgnc
            )
            
            # Assert
            mock_create_gene_has_xref.assert_called_once_with(
                mock_session, 
                sample_data_hgnc["gene_id"], 
                mock_xref.id, 
                sample_data_hgnc["creator_id"], 
                sample_data_hgnc["source"],
                sample_data_hgnc["status"]
            )
            
            # Verify instance attributes
            assert gene_xref.xref_id == mock_xref.id
            assert gene_xref.gene_id == sample_data_hgnc["gene_id"]
            assert gene_xref.creator_id == sample_data_hgnc["creator_id"]
            assert gene_xref.source == sample_data_hgnc["source"]
            assert gene_xref.status == sample_data_hgnc["status"]
            assert gene_xref.creation_date == mock_gene_has_xref.creation_date
    
    def test_init_creates_gene_xref_with_new_xref(self, mock_session, mock_xref, mock_gene_has_xref, sample_data):
        """Test that GeneXref initialization creates new xref when none exists"""
        # Arrange
        mock_session.query().where().one_or_none.return_value = None
        
        with patch.object(GeneXref, '_create_xref', return_value=mock_xref) as mock_create_xref, \
             patch.object(GeneXref, '_create_gene_has_xref', return_value=mock_gene_has_xref) as mock_create_gene_has_xref:
            
            # Act
            gene_xref = GeneXref(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            mock_create_xref.assert_called_once_with(
                mock_session, 
                sample_data["display_id"], 
                sample_data["ext_res_id"]
            )
            mock_create_gene_has_xref.assert_called_once_with(
                mock_session, 
                sample_data["gene_id"], 
                mock_xref.id, 
                sample_data["creator_id"], 
                sample_data["source"],
                sample_data["status"]
            )
            
            # Verify instance attributes
            assert gene_xref.xref_id == mock_xref.id
    
    def test_init_raises_error_for_existing_non_hgnc_xref(self, mock_session, mock_xref, sample_data):
        """Test that GeneXref raises error when trying to create duplicate non-HGNC xref"""
        # Arrange
        sample_data["ext_res_id"] = 1  # Not HGNC (which is 4)
        mock_session.query().where().one_or_none.return_value = mock_xref
        
        # Act & Assert
        with pytest.raises(ValueError, match="already exists"):
            GeneXref(
                session=mock_session,
                **sample_data
            )
    
    def test_init_allows_existing_hgnc_xref(self, mock_session, mock_xref, mock_gene_has_xref, sample_data):
        """Test that GeneXref allows existing HGNC xref (ext_res_id=4)"""
        # Arrange
        sample_data["ext_res_id"] = 4  # HGNC
        mock_session.query().where().one_or_none.return_value = mock_xref
        
        with patch.object(GeneXref, '_create_gene_has_xref', return_value=mock_gene_has_xref):
            
            # Act - Should not raise an exception
            gene_xref = GeneXref(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            assert gene_xref.xref_id == mock_xref.id
    
    def test_create_xref_adds_and_flushes_xref(self, mock_session, sample_data):
        """Test that _create_xref creates Xref correctly"""
        # Arrange
        mock_xref = Mock()
        mock_xref.id = 789
        mock_session.refresh.side_effect = lambda obj: setattr(obj, 'id', 789)
        
        with patch('insert.gene_xref.Xref') as MockXref:
            MockXref.return_value = mock_xref
            
            # Act
            gene_xref = GeneXref.__new__(GeneXref)  # Create instance without calling __init__
            result = gene_xref._create_xref(
                mock_session, 
                sample_data["display_id"], 
                sample_data["ext_res_id"]
            )
            
            # Assert
            MockXref.assert_called_once_with(
                display_id=sample_data["display_id"],
                ext_resource_id=sample_data["ext_res_id"]
            )
            mock_session.add.assert_called_once_with(mock_xref)
            mock_session.flush.assert_called_once()
            mock_session.refresh.assert_called_once_with(mock_xref)
            assert result == mock_xref
    
    def test_create_gene_has_xref_adds_and_flushes_relationship(self, mock_session):
        """Test that _create_gene_has_xref creates GeneHasXref correctly"""
        # Arrange
        mock_gene_has_xref = Mock()
        mock_gene_has_xref.id = 999
        mock_session.refresh.side_effect = lambda obj: setattr(obj, 'id', 999)
        
        test_data = {
            "gene_id": 1001,
            "xref_id": 2001,
            "creator_id": 3001,
            "source": "RefSeq",
            "status": "private"
        }
        
        with patch('insert.gene_xref.GeneHasXref') as MockGeneHasXref:
            MockGeneHasXref.return_value = mock_gene_has_xref
            
            # Act
            gene_xref = GeneXref.__new__(GeneXref)  # Create instance without calling __init__
            result = gene_xref._create_gene_has_xref(
                mock_session,
                test_data["gene_id"],
                test_data["xref_id"],
                test_data["creator_id"],
                test_data["source"],
                test_data["status"]
            )
            
            # Assert
            MockGeneHasXref.assert_called_once_with(
                gene_id=test_data["gene_id"],
                xref_id=test_data["xref_id"],
                creator_id=test_data["creator_id"],
                source=test_data["source"],
                status=test_data["status"]
            )
            mock_session.add.assert_called_once_with(mock_gene_has_xref)
            mock_session.flush.assert_called_once()
            mock_session.refresh.assert_called_once_with(mock_gene_has_xref)
            assert result == mock_gene_has_xref
    
    def test_repr_returns_correct_string(self, mock_session, mock_xref, mock_gene_has_xref, sample_data):
        """Test that __repr__ returns the correct string representation"""
        # Arrange - No existing xref found
        mock_session.query().where().one_or_none.return_value = None
        
        with patch.object(GeneXref, '_create_xref', return_value=mock_xref), \
             patch.object(GeneXref, '_create_gene_has_xref', return_value=mock_gene_has_xref):
            
            gene_xref = GeneXref(
                session=mock_session,
                **sample_data
            )
            
            # Act
            repr_string = repr(gene_xref)
            
            # Assert
            expected = (
                f"<GeneXref(xref_id={mock_xref.id}, "
                f"gene_id={sample_data['gene_id']}, creator_id={sample_data['creator_id']}, "
                f"source='{sample_data['source']}', status='{sample_data['status']}', "
                f"creation_date={mock_gene_has_xref.creation_date})>"
            )
            assert repr_string == expected
    
    @pytest.mark.parametrize("status_value", ["public", "private"])
    def test_valid_status_values(self, mock_session, mock_xref, mock_gene_has_xref, sample_data, status_value):
        """Test that all valid status values work correctly"""
        # Arrange
        sample_data["status"] = status_value
        mock_session.query().where().one_or_none.return_value = None  # No existing xref
        
        with patch.object(GeneXref, '_create_xref', return_value=mock_xref), \
             patch.object(GeneXref, '_create_gene_has_xref', return_value=mock_gene_has_xref):
            
            # Act
            gene_xref = GeneXref(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            assert gene_xref.status == status_value
    
    def test_xref_query_executed_correctly(self, mock_session, mock_xref, mock_gene_has_xref, sample_data):
        """Test that xref query is executed with correct parameters"""
        # Arrange
        mock_session.query().where().one_or_none.return_value = None  # No existing xref
        
        with patch.object(GeneXref, '_create_xref', return_value=mock_xref), \
             patch.object(GeneXref, '_create_gene_has_xref', return_value=mock_gene_has_xref), \
             patch('insert.gene_xref.Xref') as MockXref:
            
            # Act
            GeneXref(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            # Check that query was called with the Xref model
            mock_session.query.assert_called_with(MockXref)
            # Verify the where clause was called (exact parameters are harder to test due to SQLAlchemy syntax)
            mock_session.query().where.assert_called()
            mock_session.query().where().one_or_none.assert_called_once()
    
    def test_session_operations_called_in_order_new_xref(self, mock_session, sample_data):
        """Test that session operations are called in the correct order when creating new xref"""
        # Arrange
        call_order = []
        mock_session.query().where().one_or_none.return_value = None  # No existing xref
        
        def track_add(obj):
            call_order.append(f"add_{type(obj).__name__}")
        
        def track_flush():
            call_order.append("flush")
        
        def track_refresh(obj):
            call_order.append(f"refresh_{type(obj).__name__}")
        
        mock_session.add.side_effect = track_add
        mock_session.flush.side_effect = track_flush
        mock_session.refresh.side_effect = track_refresh
        
        with patch('insert.gene_xref.Xref') as MockXref, \
             patch('insert.gene_xref.GeneHasXref') as MockGeneHasXref:
            
            MockXref.return_value = Mock()
            MockGeneHasXref.return_value = Mock()
            
            # Act
            GeneXref(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            expected_order = [
                "add_Mock",  # Xref
                "flush",
                "refresh_Mock",
                "add_Mock",  # GeneHasXref
                "flush", 
                "refresh_Mock"
            ]
            assert call_order == expected_order
    
    @pytest.mark.parametrize("source", [
        "RefSeq",
        "Ensembl",
        "UCSC",
        "NCBI",
        "UniProt",
        "HGNC"
    ])
    def test_various_source_values(self, mock_session, mock_xref, mock_gene_has_xref, sample_data, source):
        """Test behavior with various source values"""
        # Arrange
        sample_data["source"] = source
        mock_session.query().where().one_or_none.return_value = None  # No existing xref
        
        with patch.object(GeneXref, '_create_xref', return_value=mock_xref), \
             patch.object(GeneXref, '_create_gene_has_xref', return_value=mock_gene_has_xref):
            
            # Act
            gene_xref = GeneXref(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            assert gene_xref.source == source
    
    @pytest.mark.parametrize("display_id", [
        "NM_000001",
        "ENSG00000000001",
        "uc001abc.1",
        "12345",
        "P12345"
    ])
    def test_various_display_id_formats(self, mock_session, mock_xref, mock_gene_has_xref, sample_data, display_id):
        """Test behavior with various display ID formats"""
        # Arrange
        sample_data["display_id"] = display_id
        mock_session.query().where().one_or_none.return_value = None  # Force creation of new xref
        
        with patch.object(GeneXref, '_create_xref', return_value=mock_xref), \
             patch.object(GeneXref, '_create_gene_has_xref', return_value=mock_gene_has_xref):
            
            # Act
            gene_xref = GeneXref(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            assert gene_xref is not None
    
    def test_database_exception_handling(self, mock_session, sample_data):
        """Test behavior when database operations raise exceptions"""
        # Arrange
        mock_session.query().where().one_or_none.return_value = None
        mock_session.flush.side_effect = Exception("Database error")
        
        with patch('insert.gene_xref.Xref') as MockXref:
            MockXref.return_value = Mock()
            
            # Act & Assert
            with pytest.raises(Exception, match="Database error"):
                GeneXref(
                    session=mock_session,
                    **sample_data
                )
    
    def test_large_integer_ids(self, mock_session, mock_xref, mock_gene_has_xref, sample_data):
        """Test behavior with large integer IDs"""
        # Arrange
        large_id = 9223372036854775807  # Max value for 64-bit signed integer
        sample_data["gene_id"] = large_id
        sample_data["creator_id"] = large_id
        sample_data["ext_res_id"] = large_id
        mock_xref.id = large_id
        mock_session.query().where().one_or_none.return_value = None  # No existing xref
        
        with patch.object(GeneXref, '_create_xref', return_value=mock_xref), \
             patch.object(GeneXref, '_create_gene_has_xref', return_value=mock_gene_has_xref):
            
            # Act
            gene_xref = GeneXref(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            assert gene_xref.gene_id == large_id
            assert gene_xref.creator_id == large_id
            assert gene_xref.xref_id == large_id
