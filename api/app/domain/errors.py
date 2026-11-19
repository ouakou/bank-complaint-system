class DomainError(Exception):
    """Base class for all business-rule errors; the API turns these into the error envelope."""

    http_status = 400
    code = "DOMAIN_ERROR"
    retryable = False

    def __init__(self, message="", details=None):
        super().__init__(message)
        self.message = message
        self.details = details


class NotFound(DomainError):
    http_status = 404

    def __init__(self, entity, entity_id):
        super().__init__(
            f"{entity.capitalize()} {entity_id} not found",
            details={"entity": entity, "id": entity_id},
        )
        self.code = f"{entity.upper()}_NOT_FOUND"


class InvalidTransition(DomainError):
    code = "INVALID_STATUS_TRANSITION"
    http_status = 409

    def __init__(self, old_status, new_status, hint=""):
        super().__init__(
            f"Cannot change status from '{old_status}' to '{new_status}'{hint}",
            details={"from": old_status, "to": new_status},
        )


class ForbiddenRole(DomainError):
    code = "FORBIDDEN_ROLE"
    http_status = 403

    def __init__(self, role, action):
        super().__init__(
            f"Role '{role}' is not allowed to {action}",
            details={"role": role},
        )


class ApprovalRequired(DomainError):
    code = "APPROVAL_REQUIRED"
    http_status = 409

    def __init__(self, complaint_id, action="this change"):
        super().__init__(
            f"Complaint {complaint_id} requires approval for {action}",
            details={"complaint_id": complaint_id},
        )



class ApiError(Exception): 
    """Raised by API dependencies (for example missing actor headers).""" 

    def __init__(self, http_status, code, message): 
        super().__init__(message) 
        self.http_status, self.code, self.message = http_status, code, message 