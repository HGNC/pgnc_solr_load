# API Reference Documentation

## 📚 Core API Reference

This document provides detailed API documentation for the PGNC External Stack Python components.

## 🗂️ Module Structure

### Data Loading Module (`bin/data-load/`)

#### Main Data Loading Class

##### `GeneDataLoader`

The primary class for importing gene data from CSV files into the PostgreSQL database.

```python
class GeneDataLoader:
    """
    A class to handle loading and parsing gene data from a CSV file.
    
    This class provides methods to read gene data from a CSV file,
    parse it into a pandas DataFrame, and process the data to create
    appropriate database records.
    """
    
    def __init__(self, file_path: str) -> None:
        """
        Initialize the GeneDataLoader with the path to the CSV file.
        
        Args:
            file_path (str): Path to the CSV file containing gene data.
        """
    
    def parse_csv(self) -> Optional[pd.DataFrame]:
        """
        Parse the CSV file and extract gene-related data.
        
        Returns:
            Optional[pd.DataFrame]: Parsed data or None if error occurs.
            
        Raises:
            FileNotFoundError: If the specified file is not found.
            pandas.errors.EmptyDataError: If the CSV file is empty.
            pandas.errors.ParserError: If the CSV file cannot be parsed.
        """
    
    def process_data(self) -> None:
        """
        Process the gene data loaded from the CSV file.
        
        This method orchestrates the overall data processing flow by iterating
        through each row of the DataFrame and delegating specific processing
        to specialized methods.
        
        Raises:
            ValueError: If required data fields are missing.
        """
```

#### Core Processing Methods

##### Gene Management

```python
def _get_gene_and_creator(
    self, 
    session: Session, 
    primary_id: str, 
    primary_id_source: str
) -> Tuple[Gene, User]:
    """
    Get gene and creator objects from the database.
    
    Args:
        session: SQLAlchemy database session.
        primary_id: The primary ID of the gene.
        primary_id_source: The source of the primary ID.
        
    Returns:
        Tuple of (gene, creator) SQLAlchemy model objects.
        
    Raises:
        sqlalchemy.orm.exc.NoResultFound: If gene or creator not found.
    """

def _create_new_gene(
    self,
    session: Session,
    primary_id: str,
    primary_id_source: str
) -> Tuple[Gene, User]:
    """
    Create a new gene record in the database.
    
    Args:
        session: SQLAlchemy database session.
        primary_id: The primary ID of the gene.
        primary_id_source: The source of the primary ID.
        
    Returns:
        Tuple of (gene, creator) SQLAlchemy model objects.
        
    Raises:
        sqlalchemy.orm.exc.NoResultFound: If creator not found.
    """
```

##### Symbol Processing

```python
def _process_symbols(
    self,
    session: Session,
    row: pd.Series,
    gene_i: Gene,
    creator_i: User
) -> None:
    """
    Process and create gene symbol records.
    
    Args:
        session: SQLAlchemy database session.
        row: DataFrame row containing gene data.
        gene_i: The gene model object.
        creator_i: The creator user model object.
        
    Raises:
        ValueError: If gene_symbol_string is missing.
    """

def _process_approved_symbol(
    self,
    session: Session,
    symbol: str,
    gene_i: Gene,
    creator_i: User
) -> None:
    """
    Process and create approved gene symbol record.
    
    Args:
        session: SQLAlchemy database session.
        symbol: The symbol string to process.
        gene_i: The gene model object.
        creator_i: The creator user model object.
        
    Raises:
        ValueError: If conflicts with existing symbols.
    """

def _process_alias_symbols(
    self,
    session: Session,
    row: pd.Series,
    gene_i: Gene,
    creator_i: User
) -> None:
    """
    Process and create alias gene symbol records.
    
    Args:
        session: SQLAlchemy database session.
        row: DataFrame row containing gene data.
        gene_i: The gene model object.
        creator_i: The creator user model object.
    """
```

##### Name Processing

