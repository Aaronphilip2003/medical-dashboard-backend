from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import disease_routes, demographic_routes, resource_routes

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(disease_routes.router)
app.include_router(demographic_routes.router)
app.include_router(resource_routes.router)
