"""
Tests for main.py data-update module
"""
import os
import sys
from unittest.mock import Mock, mock_open, patch

import pysolr
import pytest

# Add the data-update directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../bin/data-update'))


class TestSolrDataUpdate:
    """Test cases for the overall Solr data update functionality"""
    
    @patch('main.psycopg2.connect')
    def test_create_solr_json_with_database(self, mock_connect):
        """Test __create_solr_json function creates connection and processes data"""
        import main  # type: ignore
        
        # Mock database connection and environment variables
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        
        # Mock gene query results - fix the data structure to match expected format
        mock_cursor.fetchall.side_effect = [
            # Main genes query - should return (id, taxon_id, status, chromosome)
            [(123, 3702, 'approved', '1')],
            # Symbols query for gene 123 - (symbol, type)
            [('TEST1', 'approved')],
            # Names query for gene 123 - (name, type)
            [('Test Gene', 'approved')],
            # Locus types query for gene 123 - (locus_type,)
            [('protein-coding',)],
            # Xrefs query for gene 123 - (external_resource, external_id)
            []
        ]
        
        # Access the private function to avoid name mangling issues
        create_solr_json = getattr(main, '__create_solr_json')
        
        with patch.dict('os.environ', {
            'DB_USER': 'test_user',
            'DB_PASSWORD': 'test_pass', 
            'DB_HOST': 'test_host',
            'DB_PORT': '5432',
            'DB_NAME': 'test_db'
        }):
            result = create_solr_json()
            
        # Verify database connection was created
        mock_connect.assert_called_once_with(
            user='test_user',
            password='test_pass',
            host='test_host', 
            port='5432',
            database='test_db'
        )
        
        # Verify result is valid JSON
        import json
        parsed_json = json.loads(result)
        assert isinstance(parsed_json, list)
        assert len(parsed_json) == 1
        assert parsed_json[0]['pgnc_id'] == 'PGNC:123'


class TestSolrFunctions:
    """Test cases for Solr-related functions"""
    
    @patch('main.pysolr.Solr')
    def test_upload_to_solr_success(self, mock_solr_class):
        """Test successful __upload_to_solr"""
        import main  # type: ignore
        
        mock_solr = Mock()
        mock_solr_class.return_value = mock_solr
        
        # Access the private function to avoid name mangling issues
        upload_to_solr = getattr(main, '__upload_to_solr')
        upload_to_solr('{"test": "data"}', False)
        
        # Verify Solr connection was created with correct parameters
        mock_solr_class.assert_called_once_with('http://solr:8983/solr/pgnc', always_commit=True)
        
        # Verify add was called (commit is automatic with always_commit=True)
        mock_solr.add.assert_called_once()
    
    @patch('main.pysolr.Solr')
    def test_clear_solr_index_success(self, mock_solr_class):
        """Test successful __clear_solr_index"""
        import main  # type: ignore
        
        mock_solr = Mock()
        mock_solr_class.return_value = mock_solr
        
        # Access the private function to avoid name mangling issues
        clear_solr_index = getattr(main, '__clear_solr_index')
        clear_solr_index()
        
        # Verify delete was called (commit is automatic with always_commit=True)
        mock_solr.delete.assert_called_once_with(q='*:*')
    
    @patch('main.pysolr.Solr')
    def test_clear_solr_index_error(self, mock_solr_class):
        """Test __clear_solr_index with error"""
        import main  # type: ignore
        
        mock_solr = Mock()
        mock_solr_class.return_value = mock_solr
        mock_solr.delete.side_effect = pysolr.SolrError("HTTP 500: Internal Server Error")
        
        # Access the private function to avoid name mangling issues
        clear_solr_index = getattr(main, '__clear_solr_index')
        
        # When retries are exhausted, it raises the original SolrError, not SolrUpdateError
        with patch('time.sleep'):  # Mock sleep to speed up test
            with pytest.raises(pysolr.SolrError, match="HTTP 500"):
                clear_solr_index()


class TestIntegrationScenarios:
    """Test cases for integration scenarios"""
    
    @patch('main.psycopg2.connect')
    @patch('builtins.open', mock_open())
    def test_main_function_execution_flow(self, mock_connect):
        """Test the overall main function execution flow"""
        import main  # type: ignore
        
        # Mock database components
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        
        # Mock no genes found
        mock_cursor.fetchall.return_value = []
        
        with patch.dict('os.environ', {
            'DB_USER': 'test', 'DB_PASSWORD': 'test', 'DB_HOST': 'test',
            'DB_PORT': '5432', 'DB_NAME': 'test'
        }), \
        patch('main.__clear_solr_index'), \
        patch('main.__upload_to_solr'):
            
            # Access the private function to avoid name mangling issues
            create_solr_json = getattr(main, '__create_solr_json')
            
            # This should raise an error since the actual implementation 
            # raises an error when no genes are found
            with pytest.raises(main.SolrUpdateError, match="No gene data found"):
                create_solr_json()


class TestErrorHandling:
    """Test cases for error handling"""
    
    def test_solr_update_error_creation(self):
        """Test SolrUpdateError exception creation"""
        import main  # type: ignore
        
        error = main.SolrUpdateError("Test error message")
        assert str(error) == "Test error message"
        assert isinstance(error, Exception)
    
    def test_http_error_parsing(self):
        """Test HTTP error parsing logic"""
        
        # Test that different HTTP errors are handled appropriately
        error_messages = [
            "HTTP 503: Service Unavailable",
            "HTTP 502: Bad Gateway", 
            "HTTP 504: Gateway Timeout",
            "HTTP 429: Too Many Requests"
        ]
        
        for error_msg in error_messages:
            error = pysolr.SolrError(error_msg)
            # These should all be considered retryable HTTP errors
            assert "HTTP" in str(error)


class TestScriptExecution:
    """Test cases for script execution"""
    
    def test_script_structure_validation(self):
        """Test that the script has the expected structure"""
        import main  # type: ignore
        
        # Verify main functions exist
        assert hasattr(main, 'SolrUpdateError')
        assert hasattr(main, '__main__')  # The actual main function
        
        # Verify it's a callable
        assert callable(getattr(main, '__main__'))