```python
def _process_names(
    self,
    session: Session,
    row: pd.Series,
    gene_i: Gene,
    creator_i: User
) -> None:
    """
    Process and create gene name records.
    
    Args:
        session: SQLAlchemy database session.
        row: DataFrame row containing gene data.
        gene_i: The gene model object.
        creator_i: The creator user model object.
        
    Raises:
        ValueError: If gene_name_string is missing.
    """

def _process_approved_name(
    self,
    session: Session,
    name: str,
    gene_i: Gene,
    creator_i: User
) -> None:
    """
    Process and create approved gene name record.
    
    Args:
        session: SQLAlchemy database session.
        name: The name string to process.
        gene_i: The gene model object.
        creator_i: The creator user model object.
        
    Raises:
        ValueError: If conflicts with existing names.
    """
```

##### Location and Type Processing

```python
def _process_location(
    self,
    session: Session,
    row: pd.Series,
    gene_i: Gene,
    creator_i: User
) -> None:
    """
    Process and create gene location record.
    
    Args:
        session: SQLAlchemy database session.
        row: DataFrame row containing gene data.
        gene_i: The gene model object.
        creator_i: The creator user model object.
    """

def _process_locus_type(
    self,
    session: Session,
    row: pd.Series,
    gene_i: Gene,
    creator_i: User
) -> None:
    """
    Process and create gene locus type record.
    
    Args:
        session: SQLAlchemy database session.
        row: DataFrame row containing gene data.
        gene_i: The gene model object.
        creator_i: The creator user model object.
        
    Raises:
        ValueError: If locus_type is missing.
    """
```

##### Cross-reference Processing

```python
def _process_crossrefs(
    self,
    session: Session,
    row: pd.Series,
    gene_i: Gene,
    creator_i: User
) -> None:
    """
    Process and create gene cross-reference records.
    
    Args:
        session: SQLAlchemy database session.
        row: DataFrame row containing gene data.
        gene_i: The gene model object.
        creator_i: The creator user model object.
    """

def _process_xref_field(
    self,
    session: Session,
    row: pd.Series,
    field_name: str,
    xref_type: int,
    gene_i: Gene,
    creator_i: User
) -> None:
    """
    Process and create gene cross-references of a specific type.
    
    Args:
        session: SQLAlchemy database session.
        row: DataFrame row containing gene data.
        field_name: Name of field containing cross-references.
        xref_type: Type ID of the cross-reference.
        gene_i: The gene model object.
        creator_i: The creator user model object.
    """
```

#### Utility Functions

```python
def dump_db(cmd: Tuple[str, ...], file_name: str) -> None:
    """
    Dump database content to a gzipped file.
    
    Args:
        cmd: Command to execute as subprocess.
        file_name: Name of output file in '/usr/src/app/db-data/'.
    """

def main() -> None:
    """
    Main function to handle command-line arguments and execute data processing.
    
    Command line arguments:
        --file: Path to the CSV file containing gene data.
        
    Exit codes:
        1: If CSV file could not be loaded or parsed.
    """
```

### Data Update Module (`bin/data-update/`)

#### Solr Update Operations

```python
def update_solr_index(
    dump: bool = False,
    dry_run: bool = False,
    clear: bool = False
) -> None:
    """
    Update Solr search index with current database state.
    
    Args:
        dump: Export Solr JSON to file without updating index.
        dry_run: Preview changes without applying them.
        clear: Clear existing Solr index before updating.
    """

def export_gene_data() -> List[Dict[str, Any]]:
    """
    Export gene data from database in Solr JSON format.
    
    Returns:
        List of gene documents formatted for Solr indexing.
    """

def clear_solr_index() -> bool:
    """
    Clear all documents from the Solr index.
    
    Returns:
        True if successful, False otherwise.
    """
```

## 🗃️ Database Models

### Core Gene Model

