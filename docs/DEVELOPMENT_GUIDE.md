# Development Guide

## 🚀 Getting Started with Development

This guide provides comprehensive information for developers working on the PGNC External Stack Python project.

## 🏗️ Development Environment Setup

### Prerequisites

Before starting development, ensure you have:

- **Python 3.13+** installed
- **Git** for version control
- **PostgreSQL 13+** database access
- **Apache Solr 8+** instance
- **IDE** with Python support (VS Code recommended)

### Environment Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/HGNC/pgnc-external-stack.git
   cd pgnc-external-stack/python
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   # Install all dependencies including development tools
   pip install -r requirements.txt
   
   # Verify installation
   python -c "import pytest, pandas, sqlalchemy; print('All dependencies installed successfully')"
   ```

4. **Configure IDE (VS Code)**
   ```bash
   # Install recommended extensions
   code --install-extension ms-python.python
   code --install-extension ms-python.pylance
   
   # Open project
   code .
   ```

5. **Set Up Environment Variables**
   ```bash
   # Copy example environment file
   cp ../.env.example .env
   
   # Edit .env with your settings
   nano .env
   ```

### IDE Configuration

#### VS Code Settings (`.vscode/settings.json`)

```json
{
    "python.defaultInterpreterPath": "./.venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.pycodestyleEnabled": false,
    "python.analysis.typeCheckingMode": "strict",
    "python.analysis.extraPaths": [
        "./bin/data-load",
        "./bin/data-update"
    ],
    "pytest.enabled": true,
    "pytest.args": [
        "tests/"
    ],
    "files.exclude": {
        "**/__pycache__": true,
        "**/.pytest_cache": true,
        "**/htmlcov": true
    }
}
```

## 📝 Coding Standards

### Code Style Guidelines

We follow strict coding standards to ensure consistency and maintainability:

#### 1. Python Style Guide

- **PEP 8** compliance for basic formatting
- **Google-style docstrings** for all public functions
- **Type hints** mandatory for all function signatures
- **Maximum line length**: 88 characters (Black formatter)

#### 2. Naming Conventions

```python
# Classes: PascalCase
class GeneDataLoader:
    pass

# Functions/Variables: snake_case
def process_gene_data():
    gene_count = 0
    
# Constants: UPPER_SNAKE_CASE
DATABASE_TIMEOUT = 30

# Private methods: leading underscore
def _process_internal_data():
    pass
```

#### 3. Type Annotations

All functions must include comprehensive type hints:

```python
from typing import Optional, List, Dict, Any, Tuple

def process_gene_symbols(
    symbols: List[str], 
    gene_id: int,
    validate: bool = True
) -> Optional[Dict[str, Any]]:
    """
    Process gene symbols for database insertion.
    
    Args:
        symbols: List of symbol strings to process.
        gene_id: Database ID of the associated gene.
        validate: Whether to perform validation checks.
        
    Returns:
        Dictionary of processed symbol data, or None if processing fails.
        
    Raises:
        ValueError: If symbol data is invalid.
        DatabaseError: If database operations fail.
    """
    pass
```

#### 4. Docstring Standards

Use Google-style docstrings for all public functions:

```python
def load_gene_data(file_path: str, batch_size: int = 1000) -> bool:
    """
    Load gene data from CSV file into database.
    
    This function reads gene nomenclature data from a CSV file and imports
    it into the PostgreSQL database with proper validation and error handling.
    
    Args:
        file_path: Path to the CSV file containing gene data.
        batch_size: Number of records to process in each batch. Default is 1000.
        
    Returns:
        True if loading succeeds, False otherwise.
        
    Raises:
        FileNotFoundError: If the specified CSV file doesn't exist.
        DatabaseError: If database connection or operations fail.
        ValidationError: If CSV data doesn't meet required format.
        
    Example:
        >>> success = load_gene_data('/path/to/genes.csv', batch_size=500)
        >>> if success:
        ...     print("Data loaded successfully")
    """
    pass
```

### Error Handling Patterns

#### 1. Exception Hierarchy

```python
# Custom exception hierarchy
class PGNCError(Exception):
    """Base exception for PGNC-specific errors."""
    pass

