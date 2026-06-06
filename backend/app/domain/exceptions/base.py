class DomainException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class EntityNotFoundError(DomainException):
    def __init__(self, entity_name: str, entity_id: str):
        super().__init__(f"{entity_name} с id {entity_id} не найден(а).")


class EmergencyStateError(DomainException):
    pass


class ExternalProviderError(DomainException):
    pass
