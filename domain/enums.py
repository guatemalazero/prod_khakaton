from enum import Enum

class PurchaseStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    SUCCESS = 'SUCCESS'
    CANCELED = 'CANCELED'

class OrderStatus(str, Enum):
    PENDING = 'PENDING'
    PAID = 'PAID'
    REFUNDED = 'REFUNDED'

class TransactionType(str, Enum):
    DEPOSIT = 'DEPOSIT'
    PAYMENT = 'PAYMENT'
    REFUND = 'REFUND'
    REWARD = 'REWARD'

class ParticipantRole(str, Enum):
    ORGANIZER = 'ORGANIZER'
    PARTICIPANT = 'PARTICIPANT'