"""
Pytest configuration and fixtures for all tests
"""
import os
import sys
from unittest.mock import Mock

# Add the bin directory to the path to import the modules
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
data_load_path = os.path.join(project_root, 'bin/data-load/db')
if data_load_path not in sys.path:
    sys.path.insert(0, data_load_path)

# Only mock db.models if we're not running model tests
# Check if we're in the models test directory
current_file = os.path.abspath(__file__)
models_test_dir = os.path.join(os.path.dirname(current_file), 'models')
is_model_test = any('models' in arg for arg in sys.argv)

if not is_model_test:
    # Mock the db.models modules to avoid import errors for insert tests
    mock_models = Mock()
    sys.modules['db'] = mock_models
    sys.modules['db.models'] = mock_models
    sys.modules['db.models.symbol'] = mock_models
    sys.modules['db.models.gene_has_symbol'] = mock_models
    sys.modules['db.models.name'] = mock_models
    sys.modules['db.models.gene_has_name'] = mock_models
    sys.modules['db.models.location'] = mock_models
    sys.modules['db.models.gene_has_location'] = mock_models
    sys.modules['db.models.locus_type'] = mock_models
    sys.modules['db.models.gene_has_locus_type'] = mock_models
    sys.modules['db.models.xref'] = mock_models
    sys.modules['db.models.gene_has_xref'] = mock_models

    # Mock the actual model classes
    mock_models.Symbol = Mock()
    mock_models.GeneHasSymbol = Mock()
    mock_models.Name = Mock()
    mock_models.GeneHasName = Mock()
    mock_models.Location = Mock()
    mock_models.GeneHasLocation = Mock()
    mock_models.LocusType = Mock()
    mock_models.GeneHasLocusType = Mock()
    mock_models.Xref = Mock()
    mock_models.GeneHasXref = Mock()
