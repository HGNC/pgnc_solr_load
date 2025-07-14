"""
Tests for the Gene model
"""
import datetime

import pytest
import sqlalchemy as sa
from db.enum_types.gene_status import GeneStatusEnum  # type: ignore
from db.models.base import Base  # type: ignore
from db.models.gene import Gene  # type: ignore


class TestGeneModel:
    """Test cases for the Gene model"""
    
    def test_gene_inheritance(self):
        """Test that Gene inherits from Base"""
        assert issubclass(Gene, Base)
    
    def test_gene_table_name(self):
        """Test that Gene has the correct table name"""
        assert Gene.__tablename__ == "gene"
    
    def test_gene_has_required_columns(self):
        """Test that Gene model has all required columns"""
        # Check that all expected columns exist
        columns = Gene.__table__.columns
        column_names = [col.name for col in columns]
        
        expected_columns = [
            'id', 'taxon_id', 'creator_id', 'creation_date',
            'editor_id', 'mod_date', 'withdrawn_date', 'status',
            'primary_id', 'primary_id_source'
        ]
        
        for col in expected_columns:
            assert col in column_names, f"Column {col} not found in Gene model"
    
    def test_gene_primary_key(self):
        """Test that id is the primary key"""
        primary_keys = [col.name for col in Gene.__table__.primary_key.columns]
        assert primary_keys == ['id']
        assert Gene.__table__.columns['id'].type.python_type is int
    
    def test_gene_foreign_keys(self):
        """Test that foreign key relationships are properly defined"""
        # Check taxon_id foreign key
        taxon_id_col = Gene.__table__.columns['taxon_id']
        assert len(taxon_id_col.foreign_keys) == 1
        fk = list(taxon_id_col.foreign_keys)[0]
        assert str(fk.target_fullname) == "species.taxon_id"
        
        # Check creator_id foreign key
        creator_id_col = Gene.__table__.columns['creator_id']
        assert len(creator_id_col.foreign_keys) == 1
        fk = list(creator_id_col.foreign_keys)[0]
        assert str(fk.target_fullname) == "user.id"
        
        # Check editor_id foreign key
        editor_id_col = Gene.__table__.columns['editor_id']
        assert len(editor_id_col.foreign_keys) == 1
        fk = list(editor_id_col.foreign_keys)[0]
        assert str(fk.target_fullname) == "user.id"
    
    def test_gene_nullable_constraints(self):
        """Test that nullable constraints are correctly set"""
        columns = Gene.__table__.columns
        
        # Required columns (not nullable)
        required_columns = ['id', 'taxon_id', 'creator_id', 'creation_date', 'status']
        for col_name in required_columns:
            assert not columns[col_name].nullable, f"Column {col_name} should not be nullable"
        
        # Optional columns (nullable)
        optional_columns = ['editor_id', 'mod_date', 'withdrawn_date', 'primary_id', 'primary_id_source']
        for col_name in optional_columns:
            assert columns[col_name].nullable, f"Column {col_name} should be nullable"
    
    def test_gene_column_types(self):
        """Test that column types are correctly defined"""
        columns = Gene.__table__.columns
        
        # Check BigInteger columns
        assert isinstance(columns['id'].type, sa.BigInteger)
        assert isinstance(columns['taxon_id'].type, sa.Integer)
        assert isinstance(columns['creator_id'].type, sa.Integer)
        assert isinstance(columns['editor_id'].type, sa.Integer)
        
        # Check DateTime columns
        assert isinstance(columns['creation_date'].type, sa.DateTime)
        assert isinstance(columns['mod_date'].type, sa.DateTime)
        assert isinstance(columns['withdrawn_date'].type, sa.DateTime)
        
        # Check Enum column
        assert isinstance(columns['status'].type, sa.Enum)
        
        # Check String columns
        assert isinstance(columns['primary_id'].type, sa.String)
        assert isinstance(columns['primary_id_source'].type, sa.String)
        assert columns['primary_id'].type.length == 16
        assert columns['primary_id_source'].type.length == 50
    
    def test_gene_enum_column(self):
        """Test that status column uses GeneStatusEnum"""
        status_col = Gene.__table__.columns['status']
        assert isinstance(status_col.type, sa.Enum)
        assert status_col.type.enum_class == GeneStatusEnum
    
    def test_gene_default_values(self):
        """Test that default values are properly set"""
        creation_date_col = Gene.__table__.columns['creation_date']
        assert creation_date_col.server_default is not None
    
    def test_gene_relationships_exist(self):
        """Test that relationships are defined"""
        # Check that relationship attributes exist
        assert hasattr(Gene, 'gene_has_symbols')
        assert hasattr(Gene, 'gene_has_names')
        assert hasattr(Gene, 'gene_has_locations')
        assert hasattr(Gene, 'gene_has_locus_types')
        assert hasattr(Gene, 'gene_has_xrefs')
        assert hasattr(Gene, 'species')
        assert hasattr(Gene, 'creator')
        assert hasattr(Gene, 'editor')
    
    def test_gene_repr(self):
        """Test that __repr__ method works correctly"""
        # Create a mock gene instance
        gene = Gene()
        gene.id = 123
        gene.taxon_id = 9606
        gene.status = GeneStatusEnum.approved
        gene.creation_date = datetime.datetime(2025, 1, 1, 12, 0, 0)
        gene.creator_id = 1
        gene.editor_id = 2
        gene.mod_date = datetime.datetime(2025, 1, 2, 12, 0, 0)
        gene.withdrawn_date = None
        gene.primary_id = "HGNC:123"
        gene.primary_id_source = "HGNC"
        
        repr_str = repr(gene)
        
        # Check that key information is in the repr
        assert "Gene(" in repr_str
        assert "id=123" in repr_str
        assert "taxon_id=9606" in repr_str
        assert "status=GeneStatusEnum.approved" in repr_str
        assert "creator_id=1" in repr_str
        assert "editor_id=2" in repr_str
        assert "primary_id=HGNC:123" in repr_str
        assert "primary_id_source=HGNC" in repr_str
    
    def test_gene_instantiation(self):
        """Test that Gene can be instantiated"""
        gene = Gene()
        assert isinstance(gene, Gene)
        assert isinstance(gene, Base)
    
    @pytest.mark.parametrize("status", [
        GeneStatusEnum.internal,
        GeneStatusEnum.approved,
        GeneStatusEnum.withdrawn,
        GeneStatusEnum.review,
        GeneStatusEnum.merged,
        GeneStatusEnum.split
    ])
    def test_gene_status_enum_values(self, status):
        """Test that all GeneStatusEnum values can be assigned"""
        gene = Gene()
        gene.status = status
        assert gene.status == status
    
    def test_gene_creation_with_required_fields(self):
        """Test creating a gene with required fields"""
        gene = Gene()
        gene.taxon_id = 9606
        gene.creator_id = 1
        gene.status = GeneStatusEnum.approved
        
        assert gene.taxon_id == 9606
        assert gene.creator_id == 1
        assert gene.status == GeneStatusEnum.approved
    
    def test_gene_optional_fields(self):
        """Test that optional fields can be None"""
        gene = Gene()
        
        # These should be able to be None
        assert gene.editor_id is None
        assert gene.mod_date is None
        assert gene.withdrawn_date is None
        assert gene.primary_id is None
        assert gene.primary_id_source is None
