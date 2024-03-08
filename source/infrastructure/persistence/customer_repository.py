from ...domain.model.customer.customer import Customer


class CustomerRepository:
    def find_by_id(self, id: str) -> Customer:
        pass

    def find_by_name(self, name: str) -> Customer:
        pass

    def find_by_cargo_tracking_id(self, cargo_tracking_id: str) -> Customer:
        pass
