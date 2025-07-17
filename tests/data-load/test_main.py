"""
Tests for the main.py data loading functionality
"""
from unittest.mock import Mock, patch

import pandas as pd
import pytest


class TestGeneDataLoader:
    """Test cases for the GeneDataLoader class"""
    
    def test_init_with_valid_csv(self, sample_csv_file):
        """Test GeneDataLoader initialization with valid CSV file"""
        with patch('main.GeneDataLoader.parse_csv') as mock_parse:
            mock_parse.return_value = pd.DataFrame({'test': [1, 2, 3]})
            
            from main import GeneDataLoader  # type: ignore
            loader = GeneDataLoader(sample_csv_file)
            
            assert loader.file_path == sample_csv_file
            mock_parse.assert_called_once()
    
    def test_parse_csv_success(self, sample_csv_file):
        """Test successful CSV parsing"""
        from main import GeneDataLoader  # type: ignore
        loader = GeneDataLoader.__new__(GeneDataLoader)
        loader.file_path = sample_csv_file
        
        result = loader.parse_csv()
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert 'primary_id' in result.columns
        assert 'gene_symbol_string' in result.columns
        assert result.iloc[0]['primary_id'] == 'Phytozome.1.1'
    
    def test_parse_csv_file_not_found(self):
        """Test CSV parsing with non-existent file"""
        from main import GeneDataLoader  # type: ignore
        loader = GeneDataLoader.__new__(GeneDataLoader)
        loader.file_path = "/non/existent/file.csv"
        
        with patch('builtins.print') as mock_print:
            result = loader.parse_csv()
            
            assert result is None
            mock_print.assert_called_with(
                "Error: File not found at path: /non/existent/file.csv"
            )
    
    def test_parse_csv_empty_file(self, empty_csv_file):
        """Test CSV parsing with empty file"""
        from main import GeneDataLoader  # type: ignore
        loader = GeneDataLoader.__new__(GeneDataLoader)
        loader.file_path = empty_csv_file
        
        with patch('builtins.print') as mock_print:
            result = loader.parse_csv()
            
            assert result is None
            mock_print.assert_called_with("Error: The CSV file is empty.")
    
    def test_parse_csv_malformed_file(self, malformed_csv_file):
        """Test CSV parsing with malformed file"""
        from main import GeneDataLoader  # type: ignore
        loader = GeneDataLoader.__new__(GeneDataLoader)
        loader.file_path = malformed_csv_file
        
        # This should actually succeed with pandas being lenient, but let's test the exception path
        with patch('pandas.read_csv', side_effect=pd.errors.ParserError("Test error")):
            with patch('builtins.print') as mock_print:
                result = loader.parse_csv()
                
                assert result is None
                mock_print.assert_called_with(
                    "Error: Failed to parse the CSV file. It may be malformed."
                )
    
    def test_process_data_no_dataframe(self):
        """Test process_data when no DataFrame is available"""
        from main import GeneDataLoader  # type: ignore
        loader = GeneDataLoader.__new__(GeneDataLoader)
        loader.df = None
        
        with patch('builtins.print') as mock_print:
            loader.process_data()
            
            mock_print.assert_called_with(
                "No data to process. Ensure the CSV file was loaded correctly."
            )
    
    @patch('main.sa.create_engine')
    def test_process_data_success(self, mock_create_engine, sample_dataframe):
        """Test successful data processing"""
        from main import GeneDataLoader  # type: ignore
        
        # Mock engine and session
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine
        
        loader = GeneDataLoader.__new__(GeneDataLoader)
        loader.df = sample_dataframe
        
        with patch.object(loader, '_process_row', return_value=True) as mock_process_row:
            with patch('builtins.print') as mock_print:
                loader.process_data()
                
                # Verify engine creation and disposal
                mock_create_engine.assert_called_once()
                mock_engine.dispose.assert_called_once()
                
                # Verify _process_row called for each row
                assert mock_process_row.call_count == 2
                
                # Verify completion message
                mock_print.assert_any_call("Data processing complete.")
    
    @patch('main.sa.create_engine')
    def test_process_data_with_exception(self, mock_create_engine, sample_dataframe):
        """Test data processing with exception during processing"""
        from main import GeneDataLoader  # type: ignore
        
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine
        
        loader = GeneDataLoader.__new__(GeneDataLoader)
        loader.df = sample_dataframe
        
        # Mock _process_row to raise an exception
        with patch.object(loader, '_process_row', side_effect=Exception("Test error")):
            with pytest.raises(Exception, match="Test error"):
                loader.process_data()
                
                # Engine should still be disposed even with exception
                mock_engine.dispose.assert_called_once()
    
    def test_process_row_missing_primary_id(self, mock_engine):
        """Test _process_row with missing primary_id"""
        from main import GeneDataLoader  # type: ignore
        
        loader = GeneDataLoader.__new__(GeneDataLoader)
        row = pd.Series({'gene_symbol_string': 'TEST', 'primary_id_source': 'phytozome'})
        
        with patch('builtins.print') as mock_print:
            result = loader._process_row(mock_engine, 0, row)
            
            assert result is False
            mock_print.assert_any_call("WARNING: Row 0 is missing primary_id:")
    
    def test_process_row_missing_primary_id_source(self, mock_engine):
        """Test _process_row with missing primary_id_source"""
        from main import GeneDataLoader  # type: ignore
        
        loader = GeneDataLoader.__new__(GeneDataLoader)
        row = pd.Series({'primary_id': 'TEST.1.1', 'gene_symbol_string': 'TEST'})
        
        with patch('builtins.print') as mock_print:
            result = loader._process_row(mock_engine, 0, row)
            
            assert result is False
            mock_print.assert_any_call("WARNING: Row 0 is missing primary_id_source:")
    
    @patch('main.sa.orm.sessionmaker')
    def test_process_row_success(self, mock_sessionmaker, mock_engine, sample_row):
        """Test successful row processing"""
        from main import (  # type: ignore
            GeneDataLoader,
            GeneStatusEnum,
        )
        
        # Mock session and its context manager
        mock_session = Mock()
        mock_session.__enter__ = Mock(return_value=mock_session)
        mock_session.__exit__ = Mock(return_value=None)
        mock_sessionmaker.return_value = Mock(return_value=mock_session)
        
        # Mock gene and user objects
        mock_gene = Mock()
        mock_gene.primary_id = "Phytozome.1.1"
        mock_gene.status = GeneStatusEnum.internal
        mock_user = Mock()
        
        loader = GeneDataLoader.__new__(GeneDataLoader)
        
        with patch.object(loader, '_get_gene_and_creator', return_value=(mock_gene, mock_user)):
            with patch.object(loader, '_process_symbols'):
                with patch.object(loader, '_process_names'):
                    with patch.object(loader, '_process_location'):
                        with patch.object(loader, '_process_locus_type'):
                            with patch.object(loader, '_process_crossrefs'):
                                with patch('builtins.print') as mock_print:
                                    result = loader._process_row(mock_engine, 0, sample_row)
                                    
                                    assert result is True
                                    assert mock_gene.status == GeneStatusEnum.approved
                                    mock_session.add.assert_called_with(mock_gene)
                                    mock_session.commit.assert_called_once()
                                    mock_print.assert_any_call("Making gene Phytozome.1.1 public")
                                    mock_print.assert_any_call("Processed row 0: Phytozome.1.1 successfully.")
    
    @patch('main.sa.orm.sessionmaker')
    def test_process_row_exception_handling(self, mock_sessionmaker, mock_engine, sample_row):
        """Test row processing with exception handling"""
        from main import GeneDataLoader  # type: ignore
        
        # Mock session and its context manager
        mock_session = Mock()
        mock_session.__enter__ = Mock(return_value=mock_session)
        mock_session.__exit__ = Mock(return_value=None)
        mock_sessionmaker.return_value = Mock(return_value=mock_session)
        
        loader = GeneDataLoader.__new__(GeneDataLoader)
        
        # Mock gene and user objects
        mock_gene = Mock()
        mock_gene.primary_id = "Phytozome.1.1"
        mock_user = Mock()
        
        # Mock _get_gene_and_creator to raise an exception
        with patch.object(loader, '_get_gene_and_creator', return_value=(mock_gene, mock_user)):
            with patch.object(loader, '_process_symbols', side_effect=Exception("Test error")):
                with patch('builtins.print') as mock_print:
                    result = loader._process_row(mock_engine, 0, sample_row)
                    
                    assert result is False
                    mock_session.rollback.assert_called_once()
                    # Check that print was called twice - once for the row, once for the error
                    assert mock_print.call_count == 2
                    # Check the error message specifically
                    error_call = mock_print.call_args_list[1]
                    assert "Error processing row 0: Test error" in str(error_call)
    
    @patch('main.sa.orm.sessionmaker')
    def test_process_row_gene_not_found_creates_new(self, mock_sessionmaker, mock_engine, sample_row):
        """Test row processing when gene is not found, creates new gene"""
        import sqlalchemy as sa
        from main import GeneDataLoader, GeneStatusEnum  # type: ignore
        
        # Mock session and its context manager
        mock_session = Mock()
        mock_session.__enter__ = Mock(return_value=mock_session)
        mock_session.__exit__ = Mock(return_value=None)
        mock_sessionmaker.return_value = Mock(return_value=mock_session)
        
        # Mock gene and user objects
        mock_gene = Mock()
        mock_gene.primary_id = "Phytozome.1.1"
        mock_gene.status = GeneStatusEnum.internal
        mock_user = Mock()
        
        loader = GeneDataLoader.__new__(GeneDataLoader)
        
        # Mock _get_gene_and_creator to raise NoResultFound, then _create_new_gene to return gene and user
        with patch.object(loader, '_get_gene_and_creator', side_effect=sa.orm.exc.NoResultFound("Gene not found")):
            with patch.object(loader, '_create_new_gene', return_value=(mock_gene, mock_user)):
                with patch.object(loader, '_process_symbols'):
                    with patch.object(loader, '_process_names'):
                        with patch.object(loader, '_process_location'):
                            with patch.object(loader, '_process_locus_type'):
                                with patch.object(loader, '_process_crossrefs'):
                                    with patch('builtins.print') as mock_print:
                                        result = loader._process_row(mock_engine, 0, sample_row)
                                        
                                        assert result is True
                                        mock_session.add.assert_called_with(mock_gene)
                                        mock_session.commit.assert_called_once()
                                        mock_print.assert_any_call("Gene Phytozome.1.1 not found in the database. Creating new gene.")
                                        mock_print.assert_any_call("Processed row 0: Phytozome.1.1 successfully.")
    
    def test_get_gene_and_creator_success(self, mock_session):
        """Test successful gene and creator retrieval"""
        from main import GeneDataLoader  # type: ignore
        
        # Mock query results
        mock_gene = Mock()
        mock_user = Mock()
        
        mock_gene_query = Mock()
        mock_gene_query.where.return_value.one.return_value = mock_gene
        
        mock_user_query = Mock()
        mock_user_query.where.return_value.one.return_value = mock_user
        
        # Configure session.query to return different mocks for Gene and User
        def query_side_effect(model):
            if hasattr(model, '__name__') and model.__name__ == 'Gene':
                return mock_gene_query
            elif hasattr(model, '__name__') and model.__name__ == 'User':
                return mock_user_query
            return Mock()
        
        mock_session.query.side_effect = query_side_effect
        
        loader = GeneDataLoader.__new__(GeneDataLoader)
        
        with patch('main.Gene') as mock_gene_class:
            with patch('main.User') as mock_user_class:
                mock_gene_class.__name__ = 'Gene'
                mock_user_class.__name__ = 'User'
                
                result_gene, result_user = loader._get_gene_and_creator(mock_session, "Phytozome.1.1", "phytozome")
                
                assert result_gene == mock_gene
                assert result_user == mock_user
    
    def test_create_new_gene_success(self, mock_session):
        """Test successful gene creation"""
        from main import GeneDataLoader, GeneStatusEnum  # type: ignore
        
        # Mock user query result
        mock_user = Mock()
        mock_user.id = 1
        mock_user_query = Mock()
        mock_user_query.where.return_value.one.return_value = mock_user
        
        # Mock external resource query result
        mock_ext_res = Mock()
        mock_ext_res.id = 1
        mock_ext_res_query = Mock()
        mock_ext_res_query.where.return_value.one.return_value = mock_ext_res
        
        # Mock xref query to return None (no existing xref)
        mock_xref_query = Mock()
        mock_xref_query.where.return_value.one_or_none.return_value = None
        
        # Configure session.query to return different mocks based on model
        def query_side_effect(model):
            if hasattr(model, '__name__'):
                if model.__name__ == 'User':
                    return mock_user_query
                elif model.__name__ == 'ExternalResource':
                    return mock_ext_res_query
                elif model.__name__ == 'Xref':
                    return mock_xref_query
            return Mock()
        
        mock_session.query.side_effect = query_side_effect
        
        loader = GeneDataLoader.__new__(GeneDataLoader)
        
        with patch('main.Gene') as mock_gene_class:
            with patch('main.Xref') as mock_xref_class:
                with patch('main.GeneHasXref') as mock_gene_has_xref_class:
                    with patch('main.User') as mock_user_class:
                        with patch('main.ExternalResource') as mock_ext_res_class:
                            with patch('pandas.Timestamp') as mock_timestamp:
                                mock_gene = Mock()
                                mock_gene.id = 1
                                mock_gene.primary_id = "Phytozome.1.1"
                                mock_gene.primary_id_source = "phytozome"
                                mock_gene.status = GeneStatusEnum.internal
                                mock_gene_class.return_value = mock_gene
                                
                                mock_xref = Mock()
                                mock_xref.id = 1
                                mock_xref_class.return_value = mock_xref
                                
                                mock_gene_has_xref = Mock()
                                mock_gene_has_xref_class.return_value = mock_gene_has_xref
                                
                                mock_timestamp.now.return_value = "2023-01-01"
                                
                                # Set up class names for query side effect
                                mock_user_class.__name__ = 'User'
                                mock_ext_res_class.__name__ = 'ExternalResource'
                                mock_xref_class.__name__ = 'Xref'
                                
                                result_gene, result_user = loader._create_new_gene(
                                    mock_session, "Phytozome.1.1", "phytozome"
                                )
                                
                                # Verify gene creation
                                mock_gene_class.assert_called_once_with(
                                    taxon_id=3694,
                                    primary_id="Phytozome.1.1",
                                    primary_id_source="phytozome",
                                    status=GeneStatusEnum.internal,
                                    creator_id=mock_user.id,
                                    creation_date="2023-01-01"
                                )
                                
                                # Verify xref creation
                                mock_xref_class.assert_called_once_with(
                                    display_id="Phytozome.1.1",
                                    ext_res_id=mock_ext_res.id
                                )
                                
                                # Verify gene_has_xref creation
                                mock_gene_has_xref_class.assert_called_once()
                                
                                # Verify session operations
                                assert mock_session.add.call_count == 3  # gene, xref, gene_has_xref
                                assert mock_session.flush.call_count == 3
                                assert mock_session.refresh.call_count == 3
                                
                                assert result_gene == mock_gene
                                assert result_user == mock_user
    
    def test_create_new_gene_xref_already_exists(self, mock_session):
        """Test gene creation when xref already exists"""
        from main import GeneDataLoader  # type: ignore
        
        # Mock user query result
        mock_user = Mock()
        mock_user_query = Mock()
        mock_user_query.where.return_value.one.return_value = mock_user
        
        # Mock xref query to return existing xref
        mock_existing_xref = Mock()
        mock_xref_query = Mock()
        mock_xref_query.where.return_value.one_or_none.return_value = mock_existing_xref
        
        # Configure session.query
        def query_side_effect(model):
            if hasattr(model, '__name__'):
                if model.__name__ == 'User':
                    return mock_user_query
                elif model.__name__ == 'Xref':
                    return mock_xref_query
            return Mock()
        
        mock_session.query.side_effect = query_side_effect
        
        loader = GeneDataLoader.__new__(GeneDataLoader)
        
        with patch('main.User') as mock_user_class:
            with patch('main.Xref') as mock_xref_class:
                mock_user_class.__name__ = 'User'
                mock_xref_class.__name__ = 'Xref'
                
                with pytest.raises(ValueError, match="Xref with display_id 'Phytozome.1.1' already exists"):
                    loader._create_new_gene(mock_session, "Phytozome.1.1", "phytozome")
    
    def test_process_symbols_missing_symbol(self, mock_session, mock_gene, mock_user):
        """Test _process_symbols with missing gene_symbol_string"""
        from main import GeneDataLoader  # type: ignore
        
        loader = GeneDataLoader.__new__(GeneDataLoader)
        row = pd.Series({'primary_id': 'Phytozome.1.1', 'primary_id_source': 'phytozome'})  # Missing gene_symbol_string
        
        with pytest.raises(ValueError, match="gene_symbol_string is required."):
            loader._process_symbols(mock_session, row, mock_gene, mock_user)
    
    def test_process_symbols_success(self, mock_session, mock_gene, mock_user, sample_row):
        """Test successful symbol processing"""
        from main import GeneDataLoader  # type: ignore
        
        loader = GeneDataLoader.__new__(GeneDataLoader)
        
        with patch.object(loader, '_process_approved_symbol') as mock_approved:
            with patch.object(loader, '_process_alias_symbols') as mock_alias:
                loader._process_symbols(mock_session, sample_row, mock_gene, mock_user)
                
                mock_approved.assert_called_once_with(
                    mock_session, 'SYMBOL1', mock_gene, mock_user
                )
                mock_alias.assert_called_once_with(
                    mock_session, sample_row, mock_gene, mock_user
                )
    
    def test_process_symbols_with_value_error_handling(self, mock_session, mock_gene, mock_user, sample_row):
        """Test symbol processing with ValueError handling"""
        from main import GeneDataLoader  # type: ignore
        
        loader = GeneDataLoader.__new__(GeneDataLoader)
        
        with patch.object(loader, '_process_approved_symbol', side_effect=ValueError("Already exists")):
            with patch.object(loader, '_process_alias_symbols', side_effect=ValueError("Alias exists")):
                with patch('builtins.print') as mock_print:
                    loader._process_symbols(mock_session, sample_row, mock_gene, mock_user)
                    
                    expected_calls = [
                        "Gene Phytozome.1.1 already has approved symbol SYMBOL1. Skipping",
                        "Gene Phytozome.1.1 already has alias symbol SYMBOL1. Skipping"
                    ]
                    for call in expected_calls:
                        mock_print.assert_any_call(call)


