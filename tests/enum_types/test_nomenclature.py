"""
Unit tests for NomenclatureEnum
"""
import enum

import pytest
from enum_types.nomenclature import NomenclatureEnum  # type: ignore


class TestNomenclatureEnum:
    """Test cases for NomenclatureEnum"""
    
    def test_enum_inheritance(self):
        """Test that NomenclatureEnum inherits from enum.Enum"""
        assert issubclass(NomenclatureEnum, enum.Enum)
    
    def test_enum_members_exist(self):
        """Test that all expected enum members exist"""
        expected_members = ['approved', 'alias', 'previous']
        actual_members = [member.name for member in NomenclatureEnum]
        
        assert len(actual_members) == len(expected_members)
        for expected_member in expected_members:
            assert expected_member in actual_members
    
    def test_enum_values_correct(self):
        """Test that enum values are correctly assigned"""
        assert NomenclatureEnum.approved.value == "approved"
        assert NomenclatureEnum.alias.value == "alias"
        assert NomenclatureEnum.previous.value == "previous"
    
    def test_enum_name_value_consistency(self):
        """Test that enum names match their values"""
        for member in NomenclatureEnum:
            assert member.name == member.value
    
    def test_enum_access_by_name(self):
        """Test accessing enum members by name"""
        assert NomenclatureEnum['approved'] == NomenclatureEnum.approved
        assert NomenclatureEnum['alias'] == NomenclatureEnum.alias
        assert NomenclatureEnum['previous'] == NomenclatureEnum.previous
    
    def test_enum_access_by_value(self):
        """Test accessing enum members by value"""
        assert NomenclatureEnum("approved") == NomenclatureEnum.approved
        assert NomenclatureEnum("alias") == NomenclatureEnum.alias
        assert NomenclatureEnum("previous") == NomenclatureEnum.previous
    
    def test_enum_membership(self):
        """Test enum membership operations"""
        assert NomenclatureEnum.approved in NomenclatureEnum
        assert NomenclatureEnum.alias in NomenclatureEnum
        assert NomenclatureEnum.previous in NomenclatureEnum
    
    def test_enum_iteration(self):
        """Test that enum is iterable and returns all members"""
        members = list(NomenclatureEnum)
        assert len(members) == 3
        
        expected_values = ["approved", "alias", "previous"]
        actual_values = [member.value for member in members]
        
        for expected_value in expected_values:
            assert expected_value in actual_values
    
    def test_enum_equality(self):
        """Test enum member equality"""
        # Same member should be equal
        assert NomenclatureEnum.approved == NomenclatureEnum.approved
        assert NomenclatureEnum.alias == NomenclatureEnum.alias
        
        # Different members should not be equal
        assert NomenclatureEnum.approved != NomenclatureEnum.alias
        assert NomenclatureEnum.alias != NomenclatureEnum.previous
    
    def test_enum_identity(self):
        """Test enum member identity"""
        # Same member should have same identity
        assert NomenclatureEnum.approved is NomenclatureEnum.approved
        assert NomenclatureEnum.alias is NomenclatureEnum.alias
        
        # Different members should have different identity
        assert NomenclatureEnum.approved is not NomenclatureEnum.alias
    
    def test_enum_string_representation(self):
        """Test enum string representation"""
        assert str(NomenclatureEnum.approved) == "NomenclatureEnum.approved"
        assert str(NomenclatureEnum.alias) == "NomenclatureEnum.alias"
        assert str(NomenclatureEnum.previous) == "NomenclatureEnum.previous"
    
    def test_enum_repr(self):
        """Test enum repr representation"""
        assert repr(NomenclatureEnum.approved) == "<NomenclatureEnum.approved: 'approved'>"
        assert repr(NomenclatureEnum.alias) == "<NomenclatureEnum.alias: 'alias'>"
        assert repr(NomenclatureEnum.previous) == "<NomenclatureEnum.previous: 'previous'>"
    
    def test_invalid_enum_access(self):
        """Test that accessing invalid enum members raises appropriate errors"""
        with pytest.raises(KeyError):
            NomenclatureEnum['invalid_nomenclature']
        
        with pytest.raises(ValueError):
            NomenclatureEnum('invalid_nomenclature')
    
    def test_enum_members_are_immutable(self):
        """Test that enum members cannot be modified"""
        with pytest.raises(AttributeError):
            NomenclatureEnum.approved.value = "new_value"
    
    def test_enum_uniqueness(self):
        """Test that all enum values are unique"""
        values = [member.value for member in NomenclatureEnum]
        assert len(values) == len(set(values)), "Enum values should be unique"
    
    def test_enum_hash(self):
        """Test that enum members are hashable"""
        # Should be able to use as dictionary keys
        nomenclature_dict = {
            NomenclatureEnum.approved: "Approved nomenclature",
            NomenclatureEnum.alias: "Alias nomenclature"
        }
        
        assert nomenclature_dict[NomenclatureEnum.approved] == "Approved nomenclature"
        assert nomenclature_dict[NomenclatureEnum.alias] == "Alias nomenclature"
        
        # Should be able to use in sets
        nomenclature_set = {NomenclatureEnum.approved, NomenclatureEnum.alias, NomenclatureEnum.approved}
        assert len(nomenclature_set) == 2  # Duplicates should be removed
    
    def test_enum_functional_api_compatibility(self):
        """Test compatibility with functional API usage patterns"""
        # Test that the enum works with common functional patterns
        nomenclatures = list(NomenclatureEnum)
        
        # Filter test
        approved_nomenclatures = [n for n in nomenclatures if 'approved' in n.value]
        assert len(approved_nomenclatures) == 1
        assert approved_nomenclatures[0] == NomenclatureEnum.approved
        
        # Map test
        nomenclature_values = [n.value for n in nomenclatures]
        assert "approved" in nomenclature_values
        assert "alias" in nomenclature_values
        assert "previous" in nomenclature_values
    
    def test_enum_ordering_consistency(self):
        """Test that enum maintains consistent ordering"""
        members = list(NomenclatureEnum)
        # Test that the order is consistent between calls
        members2 = list(NomenclatureEnum)
        assert members == members2
    
    def test_enum_with_different_values(self):
        """Test enum behavior with different value types (all strings here)"""
        for member in NomenclatureEnum:
            assert isinstance(member.value, str)
            assert len(member.value) > 0
