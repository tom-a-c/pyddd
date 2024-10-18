import pytest

from dddpy.business.domain_model.aggregate import aggregate, Aggregate
from dddpy.business.domain_model.entity import entity
from dddpy.business.domain_model.value_object import value_object


@entity
class MockEntity:
    pass


@value_object
class MockValueObject:
    pass


class TestAggregate:
    def test_snake_case_alias(self):
        assert Aggregate == aggregate

    def test_init_root_is_true(self):
        agg = Aggregate(root=True)
        assert agg.root is True

    def test_init_root_is_false(self):
        agg = Aggregate(root=False)
        assert agg.root is False

    def test_init_root_not_specified(self):
        agg = Aggregate()
        assert agg.root is False

    def test_call_with_entity(self):
        agg = Aggregate()
        result = agg(MockEntity)
        assert result == MockEntity

    def test_call_with_entity_as_aggregate_root(self):
        agg = Aggregate(root=True)
        result = agg(MockEntity)
        assert result == MockEntity

    def test_call_with_value_object(self):
        agg = Aggregate()
        result = agg(MockValueObject)
        assert result == MockValueObject

    def test_call_with_value_object_as_aggregate_root(self):
        agg = Aggregate(root=True)
        with pytest.raises(TypeError):
            agg(MockValueObject)

    def test_validate_root_is_entity_with_entity(self):
        # Arrange
        agg = Aggregate(root=True)
        # Act + Assert
        agg._validate_root_is_entity(MockEntity)  # Doesn't throw exception.

    def test_validate_root_is_entity_with_value_object(self):
        # Arrange
        agg = Aggregate(root=True)
        # Act + Assert
        with pytest.raises(TypeError):
            # Ignore type check - testing type validation:
            # noinspection PyTypeChecker
            agg._validate_root_is_entity(MockValueObject)

    def test_validate_entity_or_vo_with_entity(self):
        # Arrange
        agg = Aggregate()
        # Act + Assert
        agg._validate_entity_or_vo(MockEntity)  # Doesn't throw exception.

    def test_validate_entity_or_vo_with_value_object(self):
        # Arrange
        agg = Aggregate()
        # Act + Assert
        agg._validate_entity_or_vo(MockValueObject)  # Doesn't throw exception.

    def test_validate_entity_or_vo_with_invalid_type(self):
        # Arrange
        agg = Aggregate()
        # Act + Assert
        with pytest.raises(TypeError):
            # Ignore type check - testing type validation:
            # noinspection PyTypeChecker
            agg._validate_entity_or_vo('invalid_type')

