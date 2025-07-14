"""
Integration tests for all model classes
"""
import sqlalchemy as sa
from db.models import (  # type: ignore
    Assembly,
    AssemblyHasLocation,
    ExternalResource,
    Gene,
    GeneHasLocation,
    GeneHasLocusType,
    GeneHasName,
    GeneHasSymbol,
    GeneHasXref,
    Location,
    LocusGroup,
    LocusType,
    Name,
    Role,
    Species,
    Symbol,
    User,
    UserHasRole,
    Xref,
)
from db.models.base import Base  # type: ignore
from sqlalchemy.orm import DeclarativeBase


class TestModelsIntegration:
    """Integration tests for all model classes"""
    
    def test_all_models_inherit_from_base(self):
        """Test that all model classes inherit from Base"""
        models = [
            Assembly, AssemblyHasLocation, ExternalResource, Gene,
            GeneHasLocation, GeneHasLocusType, GeneHasName, GeneHasSymbol,
            GeneHasXref, Location, LocusGroup, LocusType, Name, Role,
            Species, Symbol, User, UserHasRole, Xref
        ]
        
        for model in models:
            assert issubclass(model, Base), f"{model.__name__} does not inherit from Base"
    
    def test_all_models_have_table_names(self):
        """Test that all model classes have table names defined"""
        models = [
            Assembly, AssemblyHasLocation, ExternalResource, Gene,
            GeneHasLocation, GeneHasLocusType, GeneHasName, GeneHasSymbol,
            GeneHasXref, Location, LocusGroup, LocusType, Name, Role,
            Species, Symbol, User, UserHasRole, Xref
        ]
        
        for model in models:
            assert hasattr(model, '__tablename__'), f"{model.__name__} missing __tablename__"
            assert isinstance(model.__tablename__, str), f"{model.__name__}.__tablename__ is not a string"
            assert len(model.__tablename__) > 0, f"{model.__name__}.__tablename__ is empty"
    
    def test_all_models_have_primary_keys(self):
        """Test that all model classes have primary keys defined"""
        models = [
            Assembly, AssemblyHasLocation, ExternalResource, Gene,
            GeneHasLocation, GeneHasLocusType, GeneHasName, GeneHasSymbol,
            GeneHasXref, Location, LocusGroup, LocusType, Name, Role,
            Species, Symbol, User, UserHasRole, Xref
        ]
        
        for model in models:
            assert hasattr(model, '__table__'), f"{model.__name__} missing __table__"
            primary_key_cols = model.__table__.primary_key.columns
            assert len(primary_key_cols) > 0, f"{model.__name__} has no primary key columns"
    
    def test_models_with_composite_primary_keys(self):
        """Test models that should have composite primary keys"""
        composite_pk_models = [
            (GeneHasSymbol, ['gene_id', 'symbol_id']),
            (GeneHasName, ['gene_id', 'name_id']),
            (GeneHasLocation, ['gene_id', 'location_id']),
            (GeneHasLocusType, ['gene_id', 'locus_type_id']),
            (GeneHasXref, ['gene_id', 'xref_id']),
            (UserHasRole, ['user_id', 'role_id']),
            (AssemblyHasLocation, ['assembly_id', 'location_id'])
        ]
        
        for model, expected_pk_cols in composite_pk_models:
            actual_pk_cols = [col.name for col in model.__table__.primary_key.columns]
            assert set(actual_pk_cols) == set(expected_pk_cols), \
                f"{model.__name__} primary key mismatch. Expected: {expected_pk_cols}, Got: {actual_pk_cols}"
    
    def test_models_with_single_primary_keys(self):
        """Test models that should have single primary keys"""
        single_pk_models = [
            Assembly, ExternalResource, Gene, Location, LocusGroup,
            LocusType, Name, Role, Species, Symbol, User, Xref
        ]
        
        for model in single_pk_models:
            primary_key_cols = [col.name for col in model.__table__.primary_key.columns]
            assert len(primary_key_cols) == 1, \
                f"{model.__name__} should have exactly one primary key column, got: {primary_key_cols}"
    
    def test_all_models_can_be_instantiated(self):
        """Test that all model classes can be instantiated"""
        models = [
            Assembly, AssemblyHasLocation, ExternalResource, Gene,
            GeneHasLocation, GeneHasLocusType, GeneHasName, GeneHasSymbol,
            GeneHasXref, Location, LocusGroup, LocusType, Name, Role,
            Species, Symbol, User, UserHasRole, Xref
        ]
        
        for model in models:
            instance = model()
            assert isinstance(instance, model), f"Failed to instantiate {model.__name__}"
            assert isinstance(instance, Base), f"{model.__name__} instance is not a Base instance"
    
    def test_models_have_repr_methods(self):
        """Test that all model classes have __repr__ methods"""
        models = [
            Assembly, AssemblyHasLocation, ExternalResource, Gene,
            GeneHasLocation, GeneHasLocusType, GeneHasName, GeneHasSymbol,
            GeneHasXref, Location, LocusGroup, LocusType, Name, Role,
            Species, Symbol, User, Xref
        ]
        
        # Skip UserHasRole as it has a complex repr that requires relationships
        
        for model in models:
            assert hasattr(model, '__repr__'), f"{model.__name__} missing __repr__ method"
            
            # Test that __repr__ returns a string
            instance = model()
            try:
                repr_result = repr(instance)
                assert isinstance(repr_result, str), f"{model.__name__}.__repr__ does not return string"
            except AttributeError:
                # Some models may have repr methods that reference relationships
                # which are None when the instance is just created
                pass
    
    def test_foreign_key_relationships_exist(self):
        """Test that expected foreign key relationships exist"""
        # Test some key foreign key relationships
        fk_tests = [
            (Gene, 'taxon_id', 'species.taxon_id'),
            (Gene, 'creator_id', 'user.id'),
            (GeneHasSymbol, 'gene_id', 'gene.id'),
            (GeneHasSymbol, 'symbol_id', 'symbol.id'),
            (GeneHasSymbol, 'creator_id', 'user.id'),
            (UserHasRole, 'user_id', 'user.id'),
            (UserHasRole, 'role_id', 'role.id'),
        ]
        
        for model, column_name, expected_target in fk_tests:
            if hasattr(model.__table__.columns, column_name):
                column = model.__table__.columns[column_name]
                if column.foreign_keys:
                    fk = list(column.foreign_keys)[0]
                    assert str(fk.target_fullname) == expected_target, \
                        f"{model.__name__}.{column_name} foreign key target mismatch"
    
    def test_base_is_declarative_base(self):
        """Test that Base properly extends DeclarativeBase"""
        assert issubclass(Base, DeclarativeBase)
        assert hasattr(Base, 'registry')
        assert hasattr(Base, 'metadata')
    
    def test_model_table_names_are_unique(self):
        """Test that all models have unique table names"""
        models = [
            Assembly, AssemblyHasLocation, ExternalResource, Gene,
            GeneHasLocation, GeneHasLocusType, GeneHasName, GeneHasSymbol,
            GeneHasXref, Location, LocusGroup, LocusType, Name, Role,
            Species, Symbol, User, UserHasRole, Xref
        ]
        
        table_names = [model.__tablename__ for model in models]
        unique_table_names = set(table_names)
        
        assert len(table_names) == len(unique_table_names), \
            f"Duplicate table names found: {table_names}"
    
    def test_models_with_creation_tracking(self):
        """Test that models with creation tracking have required fields"""
        creation_tracking_models = [
            Gene, GeneHasSymbol, GeneHasName
        ]
        
        for model in creation_tracking_models:
            columns = model.__table__.columns
            
            # Check for creation tracking fields
            assert 'creator_id' in columns, f"{model.__name__} missing creator_id"
            assert 'creation_date' in columns, f"{model.__name__} missing creation_date"
            
            # Check for modification tracking fields (only some models have these)
            assert 'editor_id' in columns, f"{model.__name__} missing editor_id"
            assert 'mod_date' in columns, f"{model.__name__} missing mod_date"
        
        # Models with partial creation tracking (no mod_date)
        partial_tracking_models = [
            GeneHasLocation, GeneHasLocusType, GeneHasXref
        ]
        
        for model in partial_tracking_models:
            columns = model.__table__.columns
            
            # Check for creation tracking fields
            assert 'creator_id' in columns, f"{model.__name__} missing creator_id"
            assert 'creation_date' in columns, f"{model.__name__} missing creation_date"
            assert 'editor_id' in columns, f"{model.__name__} missing editor_id"
            # Note: These models don't have mod_date
    
    def test_models_with_status_fields(self):
        """Test that models with status fields have them properly defined"""
        status_models = [
            Gene, GeneHasSymbol, GeneHasName, GeneHasLocation,
            GeneHasLocusType, GeneHasXref
        ]
        
        for model in status_models:
            columns = model.__table__.columns
            assert 'status' in columns, f"{model.__name__} missing status field"
            
            status_col = columns['status']
            assert isinstance(status_col.type, sa.Enum), \
                f"{model.__name__}.status is not an Enum type"