class DataValidationError(PGNCError):
    """Raised when input data fails validation."""
    
    def __init__(self, message: str, invalid_data: Any = None):
        super().__init__(message)
        self.invalid_data = invalid_data

class DatabaseError(PGNCError):
    """Raised when database operations fail."""
    
    def __init__(self, message: str, query: str = None):
        super().__init__(message)
        self.query = query
```

#### 2. Error Handling Best Practices

```python
def process_gene_row(session: Session, row: pd.Series, index: int) -> bool:
    """Process a single gene data row with comprehensive error handling."""
    
    # Early validation of required fields
    primary_id = row.get("primary_id", None)
    if primary_id is None:
        logger.warning(f"Row {index} is missing primary_id:")
        logger.warning(row.to_dict())
        return False
        
    primary_id_source = row.get("primary_id_source", None)
    if primary_id_source is None:
        logger.warning(f"Row {index} is missing primary_id_source:")
        logger.warning(row.to_dict())
        return False
    
    try:
        # Validate additional data
        if not _validate_gene_data(row):
            raise DataValidationError(f"Invalid gene data: {row.to_dict()}")
        
        # Process the data
        gene = _create_gene_entity(row)
        session.add(gene)
        session.commit()
        
        logger.info(f"Successfully processed gene: {row['primary_id']}")
        return True
        
    except DataValidationError as e:
        logger.warning(f"Validation failed for row {index}: {e}")
        session.rollback()
        return False
        
    except DatabaseError as e:
        logger.error(f"Database error processing row {index}: {e}")
        session.rollback()
        return False
        
    except Exception as e:
        logger.error(f"Unexpected error processing row {index}: {e}")
        session.rollback()
        raise  # Re-raise unexpected errors
```

## 🧪 Testing Guidelines

### Test-Driven Development (TDD)

We follow TDD principles for all new features:

1. **Write tests first** before implementing functionality
2. **Run tests** to ensure they fail initially
3. **Implement** minimum code to make tests pass
4. **Refactor** while keeping tests green
5. **Repeat** for each new feature or bug fix

### Test Structure

#### 1. Test Organization

```
tests/
├── unit/                    # Unit tests for individual components
│   ├── test_gene_loader.py
│   ├── test_symbol_processor.py
│   └── test_database_models.py
├── integration/             # Integration tests for component interaction
│   ├── test_data_pipeline.py
│   └── test_solr_integration.py
├── fixtures/                # Test data and fixtures
│   ├── sample_data.csv
│   └── test_database.sql
└── conftest.py             # Shared test configuration
```

#### 2. Test Writing Patterns

```python
import pytest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd

class TestGeneDataLoader:
    """Test suite for GeneDataLoader class."""
    
    def test_init_with_valid_csv(self, sample_csv_file):
        """Test GeneDataLoader initialization with valid CSV file."""
        # Arrange
        expected_columns = ['primary_id', 'gene_symbol_string']
        
        # Act
        loader = GeneDataLoader(sample_csv_file)
        
        # Assert
        assert loader.file_path == sample_csv_file
        assert loader.df is not None
        assert all(col in loader.df.columns for col in expected_columns)
    
    def test_parse_csv_file_not_found(self):
        """Test CSV parsing with non-existent file."""
        # Arrange
        non_existent_file = "/path/to/non/existent/file.csv"
        
        # Act & Assert
        with pytest.raises(FileNotFoundError):
            GeneDataLoader(non_existent_file)
    
    @patch('main.sa.create_engine')
    def test_process_data_success(self, mock_create_engine, sample_dataframe):
        """Test successful data processing with mocked database."""
        # Arrange
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine
        
        loader = GeneDataLoader.__new__(GeneDataLoader)
        loader.df = sample_dataframe
        
        # Act
        with patch.object(loader, '_process_row', return_value=True) as mock_process:
            loader.process_data()
        
        # Assert
        assert mock_process.call_count == len(sample_dataframe)
        mock_engine.dispose.assert_called_once()
```

#### 3. Fixture Patterns

```python
# conftest.py
import pytest
import pandas as pd
from unittest.mock import Mock

