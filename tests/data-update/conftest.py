"""
Test fixtures and configuration for data-update module tests
"""
import os
import sys
from http import HTTPStatus
from unittest.mock import Mock

import psycopg2
import pytest

# Setup paths
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
data_update_path = os.path.join(project_root, 'bin/data-update')
data_load_path = os.path.join(project_root, 'bin/data-load')

# Function to setup data-update imports
def setup_data_update_imports():
    # Clear any potentially interfering modules to avoid conflicts
    modules_to_clear = [
        'main', 'models', 'models.gene'
    ]
    
    for module in modules_to_clear:
        if module in sys.modules:
            del sys.modules[module]
    
    # Remove data-load path if it exists to avoid conflicts
    if data_load_path in sys.path:
        sys.path.remove(data_load_path)
    
    # Add the data-update directory to the Python path
    if data_update_path not in sys.path:
        sys.path.insert(0, data_update_path)

# Call setup function
setup_data_update_imports()


@pytest.fixture(autouse=True)
def ensure_data_update_imports():
    """Ensure data-update imports are properly configured before each test"""
    setup_data_update_imports()


@pytest.fixture
def mock_db_connection():
    """Mock psycopg2 database connection"""
    connection = Mock(spec=psycopg2.extensions.connection)
    cursor = Mock(spec=psycopg2.extensions.cursor)
    connection.cursor.return_value = cursor
    return connection


@pytest.fixture
def mock_cursor():
    """Mock database cursor"""
    cursor = Mock(spec=psycopg2.extensions.cursor)
    return cursor


@pytest.fixture
def sample_gene_row():
    """Sample gene row data from database"""
    return (1, 3702, 'approved', '1')


@pytest.fixture
def sample_xref_rows():
    """Sample cross-reference rows from database"""
    return [
        ('ENSG00000123456', 'Ensembl Gene'),
        ('12345', 'NCBI Gene'),
        ('P12345', 'UniProt'),
        ('Atg123456', 'Phytozome')
    ]


@pytest.fixture
def sample_locus_type_rows():
    """Sample locus type rows from database"""
    return [('protein-coding',), ('gene',)]


@pytest.fixture
def sample_symbol_rows():
    """Sample symbol rows from database"""
    return [
        ('TEST1', 'approved'),
        ('ALIAS1', 'alias'),
        ('ALIAS2', 'alias'),
        ('PREV1', 'prev')
    ]


@pytest.fixture
def sample_name_rows():
    """Sample name rows from database"""
    return [
        ('Test Gene 1', 'approved'),
        ('Test Alias Name 1', 'alias'),
        ('Test Previous Name 1', 'prev')
    ]


@pytest.fixture
def mock_gene():
    """Mock Gene object with sample data"""
    from models.gene import Gene  # type: ignore
    gene = Gene()
    gene.pgnc_id = 1
    gene.taxon_id = 3702
    gene.status = 'approved'
    gene.chromosome = '1'
    gene.gene_symbol_string = 'TEST1'
    gene.gene_name_string = 'Test Gene 1'
    gene.alias_gene_symbol_string = ['ALIAS1', 'ALIAS2']
    gene.alias_gene_name_string = ['Test Alias Name 1']
    gene.prev_gene_symbol_string = ['PREV1']
    gene.prev_gene_name_string = ['Test Previous Name 1']
    gene.locus_types = ['protein-coding', 'gene']
    gene.ensembl_gene_id = ['ENSG00000123456']
    gene.ncbi_gene_id = [12345]
    gene.uniprot_id = ['P12345']
    gene.phytozome_id = ['Atg123456']
    gene.primary_id = 'Atg123456'
    return gene


@pytest.fixture
def sample_solr_dict():
    """Sample dictionary for Solr indexing"""
    return {
        'pgnc_id': 'PGNC:1',
        'taxon_id': 3702,
        'chromosome': '1',
        'gene_symbol_string': 'TEST1',
        'gene_name_string': 'Test Gene 1',
        'locus_type': ['protein-coding', 'gene'],
        'status': 'approved',
        'alias_gene_symbol_string': ['ALIAS1', 'ALIAS2'],
        'alias_gene_name_string': ['Test Alias Name 1'],
        'prev_gene_symbol_string': ['PREV1'],
        'prev_gene_name_string': ['Test Previous Name 1'],
        'phytozome_id': ['Atg123456'],
        'ncbi_gene_id': [12345],
        'ensembl_gene_id': ['ENSG00000123456'],
        'uniprot_id': ['P12345'],
        'primary_id': 'Atg123456'
    }


@pytest.fixture
def sample_solr_json():
    """Sample JSON for Solr indexing"""
    return '''[
    {
        "pgnc_id": "PGNC:1",
        "taxon_id": 3702,
        "chromosome": "1",
        "gene_symbol_string": "TEST1",
        "gene_name_string": "Test Gene 1",
        "locus_type": ["protein-coding", "gene"],
        "status": "approved",
        "alias_gene_symbol_string": ["ALIAS1", "ALIAS2"],
        "alias_gene_name_string": ["Test Alias Name 1"],
        "prev_gene_symbol_string": ["PREV1"],
        "prev_gene_name_string": ["Test Previous Name 1"],
        "phytozome_id": ["Atg123456"],
        "ncbi_gene_id": [12345],
        "ensembl_gene_id": ["ENSG00000123456"],
        "uniprot_id": ["P12345"],
        "primary_id": "Atg123456"
    }
]'''


@pytest.fixture
def mock_solr():
    """Mock pysolr.Solr object"""
    solr = Mock()
    solr.add = Mock()
    solr.delete = Mock()
    return solr


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Mock environment variables for database connection"""
    monkeypatch.setenv("DB_USER", "test_user")
    monkeypatch.setenv("DB_PASSWORD", "test_password")
    monkeypatch.setenv("DB_HOST", "test_host")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_NAME", "test_db")


@pytest.fixture
def mock_solr_error():
    """Mock pysolr.SolrError with HTTP status code"""
    import pysolr
    error = pysolr.SolrError("HTTP 429 Too Many Requests")
    return error


@pytest.fixture
def retry_codes():
    """List of HTTP status codes that should trigger retries"""
    return [
        HTTPStatus.TOO_MANY_REQUESTS,
        HTTPStatus.INTERNAL_SERVER_ERROR,
        HTTPStatus.BAD_GATEWAY,
        HTTPStatus.SERVICE_UNAVAILABLE,
        HTTPStatus.GATEWAY_TIMEOUT,
    ]


@pytest.fixture
def sample_genes():
    """Provide sample Gene objects for testing"""
    # We'll need to import Gene here to avoid import issues
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../bin/data-update'))
    from models.gene import Gene  # type: ignore
    
    gene1 = Gene()
    gene1.pgnc_id = 123
    gene1.taxon_id = 3702
    gene1.chromosome = '1'
    gene1.gene_symbol_string = 'TEST1'
    gene1.gene_name_string = 'Test Gene'
    gene1.locus_types = ['protein-coding']
    gene1.status = 'approved'
    gene1.primary_id = 'Atg123'
    
    return [gene1]


# Clear any potentially interfering modules  
modules_to_clear = [
    'main', 'models', 'models.gene'
]

for module in modules_to_clear:
    if module in sys.modules:
        del sys.modules[module]
