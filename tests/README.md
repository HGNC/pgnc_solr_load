# PGNC External Stack - Python Test Suite

This directory contains comprehensive unit tests for the PGNC external stack Python components, specifically testing the database layer, models, insert functionality, enum types, and configuration.

## Overview

The test suite provides comprehensive coverage for the core database functionality:

- **DB Module**: Database configuration and package initialization
- **Models**: SQLAlchemy ORM models and relationships
- **Insert Classes**: Database insertion functionality
- **Enum Types**: Enumeration classes for data validation

## Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Main pytest configuration and path setup
├── db/                      # NEW: Database module tests (29 tests)
│   ├── __init__.py
│   ├── conftest.py          # DB-specific configuration
│   ├── test_config.py       # Database configuration testing
│   ├── test_init.py         # Package initialization testing
│   ├── test_integration.py  # Integration testing
│   └── README.md            # Detailed documentation
├── models/                  # SQLAlchemy model tests (121 tests)
│   ├── __init__.py
│   ├── conftest.py          # Model-specific configuration
│   ├── test_base.py         # Base model class tests
│   ├── test_gene.py         # Gene model tests
│   ├── test_symbol.py       # Symbol model tests
│   ├── test_user.py         # User model tests
│   ├── test_location.py     # Location model tests
│   ├── test_gene_has_symbol.py # Relationship model tests
│   ├── test_integration.py  # Cross-model integration tests
│   └── README.md            # Model testing documentation
├── insert/                  # Insert functionality tests (111 tests)
│   ├── __init__.py
│   ├── conftest.py          # Insert-specific configuration
│   ├── test_gene_symbol.py  # GeneSymbol insert tests
│   ├── test_gene_name.py    # GeneName insert tests
│   ├── test_gene_location.py # GeneLocation insert tests
│   ├── test_gene_locus_type.py # GeneLocusType insert tests
│   ├── test_gene_xref.py    # GeneXref insert tests
│   ├── test_integration.py  # Insert integration tests
│   └── README.md            # Insert testing documentation
├── enum_types/              # Enum type tests (52 tests)
│   ├── __init__.py
│   ├── test_gene_status.py  # GeneStatusEnum tests
│   ├── test_nomenclature.py # NomenclatureEnum tests
│   ├── test_basic_status.py # BasicStatusEnum tests
│   └── test_integration.py  # Enum integration tests
└── README.md                # This file
```

## Test Statistics

- **Total Tests**: 313
- **Test Categories**: 4 (DB, Models, Insert, Enums)
- **Test Files**: 20
- **Pass Rate**: 100%

### Breakdown by Category

1. **DB Tests**: 29 tests
   - Configuration: 10 tests
   - Package Init: 6 tests
   - Integration: 13 tests

2. **Model Tests**: 121 tests
   - Individual models: 109 tests
   - Integration: 12 tests

3. **Insert Tests**: 111 tests
   - Individual classes: 99 tests
   - Integration: 12 tests

4. **Enum Tests**: 52 tests
   - Individual enums: 40 tests
   - Integration: 12 tests

## Running the Tests

### Prerequisites

Make sure pytest and pytest-cov are installed:

```bash
pip install pytest pytest-cov
```

### Running All Tests

From the python directory, run:

```bash
python -m pytest tests/ -v
```

### Running Specific Test Categories

```bash
# Test database module
python -m pytest tests/db/ -v

# Test models
python -m pytest tests/models/ -v

# Test insert functionality
python -m pytest tests/insert/ -v

# Test enum types
python -m pytest tests/enum_types/ -v
```

### Running Specific Test Files

```bash
# Test only GeneStatusEnum
python -m pytest tests/enum_types/test_gene_status.py -v

# Test only integration tests
python -m pytest tests/enum_types/test_integration.py -v
```

### Running with Coverage

```bash
python -m pytest tests/enum_types/ --cov=bin/data-load/db/enum_types --cov-report=term-missing
```

### Running Specific Test Methods

```bash
# Run a specific test method
python -m pytest tests/enum_types/test_gene_status.py::TestGeneStatusEnum::test_enum_inheritance -v
```

## Test Categories

### Unit Tests

Each enum class has its own comprehensive unit test suite that covers:

#### Basic Functionality

- Enum inheritance verification
- Member existence validation
- Value correctness
- Name-value consistency

#### Access Patterns

- Access by name (`EnumClass['member_name']`)
- Access by value (`EnumClass('member_value')`)
- Membership testing (`member in EnumClass`)

#### Iteration and Equality

- Enum iteration behavior
- Member equality and identity
- String representation and repr

#### Error Handling

- Invalid member access
- Immutability enforcement
- Value uniqueness

#### Advanced Features

- Hashability (for use as dict keys and in sets)
- Functional API compatibility
- Serialization compatibility

### Integration Tests

The integration test suite (`test_integration.py`) verifies:

- All enums are properly exported
- Enum distinctness and type safety
- Cross-enum operations
- Combined usage patterns
- Performance characteristics

## Test Coverage

The current test suite achieves **100% code coverage** for all enum modules:

- `enum_types/__init__.py`: 100%
- `enum_types/basic_status.py`: 100%
- `enum_types/gene_status.py`: 100%
- `enum_types/nomenclature.py`: 100%

## Key Test Features

### Comprehensive Enum Testing

Each enum is tested for:

- All standard enum behaviors
- Python enum module compliance
- Custom value handling
- Error conditions

### Type Safety

Tests ensure:

- Enum members from different enums are distinct
- Type checking works correctly
- No inappropriate cross-enum equality

### Performance Testing

Integration tests include:

- Lookup performance validation
- Memory usage patterns
- Iteration consistency

### Real-world Usage Patterns

Tests cover:

- Dictionary usage as keys
- Set operations
- Filtering and mapping
- Serialization scenarios

## Adding New Tests

When adding new enum types or modifying existing ones:

1. Create a new test file following the naming pattern `test_<enum_name>.py`
2. Use the existing test classes as templates
3. Ensure comprehensive coverage of all enum members and methods
4. Add integration tests for cross-enum interactions
5. Run the full test suite to ensure no regressions

## Continuous Integration

These tests are designed to be:

- Fast-running (all tests complete in under 1 second)
- Deterministic (no flaky tests)
- Environment-independent
- CI/CD friendly

## Troubleshooting

### Import Errors

If you encounter import errors, ensure:

1. You're running tests from the `python` directory
2. The `conftest.py` file is properly setting up the Python path
3. The enum modules exist in `bin/data-load/db/enum_types/`

### Path Issues

The test suite uses `conftest.py` to automatically configure the Python path. If you need to run tests from a different location, you may need to adjust the path setup in `conftest.py`.

### Coverage Issues

To debug coverage issues:

1. Use `--cov-report=html` to generate an HTML coverage report
2. Check that all enum files are being imported correctly
3. Verify that the coverage path matches your project structure