@pytest.fixture
def sample_gene_data():
    """Sample gene data for testing."""
    return {
        'primary_id': 'TEST.1.1',
        'primary_id_source': 'test_source',
        'gene_symbol_string': 'TEST_SYMBOL',
        'gene_name_string': 'Test Gene Name',
        'chromosome': '1',
        'locus_type': 'protein-coding'
    }

@pytest.fixture
def sample_dataframe(sample_gene_data):
    """Sample pandas DataFrame for testing."""
    return pd.DataFrame([sample_gene_data])

@pytest.fixture
def mock_database_session():
    """Mock database session for testing."""
    session = Mock()
    session.query.return_value.filter.return_value.first.return_value = None
    session.add = Mock()
    session.commit = Mock()
    session.rollback = Mock()
    return session
```

### Test Coverage Requirements

- **Minimum coverage**: 95% for all new code
- **Critical paths**: 100% coverage for data processing logic
- **Error scenarios**: Comprehensive testing of error conditions
- **Integration points**: Full coverage of external system interactions

#### Running Coverage Analysis

```bash
# Generate coverage report
pytest tests/ --cov=bin --cov-report=html --cov-report=term-missing

# View HTML report
open htmlcov/index.html

# Check coverage threshold
pytest tests/ --cov=bin --cov-fail-under=95
```

## 🔧 Development Workflow

### Git Workflow

We use **GitFlow** for branch management:

#### 1. Branch Types

- **main**: Production-ready code
- **develop**: Integration branch for features
- **feature/**: New features (`feature/gene-validation`)
- **hotfix/**: Critical bug fixes (`hotfix/csv-parsing-error`)
- **release/**: Release preparation (`release/v1.2.0`)

#### 2. Typical Workflow

```bash
# Start new feature
git checkout develop
git pull origin develop
git checkout -b feature/new-gene-processor

# Make changes
git add .
git commit -m "Add new gene processing functionality

- Implement enhanced validation logic
- Add support for new CSV format
- Update tests for new functionality"

# Push feature branch
git push -u origin feature/new-gene-processor

# Create pull request
gh pr create --title "Add new gene processor" --body "Detailed description..."

# After review and approval
git checkout develop
git pull origin develop
git branch -d feature/new-gene-processor
```

#### 3. Commit Message Format

Follow **Conventional Commits** specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Examples:
```bash
feat(data-load): add support for new CSV format
fix(solr): resolve connection timeout issues
docs(api): update API documentation for new endpoints
test(integration): add comprehensive pipeline tests
```

### Code Review Process

#### 1. Pull Request Checklist

Before submitting a PR, ensure:

- [ ] All tests pass (`pytest tests/`)
- [ ] Code coverage meets requirements (95%+)
- [ ] Type checking passes (no Pylance errors)
- [ ] Documentation is updated
- [ ] Commit messages follow conventions
- [ ] No merge conflicts with target branch

#### 2. Review Criteria

Reviewers should check:

- **Functionality**: Does the code solve the intended problem?
- **Testing**: Are there comprehensive tests covering the changes?
- **Design**: Is the code well-structured and maintainable?
- **Performance**: Are there any performance implications?
- **Security**: Are there any security considerations?
- **Documentation**: Is the code properly documented?

### Continuous Integration

#### 1. Automated Checks

Our CI pipeline runs:

```yaml
# .github/workflows/test.yml
name: Test Suite
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run type checking
        run: |
          pylance bin/ tests/
      
      - name: Run tests with coverage
        run: |
          pytest tests/ --cov=bin --cov-fail-under=95
      
      - name: Upload coverage reports
        uses: codecov/codecov-action@v3
```

#### 2. Quality Gates

All PRs must pass:
- ✅ Type checking (Pylance)
- ✅ Test suite (100% pass rate)
- ✅ Coverage threshold (95%+)
- ✅ Code style checks
- ✅ Security scans

## 🏗️ Architecture Guidelines

### Module Design Principles

#### 1. Single Responsibility

Each module should have one clear purpose:

```python
# Good: Single responsibility
class CSVParser:
    """Handles only CSV file parsing logic."""
    def parse_file(self, file_path: str) -> pd.DataFrame: ...

