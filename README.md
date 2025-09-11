# PGNC External Stack - Python Components

[![Python](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![pytest](https://img.shields.io/badge/pytest-8.4+-green.svg)](https://pytest.org/)
[![Coverage](https://img.shields.io/badge/coverage-95%2B-brightgreen.svg)](./htmlcov/index.html)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

## Overview

The Python components of the PGNC External Stack provide essential data processing, database management, and search index maintenance functionality. These tools handle the complex operations required to maintain the PGNC gene nomenclature database and its associated search infrastructure.

### Key Capabilities

- **Gene Data Loading**: Import gene nomenclature data from CSV files into PostgreSQL database
- **Search Index Management**: Maintain Apache Solr search indices with real-time gene data
- **Data Processing**: Transform and validate gene nomenclature information
- **Database Operations**: Comprehensive CRUD operations for gene-related entities
- **Testing Infrastructure**: Extensive test coverage for data integrity and reliability

## Architecture

```
python/
├── bin/                    # Executable scripts and utilities
│   ├── data-load/         # Gene data import from CSV to database
│   ├── data-update/       # Solr index synchronization with database
│   └── update.sh          # Update orchestration script
├── tests/                 # Comprehensive test suites
│   ├── data-load/        # Tests for data loading functionality
│   └── data-update/      # Tests for Solr update functionality
├── input/                # Input data files (CSV, etc.)
├── output/               # Generated output files (JSON, logs)
└── htmlcov/             # Test coverage reports
```

## Components

### 1. Data Loading Module (`bin/data-load/`)

**Purpose**: Import gene nomenclature data from CSV files into the PostgreSQL database.

**Key Features**:

- CSV parsing and validation
- Database schema management
- Gene entity creation (symbols, names, locations, cross-references)
- Bulk data import operations
- Error handling and rollback capabilities

**Usage**:

```bash
cd bin/data-load
python main.py --file /path/to/gene_data.csv
```

**Database Entities Managed**:

- Genes (core gene records)
- Gene symbols (approved, alias, previous)
- Gene names (approved, alias, previous)
- Chromosomal locations
- Locus types (protein-coding, pseudogene, etc.)
- Cross-references (Ensembl, NCBI, UniProt, Phytozome)

### 2. Data Update Module (`bin/data-update/`)

**Purpose**: Synchronize Apache Solr search indices with the current database state.

**Key Features**:

- Real-time database-to-Solr synchronization
- JSON document generation for Solr indexing
- Index management (clear, update, bulk operations)
- Retry logic for network resilience
- Dry-run mode for testing

**Usage**:

```bash
cd bin/data-update
python main.py [--dump] [--dry-run] [--clear]
```

**Command Options**:

- `--dump`: Export Solr JSON to file without updating index
- `--dry-run`: Preview changes without applying them
- `--clear`: Clear existing Solr index before updating

**Environment Variables**:

```bash
DB_USER=postgres_username
DB_PASSWORD=postgres_password  
DB_HOST=database_host
DB_PORT=5432
DB_NAME=pgnc_database
```

## Installation

### Prerequisites

- Python 3.13 or higher (tested with 3.13.2)
- pip (Python package installer)
- Access to PostgreSQL 17.0 database
- Access to Apache Solr 8.x instance

### Setup

1. **Clone the repository** (if not already done):

```bash
git clone --recursive https://github.com/HGNC/pgnc-external-stack.git
cd pgnc-external-stack/python
```

2. **Create virtual environment** (recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Configure environment** (for data-update module):

```bash
# Copy and edit environment variables
cp ../.env.example .env
# Edit .env with your database and Solr configurations
```

## Dependencies

### Core Dependencies

- **psycopg2-binary** (2.9.10): PostgreSQL database adapter
- **pysolr** (3.10.0): Apache Solr client library
- **pandas** (2.2.3): Data manipulation and analysis
- **SQLAlchemy** (2.0.38): Database ORM and toolkit
- **numpy** (2.2.3): Numerical computing support

### Development Dependencies

- **pytest** (8.4.1): Testing framework
- **pytest-cov** (6.2.1): Coverage reporting
- **pytest-mock** (3.15.0): Mocking utilities

## Testing

### Test Coverage

The Python components maintain **95%+ test coverage** across all modules:

- **Data Load Tests**: 15 comprehensive test cases
- **Data Update Tests**: 19 comprehensive test cases  
- **Gene Model Tests**: 11 detailed validation tests
- **Integration Tests**: End-to-end workflow validation

### Running Tests

```bash
# Run all tests with coverage
pytest tests/ --cov=bin --cov-report=html

# Run specific test modules
pytest tests/data-load/ -v
pytest tests/data-update/ -v

# Run with detailed output
pytest tests/ -v --tb=short

# Generate coverage report
pytest tests/ --cov=bin --cov-report=term-missing
```

### Test Organization

```
tests/
├── data-load/
│   ├── test_main.py           # Main functionality tests
│   ├── test_csv_parsing.py    # CSV parsing validation
│   ├── test_database_ops.py   # Database operation tests
│   └── conftest.py           # Test fixtures and configuration
└── data-update/
    ├── test_main.py           # Solr update functionality
    ├── test_gene_model.py     # Gene model validation
    └── conftest.py           # Test fixtures and mocks
```

## Development

### Code Quality

The project maintains high code quality standards:

- **Type Hints**: Comprehensive type annotations using Python 3.13+ syntax
- **Pylance Compliance**: Zero pylance errors across all modules
- **Error Handling**: Robust exception handling with custom error types
- **Documentation**: Comprehensive docstrings following Google style

### Development Workflow

1. **Make changes** to the codebase
2. **Run tests** to ensure functionality: `pytest tests/`
3. **Check coverage**: `pytest tests/ --cov=bin --cov-report=term-missing`
4. **Validate types**: Ensure no pylance errors in your IDE
5. **Update documentation** as needed

### Adding New Features

1. **Create tests first** (TDD approach)
2. **Implement functionality** with proper type hints
3. **Update docstrings** with comprehensive descriptions
4. **Ensure 95%+ test coverage** for new code
5. **Update this README** if adding new modules

## Configuration

### Environment Variables (data-update)

| Variable | Description | Example |
|----------|-------------|---------|
| `DB_USER` | PostgreSQL username | `pgnc_user` |
| `DB_PASSWORD` | PostgreSQL password | `secure_password` |
| `DB_HOST` | Database host address | `localhost` |
| `DB_PORT` | Database port | `5432` |
| `DB_NAME` | Database name | `pgnc_db` |

### File Paths

| Directory | Purpose | Notes |
|-----------|---------|-------|
| `input/` | CSV files for data loading | Place source data files here |
| `output/` | Generated JSON and log files | Solr JSON exports and processing logs |
| `tests/` | Test suites and fixtures | Comprehensive test coverage |
| `htmlcov/` | Coverage reports | Generated by pytest-cov |

## Data Flow

### Data Loading Process

1. **CSV Input** → Parse gene nomenclature data
2. **Validation** → Verify data integrity and format
3. **Database Insertion** → Create gene entities and relationships  
4. **Verification** → Confirm successful data import

### Solr Update Process

1. **Database Query** → Retrieve current gene data
2. **JSON Generation** → Format data for Solr indexing
3. **Index Update** → Upload to Solr with retry logic
4. **Verification** → Confirm successful index update

## Performance Considerations

- **Batch Processing**: Large datasets processed in configurable chunks
- **Connection Pooling**: Efficient database connection management
- **Retry Logic**: Network resilience with exponential backoff
- **Memory Management**: Streaming processing for large files
- **Index Optimization**: Efficient Solr document structure

## Troubleshooting

### Common Issues

**Database Connection Errors**:

```bash
# Verify database connectivity
python -c "import psycopg2; print('Database module loaded')"
```

**Solr Connection Issues**:

```bash
# Test Solr connectivity
curl http://localhost:8983/solr/admin/ping
```

**Import Path Issues**:

```bash
# Ensure proper PYTHONPATH
export PYTHONPATH=/path/to/pgnc-external-stack/python/bin/data-update:$PYTHONPATH
```

**Test Failures**:

```bash
# Run with verbose output for debugging
pytest tests/ -v --tb=long
```

### Performance Optimization

- **Database Indexing**: Ensure proper indices on frequently queried columns
- **Batch Sizes**: Adjust batch sizes based on available memory
- **Connection Limits**: Configure appropriate database connection pools
- **Solr Heap**: Allocate sufficient heap memory for Solr operations

## Documentation

- **[Testing Summary](TESTING_SUMMARY.md)**: Detailed testing documentation
- **[Pylance Configuration](PYLANCE_CONFIG.md)**: IDE setup and type checking
- **Module Docstrings**: Comprehensive API documentation in source code
- **Type Hints**: Full type annotations for all public interfaces

## API Reference

### Data Loading

```python
from bin.data_load.main import load_gene_data

# Load gene data from CSV
load_gene_data(
    file_path='/path/to/genes.csv',
    batch_size=1000,
    validate=True
)
```

### Solr Updates

```python
from bin.data_update.main import update_solr_index

# Update Solr index
update_solr_index(
    dry_run=False,
    clear_existing=False
)
```

## Contributing

We welcome contributions to the Python components! Please follow these guidelines:

### Development Setup

1. **Fork and clone** the repository
2. **Create a virtual environment**: `python -m venv .venv`
3. **Install development dependencies**: `pip install -r requirements.txt`
4. **Run tests** to ensure everything works: `pytest tests/`

### Contribution Process

1. **Create a feature branch**: `git checkout -b feature/your-feature-name`
2. **Write tests first** (Test-Driven Development)
3. **Implement your changes** with proper type hints
4. **Ensure tests pass**: `pytest tests/ --cov=bin`
5. **Maintain 95%+ coverage**: `pytest tests/ --cov=bin --cov-report=term-missing`
6. **Update documentation** as needed
7. **Submit a pull request** with clear description

### Code Standards

- **Python 3.13+** compatibility required
- **Type hints** mandatory for all functions and methods
- **Docstrings** required for all public interfaces (Google style)
- **95%+ test coverage** required for new code
- **Pylance compliance** - zero type checking errors
- **Error handling** - comprehensive exception handling

### Testing Requirements

- All new functionality must include comprehensive tests
- Integration tests for database and Solr operations
- Mock external dependencies appropriately
- Test both success and failure scenarios
- Maintain existing test patterns and fixtures

## License

This project is licensed under the **GNU Affero General Public License v3.0** (AGPL-3.0).

### Key Points

- **Source Code Availability**: Any modifications must be made available under the same license
- **Network Use**: If you run modified code on a server, you must provide source code to users
- **Commercial Use**: Permitted with source disclosure requirements
- **Distribution**: Must include license and copyright notices
- **Patent Protection**: Express patent grant included

See the [LICENSE](LICENSE) file for complete terms and conditions.

---

## Support

- **Issues**: Report bugs and feature requests via GitHub Issues
- **Documentation**: See linked documentation files for detailed guidance
- **Community**: Follow PGNC contribution guidelines in the main repository

**Plant Gene Nomenclature Committee (PGNC)**  
*Advancing plant genomics through standardized gene nomenclature*
