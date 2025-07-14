"""
Tests for the db.config module
"""
import os
import sys
from unittest.mock import patch


class TestConfig:
    """Test cases for the Config class"""
    
    def test_config_class_exists(self):
        """Test that Config class can be imported"""
        from db.config import Config  # type: ignore
        assert Config is not None
    
    @patch.dict(os.environ, {
        'DB_USER': 'test_user',
        'DB_PASSWORD': 'test_password', 
        'DB_HOST': 'test_host',
        'DB_PORT': '5432',
        'DB_NAME': 'test_db'
    })
    def test_config_with_all_env_vars(self):
        """Test Config when all environment variables are set"""
        # Remove the module from cache and reload
        if 'db.config' in sys.modules:
            del sys.modules['db.config']
        
        from db.config import Config  # type: ignore
        
        assert Config.db_user == 'test_user'
        assert Config.db_password == 'test_password'
        assert Config.db_host == 'test_host'
        assert Config.db_port == '5432'
        assert Config.db_name == 'test_db'
        
        expected_uri = "postgresql://test_user:test_password@test_host:5432/test_db"
        assert Config.DATABASE_URI == expected_uri
    
    @patch.dict(os.environ, {}, clear=True)
    def test_config_with_no_env_vars(self):
        """Test Config when no environment variables are set"""
        # Remove the module from cache and reload
        if 'db.config' in sys.modules:
            del sys.modules['db.config']
        
        from db.config import Config  # type: ignore
        
        assert Config.db_user is None
        assert Config.db_password is None
        assert Config.db_host is None
        assert Config.db_port is None
        assert Config.db_name is None
        
        expected_uri = "postgresql://None:None@None:None/None"
        assert Config.DATABASE_URI == expected_uri
    
    def test_config_with_partial_env_vars(self):
        """Test Config when only some environment variables are set"""
        # Save original environment
        original_env = {}
        db_vars = ['DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT', 'DB_NAME']
        
        for var in db_vars:
            if var in os.environ:
                original_env[var] = os.environ[var]
                del os.environ[var]
        
        try:
            # Set only partial variables
            os.environ['DB_USER'] = 'partial_user'
            os.environ['DB_HOST'] = 'partial_host'
            
            # Remove the module from cache and reload
            if 'db.config' in sys.modules:
                del sys.modules['db.config']
            
            from db.config import Config  # type: ignore
            
            assert Config.db_user == 'partial_user'
            assert Config.db_password is None
            assert Config.db_host == 'partial_host'
            assert Config.db_port is None
            assert Config.db_name is None
            
            expected_uri = "postgresql://partial_user:None@partial_host:None/None"
            assert Config.DATABASE_URI == expected_uri
            
        finally:
            # Restore original environment
            for var in db_vars:
                if var in os.environ:
                    del os.environ[var]
            for var, value in original_env.items():
                os.environ[var] = value
    
    @patch.dict(os.environ, {
        'DB_USER': 'user@domain.com',
        'DB_PASSWORD': 'password!@#$%',
        'DB_HOST': 'db.example.com',
        'DB_PORT': '3306',
        'DB_NAME': 'production_db'
    })
    def test_config_with_special_characters(self):
        """Test Config with special characters in values"""
        # Remove the module from cache and reload
        if 'db.config' in sys.modules:
            del sys.modules['db.config']
        
        from db.config import Config  # type: ignore
        
        assert Config.db_user == 'user@domain.com'
        assert Config.db_password == 'password!@#$%'
        assert Config.db_host == 'db.example.com'
        assert Config.db_port == '3306'
        assert Config.db_name == 'production_db'
        
        expected_uri = "postgresql://user@domain.com:password!@#$%@db.example.com:3306/production_db"
        assert Config.DATABASE_URI == expected_uri
    
    @patch.dict(os.environ, {
        'DB_USER': '',
        'DB_PASSWORD': '',
        'DB_HOST': '',
        'DB_PORT': '',
        'DB_NAME': ''
    })
    def test_config_with_empty_env_vars(self):
        """Test Config when environment variables are empty strings"""
        # Remove the module from cache and reload
        if 'db.config' in sys.modules:
            del sys.modules['db.config']
        
        from db.config import Config  # type: ignore
        
        assert Config.db_user == ''
        assert Config.db_password == ''
        assert Config.db_host == ''
        assert Config.db_port == ''
        assert Config.db_name == ''
        
        expected_uri = "postgresql://:@:/"
        assert Config.DATABASE_URI == expected_uri
    
    def test_config_attributes_are_class_attributes(self):
        """Test that config values are class attributes, not instance attributes"""
        from db.config import Config  # type: ignore
        
        # Check that these are accessible as class attributes
        assert hasattr(Config, 'db_user')
        assert hasattr(Config, 'db_password')
        assert hasattr(Config, 'db_host')
        assert hasattr(Config, 'db_port')
        assert hasattr(Config, 'db_name')
        assert hasattr(Config, 'DATABASE_URI')
    
    def test_config_can_be_instantiated(self):
        """Test that Config class can be instantiated"""
        from db.config import Config  # type: ignore
        
        config_instance = Config()
        assert isinstance(config_instance, Config)
    
    @patch.dict(os.environ, {
        'DB_USER': 'localhost_user',
        'DB_PASSWORD': 'localhost_pass',
        'DB_HOST': '127.0.0.1',
        'DB_PORT': '5433',
        'DB_NAME': 'dev_database'
    })
    def test_config_database_uri_format(self):
        """Test that DATABASE_URI follows correct PostgreSQL URL format"""
        # Remove the module from cache and reload
        if 'db.config' in sys.modules:
            del sys.modules['db.config']
        
        from db.config import Config  # type: ignore
        
        uri = Config.DATABASE_URI
        
        # Check basic structure
        assert uri.startswith('postgresql://')
        assert '@' in uri
        assert ':' in uri
        
        # Check specific components
        assert 'localhost_user' in uri
        assert 'localhost_pass' in uri
        assert '127.0.0.1' in uri
        assert '5433' in uri
        assert 'dev_database' in uri
        
        # Verify exact format
        expected = "postgresql://localhost_user:localhost_pass@127.0.0.1:5433/dev_database"
        assert uri == expected
    
    def test_config_immutable_behavior(self):
        """Test that Config class behavior is consistent across imports"""
        # Import Config multiple times to ensure consistent behavior
        from db.config import Config as Config1  # type: ignore
        from db.config import Config as Config2  # type: ignore
        
        # Should be the same class
        assert Config1 is Config2
        
        # Should have same attributes
        assert Config1.DATABASE_URI == Config2.DATABASE_URI
