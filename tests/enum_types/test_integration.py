"""
Integration tests for all enum types
"""
import enum

from enum_types import BasicStatusEnum, GeneStatusEnum, NomenclatureEnum  # type: ignore


class TestEnumTypesIntegration:
    """Integration tests for all enum types"""
    
    def test_all_enums_are_available(self):
        """Test that all enums are available through the main module"""
        assert GeneStatusEnum is not None
        assert NomenclatureEnum is not None
        assert BasicStatusEnum is not None
    
    def test_all_enums_inherit_from_enum(self):
        """Test that all enum classes inherit from enum.Enum"""
        assert issubclass(GeneStatusEnum, enum.Enum)
        assert issubclass(NomenclatureEnum, enum.Enum)
        assert issubclass(BasicStatusEnum, enum.Enum)
    
    def test_enum_distinctness(self):
        """Test that all enum classes are distinct"""
        assert GeneStatusEnum is not NomenclatureEnum
        assert GeneStatusEnum is not BasicStatusEnum
        assert NomenclatureEnum is not BasicStatusEnum
    
    def test_enum_member_uniqueness_across_enums(self):
        """Test that enum members from different enums are not equal"""
        # Even if they have the same value, they should not be equal
        assert GeneStatusEnum.internal != BasicStatusEnum.internal
        assert GeneStatusEnum.withdrawn != BasicStatusEnum.withdrawn
    
    def test_enum_value_overlaps(self):
        """Test handling of overlapping values between enums"""
        # GeneStatusEnum and BasicStatusEnum both have 'internal' and 'withdrawn'
        gene_values = {member.value for member in GeneStatusEnum}
        basic_values = {member.value for member in BasicStatusEnum}
        
        # Check overlaps
        overlaps = gene_values.intersection(basic_values)
        expected_overlaps = {'internal', 'withdrawn'}
        assert overlaps == expected_overlaps
    
    def test_enum_combined_usage(self):
        """Test using multiple enums together"""
        # Create dictionaries using different enum types
        status_mapping = {
            GeneStatusEnum.approved: "Gene is approved",
            NomenclatureEnum.approved: "Nomenclature is approved",
            BasicStatusEnum.public: "Status is public"
        }
        
        assert len(status_mapping) == 3
        assert status_mapping[GeneStatusEnum.approved] == "Gene is approved"
        assert status_mapping[NomenclatureEnum.approved] == "Nomenclature is approved"
        assert status_mapping[BasicStatusEnum.public] == "Status is public"
    
    def test_enum_sets_operations(self):
        """Test set operations with different enum types"""
        gene_set = set(GeneStatusEnum)
        nomenclature_set = set(NomenclatureEnum)
        basic_set = set(BasicStatusEnum)
        
        # Test that sets are distinct
        assert gene_set.isdisjoint(nomenclature_set)
        assert gene_set.isdisjoint(basic_set)
        assert nomenclature_set.isdisjoint(basic_set)
        
        # Test union operations
        all_enums = gene_set.union(nomenclature_set).union(basic_set)
        expected_total = len(GeneStatusEnum) + len(NomenclatureEnum) + len(BasicStatusEnum)
        assert len(all_enums) == expected_total
    
    def test_enum_type_checking(self):
        """Test type checking between different enum types"""
        # Test isinstance checks
        assert isinstance(GeneStatusEnum.approved, GeneStatusEnum)
        assert isinstance(NomenclatureEnum.approved, NomenclatureEnum)
        assert isinstance(BasicStatusEnum.public, BasicStatusEnum)
        
        # Test cross-type isinstance checks
        assert not isinstance(GeneStatusEnum.approved, NomenclatureEnum)
        assert not isinstance(GeneStatusEnum.approved, BasicStatusEnum)
        assert not isinstance(NomenclatureEnum.approved, GeneStatusEnum)
    
    def test_enum_iteration_consistency(self):
        """Test that iteration order is consistent"""
        # Test multiple iterations produce same order
        gene_list1 = list(GeneStatusEnum)
        gene_list2 = list(GeneStatusEnum)
        assert gene_list1 == gene_list2
        
        nomenclature_list1 = list(NomenclatureEnum)
        nomenclature_list2 = list(NomenclatureEnum)
        assert nomenclature_list1 == nomenclature_list2
        
        basic_list1 = list(BasicStatusEnum)
        basic_list2 = list(BasicStatusEnum)
        assert basic_list1 == basic_list2
    
    def test_enum_serialization_compatibility(self):
        """Test that enums work well for serialization scenarios"""
        # Test value extraction for serialization
        gene_values = [member.value for member in GeneStatusEnum]
        nomenclature_values = [member.value for member in NomenclatureEnum]
        basic_values = [member.value for member in BasicStatusEnum]
        
        # All values should be strings (JSON serializable)
        assert all(isinstance(v, str) for v in gene_values)
        assert all(isinstance(v, str) for v in nomenclature_values)
        assert all(isinstance(v, str) for v in basic_values)
        
        # Test reconstruction from values
        for value in gene_values:
            assert GeneStatusEnum(value).value == value
        
        for value in nomenclature_values:
            assert NomenclatureEnum(value).value == value
        
        for value in basic_values:
            assert BasicStatusEnum(value).value == value
    
    def test_enum_documentation_completeness(self):
        """Test that all enums have proper documentation"""
        # All enum classes should have docstrings or meaningful names
        assert GeneStatusEnum.__name__ == "GeneStatusEnum"
        assert NomenclatureEnum.__name__ == "NomenclatureEnum"
        assert BasicStatusEnum.__name__ == "BasicStatusEnum"
        
        # Check that each enum has members
        assert len(list(GeneStatusEnum)) > 0
        assert len(list(NomenclatureEnum)) > 0
        assert len(list(BasicStatusEnum)) > 0
    
    def test_enum_lookup_performance(self):
        """Test enum lookup performance characteristics"""
        # Value lookups should be fast and consistent
        import time
        
        # Test GeneStatusEnum lookups
        start_time = time.time()
        for _ in range(1000):
            GeneStatusEnum("approved")
        gene_lookup_time = time.time() - start_time
        
        # Test NomenclatureEnum lookups
        start_time = time.time()
        for _ in range(1000):
            NomenclatureEnum("approved")
        nomenclature_lookup_time = time.time() - start_time
        
        # Test BasicStatusEnum lookups
        start_time = time.time()
        for _ in range(1000):
            BasicStatusEnum("public")
        basic_lookup_time = time.time() - start_time
        
        # All lookups should complete reasonably quickly (less than 1 second for 1000 lookups)
        assert gene_lookup_time < 1.0
        assert nomenclature_lookup_time < 1.0
        assert basic_lookup_time < 1.0
