"""
Integration tests for the data-load module
"""

import csv
import os
import tempfile
from unittest.mock import Mock, patch

import pandas as pd


class TestDataLoadIntegration:
    """Integration tests for the entire data loading process"""

    def test_complete_data_loading_workflow(self):
        """Test the complete workflow from CSV parsing to database processing"""
        # Create a temporary CSV file with comprehensive test data
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as temp_file:
            writer = csv.writer(temp_file)
            writer.writerow(
                [
                    "primary_id",
                    "primary_id_source",
                    "gene_symbol_string",
                    "gene_name_string",
                    "alias_symbol_string",
                    "alias_name_string",
                    "location_string",
                    "locus_type_string",
                    "external_id_ensembl",
                    "external_id_refseq",
                    "external_id_ucsc",
                ]
            )
            writer.writerow(
                [
                    "TEST.1",
                    "HGNC",
                    "TEST_SYMBOL",
                    "Test Gene Name",
                    "TEST_ALIAS",
                    "Test Alias Name",
                    "1q21.1",
                    "gene with protein product",
                    "ENSG123456",
                    "NM_123456",
                    "uc001abc.1",
                ]
            )
            temp_csv_path = temp_file.name

        try:
            from main import GeneDataLoader  # type: ignore

            # Mock database components
            with patch("main.sa.create_engine") as mock_create_engine:
                mock_engine = Mock()
                mock_create_engine.return_value = mock_engine

                with patch("main.sa.orm.sessionmaker") as mock_sessionmaker:
                    mock_session = Mock()
                    mock_session.__enter__ = Mock(return_value=mock_session)
                    mock_session.__exit__ = Mock(return_value=None)
                    mock_sessionmaker.return_value = Mock(return_value=mock_session)

                    # Mock database objects
                    mock_gene = Mock()
                    mock_gene.primary_id = "TEST.1"
                    mock_user = Mock()

                    with patch.object(
                        GeneDataLoader,
                        "_get_gene_and_creator",
                        return_value=(mock_gene, mock_user),
                    ):
                        with patch.object(GeneDataLoader, "_process_symbols"):
                            with patch.object(GeneDataLoader, "_process_names"):
                                with patch.object(GeneDataLoader, "_process_location"):
                                    with patch.object(
                                        GeneDataLoader, "_process_locus_type"
                                    ):
                                        with patch.object(
                                            GeneDataLoader, "_process_crossrefs"
                                        ):
                                            # Initialize and process
                                            loader = GeneDataLoader(temp_csv_path)

                                            # Verify CSV was parsed correctly
                                            assert loader.df is not None
                                            assert len(loader.df) == 1
                                            assert (
                                                loader.df.iloc[0]["primary_id"]
                                                == "TEST.1"
                                            )

                                            # Process the data
                                            loader.process_data()

                                            # Verify database interactions
                                            mock_create_engine.assert_called_once()
                                            mock_engine.dispose.assert_called_once()
                                            # Note: Since all the processing methods are mocked,
                                            # session.add might not be called in the test, but that's expected
                                            mock_session.commit.assert_called_once()

        finally:
            # Clean up temporary file
            os.unlink(temp_csv_path)

    def test_error_handling_during_workflow(self):
        """Test error handling during the complete workflow"""
        # Create a minimal CSV file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as temp_file:
            writer = csv.writer(temp_file)
            writer.writerow(["primary_id", "primary_id_source", "gene_symbol_string"])
            writer.writerow(["ERROR.1", "HGNC", "ERROR_SYMBOL"])
            temp_csv_path = temp_file.name

        try:
            from main import GeneDataLoader  # type: ignore

            # Mock database components
            with patch("main.sa.create_engine") as mock_create_engine:
                mock_engine = Mock()
                mock_create_engine.return_value = mock_engine

                with patch("main.sa.orm.sessionmaker") as mock_sessionmaker:
                    mock_session = Mock()
                    mock_session.__enter__ = Mock(return_value=mock_session)
                    mock_session.__exit__ = Mock(return_value=None)
                    mock_sessionmaker.return_value = Mock(return_value=mock_session)

                    # Mock database objects
                    mock_gene = Mock()
                    mock_gene.primary_id = "ERROR.1"
                    mock_user = Mock()

                    # Mock _get_gene_and_creator to succeed, but _process_symbols to raise an exception
                    # This ensures the exception occurs within the try-catch block that handles rollback
                    with patch.object(
                        GeneDataLoader,
                        "_get_gene_and_creator",
                        return_value=(mock_gene, mock_user),
                    ):
                        with patch.object(
                            GeneDataLoader,
                            "_process_symbols",
                            side_effect=Exception("Database error"),
                        ):
                            with patch("builtins.print") as mock_print:
                                loader = GeneDataLoader(temp_csv_path)
                                loader.process_data()

                                # Verify error handling
                                mock_session.rollback.assert_called_once()
                                # Check that the error message was printed
                                error_calls = [
                                    str(call) for call in mock_print.call_args_list
                                ]
                                error_found = any(
                                    "Error processing row 0: Database error" in call
                                    for call in error_calls
                                )
                                assert error_found, (
                                    f"Expected error message not found in calls: {error_calls}"
                                )

        finally:
            # Clean up temporary file
            os.unlink(temp_csv_path)

    def test_csv_validation_edge_cases(self):
        """Test CSV validation with various edge cases"""
        from main import GeneDataLoader  # type: ignore

        # Test with non-existent file
        loader = GeneDataLoader.__new__(GeneDataLoader)
        loader.file_path = "/non/existent/file.csv"

        with patch("builtins.print") as mock_print:
            result = loader.parse_csv()
            assert result is None
            mock_print.assert_called_with(
                "Error: File not found at path: /non/existent/file.csv"
            )

        # Test with empty file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as temp_file:
            temp_empty_path = temp_file.name

        try:
            loader.file_path = temp_empty_path
            with patch("builtins.print") as mock_print:
                result = loader.parse_csv()
                assert result is None
                mock_print.assert_called_with("Error: The CSV file is empty.")

        finally:
            os.unlink(temp_empty_path)

    def test_data_processing_without_dataframe(self):
        """Test data processing when no DataFrame is available"""
        from main import GeneDataLoader  # type: ignore

        loader = GeneDataLoader.__new__(GeneDataLoader)
        loader.df = None

        with patch("builtins.print") as mock_print:
            loader.process_data()
            mock_print.assert_called_with(
                "No data to process. Ensure the CSV file was loaded correctly."
            )

    def test_main_function_integration(self):
        """Test the main function with argument parsing and processing"""
        # Create a test CSV file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as temp_file:
            writer = csv.writer(temp_file)
            writer.writerow(["primary_id", "gene_symbol_string"])
            writer.writerow(["MAIN.1", "MAIN_SYMBOL"])
            temp_csv_path = temp_file.name

        try:
            from main import main  # type: ignore

            # Mock command line arguments
            with patch("main.argparse.ArgumentParser") as mock_argument_parser:
                mock_args = Mock()
                mock_args.file = temp_csv_path
                mock_parser = Mock()
                mock_parser.parse_args.return_value = mock_args
                mock_argument_parser.return_value = mock_parser

                # Mock GeneDataLoader and database dump
                with patch("main.GeneDataLoader") as mock_gene_data_loader:
                    mock_loader = Mock()
                    mock_loader.df = Mock()  # Not None
                    mock_gene_data_loader.return_value = mock_loader

                    with patch("main.dump_db") as mock_dump_db:
                        with patch("builtins.print") as mock_print:
                            with patch.dict(
                                "main.os.environ",
                                {
                                    "DB_HOST": "localhost",
                                    "DB_PORT": "5432",
                                    "DB_USER": "testuser",
                                    "DB_NAME": "testdb",
                                },
                            ):
                                main()

                                # Verify the complete workflow
                                mock_gene_data_loader.assert_called_once_with(
                                    temp_csv_path
                                )
                                mock_loader.process_data.assert_called_once()
                                mock_dump_db.assert_called_once()
                                mock_print.assert_any_call("Dumping database...")

        finally:
            os.unlink(temp_csv_path)

    def test_database_dump_functionality(self):
        """Test database dump functionality"""
        from main import dump_db  # type: ignore

        # Test successful dump
        with patch("main.gzip.open") as mock_gzip_open:
            mock_file = Mock()
            mock_gzip_open.return_value.__enter__.return_value = mock_file

            with patch("main.subprocess.Popen") as mock_popen:
                mock_process = Mock()
                mock_process.stdout.readline.side_effect = ["line1\n", "line2\n", ""]
                mock_popen.return_value = mock_process

                dump_db(("pg_dump", "-h", "localhost"), "test.sql")

                mock_gzip_open.assert_called_once_with(
                    "/usr/src/app/db-data/test.sql", "wb"
                )
                mock_popen.assert_called_once()

    def test_pandas_dataframe_operations(self):
        """Test pandas DataFrame operations used in the data loader"""
        # Create test data
        test_data = {
            "primary_id": ["TEST.1", "TEST.2"],
            "gene_symbol_string": ["SYMBOL1", "SYMBOL2"],
            "gene_name_string": ["Name 1", "Name 2"],
        }
        df = pd.DataFrame(test_data)

        # Test DataFrame iteration (as used in process_data)
        for index, row in df.iterrows():
            assert "primary_id" in row
            assert "gene_symbol_string" in row
            assert "gene_name_string" in row
            assert isinstance(index, int)
            assert isinstance(row, pd.Series)

        # Test column access patterns used in the code
        assert df["primary_id"].iloc[0] == "TEST.1"
        assert df.iloc[0]["gene_symbol_string"] == "SYMBOL1"

        # Test empty/null handling
        df_with_nulls = df.copy()
        df_with_nulls.loc[0, "gene_name_string"] = None
        assert pd.isna(df_with_nulls.iloc[0]["gene_name_string"])

    def test_error_propagation_patterns(self):
        """Test error propagation patterns used throughout the code"""
        from main import GeneDataLoader  # type: ignore

        loader = GeneDataLoader.__new__(GeneDataLoader)

        # Test ValueError propagation in symbol processing
        mock_session = Mock()
        mock_gene = Mock()
        mock_gene.primary_id = "TEST.1"
        mock_user = Mock()

        # Create test row with required data
        row = pd.Series({"primary_id": "TEST.1", "gene_symbol_string": "TEST_SYMBOL"})

        # Mock _process_approved_symbol to raise ValueError
        with patch.object(
            loader, "_process_approved_symbol", side_effect=ValueError("Symbol exists")
        ):
            with patch.object(loader, "_process_alias_symbols"):
                with patch("builtins.print") as mock_print:
                    # This should catch the ValueError and print a message
                    loader._process_symbols(mock_session, row, mock_gene, mock_user)

                    # Verify error message was printed (use string matching to avoid pandas Series comparison)
                    error_calls = [str(call) for call in mock_print.call_args_list]
                    error_found = any(
                        "already has approved symbol TEST_SYMBOL. Skipping" in call
                        for call in error_calls
                    )
                    assert error_found, (
                        f"Expected error message not found in calls: {error_calls}"
                    )