class TestGeneDataLoaderSymbolProcessing:
    """Test cases for symbol processing methods"""
    
    def test_process_approved_symbol_new_symbol(self, mock_session, mock_gene, mock_user):
        """Test processing approved symbol when symbol doesn't exist"""
        from main import GeneDataLoader  # type: ignore
        
        # Mock that symbol doesn't exist
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        loader = GeneDataLoader.__new__(GeneDataLoader)
        
        with patch('main.GeneSymbol') as mock_gene_symbol:
            loader._process_approved_symbol(mock_session, "NEW_SYMBOL", mock_gene, mock_user)
            
            mock_gene_symbol.assert_called_once()
    
    def test_process_approved_symbol_existing_approved(self, mock_session, mock_gene, mock_user):
        """Test processing approved symbol when approved symbol already exists"""
        from main import (  # type: ignore
            GeneDataLoader,
            NomenclatureEnum,
        )
        
        # Mock existing symbol with approved type
        mock_symbol = Mock()
        mock_symbol_has_gene = Mock()
        mock_symbol_has_gene.type = NomenclatureEnum.approved
        mock_symbol.symbol_has_genes = [mock_symbol_has_gene]
        
        mock_session.query.return_value.filter.return_value.first.return_value = mock_symbol
        
        loader = GeneDataLoader.__new__(GeneDataLoader)
        
        with pytest.raises(ValueError, match="gene_symbol_string already exists as an approved symbol"):
            loader._process_approved_symbol(mock_session, "EXISTING_SYMBOL", mock_gene, mock_user)


