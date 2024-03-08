from ...domain.model.location.location import Location


class LocationRepository:
    def find_by_port_code(self, port_code: str) -> Location:
        pass

    def find_by_city_name(self, city_name: str) -> Location:
        pass
