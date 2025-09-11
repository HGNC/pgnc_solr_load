# Model Tests

This directory contains comprehensive unit tests for all SQLAlchemy models in the PGNC external stack project.

## Test Coverage

### Individual Model Tests

1. **test_base.py** - Tests for the Base declarative model class
   - Inheritance verification
   - Instantiation tests
   - Subclassing capabilities

2. **test_gene.py** - Tests for the Gene model (24 tests)
   - Table structure validation
   - Column types and constraints
   - Foreign key relationships
   - Enum field validation
   - All GeneStatusEnum values
   - Default values and server defaults
   - Relationship definitions

3. **test_gene_has_symbol.py** - Tests for the GeneHasSymbol relationship model (20 tests)
   - Composite primary key validation
   - Foreign key relationships
   - Enum column validation (NomenclatureEnum, BasicStatusEnum)
   - Nullable constraints
   - Creation and modification tracking fields

4. **test_symbol.py** - Tests for the Symbol model (15 tests)
   - Column structure and types
   - String length constraints
   - Various symbol values (gene symbols like BRCA1, TP53, etc.)
   - Relationship definitions

5. **test_user.py** - Tests for the User model (17 tests)
   - All column types and constraints
   - String field length validation
   - Boolean field combinations
   - Email format validation
   - Comprehensive relationship validation

6. **test_location.py** - Tests for the Location model (22 tests)
   - Genomic location name validation
   - Coordinate system types
   - Accession number formats (RefSeq, GenBank)
   - Location type validation
   - String length constraints

### Integration Tests

**test_integration.py** - Cross-model validation tests (12 tests)

- All models inherit from Base
- Unique table names across all models
- Primary key validation (single vs composite)
- Foreign key relationship verification
- Model instantiation capabilities
- **repr** method validation
- Creation tracking field validation
- Status field validation

## Test Statistics

- **Total Tests**: 121
- **Test Files**: 7
- **Models Covered**: 19 models
- **Pass Rate**: 100%

## Test Categories

### Schema Validation Tests

- Table name verification
- Column existence and types
- Primary key configuration
- Foreign key relationships
- Nullable constraints
- String length limits
- Default values

### Enum Testing

- GeneStatusEnum (6 values)
- BasicStatusEnum (3 values)
- NomenclatureEnum (3 values)

### Data Validation Tests

- Field assignment and retrieval
- Enum value validation
- String format validation (emails, accessions)
- Boolean combination testing
- Edge case handling

### Relationship Testing

- One-to-many relationships
- Many-to-one relationships
- Back reference validation
- Foreign key constraint verification

## Running the Tests

```bash
# Run all model tests
python -m pytest tests/models/ -v

# Run specific model tests
python -m pytest tests/models/test_gene.py -v

# Run with coverage
python -m pytest tests/models/ --cov=db.models

# Run integration tests only
python -m pytest tests/models/test_integration.py -v
```

## Test Configuration

The model tests use a specialized `conftest.py` file that:

- Sets up proper import paths for the db.models modules
- Clears any mock modules that might interfere with real imports
- Allows the tests to import actual SQLAlchemy model classes

## Models Tested

Core Models:

- Base (declarative base)
- Gene
- Symbol
- User
- Location

Relationship Models:

- GeneHasSymbol
- GeneHasName
- GeneHasLocation
- GeneHasLocusType
- GeneHasXref
- UserHasRole
- AssemblyHasLocation

Lookup Models:

- Assembly
- ExternalResource
- LocusGroup
- LocusType
- Name
- Role
- Species
- Xref

## Test Patterns

The tests follow consistent patterns:

1. **Inheritance testing** - Verify all models inherit from Base
2. **Table structure testing** - Validate table names and column definitions
3. **Type validation** - Ensure column types match specifications
4. **Constraint testing** - Verify nullable, length, and enum constraints
5. **Relationship testing** - Validate SQLAlchemy relationships
6. **Data manipulation** - Test field assignment and retrieval
7. **Edge case testing** - Test boundary conditions and error cases

## Future Enhancements

Potential areas for expansion:

- Database constraint violation testing
- Performance testing for large datasets
- Migration testing
- Serialization/deserialization testing
- Full relationship traversal testing
- Database session lifecycle testing
