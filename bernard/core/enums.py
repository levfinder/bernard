from enum import Enum


class DeliveryStatusEnum(Enum):
    SCHEDULED = 'Scheduled'
    IN_PROGRESS = 'In progress'
    COMPLETE = 'Complete'
    CANCELLED = 'Cancelled'
