from enum import Enum

class GroupBuyStatus(str, Enum):
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failed'

class UserRole(str, Enum):
    USER = 'user'
    ADMIN = 'admin'