class TestGeneDataLoaderNameProcessing:
    """Test cases for name processing methods"""
    
    def test_process_names_missing_name(self, mock_session, mock_gene, mock_user):
        """Test _process_names with missing gene_name_string"""
        from main import GeneDataLoader  # type: ignore
        
        loader = GeneDataLoader.__new__(GeneDataLoader)
        row = pd.Series({'primary_id': 'Phytozome.1.1', 'primary_id_source': 'phytozome'})  # Missing gene_name_string
        
        with pytest.raises(ValueError, match="gene_name_string is required."):
            loader._process_names(mock_session, row, mock_gene, mock_user)
    
    def test_process_names_success(self, mock_session, mock_gene, mock_user, sample_row):
        """Test successful name processing"""
        from main import GeneDataLoader  # type: ignore
        
        loader = GeneDataLoader.__new__(GeneDataLoader)
        
        with patch.object(loader, '_process_approved_name') as mock_approved:
            with patch.object(loader, '_process_alias_names') as mock_alias:
                loader._process_names(mock_session, sample_row, mock_gene, mock_user)
                
                mock_approved.assert_called_once_with(
                    mock_session, 'Gene Name 1', mock_gene, mock_user
                )
                mock_alias.assert_called_once_with(
                    mock_session, sample_row, mock_gene, mock_user
                )


