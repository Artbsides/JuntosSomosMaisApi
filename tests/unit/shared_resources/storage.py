import pytest

from api.shared_resources.storage import Storage


class TestStorage:
    def storage_successful_test(self) -> None:
        storage = Storage()

        assert storage.users is None
        assert storage.states is None

    def storage_failure_test(self) -> None:
        with pytest.raises(TypeError) as exception:
            Storage("string")

        assert exception.value.args is not None
