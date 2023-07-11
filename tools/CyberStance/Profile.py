
from enum import Enum

# Defining a profile

class Size(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    #_str_ method than converts to tag
class IndustryType(Enum):
    CONSUMER_PRODUCTS = 1
    MANUFACTURING = 2
    SERVICE_PROVIDER = 3
    TECHNOLOGIES = 4
    #_str_ method than converts to tag
class StandardType(Enum):
    ISO=1
    NIST=2
    ISM=3
    ITSG=4
    CIS=5
    OTHER=6

class Standard:
    def __init__(self, type: StandardType, other="") -> None:
        self.type: StandardType = type
        self.other: str = other

class Profile:
    def __init__(self) -> None:
        org_size: Size = None
        dedicated_sec_team: bool = None
        expertise: Size = None
        industry_type: IndustryType = None
        standard: Standard = None
    pass