class TestGeneDataLoaderLocationProcessing:
    """Test cases for location processing methods"""
    
    def test_process_location_success(self, mock_session, mock_gene, mock_user, sample_row):
        """Test successful location processing"""
        from main import GeneDataLoader  # type: ignore
        
        loader = GeneDataLoader.__new__(GeneDataLoader)
        
        # Mock that location exists in database
        mock_location = Mock()
        mock_location.id = 1
        mock_location.chromosome = "1"
        
        # Mock that no existing location relationship exists  
        mock_session.query.return_value.filter.return_value.first.side_effect = [
            mock_location,  # First call: location lookup
            None            # Second call: existing relationship check
        ]
        
        with patch('main.GeneHasLocation') as mock_gene_has_location:
            with patch('main.Location'):
                loader._process_location(mock_session, sample_row, mock_gene, mock_user)
                
                # Should call GeneHasLocation when no existing relationship
                mock_gene_has_location.assert_called_once()


class TestGeneDataLoaderLocusTypeProcessing:
    """Test cases for locus type processing methods"""
    
    def test_process_locus_type_success(self, mock_session, mock_gene, mock_user, sample_row):
        """Test successful locus type processing"""
        from main import GeneDataLoader  # type: ignore
        
        loader = GeneDataLoader.__new__(GeneDataLoader)
        
        # Mock that locus type exists in database
        mock_locus_type = Mock()
        mock_locus_type.id = 1
        mock_locus_type.locus_type = "protein-coding"
        
        # Mock that no existing locus type relationship exists
        mock_session.query.return_value.filter.return_value.first.side_effect = [
            mock_locus_type,  # First call: locus type lookup
            None              # Second call: existing relationship check
        ]
        
        with patch('main.GeneHasLocusType') as mock_gene_has_locus_type:
            with patch('main.LocusType'):
                loader._process_locus_type(mock_session, sample_row, mock_gene, mock_user)
                
                mock_gene_has_locus_type.assert_called_once()


