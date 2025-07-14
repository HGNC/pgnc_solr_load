"""
Tests for the Base model class
"""
from db.models.base import Base  # type: ignore
from sqlalchemy.orm import DeclarativeBase


class TestBase:
    """Test cases for the Base model class"""
    
    def test_base_inheritance(self):
        """Test that Base inherits from DeclarativeBase"""
        assert issubclass(Base, DeclarativeBase)
    
    def test_base_instantiation(self):
        """Test that Base can be instantiated"""
        base_instance = Base()
        assert isinstance(base_instance, Base)
        assert isinstance(base_instance, DeclarativeBase)
    
    def test_base_is_declarative_base(self):
        """Test that Base has the expected DeclarativeBase properties"""
        # Check that Base has the registry attribute (key property of DeclarativeBase)
        assert hasattr(Base, 'registry')
        assert hasattr(Base, 'metadata')
    
    def test_base_can_be_subclassed(self):
        """Test that Base can be used as a parent class"""
        import sqlalchemy as sa
        
        class TestModel(Base):
            __tablename__ = 'test_table'
            
            id: sa.orm.Mapped[int] = sa.orm.mapped_column(sa.Integer, primary_key=True)
        
        test_instance = TestModel()
        assert isinstance(test_instance, Base)
        assert isinstance(test_instance, DeclarativeBase)
        assert test_instance.__tablename__ == 'test_table'
