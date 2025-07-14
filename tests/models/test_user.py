"""
Tests for the User model
"""
import pytest
import sqlalchemy as sa
from db.models.base import Base  # type: ignore
from db.models.user import User  # type: ignore


class TestUserModel:
    """Test cases for the User model"""
    
    def test_user_inheritance(self):
        """Test that User inherits from Base"""
        assert issubclass(User, Base)
    
    def test_user_table_name(self):
        """Test that User has the correct table name"""
        assert User.__tablename__ == "user"
    
    def test_user_has_required_columns(self):
        """Test that User model has all required columns"""
        columns = User.__table__.columns
        column_names = [col.name for col in columns]
        
        expected_columns = [
            'id', 'display_name', 'first_name', 'last_name', 
            'email', 'password', 'current', 'connected'
        ]
        
        for col in expected_columns:
            assert col in column_names, f"Column {col} not found in User model"
    
    def test_user_primary_key(self):
        """Test that id is the primary key"""
        primary_keys = [col.name for col in User.__table__.primary_key.columns]
        assert primary_keys == ['id']
        assert User.__table__.columns['id'].type.python_type is int
    
    def test_user_column_types(self):
        """Test that column types are correctly defined"""
        columns = User.__table__.columns
        
        # Check BigInteger for id
        assert isinstance(columns['id'].type, sa.BigInteger)
        
        # Check String columns and their lengths
        string_columns = {
            'display_name': 128,
            'first_name': 128,
            'last_name': 128,
            'email': 128,
            'password': 255
        }
        
        for col_name, length in string_columns.items():
            assert isinstance(columns[col_name].type, sa.String)
            assert columns[col_name].type.length == length
        
        # Check Boolean columns
        assert isinstance(columns['current'].type, sa.Boolean)
        assert isinstance(columns['connected'].type, sa.Boolean)
    
    def test_user_nullable_constraints(self):
        """Test that nullable constraints are correctly set"""
        columns = User.__table__.columns
        
        # All columns should be required (not nullable)
        required_columns = [
            'id', 'display_name', 'first_name', 'last_name',
            'email', 'password', 'current', 'connected'
        ]
        for col_name in required_columns:
            assert not columns[col_name].nullable, f"Column {col_name} should not be nullable"
    
    def test_user_relationships_exist(self):
        """Test that relationships are defined"""
        # Check that relationship attributes exist
        expected_relationships = [
            'user_has_roles',
            'editor_has_genes',
            'creator_has_genes',
            'editor_has_gene_symbols',
            'creator_has_gene_symbols',
            'editor_has_gene_names',
            'creator_has_gene_names',
            'editor_has_gene_locations',
            'creator_has_gene_locations',
            'editor_has_gene_locus_types',
            'creator_has_gene_locus_types',
            'editor_has_gene_xrefs',
            'creator_has_gene_xrefs'
        ]
        
        for rel in expected_relationships:
            assert hasattr(User, rel), f"Relationship {rel} not found in User model"
    
    def test_user_repr(self):
        """Test that __repr__ method works correctly"""
        # Create a mock user instance
        user = User()
        user.id = 123
        user.display_name = "testuser"
        user.first_name = "Test"
        user.last_name = "User"
        user.email = "test@example.com"
        user.current = True
        user.connected = False
        
        repr_str = repr(user)
        
        # Check that key information is in the repr
        assert "User(" in repr_str
        assert "id=123" in repr_str
        assert "display_name=testuser" in repr_str
        assert "first_name=Test" in repr_str
        assert "last_name=User" in repr_str
        assert "email=test@example.com" in repr_str
        assert "current=True" in repr_str
        assert "connected=False" in repr_str
    
    def test_user_instantiation(self):
        """Test that User can be instantiated"""
        user = User()
        assert isinstance(user, User)
        assert isinstance(user, Base)
    
    def test_user_creation_with_fields(self):
        """Test creating a user with fields"""
        user = User()
        user.display_name = "johndoe"
        user.first_name = "John"
        user.last_name = "Doe"
        user.email = "john@example.com"
        user.password = "hashedpassword"
        user.current = True
        user.connected = False
        
        assert user.display_name == "johndoe"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john@example.com"
        assert user.password == "hashedpassword"
        assert user.current is True
        assert user.connected is False
    
    @pytest.mark.parametrize("current,connected", [
        (True, True),
        (True, False),
        (False, True),
        (False, False)
    ])
    def test_user_boolean_combinations(self, current, connected):
        """Test that boolean fields can have all combinations"""
        user = User()
        user.current = current
        user.connected = connected
        
        assert user.current is current
        assert user.connected is connected
    
    def test_user_string_field_lengths(self):
        """Test that string fields respect length constraints"""
        user = User()
        
        # Test maximum lengths
        user.display_name = "A" * 128
        user.first_name = "B" * 128
        user.last_name = "C" * 128
        user.email = "D" * 128
        user.password = "E" * 255
        
        assert len(user.display_name) == 128
        assert len(user.first_name) == 128
        assert len(user.last_name) == 128
        assert len(user.email) == 128
        assert len(user.password) == 255
    
    def test_user_email_format(self):
        """Test that email field can store valid email formats"""
        user = User()
        
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "firstname+lastname@company.org",
            "admin@sub.domain.com"
        ]
        
        for email in valid_emails:
            user.email = email
            assert user.email == email
    
    def test_user_empty_strings(self):
        """Test that string fields can be set to empty strings"""
        user = User()
        
        user.display_name = ""
        user.first_name = ""
        user.last_name = ""
        user.email = ""
        user.password = ""
        
        assert user.display_name == ""
        assert user.first_name == ""
        assert user.last_name == ""
        assert user.email == ""
        assert user.password == ""