class TestGeneDataLoaderCrossrefsProcessing:
    """Test cases for cross-references processing methods"""
    
    def test_process_crossrefs_success(self, mock_session, mock_gene, mock_user, sample_row):
        """Test successful crossrefs processing"""
        from main import GeneDataLoader  # type: ignore
        
        loader = GeneDataLoader.__new__(GeneDataLoader)
        
        with patch.object(loader, '_process_xref_field') as mock_process_xref:
            loader._process_crossrefs(mock_session, sample_row, mock_gene, mock_user)
            
            # Verify _process_xref_field called for each external ID type
            expected_calls = [
                ('ncbi_gene_id', 1),
                ('uniprot_id', 3),
                ('pubmed_id', 4)
            ]
            
            assert mock_process_xref.call_count == len(expected_calls)
    
    def test_process_xref_field_success(self, mock_session, mock_gene, mock_user, sample_row):
        """Test successful xref field processing"""
        from main import GeneDataLoader  # type: ignore
        
        loader = GeneDataLoader.__new__(GeneDataLoader)
        
        # Mock that no existing xref exists
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        with patch('main.GeneXref') as mock_gene_xref:
            loader._process_xref_field(
                mock_session, sample_row, 'ncbi_gene_id', 1, mock_gene, mock_user
            )
            
            mock_gene_xref.assert_called_once()


