from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from . import authenticate_endpoint
from . import deposit_endpoint
from . import transfer_endpoint
from . import user_endpoint

app = FastAPI(
    title="Banking System API",
    description="API for a simple banking system with authentication, deposit, and transfer functionalities.",
    version="1.0.0",
)

# Add CORS middleware
# In a production environment, you should restrict the origins to the specific domain of your Streamlit app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include the routers from the respective endpoint files
app.include_router(authenticate_endpoint.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(deposit_endpoint.router, prefix="/api/v1", tags=["Transactions"])
app.include_router(transfer_endpoint.router, prefix="/api/v1", tags=["Transactions"])
app.include_router(user_endpoint.router, prefix="/api/v1", tags=["Users"])

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@app.get("/")
async def root():
    return {"message": "Welcome to the Banking System API! Visit /docs for API documentation."}
