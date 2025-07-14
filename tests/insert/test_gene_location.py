"""
Unit tests for GeneLocation class
"""
from datetime import datetime
from unittest.mock import Mock, patch

import pytest
from insert.gene_location import GeneLocation  # type: ignore


class TestGeneLocation:
    """Test cases for GeneLocation class"""
    
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
    def mock_location(self):
        """Create a mock Location instance"""
        location = Mock()
        location.id = 123
        location.name = "1p36.33"
        return location
    
    @pytest.fixture
    def mock_gene_has_location(self):
        """Create a mock GeneHasLocation instance"""
        gene_has_location = Mock()
        gene_has_location.id = 456
        gene_has_location.creation_date = datetime(2025, 7, 14, 12, 0, 0)
        return gene_has_location
    
    @pytest.fixture
    def sample_data(self):
        """Sample data for testing"""
        return {
            "location_name": "1p36.33",
            "gene_id": 1001,
            "creator_id": 2001,
            "status": "public"
        }
    
    def test_init_creates_gene_location_successfully(self, mock_session, mock_location, mock_gene_has_location, sample_data):
        """Test that GeneLocation initialization creates objects correctly"""
        # Arrange
        mock_session.query().where().one.return_value = mock_location
        
        with patch.object(GeneLocation, '_create_gene_has_location', return_value=mock_gene_has_location) as mock_create_gene_has_location:
            
            # Act
            gene_location = GeneLocation(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            mock_create_gene_has_location.assert_called_once_with(
                mock_session, 
                sample_data["gene_id"], 
                mock_location.id, 
                sample_data["creator_id"], 
                sample_data["status"]
            )
            
            # Verify instance attributes
            assert gene_location.location_id == mock_location.id
            assert gene_location.gene_id == sample_data["gene_id"]
            assert gene_location.creator_id == sample_data["creator_id"]
            assert gene_location.status == sample_data["status"]
            assert gene_location.creation_date == mock_gene_has_location.creation_date
    
    def test_location_query_executed_correctly(self, mock_session, mock_location, mock_gene_has_location, sample_data):
        """Test that location query is executed with correct parameters"""
        # Arrange
        mock_session.query().where().one.return_value = mock_location
        
        with patch.object(GeneLocation, '_create_gene_has_location', return_value=mock_gene_has_location), \
             patch('insert.gene_location.Location') as MockLocation:
            
            # Act
            GeneLocation(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            # Check that query was called with the Location model
            mock_session.query.assert_called_with(MockLocation)
            # Verify the where clause was called (exact parameters are harder to test due to SQLAlchemy syntax)
            mock_session.query().where.assert_called()
            mock_session.query().where().one.assert_called_once()
    
    def test_create_gene_has_location_adds_and_flushes_relationship(self, mock_session):
        """Test that _create_gene_has_location creates GeneHasLocation correctly"""
        # Arrange
        mock_gene_has_location = Mock()
        mock_gene_has_location.id = 999
        mock_session.refresh.side_effect = lambda obj: setattr(obj, 'id', 999)
        
        test_data = {
            "gene_id": 1001,
            "location_id": 2001,
            "creator_id": 3001,
            "status": "private"
        }
        
        with patch('insert.gene_location.GeneHasLocation') as MockGeneHasLocation:
            MockGeneHasLocation.return_value = mock_gene_has_location
            
            # Act
            gene_location = GeneLocation.__new__(GeneLocation)  # Create instance without calling __init__
            result = gene_location._create_gene_has_location(
                mock_session,
                test_data["gene_id"],
                test_data["location_id"],
                test_data["creator_id"],
                test_data["status"]
            )
            
            # Assert
            MockGeneHasLocation.assert_called_once_with(
                gene_id=test_data["gene_id"],
                location_id=test_data["location_id"],
                creator_id=test_data["creator_id"],
                status=test_data["status"]
            )
            mock_session.add.assert_called_once_with(mock_gene_has_location)
            mock_session.flush.assert_called_once()
            mock_session.refresh.assert_called_once_with(mock_gene_has_location)
            assert result == mock_gene_has_location
    
    def test_repr_returns_correct_string(self, mock_session, mock_location, mock_gene_has_location, sample_data):
        """Test that __repr__ returns the correct string representation"""
        # Arrange
        mock_session.query().where().one.return_value = mock_location
        
        with patch.object(GeneLocation, '_create_gene_has_location', return_value=mock_gene_has_location):
            
            gene_location = GeneLocation(
                session=mock_session,
                **sample_data
            )
            
            # Act
            repr_string = repr(gene_location)
            
            # Assert
            expected = (
                f"<GeneLocation(location_id={mock_location.id}, "
                f"gene_id={sample_data['gene_id']}, creator_id={sample_data['creator_id']}, "
                f"status='{sample_data['status']}', creation_date={mock_gene_has_location.creation_date})>"
            )
            assert repr_string == expected
    
    @pytest.mark.parametrize("status_value", ["public", "private"])
    def test_valid_status_values(self, mock_session, mock_location, mock_gene_has_location, sample_data, status_value):
        """Test that all valid status values work correctly"""
        # Arrange
        sample_data["status"] = status_value
        mock_session.query().where().one.return_value = mock_location
        
        with patch.object(GeneLocation, '_create_gene_has_location', return_value=mock_gene_has_location):
            
            # Act
            gene_location = GeneLocation(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            assert gene_location.status == status_value
    
    def test_location_not_found_raises_exception(self, mock_session, sample_data):
        """Test that missing location raises appropriate exception"""
        # Arrange
        from sqlalchemy.exc import NoResultFound
        mock_session.query().where().one.side_effect = NoResultFound("No location found")
        
        # Act & Assert
        with pytest.raises(NoResultFound):
            GeneLocation(
                session=mock_session,
                **sample_data
            )
    
    def test_session_operations_called_in_order(self, mock_session, mock_location, sample_data):
        """Test that session operations are called in the correct order"""
        # Arrange
        call_order = []
        mock_session.query().where().one.return_value = mock_location
        
        def track_add(obj):
            call_order.append(f"add_{type(obj).__name__}")
        
        def track_flush():
            call_order.append("flush")
        
        def track_refresh(obj):
            call_order.append(f"refresh_{type(obj).__name__}")
        
        mock_session.add.side_effect = track_add
        mock_session.flush.side_effect = track_flush
        mock_session.refresh.side_effect = track_refresh
        
        with patch('insert.gene_location.GeneHasLocation') as MockGeneHasLocation:
            MockGeneHasLocation.return_value = Mock()
            
            # Act
            GeneLocation(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            expected_order = [
                "add_Mock",  # GeneHasLocation
                "flush", 
                "refresh_Mock"
            ]
            assert call_order == expected_order
    
    def test_attribute_assignment_integrity(self, mock_session, mock_location, mock_gene_has_location, sample_data):
        """Test that all attributes are correctly assigned from constructor parameters"""
        # Arrange
        mock_session.query().where().one.return_value = mock_location
        
        with patch.object(GeneLocation, '_create_gene_has_location', return_value=mock_gene_has_location):
            
            # Act
            gene_location = GeneLocation(
                session=mock_session,
                **sample_data
            )
            
            # Assert - All constructor parameters should be stored as instance attributes
            assert hasattr(gene_location, 'location_id')
            assert hasattr(gene_location, 'gene_id')
            assert hasattr(gene_location, 'creator_id')
            assert hasattr(gene_location, 'status')
            assert hasattr(gene_location, 'creation_date')
            
            # Verify values match constructor parameters
            assert gene_location.gene_id == sample_data["gene_id"]
            assert gene_location.creator_id == sample_data["creator_id"]
            assert gene_location.status == sample_data["status"]
            assert gene_location.location_id == mock_location.id
    
    def test_database_exception_handling(self, mock_session, mock_location, sample_data):
        """Test behavior when database operations raise exceptions"""
        # Arrange
        mock_session.query().where().one.return_value = mock_location
        mock_session.flush.side_effect = Exception("Database error")
        
        with patch('insert.gene_location.GeneHasLocation') as MockGeneHasLocation:
            MockGeneHasLocation.return_value = Mock()
            
            # Act & Assert
            with pytest.raises(Exception, match="Database error"):
                GeneLocation(
                    session=mock_session,
                    **sample_data
                )
    
    @pytest.mark.parametrize("location_name", [
        "1p36.33", 
        "Xq28", 
        "22q11.2", 
        "mitochondrion",
        "unplaced"
    ])
    def test_various_location_names(self, mock_session, mock_location, mock_gene_has_location, sample_data, location_name):
        """Test behavior with various chromosome location formats"""
        # Arrange
        sample_data["location_name"] = location_name
        mock_session.query().where().one.return_value = mock_location
        
        with patch.object(GeneLocation, '_create_gene_has_location', return_value=mock_gene_has_location):
            
            # Act
            gene_location = GeneLocation(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            assert gene_location is not None
    
    def test_large_integer_ids(self, mock_session, mock_location, mock_gene_has_location, sample_data):
        """Test behavior with large integer IDs"""
        # Arrange
        large_id = 9223372036854775807  # Max value for 64-bit signed integer
        sample_data["gene_id"] = large_id
        sample_data["creator_id"] = large_id
        mock_location.id = large_id
        mock_session.query().where().one.return_value = mock_location
        
        with patch.object(GeneLocation, '_create_gene_has_location', return_value=mock_gene_has_location):
            
            # Act
            gene_location = GeneLocation(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            assert gene_location.gene_id == large_id
            assert gene_location.creator_id == large_id
            assert gene_location.location_id == large_id
