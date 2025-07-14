"""
Tests for the Gene model class
"""
import os
import sys

# Add the data-update directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../bin/data-update'))


class TestGene:
    """Test cases for the Gene model class"""
    
    def test_gene_initialization(self):
        """Test Gene object initialization with default values"""
        from models.gene import Gene  # type: ignore
        
        gene = Gene()
        
        # Check that all attributes are initialized to None
        assert gene.pgnc_id is None
        assert gene.taxon_id is None
        assert gene.chromosome is None
        assert gene.gene_symbol_string is None
        assert gene.gene_name_string is None
        assert gene.locus_types is None
        assert gene.status is None
        assert gene.alias_gene_symbol_string is None
        assert gene.alias_gene_name_string is None
        assert gene.prev_gene_symbol_string is None
        assert gene.prev_gene_name_string is None
        assert gene.phytozome_id is None
        assert gene.ncbi_gene_id is None
        assert gene.ensembl_gene_id is None
        assert gene.uniprot_id is None
        assert gene.primary_id is None
    
    def test_gene_property_setters_and_getters(self):
        """Test all property setters and getters"""
        from models.gene import Gene  # type: ignore
        
        gene = Gene()
        
        # Test integer properties
        gene.pgnc_id = 123
        assert gene.pgnc_id == 123
        
        gene.taxon_id = 3702
        assert gene.taxon_id == 3702
        
        # Test string properties
        gene.chromosome = '1'
        assert gene.chromosome == '1'
        
        gene.gene_symbol_string = 'TEST1'
        assert gene.gene_symbol_string == 'TEST1'
        
        gene.gene_name_string = 'Test Gene'
        assert gene.gene_name_string == 'Test Gene'
        
        gene.status = 'approved'
        assert gene.status == 'approved'
        
        gene.primary_id = 'PRIMARY123'
        assert gene.primary_id == 'PRIMARY123'
        
        # Test list properties
        gene.locus_types = ['protein-coding']
        assert gene.locus_types == ['protein-coding']
        
        gene.alias_gene_symbol_string = ['ALIAS1', 'ALIAS2']
        assert gene.alias_gene_symbol_string == ['ALIAS1', 'ALIAS2']
        
        gene.alias_gene_name_string = ['Alias Name']
        assert gene.alias_gene_name_string == ['Alias Name']
        
        gene.prev_gene_symbol_string = ['PREV1']
        assert gene.prev_gene_symbol_string == ['PREV1']
        
        gene.prev_gene_name_string = ['Previous Name']
        assert gene.prev_gene_name_string == ['Previous Name']
        
        gene.phytozome_id = ['Atg123']
        assert gene.phytozome_id == ['Atg123']
        
        gene.ncbi_gene_id = [12345]
        assert gene.ncbi_gene_id == [12345]
        
        gene.ensembl_gene_id = ['ENSG123']
        assert gene.ensembl_gene_id == ['ENSG123']
        
        gene.uniprot_id = ['P12345']
        assert gene.uniprot_id == ['P12345']
    
    def test_gene_to_dict(self):
        """Test Gene to_dict method"""
        from models.gene import Gene  # type: ignore
        
        gene = Gene()
        gene.pgnc_id = 123
        gene.taxon_id = 3702
        gene.chromosome = '1'
        gene.gene_symbol_string = 'TEST1'
        gene.gene_name_string = 'Test Gene'
        gene.locus_types = ['protein-coding']
        gene.status = 'approved'
        gene.alias_gene_symbol_string = ['ALIAS1']
        gene.alias_gene_name_string = ['Alias Name']
        gene.prev_gene_symbol_string = ['PREV1']
        gene.prev_gene_name_string = ['Previous Name']
        gene.phytozome_id = ['Atg123']
        gene.ncbi_gene_id = [12345]
        gene.ensembl_gene_id = ['ENSG123']
        gene.uniprot_id = ['P12345']
        gene.primary_id = 'Atg123'
        
        result = gene.to_dict()
        
        expected = {
            'pgnc_id': 'PGNC:123',
            'taxon_id': 3702,
            'chromosome': '1',
            'gene_symbol_string': 'TEST1',
            'gene_name_string': 'Test Gene',
            'locus_type': ['protein-coding'],
            'status': 'approved',
            'alias_gene_symbol_string': ['ALIAS1'],
            'alias_gene_name_string': ['Alias Name'],
            'prev_gene_symbol_string': ['PREV1'],
            'prev_gene_name_string': ['Previous Name'],
            'phytozome_id': ['Atg123'],
            'ncbi_gene_id': [12345],
            'ensembl_gene_id': ['ENSG123'],
            'uniprot_id': ['P12345'],
            'primary_id': 'Atg123'
        }
        
        assert result == expected
    
    def test_gene_to_dict_with_none_values(self):
        """Test Gene to_dict method with None values"""
        from models.gene import Gene  # type: ignore
        
        gene = Gene()
        gene.pgnc_id = 123  # Only set pgnc_id
        
        result = gene.to_dict()
        
        # Should include None values in the dictionary
        assert result['pgnc_id'] == 'PGNC:123'
        assert result['taxon_id'] is None
        assert result['chromosome'] is None
        assert result['gene_symbol_string'] is None
        assert result['gene_name_string'] is None
        assert result['locus_type'] is None
        assert result['status'] is None
        assert result['alias_gene_symbol_string'] is None
        assert result['alias_gene_name_string'] is None
        assert result['prev_gene_symbol_string'] is None
        assert result['prev_gene_name_string'] is None
        assert result['phytozome_id'] is None
        assert result['ncbi_gene_id'] is None
        assert result['ensembl_gene_id'] is None
        assert result['uniprot_id'] is None
        assert result['primary_id'] is None
    
    def test_gene_pgnc_id_formatting_in_to_dict(self):
        """Test that pgnc_id is properly formatted with PGNC: prefix"""
        from models.gene import Gene  # type: ignore
        
        gene = Gene()
        gene.pgnc_id = 456
        
        result = gene.to_dict()
        
        assert result['pgnc_id'] == 'PGNC:456'
    
    def test_gene_empty_lists(self):
        """Test Gene with empty lists"""
        from models.gene import Gene  # type: ignore
        
        gene = Gene()
        gene.pgnc_id = 789
        gene.alias_gene_symbol_string = []
        gene.locus_types = []
        
        result = gene.to_dict()
        
        assert result['pgnc_id'] == 'PGNC:789'
        assert result['alias_gene_symbol_string'] == []
        assert result['locus_type'] == []