```python
class Gene(Base):
    """
    Primary gene entity model.
    
    Attributes:
        id (int): Primary key identifier.
        primary_id (str): Primary gene identifier.
        primary_id_source (str): Source of primary identifier.
        status (GeneStatusEnum): Current gene status.
        created_by (int): Foreign key to creator user.
        created_at (datetime): Creation timestamp.
        updated_at (datetime): Last update timestamp.
    """
    
    __tablename__ = "gene"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    primary_id: Mapped[str] = mapped_column(String(100), nullable=False)
    primary_id_source: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[GeneStatusEnum] = mapped_column(
        Enum(GeneStatusEnum), 
        nullable=False,
        default=GeneStatusEnum.internal
    )
    created_by: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("user.id"), 
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        nullable=False,
        default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now()
    )
```

### Symbol and Name Models

```python
class Symbol(Base):
    """
    Gene symbol entity model.
    
    Attributes:
        id (int): Primary key identifier.
        symbol (str): The symbol string.
        created_at (datetime): Creation timestamp.
        updated_at (datetime): Last update timestamp.
    """

class Name(Base):
    """
    Gene name entity model.
    
    Attributes:
        id (int): Primary key identifier.
        name (str): The name string.
        created_at (datetime): Creation timestamp.
        updated_at (datetime): Last update timestamp.
    """
```

### Relationship Models

```python
class GeneHasSymbol(Base):
    """
    Many-to-many relationship between genes and symbols.
    
    Attributes:
        gene_id (int): Foreign key to gene.
        symbol_id (int): Foreign key to symbol.
        type (NomenclatureEnum): Symbol type (approved, alias, previous).
        status (BasicStatusEnum): Relationship status.
        created_by (int): Foreign key to creator user.
    """

class GeneHasName(Base):
    """
    Many-to-many relationship between genes and names.
    
    Attributes:
        gene_id (int): Foreign key to gene.
        name_id (int): Foreign key to name.
        type (NomenclatureEnum): Name type (approved, alias, previous).
        status (BasicStatusEnum): Relationship status.
        created_by (int): Foreign key to creator user.
    """
```

## 🏷️ Enum Types

### Gene Status Enumeration

```python
class GeneStatusEnum(Enum):
    """
    Enumeration for gene approval status.
    
    Values:
        internal: Gene exists in database but not public.
        approved: Gene is publicly approved and visible.
        withdrawn: Gene has been withdrawn from public use.
    """
    
    internal = "internal"
    approved = "approved"
    withdrawn = "withdrawn"
```

### Nomenclature Type Enumeration

```python
class NomenclatureEnum(Enum):
    """
    Enumeration for nomenclature types.
    
    Values:
        approved: Official approved nomenclature.
        alias: Alternative nomenclature still in use.
        previous: Previously used nomenclature, now deprecated.
    """
    
    approved = "approved"
    alias = "alias"
    previous = "previous"
```

### Basic Status Enumeration

```python
class BasicStatusEnum(Enum):
    """
    Enumeration for basic entity status.
    
    Values:
        public: Entity is publicly visible.
        private: Entity is internal/private.
        pending: Entity is pending approval.
    """
    
    public = "public"
    private = "private"
    pending = "pending"
```

## 🧪 Testing API

### Test Fixtures

```python
@pytest.fixture
def sample_csv_file() -> str:
    """
    Create a temporary CSV file for testing.
    
    Returns:
        str: Path to temporary CSV file.
    """

@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    """
    Sample pandas DataFrame for testing.
    
    Returns:
        pd.DataFrame: Test data frame with gene information.
    """

@pytest.fixture
def mock_session() -> Mock:
    """
    Mock SQLAlchemy session for testing.
    
    Returns:
        Mock: Configured mock session object.
    """
```

### Test Utilities

```python
def create_test_gene(
    primary_id: str = "TEST.1.1",
    primary_id_source: str = "test",
    status: GeneStatusEnum = GeneStatusEnum.internal
) -> Gene:
    """
    Create a test gene object for testing.
    
    Args:
        primary_id: Primary identifier for the gene.
        primary_id_source: Source of the primary identifier.
        status: Initial status of the gene.
        
    Returns:
        Gene: Configured gene object for testing.
    """

def assert_gene_processing_success(
    result: bool,
    mock_session: Mock,
    gene: Gene
) -> None:
    """
    Assert that gene processing completed successfully.
    
    Args:
        result: Return value from processing function.
        mock_session: Mock session object to verify calls.
        gene: Gene object that was processed.
    """
```

