from enum import Enum

class NonAdminRoles(str, Enum):
    neutralizer = "neutralizer"
    reviewer = "reviewer"
    hybrid = "hybrid"
    
class Roles(str, Enum):
    admin = "admin"
    neutralizer = "neutralizer"
    reviewer = "reviewer"
    hybrid = "hybrid"