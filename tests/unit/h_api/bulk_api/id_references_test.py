import pytest

from h_api.bulk_api.id_references import IdReferences
from h_api.bulk_api.model.data_body import CreateGroupMembership
from h_api.enums import DataType
from h_api.exceptions import UnpopulatedReferenceError


class TestIdReferences:
    def test_we_can_add_a_concrete_id(self):
        id_refs = IdReferences()

        id_refs.add_concrete_id(DataType.GROUP.value, "my_ref", "real_id")

        assert id_refs._ref_to_concrete[DataType.GROUP]["my_ref"] == "real_id"

    def test_we_can_fill_out_a_reference(self, group_membership_body):
        id_refs = IdReferences()
        id_refs.add_concrete_id(DataType.GROUP, "group_ref", "real_group_id")
        id_refs.add_concrete_id(DataType.USER, "user_ref", "real_user_id")

        id_refs.fill_out(group_membership_body)

        group_id = group_membership_body["data"]["relationships"]["group"]["data"]["id"]
        member_id = group_membership_body["data"]["relationships"]["member"]["data"][
            "id"
        ]

        assert group_id == "real_group_id"
        assert member_id == "real_user_id"

    def test_with_missing_references_we_raise_UnpopulatedReferenceError(
        self, group_membership_body
    ):
        id_refs = IdReferences()

        with pytest.raises(UnpopulatedReferenceError):
            id_refs.fill_out(group_membership_body)

    @pytest.fixture
    def group_membership_body(self):
        group_membership = CreateGroupMembership.create("user_ref", "group_ref")

        return group_membership.raw