class GeneValidator:
    """Handles only gene data validation."""
    def validate_gene_data(self, data: dict) -> bool: ...

# Avoid: Multiple responsibilities
class GeneProcessor:
    """Handles parsing, validation, AND database operations."""  # Too broad
```

#### 2. Dependency Injection

Use dependency injection for testability:

```python
# Good: Dependencies injected
class GeneDataLoader:
    def __init__(
        self, 
        parser: CSVParser, 
        validator: GeneValidator,
        database: Database
    ):
        self.parser = parser
        self.validator = validator
        self.database = database

# Better: Use interfaces/protocols
from typing import Protocol

class DatabaseProtocol(Protocol):
    def save_gene(self, gene: Gene) -> bool: ...

class GeneDataLoader:
    def __init__(self, database: DatabaseProtocol):
        self.database = database
```

#### 3. Error Boundaries

Implement clear error boundaries:

```python
def process_gene_file(file_path: str) -> ProcessingResult:
    """Process gene file with clear error boundaries."""
    try:
        # Parse CSV
        data = csv_parser.parse(file_path)
        
        # Validate data
        validation_result = validator.validate(data)
        if not validation_result.is_valid:
            return ProcessingResult.failed(validation_result.errors)
        
        # Save to database
        save_result = database.save_genes(data)
        if not save_result.success:
            return ProcessingResult.failed(save_result.errors)
        
        return ProcessingResult.success(save_result.gene_count)
        
    except FileNotFoundError:
        return ProcessingResult.failed(["File not found"])
    except Exception as e:
        logger.exception("Unexpected error processing gene file")
        return ProcessingResult.failed([f"Unexpected error: {str(e)}"])
```

### Database Design Patterns

#### 1. Repository Pattern

```python
from abc import ABC, abstractmethod
from typing import List, Optional

class GeneRepository(ABC):
    """Abstract repository for gene operations."""
    
    @abstractmethod
    def get_by_id(self, gene_id: int) -> Optional[Gene]: ...
    
    @abstractmethod
    def get_by_primary_id(self, primary_id: str) -> Optional[Gene]: ...
    
    @abstractmethod
    def save(self, gene: Gene) -> Gene: ...
    
    @abstractmethod
    def delete(self, gene_id: int) -> bool: ...

