from api.routers import router


class TestRouter:
    def router_successful_test(self) -> None:
        assert isinstance(router.prefix, str)
