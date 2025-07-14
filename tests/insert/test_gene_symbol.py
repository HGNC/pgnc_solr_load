"""
Unit tests for GeneSymbol class
"""
from datetime import datetime
from unittest.mock import Mock, patch

import pytest
from insert.gene_symbol import GeneSymbol  # type: ignore


class TestGeneSymbol:
    """Test cases for GeneSymbol class"""
    
    @pytest.fixture
    def mock_session(self):
        """Create a mock database session"""
        session = Mock()
        session.add = Mock()
        session.flush = Mock()
        session.refresh = Mock()
        return session
    
    @pytest.fixture
    def mock_symbol(self):
        """Create a mock Symbol instance"""
        symbol = Mock()
        symbol.id = 123
        symbol.symbol = "TEST_SYMBOL"
        return symbol
    
    @pytest.fixture
    def mock_gene_has_symbol(self):
        """Create a mock GeneHasSymbol instance"""
        gene_has_symbol = Mock()
        gene_has_symbol.id = 456
        gene_has_symbol.creation_date = datetime(2025, 7, 14, 12, 0, 0)
        return gene_has_symbol
    
    @pytest.fixture
    def sample_data(self):
        """Sample data for testing"""
        return {
            "symbol": "BRCA1",
            "gene_id": 1001,
            "creator_id": 2001,
            "type": "approved",
            "status": "public"
        }
    
    def test_init_creates_gene_symbol_successfully(self, mock_session, mock_symbol, mock_gene_has_symbol, sample_data):
        """Test that GeneSymbol initialization creates objects correctly"""
        # Arrange
        with patch.object(GeneSymbol, '_create_symbol', return_value=mock_symbol) as mock_create_symbol, \
             patch.object(GeneSymbol, '_create_gene_has_symbol', return_value=mock_gene_has_symbol) as mock_create_gene_has_symbol:
            
            # Act
            gene_symbol = GeneSymbol(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            mock_create_symbol.assert_called_once_with(mock_session, sample_data["symbol"])
            mock_create_gene_has_symbol.assert_called_once_with(
                mock_session, 
                sample_data["gene_id"], 
                mock_symbol.id, 
                sample_data["type"], 
                sample_data["creator_id"], 
                sample_data["status"]
            )
            
            # Verify instance attributes
            assert gene_symbol.symbol_id == mock_symbol.id
            assert gene_symbol.gene_id == sample_data["gene_id"]
            assert gene_symbol.creator_id == sample_data["creator_id"]
            assert gene_symbol.type == sample_data["type"]
            assert gene_symbol.status == sample_data["status"]
            assert gene_symbol.creation_date == mock_gene_has_symbol.creation_date
    
    def test_create_symbol_adds_and_flushes_symbol(self, mock_session, sample_data):
        """Test that _create_symbol creates Symbol correctly"""
        # Arrange
        mock_symbol = Mock()
        mock_symbol.id = 789
        mock_session.refresh.side_effect = lambda obj: setattr(obj, 'id', 789)
        
        with patch('insert.gene_symbol.Symbol') as MockSymbol:
            MockSymbol.return_value = mock_symbol
            
            # Act
            gene_symbol = GeneSymbol.__new__(GeneSymbol)  # Create instance without calling __init__
            result = gene_symbol._create_symbol(mock_session, sample_data["symbol"])
            
            # Assert
            MockSymbol.assert_called_once_with(symbol=sample_data["symbol"])
            mock_session.add.assert_called_once_with(mock_symbol)
            mock_session.flush.assert_called_once()
            mock_session.refresh.assert_called_once_with(mock_symbol)
            assert result == mock_symbol
    
    def test_create_gene_has_symbol_adds_and_flushes_relationship(self, mock_session):
        """Test that _create_gene_has_symbol creates GeneHasSymbol correctly"""
        # Arrange
        mock_gene_has_symbol = Mock()
        mock_gene_has_symbol.id = 999
        mock_session.refresh.side_effect = lambda obj: setattr(obj, 'id', 999)
        
        test_data = {
            "gene_id": 1001,
            "symbol_id": 2001,
            "type": "alias",
            "creator_id": 3001,
            "status": "private"
        }
        
        with patch('insert.gene_symbol.GeneHasSymbol') as MockGeneHasSymbol:
            MockGeneHasSymbol.return_value = mock_gene_has_symbol
            
            # Act
            gene_symbol = GeneSymbol.__new__(GeneSymbol)  # Create instance without calling __init__
            result = gene_symbol._create_gene_has_symbol(
                mock_session,
                test_data["gene_id"],
                test_data["symbol_id"],
                test_data["type"],
                test_data["creator_id"],
                test_data["status"]
            )
            
            # Assert
            MockGeneHasSymbol.assert_called_once_with(
                gene_id=test_data["gene_id"],
                symbol_id=test_data["symbol_id"],
                type=test_data["type"],
                creator_id=test_data["creator_id"],
                status=test_data["status"]
            )
            mock_session.add.assert_called_once_with(mock_gene_has_symbol)
            mock_session.flush.assert_called_once()
            mock_session.refresh.assert_called_once_with(mock_gene_has_symbol)
            assert result == mock_gene_has_symbol
    
    def test_repr_returns_correct_string(self, mock_session, mock_symbol, mock_gene_has_symbol, sample_data):
        """Test that __repr__ returns the correct string representation"""
        # Arrange
        with patch.object(GeneSymbol, '_create_symbol', return_value=mock_symbol), \
             patch.object(GeneSymbol, '_create_gene_has_symbol', return_value=mock_gene_has_symbol):
            
            gene_symbol = GeneSymbol(
                session=mock_session,
                **sample_data
            )
            
            # Act
            repr_string = repr(gene_symbol)
            
            # Assert
            expected = (
                f"<GeneSymbol(symbol_id={mock_symbol.id}, "
                f"gene_id={sample_data['gene_id']}, creator_id={sample_data['creator_id']}, "
                f"type='{sample_data['type']}', status='{sample_data['status']}', "
                f"creation_date={mock_gene_has_symbol.creation_date})>"
            )
            assert repr_string == expected
    
    @pytest.mark.parametrize("type_value", ["approved", "alias", "previous"])
    def test_valid_type_values(self, mock_session, mock_symbol, mock_gene_has_symbol, sample_data, type_value):
        """Test that all valid type values work correctly"""
        # Arrange
        sample_data["type"] = type_value
        
        with patch.object(GeneSymbol, '_create_symbol', return_value=mock_symbol), \
             patch.object(GeneSymbol, '_create_gene_has_symbol', return_value=mock_gene_has_symbol):
            
            # Act
            gene_symbol = GeneSymbol(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            assert gene_symbol.type == type_value
    
    @pytest.mark.parametrize("status_value", ["public", "private"])
    def test_valid_status_values(self, mock_session, mock_symbol, mock_gene_has_symbol, sample_data, status_value):
        """Test that all valid status values work correctly"""
        # Arrange
        sample_data["status"] = status_value
        
        with patch.object(GeneSymbol, '_create_symbol', return_value=mock_symbol), \
             patch.object(GeneSymbol, '_create_gene_has_symbol', return_value=mock_gene_has_symbol):
            
            # Act
            gene_symbol = GeneSymbol(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            assert gene_symbol.status == status_value
    
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
        
        with patch('insert.gene_symbol.Symbol') as MockSymbol, \
             patch('insert.gene_symbol.GeneHasSymbol') as MockGeneHasSymbol:
            
            MockSymbol.return_value = Mock()
            MockGeneHasSymbol.return_value = Mock()
            
            # Act
            GeneSymbol(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            expected_order = [
                "add_Mock",  # Symbol
                "flush",
                "refresh_Mock",
                "add_Mock",  # GeneHasSymbol
                "flush", 
                "refresh_Mock"
            ]
            assert call_order == expected_order
    
    def test_attribute_assignment_integrity(self, mock_session, mock_symbol, mock_gene_has_symbol, sample_data):
        """Test that all attributes are correctly assigned from constructor parameters"""
        # Arrange
        with patch.object(GeneSymbol, '_create_symbol', return_value=mock_symbol), \
             patch.object(GeneSymbol, '_create_gene_has_symbol', return_value=mock_gene_has_symbol):
            
            # Act
            gene_symbol = GeneSymbol(
                session=mock_session,
                **sample_data
            )
            
            # Assert - All constructor parameters should be stored as instance attributes
            assert hasattr(gene_symbol, 'symbol_id')
            assert hasattr(gene_symbol, 'gene_id')
            assert hasattr(gene_symbol, 'creator_id')
            assert hasattr(gene_symbol, 'type')
            assert hasattr(gene_symbol, 'status')
            assert hasattr(gene_symbol, 'creation_date')
            
            # Verify values match constructor parameters
            assert gene_symbol.gene_id == sample_data["gene_id"]
            assert gene_symbol.creator_id == sample_data["creator_id"]
            assert gene_symbol.type == sample_data["type"]
            assert gene_symbol.status == sample_data["status"]
    
    def test_database_exception_handling(self, mock_session, sample_data):
        """Test behavior when database operations raise exceptions"""
        # Arrange
        mock_session.flush.side_effect = Exception("Database error")
        
        with patch('insert.gene_symbol.Symbol') as MockSymbol:
            MockSymbol.return_value = Mock()
            
            # Act & Assert
            with pytest.raises(Exception, match="Database error"):
                GeneSymbol(
                    session=mock_session,
                    **sample_data
                )
    
    def test_empty_symbol_string(self, mock_session, mock_symbol, mock_gene_has_symbol, sample_data):
        """Test behavior with empty symbol string"""
        # Arrange
        sample_data["symbol"] = ""
        
        with patch.object(GeneSymbol, '_create_symbol', return_value=mock_symbol), \
             patch.object(GeneSymbol, '_create_gene_has_symbol', return_value=mock_gene_has_symbol):
            
            # Act
            gene_symbol = GeneSymbol(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            assert gene_symbol is not None
            # The class should handle empty strings if the database allows it
    
    def test_large_integer_ids(self, mock_session, mock_symbol, mock_gene_has_symbol, sample_data):
        """Test behavior with large integer IDs"""
        # Arrange
        large_id = 9223372036854775807  # Max value for 64-bit signed integer
        sample_data["gene_id"] = large_id
        sample_data["creator_id"] = large_id
        mock_symbol.id = large_id
        
        with patch.object(GeneSymbol, '_create_symbol', return_value=mock_symbol), \
             patch.object(GeneSymbol, '_create_gene_has_symbol', return_value=mock_gene_has_symbol):
            
            # Act
            gene_symbol = GeneSymbol(
                session=mock_session,
                **sample_data
            )
            
            # Assert
            assert gene_symbol.gene_id == large_id
            assert gene_symbol.creator_id == large_id
            assert gene_symbol.symbol_id == large_id
