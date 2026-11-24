from domain.errors import DomainError       # add to the imports 
from fastapi import Request


class ApiError(Exception): 
    """Raised by API dependencies (for example missing actor headers).""" 

  
    def __init__(self, http_status, code, message): 
        super().__init__(message) 
        self.http_status, self.code, self.message = http_status, code, message 
  

# inside install_error_handlers(app), above the 503 handler: 
def install_error_handlers(app):

    @app.exception_handler(DomainError) 
    async def domain_error(request: Request, exc: DomainError): 
        return error_response(request, exc.http_status, exc.code, exc.message, exc.retryable, 
                        details=exc.details) 

  
    @app.exception_handler(ApiError) 
    async def api_error(request: Request, exc: ApiError): 
        return error_response(request, exc.http_status, exc.code, exc.message) 