## 🔧 Configuration API

### Database Configuration

```python
class Config:
    """
    Database configuration management.
    
    Attributes:
        DATABASE_URI (str): Complete database connection string.
        DB_HOST (str): Database host address.
        DB_PORT (str): Database port number.
        DB_NAME (str): Database name.
        DB_USER (str): Database username.
        DB_PASSWORD (str): Database password.
    """
    
    @classmethod
    def get_database_uri(cls) -> str:
        """
        Construct database URI from environment variables.
        
        Returns:
            str: Complete PostgreSQL connection URI.
            
        Raises:
            ValueError: If required environment variables are missing.
        """
```

### Environment Variable Management

```python
def get_required_env(var_name: str) -> str:
    """
    Get required environment variable or raise error.
    
    Args:
        var_name: Name of environment variable.
        
    Returns:
        str: Value of environment variable.
        
    Raises:
        ValueError: If environment variable is not set.
    """

def get_optional_env(var_name: str, default: str = None) -> Optional[str]:
    """
    Get optional environment variable with default.
    
    Args:
        var_name: Name of environment variable.
        default: Default value if not set.
        
    Returns:
        Optional[str]: Value of environment variable or default.
    """
```

## 📊 Data Format Specifications

### CSV Input Format

Required columns for gene data CSV files:

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `primary_id` | string | Yes | Unique gene identifier |
| `primary_id_source` | string | Yes | Source of primary identifier |
| `gene_symbol_string` | string | Yes | Primary gene symbol |
| `gene_name_string` | string | Yes | Primary gene name |
| `chromosome` | string | Yes | Chromosomal location |
| `locus_type` | string | Yes | Gene type classification |
| `alias_gene_symbol_string` | string | No | Pipe-separated alias symbols |
| `alias_gene_name_string` | string | No | Pipe-separated alias names |
| `ncbi_gene_id` | string | No | NCBI Gene database ID |
| `uniprot_id` | string | No | UniProt database ID |
| `pubmed_id` | string | No | PubMed reference ID |

### Solr Document Format

JSON structure for Solr indexing:

```json
{
  "id": "gene_primary_id",
  "primary_id": "GENE.1.1",
  "primary_id_source": "phytozome",
  "symbols": ["SYMBOL1", "ALIAS1", "ALIAS2"],
  "names": ["Gene Name 1", "Alternative Name"],
  "chromosome": "1",
  "locus_type": "protein-coding",
  "status": "approved",
  "xrefs": {
    "ncbi": ["123456"],
    "uniprot": ["P12345"],
    "pubmed": ["98765"]
  }
}
```

## 🚨 Error Handling

### Exception Hierarchy

```python
class PGNCError(Exception):
    """Base exception for PGNC-specific errors."""

class DataValidationError(PGNCError):
    """Raised when input data fails validation."""

class DatabaseError(PGNCError):
    """Raised when database operations fail."""

class SolrError(PGNCError):
    """Raised when Solr operations fail."""

class ConfigurationError(PGNCError):
    """Raised when configuration is invalid."""
```

### Error Response Patterns

```python
def handle_processing_error(
    error: Exception,
    context: str,
    rollback_session: bool = True
) -> bool:
    """
    Standard error handling pattern for processing functions.
    
    Args:
        error: The exception that occurred.
        context: Description of operation context.
        rollback_session: Whether to rollback database session.
        
    Returns:
        bool: False to indicate processing failure.
    """
```

---

This API reference provides comprehensive documentation for all public interfaces in the PGNC External Stack Python project. For implementation examples and usage patterns, see the [Development Guide](./DEVELOPMENT_GUIDE.md) and existing test suites.
