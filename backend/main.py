from fastapi import FastAPI
from . import authenticate_endpoint
from . import deposit_endpoint
from . import transfer_endpoint
from . import user_endpoint

app = FastAPI(
    title="Banking System API",
    description="API for a simple banking system with authentication, deposit, and transfer functionalities.",
    version="1.0.0",
)

# Include the routers from the respective endpoint files
app.include_router(authenticate_endpoint.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(deposit_endpoint.router, prefix="/api/v1", tags=["Transactions"])
app.include_router(transfer_endpoint.router, prefix="/api/v1", tags=["Transactions"])
app.include_router(user_endpoint.router, prefix="/api/v1", tags=["Users"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Banking System API! Visit /docs for API documentation."}

