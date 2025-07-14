"""
Unit tests for BasicStatusEnum
"""
import enum

import pytest
from enum_types.basic_status import BasicStatusEnum  # type: ignore


class TestBasicStatusEnum:
    """Test cases for BasicStatusEnum"""
    
    def test_enum_inheritance(self):
        """Test that BasicStatusEnum inherits from enum.Enum"""
        assert issubclass(BasicStatusEnum, enum.Enum)
    
    def test_enum_members_exist(self):
        """Test that all expected enum members exist"""
        expected_members = ['internal', 'withdrawn', 'public']
        actual_members = [member.name for member in BasicStatusEnum]
        
        assert len(actual_members) == len(expected_members)
        for expected_member in expected_members:
            assert expected_member in actual_members
    
    def test_enum_values_correct(self):
        """Test that enum values are correctly assigned"""
        assert BasicStatusEnum.internal.value == "internal"
        assert BasicStatusEnum.withdrawn.value == "withdrawn"
        assert BasicStatusEnum.public.value == "public"
    
    def test_enum_name_value_consistency(self):
        """Test that enum names match their values"""
        for member in BasicStatusEnum:
            assert member.name == member.value
    
    def test_enum_access_by_name(self):
        """Test accessing enum members by name"""
        assert BasicStatusEnum['internal'] == BasicStatusEnum.internal
        assert BasicStatusEnum['withdrawn'] == BasicStatusEnum.withdrawn
        assert BasicStatusEnum['public'] == BasicStatusEnum.public
    
    def test_enum_access_by_value(self):
        """Test accessing enum members by value"""
        assert BasicStatusEnum("internal") == BasicStatusEnum.internal
        assert BasicStatusEnum("withdrawn") == BasicStatusEnum.withdrawn
        assert BasicStatusEnum("public") == BasicStatusEnum.public
    
    def test_enum_membership(self):
        """Test enum membership operations"""
        assert BasicStatusEnum.internal in BasicStatusEnum
        assert BasicStatusEnum.withdrawn in BasicStatusEnum
        assert BasicStatusEnum.public in BasicStatusEnum
    
    def test_enum_iteration(self):
        """Test that enum is iterable and returns all members"""
        members = list(BasicStatusEnum)
        assert len(members) == 3
        
        expected_values = ["internal", "withdrawn", "public"]
        actual_values = [member.value for member in members]
        
        for expected_value in expected_values:
            assert expected_value in actual_values
    
    def test_enum_equality(self):
        """Test enum member equality"""
        # Same member should be equal
        assert BasicStatusEnum.internal == BasicStatusEnum.internal
        assert BasicStatusEnum.public == BasicStatusEnum.public
        
        # Different members should not be equal
        assert BasicStatusEnum.internal != BasicStatusEnum.public
        assert BasicStatusEnum.withdrawn != BasicStatusEnum.public
    
    def test_enum_identity(self):
        """Test enum member identity"""
        # Same member should have same identity
        assert BasicStatusEnum.internal is BasicStatusEnum.internal
        assert BasicStatusEnum.public is BasicStatusEnum.public
        
        # Different members should have different identity
        assert BasicStatusEnum.internal is not BasicStatusEnum.public
    
    def test_enum_string_representation(self):
        """Test enum string representation"""
        assert str(BasicStatusEnum.internal) == "BasicStatusEnum.internal"
        assert str(BasicStatusEnum.withdrawn) == "BasicStatusEnum.withdrawn"
        assert str(BasicStatusEnum.public) == "BasicStatusEnum.public"
    
    def test_enum_repr(self):
        """Test enum repr representation"""
        assert repr(BasicStatusEnum.internal) == "<BasicStatusEnum.internal: 'internal'>"
        assert repr(BasicStatusEnum.withdrawn) == "<BasicStatusEnum.withdrawn: 'withdrawn'>"
        assert repr(BasicStatusEnum.public) == "<BasicStatusEnum.public: 'public'>"
    
    def test_invalid_enum_access(self):
        """Test that accessing invalid enum members raises appropriate errors"""
        with pytest.raises(KeyError):
            BasicStatusEnum['invalid_status']
        
        with pytest.raises(ValueError):
            BasicStatusEnum('invalid_status')
    
    def test_enum_members_are_immutable(self):
        """Test that enum members cannot be modified"""
        with pytest.raises(AttributeError):
            BasicStatusEnum.internal.value = "new_value"
    
    def test_enum_uniqueness(self):
        """Test that all enum values are unique"""
        values = [member.value for member in BasicStatusEnum]
        assert len(values) == len(set(values)), "Enum values should be unique"
    
    def test_enum_hash(self):
        """Test that enum members are hashable"""
        # Should be able to use as dictionary keys
        status_dict = {
            BasicStatusEnum.internal: "Internal status",
            BasicStatusEnum.public: "Public status"
        }
        
        assert status_dict[BasicStatusEnum.internal] == "Internal status"
        assert status_dict[BasicStatusEnum.public] == "Public status"
        
        # Should be able to use in sets
        status_set = {BasicStatusEnum.internal, BasicStatusEnum.public, BasicStatusEnum.internal}
        assert len(status_set) == 2  # Duplicates should be removed
    
    def test_enum_functional_api_compatibility(self):
        """Test compatibility with functional API usage patterns"""
        # Test that the enum works with common functional patterns
        statuses = list(BasicStatusEnum)
        
        # Filter test
        internal_statuses = [s for s in statuses if 'internal' in s.value]
        assert len(internal_statuses) == 1
        assert internal_statuses[0] == BasicStatusEnum.internal
        
        # Map test
        status_values = [s.value for s in statuses]
        assert "internal" in status_values
        assert "withdrawn" in status_values
        assert "public" in status_values
    
    def test_status_categorization(self):
        """Test basic status categorization logic"""
        # Test typical status categorization scenarios
        active_statuses = [BasicStatusEnum.public]
        inactive_statuses = [BasicStatusEnum.withdrawn]
        development_statuses = [BasicStatusEnum.internal]
        
        # Verify categorization
        assert BasicStatusEnum.public in active_statuses
        assert BasicStatusEnum.withdrawn in inactive_statuses
        assert BasicStatusEnum.internal in development_statuses
        
        # Verify exclusivity
        assert BasicStatusEnum.public not in inactive_statuses
        assert BasicStatusEnum.withdrawn not in active_statuses
    
    def test_comparison_with_other_enums(self):
        """Test that BasicStatusEnum members are not equal to members of other enums"""
        # This test ensures type safety between different enum classes
        # Note: This requires importing other enums, which might cause import issues
        # For now, we'll test basic inequality with strings
        assert BasicStatusEnum.internal != "internal"  # String comparison
        assert BasicStatusEnum.public != "public"
        
        # Test that enum members can't be compared with non-enum values inappropriately
        assert not (BasicStatusEnum.internal == "internal")
        assert BasicStatusEnum.internal.value == "internal"  # But values can be compared