class TestDataLoadPerformance:
    """Performance-related tests for data loading"""

    def test_large_csv_handling(self):
        """Test handling of larger CSV files"""
        # Create a larger test CSV file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as temp_file:
            writer = csv.writer(temp_file)
            writer.writerow(["primary_id", "gene_symbol_string", "gene_name_string"])

            # Write 100 test rows
            for i in range(100):
                writer.writerow([f"TEST.{i}", f"SYMBOL_{i}", f"Gene Name {i}"])

            temp_csv_path = temp_file.name

        try:
            from main import GeneDataLoader  # type: ignore

            loader = GeneDataLoader.__new__(GeneDataLoader)
            loader.file_path = temp_csv_path

            # Parse the CSV
            df = loader.parse_csv()

            # Verify it can handle the larger dataset
            assert df is not None
            assert len(df) == 100
            assert df.iloc[0]["primary_id"] == "TEST.0"
            assert df.iloc[99]["primary_id"] == "TEST.99"

        finally:
            os.unlink(temp_csv_path)

    def test_memory_usage_patterns(self):
        """Test memory usage patterns in data processing"""
        from main import GeneDataLoader  # type: ignore

        # Create test data
        test_data = {
            "primary_id": ["TEST.1", "TEST.2", "TEST.3"],
            "gene_symbol_string": ["SYMBOL1", "SYMBOL2", "SYMBOL3"],
        }
        df = pd.DataFrame(test_data)

        loader = GeneDataLoader.__new__(GeneDataLoader)
        loader.df = df

        # Mock engine and session
        mock_engine = Mock()

        with patch("main.sa.create_engine", return_value=mock_engine):
            with patch.object(
                loader, "_process_row", return_value=True
            ) as mock_process_row:
                with patch("builtins.print"):
                    loader.process_data()

                    # Verify each row was processed individually (memory efficient)
                    assert mock_process_row.call_count == 3

                    # Verify engine was properly disposed
                    mock_engine.dispose.assert_called_once()