class TestUtilityFunctions:
    """Test cases for utility functions"""
    
    @patch('main.subprocess.run')
    def test_dump_db_success(self, mock_subprocess_run):
        """Test successful database dump"""
        from main import dump_db  # type: ignore
        
        mock_subprocess_run.return_value = Mock(returncode=0)
        
        with patch('main.gzip.open') as mock_gzip_open:
            mock_file = Mock()
            mock_gzip_open.return_value.__enter__.return_value = mock_file
            
            with patch('main.subprocess.Popen') as mock_popen:
                mock_process = Mock()
                mock_process.stdout.readline.side_effect = ["line1\n", "line2\n", ""]
                mock_popen.return_value = mock_process
                
                dump_db(("pg_dump", "-h", "localhost"), "test.sql")
                
                mock_gzip_open.assert_called_once_with("/usr/src/app/db-data/test.sql", "wb")
                mock_popen.assert_called_once_with(
                    ("pg_dump", "-h", "localhost"), 
                    stdout=-1,  # subprocess.PIPE is actually -1
                    universal_newlines=True
                )
    
    @patch('main.subprocess.run')
    def test_dump_db_failure(self, mock_subprocess_run):
        """Test database dump failure"""
        from main import dump_db  # type: ignore
        
        mock_subprocess_run.return_value = Mock(returncode=1)
        
        with patch('main.gzip.open') as mock_gzip_open:
            mock_file = Mock()
            mock_gzip_open.return_value.__enter__.return_value = mock_file
            
            with patch('main.subprocess.Popen') as mock_popen:
                mock_process = Mock()
                mock_process.stdout.readline.side_effect = ["error line\n", ""]
                mock_popen.return_value = mock_process
                
                dump_db(("pg_dump", "-h", "localhost"), "test.sql")
                
                mock_gzip_open.assert_called_once_with("/usr/src/app/db-data/test.sql", "wb")
                mock_popen.assert_called_once()
    
    @patch('main.GeneDataLoader')
    @patch('main.argparse.ArgumentParser')
    def test_main_function_success(self, mock_argument_parser, mock_gene_data_loader):
        """Test main function with successful execution"""
        from main import main  # type: ignore
        
        # Mock argument parsing
        mock_args = Mock()
        mock_args.file = "test.csv"
        mock_parser = Mock()
        mock_parser.parse_args.return_value = mock_args
        mock_argument_parser.return_value = mock_parser
        
        # Mock GeneDataLoader
        mock_loader = Mock()
        mock_loader.df = Mock()  # Not None, so processing continues
        mock_gene_data_loader.return_value = mock_loader
        
        with patch('main.dump_db') as mock_dump_db:
            with patch('builtins.exit') as mock_exit:
                with patch('builtins.print') as mock_print:
                    with patch.dict('main.os.environ', {
                        'DB_HOST': 'localhost',
                        'DB_PORT': '5432',
                        'DB_USER': 'testuser',
                        'DB_NAME': 'testdb'
                    }):
                        main()
                        
                        mock_gene_data_loader.assert_called_once_with("test.csv")
                        mock_loader.process_data.assert_called_once()
                        mock_dump_db.assert_called_once()
                        mock_print.assert_any_call("Dumping database...")
                        mock_exit.assert_not_called()
    
    @patch('main.GeneDataLoader')
    @patch('main.argparse.ArgumentParser')
    def test_main_function_no_dataframe(self, mock_argument_parser, mock_gene_data_loader):
        """Test main function when DataFrame is None"""
        from main import main  # type: ignore
        
        # Mock argument parsing
        mock_args = Mock()
        mock_args.file = "test.csv"
        mock_parser = Mock()
        mock_parser.parse_args.return_value = mock_args
        mock_argument_parser.return_value = mock_parser
        
        # Mock GeneDataLoader with None DataFrame
        mock_loader = Mock()
        mock_loader.df = None
        mock_gene_data_loader.return_value = mock_loader
        
        with patch('builtins.exit') as mock_exit:
            # Mock the os.environ to avoid database dump errors
            with patch('main.os.environ', {'DB_HOST': 'localhost', 'DB_PORT': '5432', 'DB_USER': 'test', 'DB_NAME': 'test'}):
                main()
                
                mock_gene_data_loader.assert_called_once_with("test.csv")
                # In the actual code, main() exits immediately if df is None, before calling process_data
                # It may call exit twice - once for df being None, and once for database dump error
                assert mock_exit.call_count >= 1
                mock_exit.assert_any_call(1)
    
    @patch('main.GeneDataLoader')
    @patch('main.argparse.ArgumentParser')
    def test_main_function_processing_exception(self, mock_argument_parser, mock_gene_data_loader):
        """Test main function with exception during processing"""
        from main import main  # type: ignore
        
        # Mock argument parsing
        mock_args = Mock()
        mock_args.file = "test.csv"
        mock_parser = Mock()
        mock_parser.parse_args.return_value = mock_args
        mock_argument_parser.return_value = mock_parser
        
        # Mock GeneDataLoader
        mock_loader = Mock()
        mock_loader.df = Mock()  # Not None
        mock_loader.process_data.side_effect = Exception("Processing error")
        mock_gene_data_loader.return_value = mock_loader
        
        with patch('builtins.exit') as mock_exit:
            with patch('builtins.print') as mock_print:
                main()
                
                mock_loader.process_data.assert_called_once()
                mock_print.assert_any_call("Error processing data: Processing error")
                mock_exit.assert_called_with(1)
