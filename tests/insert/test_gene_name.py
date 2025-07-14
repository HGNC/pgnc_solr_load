"""
Unit tests for GeneName class
"""
from datetime import datetime
from unittest.mock import Mock, patch

import pytest
from insert.gene_name import GeneName  # type: ignore


class TestGeneName:
    """Test cases for GeneName class"""
    
    @pytest.fixture
    def mock_session(self):
        """Create a mock database session"""
        session = Mock()
        session.add = Mock()
        session.flush = Mock()
        session.refresh = Mock()
        return session
    
    @pytest.fixture
    def mock_name(self):
        """Create a mock Name instance"""
        name = Mock()
        name.id = 123
        name.name = "TEST_NAME"
        return name
    
    @pytest.fixture
    def mock_gene_has_name(self):
        """Create a mock GeneHasName instance"""
        gene_has_name = Mock()
        gene_has_name.id = 456
        gene_has_name.creation_date = datetime(2025, 7, 14, 12, 0, 0)
        return gene_has_name
    
    @pytest.fixture
    def sample_data(self):
        """Sample data for testing"""
        return {
            "name": "breast cancer 1",
            "gene_id": 1001,
            "creator_id": 2001,
            "type": "approved",
            "status": "public"
        }
    
    def test_init_creates_gene_name_successfully(self, mock_session, mock_name, mock_gene_has_name, sample_data):
        """Test that GeneName initialization creates objects correctly"""
        # Arrange
        with patch.object(GeneName, '_create_name', return_value=mock_name) as mock_create_name, \
             patch.object(GeneName, '_create_gene_has_name', return_value=mock_gene_has_name) as mock_create_gene_has_name:
            
            # Act
            gene_name = GeneName(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            mock_create_name.assert_called_once_with(mock_session, sample_data["name"])
            mock_create_gene_has_name.assert_called_once_with(
                mock_session, 
                sample_data["gene_id"], 
                mock_name.id, 
                sample_data["type"], 
                sample_data["creator_id"], 
                sample_data["status"]
            )
            
            # Verify instance attributes
            assert gene_name.name_id == mock_name.id
            assert gene_name.gene_id == sample_data["gene_id"]
            assert gene_name.creator_id == sample_data["creator_id"]
            assert gene_name.type == sample_data["type"]
            assert gene_name.status == sample_data["status"]
            assert gene_name.creation_date == mock_gene_has_name.creation_date
    
    def test_create_name_adds_and_flushes_name(self, mock_session, sample_data):
        """Test that _create_name creates Name correctly"""
        # Arrange
        mock_name = Mock()
        mock_name.id = 789
        mock_session.refresh.side_effect = lambda obj: setattr(obj, 'id', 789)
        
        with patch('insert.gene_name.Name') as MockName:
            MockName.return_value = mock_name
            
            # Act
            gene_name = GeneName.__new__(GeneName)  # Create instance without calling __init__
            result = gene_name._create_name(mock_session, sample_data["name"])
            
            # Assert
            MockName.assert_called_once_with(name=sample_data["name"])
            mock_session.add.assert_called_once_with(mock_name)
            mock_session.flush.assert_called_once()
            mock_session.refresh.assert_called_once_with(mock_name)
            assert result == mock_name
    
    def test_create_gene_has_name_adds_and_flushes_relationship(self, mock_session):
        """Test that _create_gene_has_name creates GeneHasName correctly"""
        # Arrange
        mock_gene_has_name = Mock()
        mock_gene_has_name.id = 999
        mock_session.refresh.side_effect = lambda obj: setattr(obj, 'id', 999)
        
        test_data = {
            "gene_id": 1001,
            "name_id": 2001,
            "type": "alias",
            "creator_id": 3001,
            "status": "private"
        }
        
        with patch('insert.gene_name.GeneHasName') as MockGeneHasName:
            MockGeneHasName.return_value = mock_gene_has_name
            
            # Act
            gene_name = GeneName.__new__(GeneName)  # Create instance without calling __init__
            result = gene_name._create_gene_has_name(
                mock_session,
                test_data["gene_id"],
                test_data["name_id"],
                test_data["type"],
                test_data["creator_id"],
                test_data["status"]
            )
            
            # Assert
            MockGeneHasName.assert_called_once_with(
                gene_id=test_data["gene_id"],
                name_id=test_data["name_id"],
                type=test_data["type"],
                creator_id=test_data["creator_id"],
                status=test_data["status"]
            )
            mock_session.add.assert_called_once_with(mock_gene_has_name)
            mock_session.flush.assert_called_once()
            mock_session.refresh.assert_called_once_with(mock_gene_has_name)
            assert result == mock_gene_has_name
    
    def test_repr_returns_correct_string(self, mock_session, mock_name, mock_gene_has_name, sample_data):
        """Test that __repr__ returns the correct string representation"""
        # Arrange
        with patch.object(GeneName, '_create_name', return_value=mock_name), \
             patch.object(GeneName, '_create_gene_has_name', return_value=mock_gene_has_name):
            
            gene_name = GeneName(
                session=mock_session,
                **sample_data
            )
            
            # Act
            repr_string = repr(gene_name)
            
            # Assert
            expected = (
                f"<GeneName(name_id={mock_name.id}, "
                f"gene_id={sample_data['gene_id']}, creator_id={sample_data['creator_id']}, "
                f"type='{sample_data['type']}', status='{sample_data['status']}', "
                f"creation_date={mock_gene_has_name.creation_date})>"
            )
            assert repr_string == expected
    
    @pytest.mark.parametrize("type_value", ["approved", "alias", "previous"])
    def test_valid_type_values(self, mock_session, mock_name, mock_gene_has_name, sample_data, type_value):
        """Test that all valid type values work correctly"""
        # Arrange
        sample_data["type"] = type_value
        
        with patch.object(GeneName, '_create_name', return_value=mock_name), \
             patch.object(GeneName, '_create_gene_has_name', return_value=mock_gene_has_name):
            
            # Act
            gene_name = GeneName(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            assert gene_name.type == type_value
    
    @pytest.mark.parametrize("status_value", ["public", "private"])
    def test_valid_status_values(self, mock_session, mock_name, mock_gene_has_name, sample_data, status_value):
        """Test that all valid status values work correctly"""
        # Arrange
        sample_data["status"] = status_value
        
        with patch.object(GeneName, '_create_name', return_value=mock_name), \
             patch.object(GeneName, '_create_gene_has_name', return_value=mock_gene_has_name):
            
            # Act
            gene_name = GeneName(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            assert gene_name.status == status_value
    
    def test_session_operations_called_in_order(self, mock_session, sample_data):
        """Test that session operations are called in the correct order"""
        # Arrange
        call_order = []
        
        def track_add(obj):
            call_order.append(f"add_{type(obj).__name__}")
        
        def track_flush():
            call_order.append("flush")
        
        def track_refresh(obj):
            call_order.append(f"refresh_{type(obj).__name__}")
        
        mock_session.add.side_effect = track_add
        mock_session.flush.side_effect = track_flush
        mock_session.refresh.side_effect = track_refresh
        
        with patch('insert.gene_name.Name') as MockName, \
             patch('insert.gene_name.GeneHasName') as MockGeneHasName:
            
            MockName.return_value = Mock()
            MockGeneHasName.return_value = Mock()
            
            # Act
            GeneName(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            expected_order = [
                "add_Mock",  # Name
                "flush",
                "refresh_Mock",
                "add_Mock",  # GeneHasName
                "flush", 
                "refresh_Mock"
            ]
            assert call_order == expected_order
    
    def test_attribute_assignment_integrity(self, mock_session, mock_name, mock_gene_has_name, sample_data):
        """Test that all attributes are correctly assigned from constructor parameters"""
        # Arrange
        with patch.object(GeneName, '_create_name', return_value=mock_name), \
             patch.object(GeneName, '_create_gene_has_name', return_value=mock_gene_has_name):
            
            # Act
            gene_name = GeneName(
                session=mock_session,
                **sample_data
            )
            
            # Assert - All constructor parameters should be stored as instance attributes
            assert hasattr(gene_name, 'name_id')
            assert hasattr(gene_name, 'gene_id')
            assert hasattr(gene_name, 'creator_id')
            assert hasattr(gene_name, 'type')
            assert hasattr(gene_name, 'status')
            assert hasattr(gene_name, 'creation_date')
            
            # Verify values match constructor parameters
            assert gene_name.gene_id == sample_data["gene_id"]
            assert gene_name.creator_id == sample_data["creator_id"]
            assert gene_name.type == sample_data["type"]
            assert gene_name.status == sample_data["status"]
    
    def test_database_exception_handling(self, mock_session, sample_data):
        """Test behavior when database operations raise exceptions"""
        # Arrange
        mock_session.flush.side_effect = Exception("Database error")
        
        with patch('insert.gene_name.Name') as MockName:
            MockName.return_value = Mock()
            
            # Act & Assert
            with pytest.raises(Exception, match="Database error"):
                GeneName(
                    session=mock_session,
                    **sample_data
                )
    
    def test_long_name_string(self, mock_session, mock_name, mock_gene_has_name, sample_data):
        """Test behavior with long name strings"""
        # Arrange
        long_name = "a" * 1000  # Very long name
        sample_data["name"] = long_name
        
        with patch.object(GeneName, '_create_name', return_value=mock_name), \
             patch.object(GeneName, '_create_gene_has_name', return_value=mock_gene_has_name):
            
            # Act
            gene_name = GeneName(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            assert gene_name is not None
    
    def test_unicode_name_string(self, mock_session, mock_name, mock_gene_has_name, sample_data):
        """Test behavior with unicode characters in names"""
        # Arrange
        unicode_name = "α-globin gene 1"  # Contains Greek alpha character
        sample_data["name"] = unicode_name
        
        with patch.object(GeneName, '_create_name', return_value=mock_name), \
             patch.object(GeneName, '_create_gene_has_name', return_value=mock_gene_has_name):
            
            # Act
            gene_name = GeneName(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            assert gene_name is not None
    
    def test_special_characters_in_name(self, mock_session, mock_name, mock_gene_has_name, sample_data):
        """Test behavior with special characters in names"""
        # Arrange
        special_name = "gene-1_variant.2 (pseudo)"
        sample_data["name"] = special_name
        
        with patch.object(GeneName, '_create_name', return_value=mock_name), \
             patch.object(GeneName, '_create_gene_has_name', return_value=mock_gene_has_name):
            
            # Act
            gene_name = GeneName(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            assert gene_name is not None
