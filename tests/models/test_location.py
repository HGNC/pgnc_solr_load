"""
Tests for the Location model
"""
import pytest
import sqlalchemy as sa
from db.models.base import Base  # type: ignore
from db.models.location import Location  # type: ignore


class TestLocationModel:
    """Test cases for the Location model"""
    
    def test_location_inheritance(self):
        """Test that Location inherits from Base"""
        assert issubclass(Location, Base)
    
    def test_location_table_name(self):
        """Test that Location has the correct table name"""
        assert Location.__tablename__ == "location"
    
    def test_location_has_required_columns(self):
        """Test that Location model has all required columns"""
        columns = Location.__table__.columns
        column_names = [col.name for col in columns]
        
        expected_columns = [
            'id', 'name', 'refseq_accession', 'genbank_accession',
            'coord_system', 'type'
        ]
        
        for col in expected_columns:
            assert col in column_names, f"Column {col} not found in Location model"
    
    def test_location_primary_key(self):
        """Test that id is the primary key"""
        primary_keys = [col.name for col in Location.__table__.primary_key.columns]
        assert primary_keys == ['id']
        assert Location.__table__.columns['id'].type.python_type is int
    
    def test_location_column_types(self):
        """Test that column types are correctly defined"""
        columns = Location.__table__.columns
        
        # Check BigInteger for id
        assert isinstance(columns['id'].type, sa.BigInteger)
        
        # Check String columns and their lengths
        string_columns = {
            'name': 255,
            'refseq_accession': 255,
            'genbank_accession': 255,
            'coord_system': 20,
            'type': 20
        }
        
        for col_name, length in string_columns.items():
            assert isinstance(columns[col_name].type, sa.String)
            assert columns[col_name].type.length == length
    
    def test_location_nullable_constraints(self):
        """Test that nullable constraints are correctly set"""
        columns = Location.__table__.columns
        
        # Required columns (not nullable)
        required_columns = ['id', 'name']
        for col_name in required_columns:
            assert not columns[col_name].nullable, f"Column {col_name} should not be nullable"
        
        # Optional columns (nullable)
        optional_columns = ['refseq_accession', 'genbank_accession', 'coord_system', 'type']
        for col_name in optional_columns:
            assert columns[col_name].nullable, f"Column {col_name} should be nullable"
    
    def test_location_relationships_exist(self):
        """Test that relationships are defined"""
        # Check that relationship attributes exist
        assert hasattr(Location, 'location_has_assemblies')
        assert hasattr(Location, 'location_has_genes')
    
    def test_location_instantiation(self):
        """Test that Location can be instantiated"""
        location = Location()
        assert isinstance(location, Location)
        assert isinstance(location, Base)
    
    def test_location_creation_with_fields(self):
        """Test creating a location with fields"""
        location = Location()
        location.name = "1p36.33"
        location.refseq_accession = "NC_000001.11"
        location.genbank_accession = "CM000663.2"
        location.coord_system = "chromosome"
        location.type = "band"
        
        assert location.name == "1p36.33"
        assert location.refseq_accession == "NC_000001.11"
        assert location.genbank_accession == "CM000663.2"
        assert location.coord_system == "chromosome"
        assert location.type == "band"
    
    @pytest.mark.parametrize("location_name", [
        "1p36.33",
        "Xq28",
        "22q11.2",
        "mitochondrion",
        "unplaced",
        "2q14.1",
        "Yp11.2"
    ])
    def test_location_various_names(self, location_name):
        """Test that various location names can be assigned"""
        location = Location()
        location.name = location_name
        assert location.name == location_name
    
    @pytest.mark.parametrize("coord_system", [
        "chromosome",
        "scaffold", 
        "contig",
        "plasmid",
        "mitochondrion"
    ])
    def test_location_coord_systems(self, coord_system):
        """Test that various coordinate systems can be assigned"""
        location = Location()
        location.coord_system = coord_system
        assert location.coord_system == coord_system
    
    @pytest.mark.parametrize("location_type", [
        "band",
        "gene",
        "region",
        "scaffold",
        "chromosome"
    ])
    def test_location_types(self, location_type):
        """Test that various location types can be assigned"""
        location = Location()
        location.type = location_type
        assert location.type == location_type
    
    def test_location_accession_formats(self):
        """Test that accession fields accept various formats"""
        location = Location()
        
        # RefSeq accessions
        refseq_accessions = [
            "NC_000001.11",
            "NM_000014.5",
            "XM_123456.1"
        ]
        
        for acc in refseq_accessions:
            location.refseq_accession = acc
            assert location.refseq_accession == acc
        
        # GenBank accessions
        genbank_accessions = [
            "CM000663.2",
            "U12345.1",
            "AB123456.1"
        ]
        
        for acc in genbank_accessions:
            location.genbank_accession = acc
            assert location.genbank_accession == acc
    
    def test_location_optional_fields_can_be_none(self):
        """Test that optional fields can be None"""
        location = Location()
        
        # These should be able to be None
        assert location.refseq_accession is None
        assert location.genbank_accession is None
        assert location.coord_system is None
        assert location.type is None
    
    def test_location_string_length_constraints(self):
        """Test that string fields respect length constraints"""
        location = Location()
        
        # Test maximum lengths
        location.name = "A" * 255
        location.refseq_accession = "B" * 255
        location.genbank_accession = "C" * 255
        location.coord_system = "D" * 20
        location.type = "E" * 20
        
        assert len(location.name) == 255
        assert len(location.refseq_accession) == 255
        assert len(location.genbank_accession) == 255
        assert len(location.coord_system) == 20
        assert len(location.type) == 20
