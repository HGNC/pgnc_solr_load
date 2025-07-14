"""
Unit tests for GeneLocusType class
"""
from datetime import datetime
from unittest.mock import Mock, patch

import pytest
from insert.gene_locus_type import GeneLocusType  # type: ignore


class TestGeneLocusType:
    """Test cases for GeneLocusType class"""
    
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
        one_mock = Mock()
        
        session.query.return_value = query_mock
        query_mock.where.return_value = where_mock
        where_mock.one.return_value = one_mock
        
        return session
    
    @pytest.fixture
    def mock_locus_type(self):
        """Create a mock LocusType instance"""
        locus_type = Mock()
        locus_type.id = 123
        locus_type.name = "gene with protein product"
        return locus_type
    
    @pytest.fixture
    def mock_gene_has_locus_type(self):
        """Create a mock GeneHasLocusType instance"""
        gene_has_locus_type = Mock()
        gene_has_locus_type.id = 456
        gene_has_locus_type.creation_date = datetime(2025, 7, 14, 12, 0, 0)
        return gene_has_locus_type
    
    @pytest.fixture
    def sample_data(self):
        """Sample data for testing"""
        return {
            "locus_type_name": "gene with protein product",
            "gene_id": 1001,
            "creator_id": 2001,
            "status": "public"
        }
    
    def test_init_creates_gene_locus_type_successfully(self, mock_session, mock_locus_type, mock_gene_has_locus_type, sample_data):
        """Test that GeneLocusType initialization creates objects correctly"""
        # Arrange
        mock_session.query().where().one.return_value = mock_locus_type
        
        with patch.object(GeneLocusType, '_create_gene_has_locus_type', return_value=mock_gene_has_locus_type) as mock_create_gene_has_locus_type:
            
            # Act
            gene_locus_type = GeneLocusType(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            mock_create_gene_has_locus_type.assert_called_once_with(
                mock_session, 
                sample_data["gene_id"], 
                mock_locus_type.id, 
                sample_data["creator_id"], 
                sample_data["status"]
            )
            
            # Verify instance attributes
            assert gene_locus_type.locus_type_id == mock_locus_type.id
            assert gene_locus_type.gene_id == sample_data["gene_id"]
            assert gene_locus_type.creator_id == sample_data["creator_id"]
            assert gene_locus_type.status == sample_data["status"]
            assert gene_locus_type.creation_date == mock_gene_has_locus_type.creation_date
    
    def test_locus_type_query_executed_correctly(self, mock_session, mock_locus_type, mock_gene_has_locus_type, sample_data):
        """Test that locus type query is executed with correct parameters"""
        # Arrange
        mock_session.query().where().one.return_value = mock_locus_type
        
        with patch.object(GeneLocusType, '_create_gene_has_locus_type', return_value=mock_gene_has_locus_type), \
             patch('insert.gene_locus_type.LocusType') as MockLocusType:
            
            # Act
            GeneLocusType(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            # Check that query was called with the LocusType model
            mock_session.query.assert_called_with(MockLocusType)
            # Verify the where clause was called (exact parameters are harder to test due to SQLAlchemy syntax)
            mock_session.query().where.assert_called()
            mock_session.query().where().one.assert_called_once()
    
    def test_create_gene_has_locus_type_adds_and_flushes_relationship(self, mock_session):
        """Test that _create_gene_has_locus_type creates GeneHasLocusType correctly"""
        # Arrange
        mock_gene_has_locus_type = Mock()
        mock_gene_has_locus_type.id = 999
        mock_session.refresh.side_effect = lambda obj: setattr(obj, 'id', 999)
        
        test_data = {
            "gene_id": 1001,
            "locus_type_id": 2001,
            "creator_id": 3001,
            "status": "private"
        }
        
        with patch('insert.gene_locus_type.GeneHasLocusType') as MockGeneHasLocusType:
            MockGeneHasLocusType.return_value = mock_gene_has_locus_type
            
            # Act
            gene_locus_type = GeneLocusType.__new__(GeneLocusType)  # Create instance without calling __init__
            result = gene_locus_type._create_gene_has_locus_type(
                mock_session,
                test_data["gene_id"],
                test_data["locus_type_id"],
                test_data["creator_id"],
                test_data["status"]
            )
            
            # Assert
            MockGeneHasLocusType.assert_called_once_with(
                gene_id=test_data["gene_id"],
                locus_type_id=test_data["locus_type_id"],
                creator_id=test_data["creator_id"],
                status=test_data["status"]
            )
            mock_session.add.assert_called_once_with(mock_gene_has_locus_type)
            mock_session.flush.assert_called_once()
            mock_session.refresh.assert_called_once_with(mock_gene_has_locus_type)
            assert result == mock_gene_has_locus_type
    
    def test_repr_returns_correct_string(self, mock_session, mock_locus_type, mock_gene_has_locus_type, sample_data):
        """Test that __repr__ returns the correct string representation"""
        # Arrange
        mock_session.query().where().one.return_value = mock_locus_type
        
        with patch.object(GeneLocusType, '_create_gene_has_locus_type', return_value=mock_gene_has_locus_type):
            
            gene_locus_type = GeneLocusType(
                session=mock_session,
                **sample_data
            )
            
            # Act
            repr_string = repr(gene_locus_type)
            
            # Assert
            expected = (
                f"<GeneLocusType(locus_type_id={mock_locus_type.id}, "
                f"gene_id={sample_data['gene_id']}, creator_id={sample_data['creator_id']}, "
                f"status='{sample_data['status']}', creation_date={mock_gene_has_locus_type.creation_date})>"
            )
            assert repr_string == expected
    
    @pytest.mark.parametrize("status_value", ["public", "private"])
    def test_valid_status_values(self, mock_session, mock_locus_type, mock_gene_has_locus_type, sample_data, status_value):
        """Test that all valid status values work correctly"""
        # Arrange
        sample_data["status"] = status_value
        mock_session.query().where().one.return_value = mock_locus_type
        
        with patch.object(GeneLocusType, '_create_gene_has_locus_type', return_value=mock_gene_has_locus_type):
            
            # Act
            gene_locus_type = GeneLocusType(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            assert gene_locus_type.status == status_value
    
    def test_locus_type_not_found_raises_exception(self, mock_session, sample_data):
        """Test that missing locus type raises appropriate exception"""
        # Arrange
        from sqlalchemy.exc import NoResultFound
        mock_session.query().where().one.side_effect = NoResultFound("No locus type found")
        
        # Act & Assert
        with pytest.raises(NoResultFound):
            GeneLocusType(
                session=mock_session,
                **sample_data
            )
    
    def test_session_operations_called_in_order(self, mock_session, mock_locus_type, sample_data):
        """Test that session operations are called in the correct order"""
        # Arrange
        call_order = []
        mock_session.query().where().one.return_value = mock_locus_type
        
        def track_add(obj):
            call_order.append(f"add_{type(obj).__name__}")
        
        def track_flush():
            call_order.append("flush")
        
        def track_refresh(obj):
            call_order.append(f"refresh_{type(obj).__name__}")
        
        mock_session.add.side_effect = track_add
        mock_session.flush.side_effect = track_flush
        mock_session.refresh.side_effect = track_refresh
        
        with patch('insert.gene_locus_type.GeneHasLocusType') as MockGeneHasLocusType:
            MockGeneHasLocusType.return_value = Mock()
            
            # Act
            GeneLocusType(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            expected_order = [
                "add_Mock",  # GeneHasLocusType
                "flush", 
                "refresh_Mock"
            ]
            assert call_order == expected_order
    
    def test_attribute_assignment_integrity(self, mock_session, mock_locus_type, mock_gene_has_locus_type, sample_data):
        """Test that all attributes are correctly assigned from constructor parameters"""
        # Arrange
        mock_session.query().where().one.return_value = mock_locus_type
        
        with patch.object(GeneLocusType, '_create_gene_has_locus_type', return_value=mock_gene_has_locus_type):
            
            # Act
            gene_locus_type = GeneLocusType(
                session=mock_session,
                **sample_data
            )
            
            # Assert - All constructor parameters should be stored as instance attributes
            assert hasattr(gene_locus_type, 'locus_type_id')
            assert hasattr(gene_locus_type, 'gene_id')
            assert hasattr(gene_locus_type, 'creator_id')
            assert hasattr(gene_locus_type, 'status')
            assert hasattr(gene_locus_type, 'creation_date')
            
            # Verify values match constructor parameters
            assert gene_locus_type.gene_id == sample_data["gene_id"]
            assert gene_locus_type.creator_id == sample_data["creator_id"]
            assert gene_locus_type.status == sample_data["status"]
            assert gene_locus_type.locus_type_id == mock_locus_type.id
    
    @pytest.mark.parametrize("locus_type_name", [
        "gene with protein product",
        "pseudogene", 
        "RNA gene",
        "immunoglobulin gene",
        "T cell receptor gene",
        "endogenous retrovirus",
        "complex locus constituent",
        "other"
    ])
    def test_various_locus_type_names(self, mock_session, mock_locus_type, mock_gene_has_locus_type, sample_data, locus_type_name):
        """Test behavior with various locus type names"""
        # Arrange
        sample_data["locus_type_name"] = locus_type_name
        mock_session.query().where().one.return_value = mock_locus_type
        
        with patch.object(GeneLocusType, '_create_gene_has_locus_type', return_value=mock_gene_has_locus_type):
            
            # Act
            gene_locus_type = GeneLocusType(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            assert gene_locus_type is not None
    
    def test_database_exception_handling(self, mock_session, mock_locus_type, sample_data):
        """Test behavior when database operations raise exceptions"""
        # Arrange
        mock_session.query().where().one.return_value = mock_locus_type
        mock_session.flush.side_effect = Exception("Database error")
        
        with patch('insert.gene_locus_type.GeneHasLocusType') as MockGeneHasLocusType:
            MockGeneHasLocusType.return_value = Mock()
            
            # Act & Assert
            with pytest.raises(Exception, match="Database error"):
                GeneLocusType(
                    session=mock_session,
                    **sample_data
                )
    
    def test_large_integer_ids(self, mock_session, mock_locus_type, mock_gene_has_locus_type, sample_data):
        """Test behavior with large integer IDs"""
        # Arrange
        large_id = 9223372036854775807  # Max value for 64-bit signed integer
        sample_data["gene_id"] = large_id
        sample_data["creator_id"] = large_id
        mock_locus_type.id = large_id
        mock_session.query().where().one.return_value = mock_locus_type
        
        with patch.object(GeneLocusType, '_create_gene_has_locus_type', return_value=mock_gene_has_locus_type):
            
            # Act
            gene_locus_type = GeneLocusType(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            assert gene_locus_type.gene_id == large_id
            assert gene_locus_type.creator_id == large_id
            assert gene_locus_type.locus_type_id == large_id
