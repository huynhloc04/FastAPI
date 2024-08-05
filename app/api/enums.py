from enum import Enum


class ItemStatus(str, Enum):
    created = "created"
    updated = "updated"
    deleted = "deleted"
    failed = "failed"


class UserStatus(str, Enum):
    created = "created"
    updated = "updated"
    deleted = "deleted"
    inactive = "inactive"
    active = "active"
    failed = "failed"


class StoreStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    temp_inactive = "temp_inactive"


class StoreCode(int, Enum):
    duplicated = 1
    not_found = 2
    temp_closed = 3
    permanently_closed = 4
    declined = 5
    new_model = 6
    no_joined = 7
    succeeded = 8
    failed = 9