class TestGenePropertyTypes:
    """Test cases for Gene property type handling"""
    
    def test_gene_with_single_values_in_lists(self):
        """Test Gene with single values in list properties"""
        from models.gene import Gene  # type: ignore
        
        gene = Gene()
        gene.ensembl_gene_id = ['ENSG00000123456']
        gene.ncbi_gene_id = [12345]
        gene.phytozome_id = ['Atg123456']
        
        assert gene.ensembl_gene_id == ['ENSG00000123456']
        assert gene.ncbi_gene_id == [12345]
        assert gene.phytozome_id == ['Atg123456']
    
    def test_gene_with_multiple_values_in_lists(self):
        """Test Gene with multiple values in list properties"""
        from models.gene import Gene  # type: ignore
        
        gene = Gene()
        gene.alias_gene_symbol_string = ['ALIAS1', 'ALIAS2', 'ALIAS3']
        gene.locus_types = ['protein-coding', 'gene', 'pseudogene']
        
        assert len(gene.alias_gene_symbol_string) == 3
        assert 'ALIAS1' in gene.alias_gene_symbol_string
        assert 'ALIAS2' in gene.alias_gene_symbol_string
        assert 'ALIAS3' in gene.alias_gene_symbol_string
        
        assert len(gene.locus_types) == 3
        assert 'protein-coding' in gene.locus_types
        assert 'gene' in gene.locus_types
        assert 'pseudogene' in gene.locus_types


class TestGeneRealWorldScenarios:
    """Test cases for realistic Gene usage scenarios"""
    
    def test_gene_approved_status_scenario(self):
        """Test Gene object for an approved gene with full data"""
        from models.gene import Gene  # type: ignore
        
        gene = Gene()
        gene.pgnc_id = 1001
        gene.taxon_id = 3702
        gene.status = 'approved'
        gene.chromosome = '1'
        gene.gene_symbol_string = 'AT1G01010'
        gene.gene_name_string = 'NAC domain containing protein 1'
        gene.locus_types = ['protein-coding']
        gene.ensembl_gene_id = ['AT1G01010']
        gene.phytozome_id = ['Athal.1.1.01010']
        gene.primary_id = 'Athal.1.1.01010'
        
        result = gene.to_dict()
        
        assert result['pgnc_id'] == 'PGNC:1001'
        assert result['status'] == 'approved'
        assert result['primary_id'] == 'Athal.1.1.01010'
        assert result['locus_type'] == ['protein-coding']
    
    def test_gene_withdrawn_status_scenario(self):
        """Test Gene object for a withdrawn gene"""
        from models.gene import Gene  # type: ignore
        
        gene = Gene()
        gene.pgnc_id = 2001
        gene.status = 'withdrawn'
        gene.prev_gene_symbol_string = ['OLD_SYMBOL']
        gene.prev_gene_name_string = ['Old Gene Name']
        
        result = gene.to_dict()
        
        assert result['pgnc_id'] == 'PGNC:2001'
        assert result['status'] == 'withdrawn'
        assert result['prev_gene_symbol_string'] == ['OLD_SYMBOL']
        assert result['prev_gene_name_string'] == ['Old Gene Name']
    
    def test_gene_with_multiple_cross_references(self):
        """Test Gene object with multiple cross-references"""
        from models.gene import Gene  # type: ignore
        
        gene = Gene()
        gene.pgnc_id = 3001
        gene.ensembl_gene_id = ['ENSG00000123456', 'ENSG00000789012']
        gene.ncbi_gene_id = [12345, 67890]
        gene.uniprot_id = ['P12345', 'Q67890']
        
        result = gene.to_dict()
        
        assert len(result['ensembl_gene_id']) == 2
        assert len(result['ncbi_gene_id']) == 2
        assert len(result['uniprot_id']) == 2
        assert 'ENSG00000123456' in result['ensembl_gene_id']
        assert 12345 in result['ncbi_gene_id']
        assert 'P12345' in result['uniprot_id']
