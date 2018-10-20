from enum import Enum, EnumMeta


class ChoiceEnumMeta(EnumMeta):
    def __iter__(self):
        return ((tag.name, tag.value) for tag in super().__iter__())


class DeliveryStatusEnum(Enum, metaclass=ChoiceEnumMeta):
    SCHEDULED = 'Scheduled'
    IN_PROGRESS = 'In progress'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'
