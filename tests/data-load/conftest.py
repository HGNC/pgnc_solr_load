"""
Pytest configuration specific for data-load tests
"""
import os
import sys
import tempfile
from unittest.mock import Mock

import pandas as pd
import pytest

# Store original sys.path to restore later
_original_sys_path = sys.path.copy()

# Setup paths
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
data_load_path = os.path.join(project_root, 'bin/data-load')
data_update_path = os.path.join(project_root, 'bin/data-update')

# Function to setup data-load imports
def setup_data_load_imports():
    # Clear any potentially interfering modules to avoid conflicts
    modules_to_clear = [
        'main', 'db', 'db.config', 'db.models', 'db.enum_types', 'db.insert'
    ]
    
    for module in modules_to_clear:
        if module in sys.modules:
            del sys.modules[module]
    
    # Remove data-update path if it exists to avoid conflicts
    if data_update_path in sys.path:
        sys.path.remove(data_update_path)
    
    # Add data-load path
    if data_load_path not in sys.path:
        sys.path.insert(0, data_load_path)
    
    # Also add the db path for imports
    db_path = os.path.join(data_load_path, 'db')
    if db_path not in sys.path:
        sys.path.insert(0, db_path)

# Call setup function
setup_data_load_imports()


@pytest.fixture(autouse=True)
def ensure_data_load_imports():
    """Ensure data-load imports are properly configured before each test"""
    setup_data_load_imports()


@pytest.fixture
def sample_csv_content():
    """Sample CSV content for testing"""
    return """primary_id,primary_id_source,gene_symbol_string,gene_name_string,gene_alt_symbol,gene_alt_name,chromosome,map_location,locus_type,external_id_ensembl,external_id_refseq,external_id_ucsc
Phytozome.1.1,phytozome,SYMBOL1,Gene Name 1,ALT_SYM1,Alt Name 1,1,1q21.1,protein-coding,ENSEMBL1,REFSEQ1,UCSC1
Phytozome.1.2,phytozome,SYMBOL2,Gene Name 2,ALT_SYM2,Alt Name 2,2,2p13.3,pseudogene,ENSEMBL2,REFSEQ2,UCSC2"""


@pytest.fixture
def sample_csv_file(sample_csv_content):
    """Create a temporary CSV file for testing"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(sample_csv_content)
        f.flush()
        yield f.name
    os.unlink(f.name)


@pytest.fixture
def empty_csv_file():
    """Create an empty CSV file for testing"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("")
        f.flush()
        yield f.name
    os.unlink(f.name)


@pytest.fixture
def malformed_csv_file():
    """Create a malformed CSV file for testing"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("primary_id,gene_symbol\nvalue1\nvalue2,value3,extra_value")
        f.flush()
        yield f.name
    os.unlink(f.name)


@pytest.fixture
def sample_dataframe():
    """Sample pandas DataFrame for testing"""
    return pd.DataFrame({
        'primary_id': ['Phytozome.1.1', 'Phytozome.1.2'],
        'primary_id_source': ['phytozome', 'phytozome'],
        'gene_symbol_string': ['SYMBOL1', 'SYMBOL2'],
        'gene_name_string': ['Gene Name 1', 'Gene Name 2'],
        'gene_alt_symbol': ['ALT_SYM1', 'ALT_SYM2'],
        'gene_alt_name': ['Alt Name 1', 'Alt Name 2'],
        'chromosome': ['1', '2'],
        'map_location': ['1q21.1', '2p13.3'],
        'locus_type': ['protein-coding', 'pseudogene'],
        'external_id_ensembl': ['ENSEMBL1', 'ENSEMBL2'],
        'external_id_refseq': ['REFSEQ1', 'REFSEQ2'],
        'external_id_ucsc': ['UCSC1', 'UCSC2']
    })


@pytest.fixture
def mock_engine():
    """Mock SQLAlchemy engine"""
    engine = Mock()
    engine.dispose = Mock()
    return engine


@pytest.fixture
def mock_session():
    """Mock SQLAlchemy session"""
    session = Mock()
    session.query = Mock()
    session.add = Mock()
    session.commit = Mock()
    session.rollback = Mock()
    session.flush = Mock()
    session.refresh = Mock()
    return session


@pytest.fixture
def mock_gene():
    """Mock Gene model object"""
    gene = Mock()
    gene.id = 1
    gene.primary_id = "Phytozome.1.1"
    gene.primary_id_source = "phytozome"
    gene.status = Mock()
    return gene


@pytest.fixture
def mock_user():
    """Mock User model object"""
    user = Mock()
    user.id = 1
    user.email = "sart2@cam.ac.uk"
    return user


@pytest.fixture
def mock_symbol():
    """Mock Symbol model object"""
    symbol = Mock()
    symbol.id = 1
    symbol.symbol = "TEST_SYMBOL"
    symbol.symbol_has_genes = []
    return symbol


@pytest.fixture
def sample_row():
    """Sample pandas Series representing a CSV row"""
    return pd.Series({
        'primary_id': 'Phytozome.1.1',
        'primary_id_source': 'phytozome',
        'gene_symbol_string': 'SYMBOL1',
        'gene_name_string': 'Gene Name 1',
        'gene_alt_symbol': 'ALT_SYM1',
        'gene_alt_name': 'Alt Name 1',
        'chromosome': '1',
        'map_location': '1q21.1',
        'locus_type': 'protein-coding',
        'external_id_ensembl': 'ENSEMBL1',
        'external_id_refseq': 'REFSEQ1',
        'external_id_ucsc': 'UCSC1',
        'ncbi_gene_id': 'NCBI123',
        'uniprot_id': 'UNIPROT123',
        'pubmed_id': 'PUBMED123'
    })


