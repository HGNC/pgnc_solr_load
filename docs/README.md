# Documentation Index

Welcome to the comprehensive documentation for the PGNC External Stack Python project. This index provides easy navigation to all project documentation.

## 📚 Core Documentation

### 🏠 [Project Overview](PROJECT_OVERVIEW.md)
Comprehensive overview of the PGNC External Stack Python project, including architecture, components, and getting started guide.

### 📖 [README](../README.md)
Main project README with quick start instructions, installation guide, and basic usage examples.

### 🔧 [API Reference](API_REFERENCE.md)
Detailed API documentation for all public interfaces, classes, and functions in the project.

### 👨‍💻 [Development Guide](DEVELOPMENT_GUIDE.md)
Complete development workflow, coding standards, testing guidelines, and contribution process.

### 🗃️ [Database Schema](DATABASE_SCHEMA.md)
Comprehensive database schema documentation with entity relationships, indexes, and optimization strategies.

## 🧪 Testing Documentation

### 📊 [Testing Summary](../TESTING_SUMMARY.md)
Detailed overview of the test suite, coverage reports, and testing methodology.

### ⚙️ [Pylance Configuration](../PYLANCE_CONFIG.md)
IDE setup and type checking configuration for optimal development experience.

## 📁 Quick Reference

### Project Structure
```
python/
├── 📂 bin/                     # Executable modules
│   ├── 📂 data-load/          # CSV to PostgreSQL import
│   └── 📂 data-update/        # PostgreSQL to Solr sync
├── 📂 tests/                   # Test suite (95%+ coverage)
├── 📂 docs/                    # This documentation
├── 📂 input/                   # Input data directory
├── 📂 output/                  # Generated output files
└── 📄 requirements.txt         # Python dependencies
```

### Key Components

| Component | Purpose | Documentation |
|-----------|---------|---------------|
| **Data Loading** | Import gene data from CSV to PostgreSQL | [API Reference](API_REFERENCE.md#data-loading-module) |
| **Data Update** | Sync PostgreSQL data to Solr index | [API Reference](API_REFERENCE.md#data-update-module) |
| **Database Models** | SQLAlchemy ORM models | [Database Schema](DATABASE_SCHEMA.md) |
| **Type System** | Enum types for data validation | [API Reference](API_REFERENCE.md#enumeration-types) |
| **Test Suite** | Comprehensive testing framework | [Testing Summary](../TESTING_SUMMARY.md) |

### Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run data loading
cd bin/data-load && python main.py --file data.csv

# Update Solr index
cd bin/data-update && python main.py

# Run tests with coverage
pytest tests/ --cov=bin --cov-report=html

# View coverage report
open htmlcov/index.html
```

## 🔍 Find What You Need

### For New Developers
1. Start with [Project Overview](PROJECT_OVERVIEW.md)
2. Follow [Development Guide](DEVELOPMENT_GUIDE.md) setup
3. Review [API Reference](API_REFERENCE.md) for key interfaces

### For Contributors
1. Read [Development Guide](DEVELOPMENT_GUIDE.md) coding standards
2. Check [Testing Summary](../TESTING_SUMMARY.md) for test requirements
3. Use [Database Schema](DATABASE_SCHEMA.md) for data model understanding

### For System Administrators
1. Review [Project Overview](PROJECT_OVERVIEW.md) architecture
2. Check [Database Schema](DATABASE_SCHEMA.md) for deployment requirements
3. See [Development Guide](DEVELOPMENT_GUIDE.md) deployment section

### For Data Scientists
1. Start with [Project Overview](PROJECT_OVERVIEW.md) data flow
2. Review [API Reference](API_REFERENCE.md) for data processing interfaces
3. Check [Database Schema](DATABASE_SCHEMA.md) for data model details

## 🚀 Getting Started Checklist

- [ ] Read [Project Overview](PROJECT_OVERVIEW.md)
- [ ] Set up development environment using [Development Guide](DEVELOPMENT_GUIDE.md)
- [ ] Run tests to verify setup: `pytest tests/`
- [ ] Review [API Reference](API_REFERENCE.md) for key interfaces
- [ ] Understand data model via [Database Schema](DATABASE_SCHEMA.md)
- [ ] Try basic operations following [README](../README.md) examples

## 📧 Support and Contributing

- **Issues**: Report bugs and feature requests via GitHub Issues
- **Contributing**: Follow guidelines in [Development Guide](DEVELOPMENT_GUIDE.md)
- **Questions**: Refer to documentation or open a discussion

---

**Plant Gene Nomenclature Committee (PGNC)**  
*Advancing plant genomics through standardized gene nomenclature*