class SQLAlchemyGeneRepository(GeneRepository):
    """SQLAlchemy implementation of gene repository."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_by_id(self, gene_id: int) -> Optional[Gene]:
        return self.session.query(Gene).filter(Gene.id == gene_id).first()
    
    def save(self, gene: Gene) -> Gene:
        self.session.add(gene)
        self.session.commit()
        return gene
```

#### 2. Unit of Work Pattern

```python
class UnitOfWork:
    """Manages database transactions and repository access."""
    
    def __init__(self, session_factory):
        self.session_factory = session_factory
        
    def __enter__(self):
        self.session = self.session_factory()
        self.genes = SQLAlchemyGeneRepository(self.session)
        self.symbols = SQLAlchemySymbolRepository(self.session)
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()

# Usage
with UnitOfWork(session_factory) as uow:
    gene = uow.genes.get_by_id(123)
    gene.status = GeneStatusEnum.approved
    uow.genes.save(gene)
    # Automatically committed when exiting context
```

## 📈 Performance Guidelines

### Database Optimization

#### 1. Batch Processing

```python
def bulk_insert_genes(genes: List[Gene], batch_size: int = 1000) -> None:
    """Insert genes in batches for better performance."""
    with session_scope() as session:
        for i in range(0, len(genes), batch_size):
            batch = genes[i:i + batch_size]
            session.bulk_insert_mappings(Gene, [gene.to_dict() for gene in batch])
            session.commit()
            logger.info(f"Inserted batch {i//batch_size + 1}, {len(batch)} genes")
```

#### 2. Connection Pooling

```python
# Database configuration with connection pooling
engine = create_engine(
    DATABASE_URI,
    pool_size=20,           # Number of connections to maintain
    max_overflow=30,        # Additional connections when pool is full
    pool_timeout=30,        # Seconds to wait for connection
    pool_recycle=3600,      # Recycle connections after 1 hour
    echo=False              # Set to True for SQL debugging
)
```

#### 3. Query Optimization

```python
# Good: Use joins instead of N+1 queries
def get_genes_with_symbols() -> List[Gene]:
    return session.query(Gene)\
        .join(GeneHasSymbol)\
        .join(Symbol)\
        .options(selectinload(Gene.symbols))\
        .all()

# Avoid: N+1 query pattern
def get_genes_with_symbols_bad() -> List[Gene]:
    genes = session.query(Gene).all()
    for gene in genes:
        gene.symbols = session.query(Symbol)\
            .join(GeneHasSymbol)\
            .filter(GeneHasSymbol.gene_id == gene.id)\
            .all()  # This executes N queries!
    return genes
```

### Memory Management

#### 1. Streaming Processing

```python
def process_large_csv(file_path: str, chunk_size: int = 10000) -> None:
    """Process large CSV files in chunks to manage memory."""
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        process_gene_chunk(chunk)
        # Memory is freed after each chunk
```

#### 2. Generator Patterns

```python
def get_all_genes() -> Iterator[Gene]:
    """Generator to iterate over all genes without loading into memory."""
    offset = 0
    batch_size = 1000
    
    while True:
        genes = session.query(Gene)\
            .offset(offset)\
            .limit(batch_size)\
            .all()
        
        if not genes:
            break
            
        for gene in genes:
            yield gene
            
        offset += batch_size

# Usage
for gene in get_all_genes():
    process_gene(gene)  # Process one at a time
```

## 🚀 Deployment Guidelines

### Environment Configuration

#### 1. Environment-Specific Settings

```python
# config.py
import os
from enum import Enum

class Environment(Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"

class Config:
    """Base configuration."""
    
    # Common settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Environment-specific
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """Development configuration."""
    
    DEBUG = True
    DATABASE_URI = os.environ.get('DEV_DATABASE_URL', 
                                 'postgresql://localhost/pgnc_dev')

class ProductionConfig(Config):
    """Production configuration."""
    
    DEBUG = False
    DATABASE_URI = os.environ.get('DATABASE_URL')
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Log to syslog in production
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```

#### 2. Container Configuration

```dockerfile
# Dockerfile
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app/bin/data-load:/app/bin/data-update
ENV PYTHONUNBUFFERED=1

# Run tests during build (optional)
RUN pytest tests/ --cov=bin --cov-fail-under=95

# Set default command
CMD ["python", "bin/data-load/main.py"]
```

### Monitoring and Logging

#### 1. Structured Logging

```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    
    def format(self, record):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        if hasattr(record, 'gene_id'):
            log_entry['gene_id'] = record.gene_id
            
        if hasattr(record, 'processing_time'):
            log_entry['processing_time'] = record.processing_time
            
        return json.dumps(log_entry)

# Configure logging
logging.basicConfig(level=logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger(__name__)
logger.addHandler(handler)

# Usage
logger.info("Processing gene data", extra={
    'gene_id': 'GENE.1.1',
    'processing_time': 1.23
})
```

#### 2. Metrics Collection

```python
import time
from contextlib import contextmanager
from typing import Dict, Any

class MetricsCollector:
    """Collect and track application metrics."""
    
    def __init__(self):
        self.counters: Dict[str, int] = {}
        self.timers: Dict[str, float] = {}
    
    def increment(self, metric_name: str, value: int = 1):
        """Increment a counter metric."""
        self.counters[metric_name] = self.counters.get(metric_name, 0) + value
    
    @contextmanager
    def timer(self, metric_name: str):
        """Time a code block."""
        start_time = time.time()
        try:
            yield
        finally:
            duration = time.time() - start_time
            self.timers[metric_name] = duration
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all collected metrics."""
        return {
            'counters': self.counters,
            'timers': self.timers
        }

# Usage
metrics = MetricsCollector()

with metrics.timer('gene_processing'):
    process_gene_data()
    metrics.increment('genes_processed')

print(metrics.get_metrics())
```

This development guide provides comprehensive information for contributing to the PGNC External Stack Python project. Follow these guidelines to ensure high-quality, maintainable code that meets our standards.
