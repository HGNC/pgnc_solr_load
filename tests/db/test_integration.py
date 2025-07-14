"""
Integration tests for the entire db module
"""
from enum import Enum
from inspect import isclass

from sqlalchemy.orm import DeclarativeBase


class TestDbIntegration:
    """Integration tests for the entire db module"""
    
    def test_all_models_inherit_from_base(self):
        """Test that all models inherit from the Base class"""
        import db.models as models  # type: ignore
        from db.models.base import Base  # type: ignore
        
        model_classes = [
            models.Assembly, models.AssemblyHasLocation, models.ExternalResource,
            models.Gene, models.GeneHasLocation, models.GeneHasLocusType,
            models.GeneHasName, models.GeneHasSymbol, models.GeneHasXref,
            models.Location, models.LocusGroup, models.LocusType,
            models.Name, models.Role, models.Species, models.Symbol,
            models.User, models.UserHasRole, models.Xref
        ]
        
        for model_class in model_classes:
            assert issubclass(model_class, Base), f"{model_class.__name__} should inherit from Base"
    
    def test_all_models_have_tablename(self):
        """Test that all models have __tablename__ defined"""
        import db.models as models  # type: ignore
        
        model_classes = [
            models.Assembly, models.AssemblyHasLocation, models.ExternalResource,
            models.Gene, models.GeneHasLocation, models.GeneHasLocusType,
            models.GeneHasName, models.GeneHasSymbol, models.GeneHasXref,
            models.Location, models.LocusGroup, models.LocusType,
            models.Name, models.Role, models.Species, models.Symbol,
            models.User, models.UserHasRole, models.Xref
        ]
        
        for model_class in model_classes:
            assert hasattr(model_class, '__tablename__'), f"{model_class.__name__} should have __tablename__"
            assert isinstance(model_class.__tablename__, str), f"{model_class.__name__}.__tablename__ should be a string"
            assert len(model_class.__tablename__) > 0, f"{model_class.__name__}.__tablename__ should not be empty"
    
    def test_all_enums_are_valid_enums(self):
        """Test that all enum classes are proper Enum subclasses"""
        import db.enum_types as enums  # type: ignore
        
        enum_classes = [
            enums.GeneStatusEnum,
            enums.NomenclatureEnum,
            enums.BasicStatusEnum
        ]
        
        for enum_class in enum_classes:
            assert issubclass(enum_class, Enum), f"{enum_class.__name__} should be an Enum"
            assert len(list(enum_class)) > 0, f"{enum_class.__name__} should have enum values"
    
    def test_all_insert_classes_are_classes(self):
        """Test that all insert classes are proper classes"""
        import db.insert as insert_module  # type: ignore
        
        insert_classes = [
            insert_module.GeneSymbol,
            insert_module.GeneName,
            insert_module.GeneLocation,
            insert_module.GeneLocusType,
            insert_module.GeneXref
        ]
        
        for insert_class in insert_classes:
            assert isclass(insert_class), f"{insert_class.__name__} should be a class"
    
    def test_config_has_required_attributes(self):
        """Test that Config class has all required database configuration attributes"""
        from db.config import Config  # type: ignore
        
        required_attrs = [
            'db_user', 'db_password', 'db_host', 'db_port', 'db_name', 'DATABASE_URI'
        ]
        
        for attr in required_attrs:
            assert hasattr(Config, attr), f"Config should have {attr} attribute"
    
    def test_database_uri_format_is_valid(self):
        """Test that DATABASE_URI has valid PostgreSQL format"""
        from db.config import Config  # type: ignore
        
        uri = Config.DATABASE_URI
        assert isinstance(uri, str), "DATABASE_URI should be a string"
        assert uri.startswith('postgresql://'), "DATABASE_URI should start with postgresql://"
        assert '@' in uri, "DATABASE_URI should contain @ symbol"
        assert '/' in uri, "DATABASE_URI should contain / for database name"
    
    def test_all_models_can_be_imported_from_main_package(self):
        """Test that all models can be imported from the main db package"""
        import db  # type: ignore
        
        # All model classes should be available from main package
        model_names = [
            'Assembly', 'AssemblyHasLocation', 'ExternalResource',
            'Gene', 'GeneHasLocation', 'GeneHasLocusType',
            'GeneHasName', 'GeneHasSymbol', 'GeneHasXref',
            'Location', 'LocusGroup', 'LocusType',
            'Name', 'Role', 'Species', 'Symbol',
            'User', 'UserHasRole', 'Xref'
        ]
        
        for model_name in model_names:
            assert hasattr(db, model_name), f"db.{model_name} should be available"
            model_class = getattr(db, model_name)
            assert isclass(model_class), f"db.{model_name} should be a class"
    
    def test_all_insert_classes_can_be_imported_from_main_package(self):
        """Test that all insert classes can be imported from the main db package"""
        import db  # type: ignore
        
        insert_names = ['GeneSymbol', 'GeneName', 'GeneLocation', 'GeneLocusType', 'GeneXref']
        
        for insert_name in insert_names:
            assert hasattr(db, insert_name), f"db.{insert_name} should be available"
            insert_class = getattr(db, insert_name)
            assert isclass(insert_class), f"db.{insert_name} should be a class"
    
    def test_all_enums_can_be_imported_from_main_package(self):
        """Test that all enum types can be imported from the main db package"""
        import db  # type: ignore
        
        enum_names = ['GeneStatusEnum', 'NomenclatureEnum', 'BasicStatusEnum']
        
        for enum_name in enum_names:
            assert hasattr(db, enum_name), f"db.{enum_name} should be available"
            enum_class = getattr(db, enum_name)
            assert issubclass(enum_class, Enum), f"db.{enum_name} should be an Enum"
    
    def test_config_can_be_imported_from_main_package(self):
        """Test that Config can be imported from the main db package"""
        import db  # type: ignore
        
        assert hasattr(db, 'Config'), "db.Config should be available"
        config_class = getattr(db, 'Config')
        assert isclass(config_class), "db.Config should be a class"
    
    def test_no_circular_imports(self):
        """Test that importing the db package doesn't cause circular import errors"""
        try:
            # Test main package and all submodules
            modules_to_test = ['db', 'db.config', 'db.enum_types', 'db.insert', 'db.models']
            for module_name in modules_to_test:
                __import__(module_name)
            
            # If we get here without exceptions, circular imports are avoided
            assert True
        except ImportError as e:
            assert False, f"Circular import detected: {e}"
    
    def test_base_class_is_sqlalchemy_declarative_base(self):
        """Test that Base class properly extends SQLAlchemy DeclarativeBase"""
        from db.models.base import Base  # type: ignore
        
        assert issubclass(Base, DeclarativeBase), "Base should inherit from DeclarativeBase"
        assert hasattr(Base, 'registry'), "Base should have registry attribute"
        assert hasattr(Base, 'metadata'), "Base should have metadata attribute"
    
    def test_package_structure_consistency(self):
        """Test that the package structure is consistent and complete"""
        import db  # type: ignore
        
        # Test that all expected submodules exist
        assert hasattr(db, 'models'), "db.models should exist"
        assert hasattr(db, 'insert'), "db.insert should exist"  
        assert hasattr(db, 'enum_types'), "db.enum_types should exist"
        assert hasattr(db, 'config'), "db.config should exist"
        
        # Test that submodules have expected content
        import db.enum_types  # type: ignore
        import db.insert  # type: ignore
        import db.models  # type: ignore
        
        # Models should have substantial content
        models_attrs = [attr for attr in dir(db.models) if not attr.startswith('_')]
        assert len(models_attrs) >= 19, "db.models should have at least 19 model classes"
        
        # Insert should have classes
        insert_attrs = [attr for attr in dir(db.insert) if not attr.startswith('_')]
        assert len(insert_attrs) >= 5, "db.insert should have at least 5 insert classes"
        
        # Enum types should have enums
        enum_attrs = [attr for attr in dir(db.enum_types) if not attr.startswith('_')]
        assert len(enum_attrs) >= 3, "db.enum_types should have at least 3 enum classes"
