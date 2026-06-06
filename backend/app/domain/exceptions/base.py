class DomainException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class EntityNotFoundException(DomainException):
    def __init__(self, entity_name: str, entity_id: str):
        super().__init__(f"{entity_name} с id {entity_id} не найден(а).")


class ConfigurationError(DomainException):
    pass


class InvalidSlotIndexError(ConfigurationError):
    def __init__(self, index: int):
        self.message = f"Некорректный индекс слота: {index}. Допустимы значения от 0 до 3."
        super().__init__(self.message)


class ExternalProviderError(DomainException):
    def __init__(self, provider_name: str, detail: str):
        super().__init__(f"Ошибка провайдера {provider_name}: {detail}")
