"""
Unit tests for GeneStatusEnum
"""
import enum

import pytest
from enum_types.gene_status import GeneStatusEnum  # type: ignore


class TestGeneStatusEnum:
    """Test cases for GeneStatusEnum"""
    
    def test_enum_inheritance(self):
        """Test that GeneStatusEnum inherits from enum.Enum"""
        assert issubclass(GeneStatusEnum, enum.Enum)
    
    def test_enum_members_exist(self):
        """Test that all expected enum members exist"""
        expected_members = ['internal', 'approved', 'withdrawn', 'review', 'merged', 'split']
        actual_members = [member.name for member in GeneStatusEnum]
        
        assert len(actual_members) == len(expected_members)
        for expected_member in expected_members:
            assert expected_member in actual_members
    
    def test_enum_values_correct(self):
        """Test that enum values are correctly assigned"""
        assert GeneStatusEnum.internal.value == "internal"
        assert GeneStatusEnum.approved.value == "approved"
        assert GeneStatusEnum.withdrawn.value == "withdrawn"
        assert GeneStatusEnum.review.value == "review"
        assert GeneStatusEnum.merged.value == "merged"
        assert GeneStatusEnum.split.value == "split"
    
    def test_enum_name_value_consistency(self):
        """Test that enum names match their values"""
        for member in GeneStatusEnum:
            assert member.name == member.value
    
    def test_enum_access_by_name(self):
        """Test accessing enum members by name"""
        assert GeneStatusEnum['internal'] == GeneStatusEnum.internal
        assert GeneStatusEnum['approved'] == GeneStatusEnum.approved
        assert GeneStatusEnum['withdrawn'] == GeneStatusEnum.withdrawn
        assert GeneStatusEnum['review'] == GeneStatusEnum.review
        assert GeneStatusEnum['merged'] == GeneStatusEnum.merged
        assert GeneStatusEnum['split'] == GeneStatusEnum.split
    
    def test_enum_access_by_value(self):
        """Test accessing enum members by value"""
        assert GeneStatusEnum("internal") == GeneStatusEnum.internal
        assert GeneStatusEnum("approved") == GeneStatusEnum.approved
        assert GeneStatusEnum("withdrawn") == GeneStatusEnum.withdrawn
        assert GeneStatusEnum("review") == GeneStatusEnum.review
        assert GeneStatusEnum("merged") == GeneStatusEnum.merged
        assert GeneStatusEnum("split") == GeneStatusEnum.split
    
    def test_enum_membership(self):
        """Test enum membership operations"""
        assert GeneStatusEnum.internal in GeneStatusEnum
        assert GeneStatusEnum.approved in GeneStatusEnum
        assert GeneStatusEnum.withdrawn in GeneStatusEnum
        assert GeneStatusEnum.review in GeneStatusEnum
        assert GeneStatusEnum.merged in GeneStatusEnum
        assert GeneStatusEnum.split in GeneStatusEnum
    
    def test_enum_iteration(self):
        """Test that enum is iterable and returns all members"""
        members = list(GeneStatusEnum)
        assert len(members) == 6
        
        expected_values = ["internal", "approved", "withdrawn", "review", "merged", "split"]
        actual_values = [member.value for member in members]
        
        for expected_value in expected_values:
            assert expected_value in actual_values
    
    def test_enum_equality(self):
        """Test enum member equality"""
        # Same member should be equal
        assert GeneStatusEnum.internal == GeneStatusEnum.internal
        assert GeneStatusEnum.approved == GeneStatusEnum.approved
        
        # Different members should not be equal
        assert GeneStatusEnum.internal != GeneStatusEnum.approved
        assert GeneStatusEnum.withdrawn != GeneStatusEnum.review
    
    def test_enum_identity(self):
        """Test enum member identity"""
        # Same member should have same identity
        assert GeneStatusEnum.internal is GeneStatusEnum.internal
        assert GeneStatusEnum.approved is GeneStatusEnum.approved
        
        # Different members should have different identity
        assert GeneStatusEnum.internal is not GeneStatusEnum.approved
    
    def test_enum_string_representation(self):
        """Test enum string representation"""
        assert str(GeneStatusEnum.internal) == "GeneStatusEnum.internal"
        assert str(GeneStatusEnum.approved) == "GeneStatusEnum.approved"
        assert str(GeneStatusEnum.withdrawn) == "GeneStatusEnum.withdrawn"
        assert str(GeneStatusEnum.review) == "GeneStatusEnum.review"
        assert str(GeneStatusEnum.merged) == "GeneStatusEnum.merged"
        assert str(GeneStatusEnum.split) == "GeneStatusEnum.split"
    
    def test_enum_repr(self):
        """Test enum repr representation"""
        assert repr(GeneStatusEnum.internal) == "<GeneStatusEnum.internal: 'internal'>"
        assert repr(GeneStatusEnum.approved) == "<GeneStatusEnum.approved: 'approved'>"
    
    def test_invalid_enum_access(self):
        """Test that accessing invalid enum members raises appropriate errors"""
        with pytest.raises(KeyError):
            GeneStatusEnum['invalid_status']
        
        with pytest.raises(ValueError):
            GeneStatusEnum('invalid_status')
    
    def test_enum_members_are_immutable(self):
        """Test that enum members cannot be modified"""
        with pytest.raises(AttributeError):
            GeneStatusEnum.internal.value = "new_value"
    
    def test_enum_uniqueness(self):
        """Test that all enum values are unique"""
        values = [member.value for member in GeneStatusEnum]
        assert len(values) == len(set(values)), "Enum values should be unique"
    
    def test_enum_hash(self):
        """Test that enum members are hashable"""
        # Should be able to use as dictionary keys
        status_dict = {
            GeneStatusEnum.internal: "Internal status",
            GeneStatusEnum.approved: "Approved status"
        }
        
        assert status_dict[GeneStatusEnum.internal] == "Internal status"
        assert status_dict[GeneStatusEnum.approved] == "Approved status"
        
        # Should be able to use in sets
        status_set = {GeneStatusEnum.internal, GeneStatusEnum.approved, GeneStatusEnum.internal}
        assert len(status_set) == 2  # Duplicates should be removed
    
    def test_enum_functional_api_compatibility(self):
        """Test compatibility with functional API usage patterns"""
        # Test that the enum works with common functional patterns
        statuses = list(GeneStatusEnum)
        
        # Filter test
        internal_statuses = [s for s in statuses if 'internal' in s.value]
        assert len(internal_statuses) == 1
        assert internal_statuses[0] == GeneStatusEnum.internal
        
        # Map test
        status_values = [s.value for s in statuses]
        assert "approved" in status_values
        assert "withdrawn" in status_values
