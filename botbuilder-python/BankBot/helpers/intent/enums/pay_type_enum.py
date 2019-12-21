from enum import Enum


class PayType(Enum):
    NET = "net"
    GROSS = "gross"
    BOTH = "both"
    NONE = "None"