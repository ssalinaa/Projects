import uuid
from datetime import datetime
from abc import ABC, abstractmethod

class BaseIdentity(ABC):
    """
    Абстрактен базов клас за управление на уникалната идентичност на ресурсите.
    Прилага принципа за единствена отговорност (SRP), като се грижи само
    за идентификацията и метаданните за време на създаване.
    """

    def __init__(self, display_name: str):
        # Генерираме уникален идентификатор (UUID) за всеки ресурс
        self.__internal_id = uuid.uuid4()

        # Име на ресурса, зададено от потребителя
        self._display_name = display_name

        # Времева клейма за създаване на обекта
        self.__created_at = datetime.now()

        # Флаг за валидност на обекта в системата
        self._is_active = True

    @property
    def unique_id(self) -> str:
        """Връща низа на уникалния идентификатор (Read-only)."""
        return str(self.__internal_id)

    @property
    def creation_time(self) -> datetime:
        """Връща датата и часа на създаване на ресурса."""
        return self.__created_at

    @property
    def name(self) -> str:
        """Гетър за името на обекта."""
        return self._display_name

    @name.setter
    def name(self, value: str):
        """Сетър с базова валидация за името."""
        if value and len(value) > 2:
            self._display_name = value
        else:
            raise ValueError("The name of the resource should be at least 3 characters.")

    def get_object_age_seconds(self) -> float:
        """Изчислява колко секунди е съществувал обектът в паметта."""
        delta = datetime.now() - self.__created_at
        return delta.total_seconds()

    def deactivate_resource(self):
        """Логическо изтриване на ресурса."""
        self._is_active = False

    @abstractmethod
    def get_full_description(self) -> str:
        """
        Заставя наследниците да дефинират собствена логика за описание.
        Това е част от Interface Segregation - дефинираме какво трябва да има,
        без да казваме как да се имплементира в детайли тук.
        """
        pass

    def __str__(self) -> str:
        """Стрингово представяне за целите на дебъгването."""
        return f"[{self.unique_id}] - {self.name} (Active: {self._is_active})"