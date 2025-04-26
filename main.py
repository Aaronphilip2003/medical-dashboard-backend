from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import (
    disease_routes, 
    demographic_routes, 
    resource_routes, 
    nlq_routes, 
    auth_routes,
    prediction_routes  # Add the new prediction routes
)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://medical-dashboard-mit-wpu.vercel.app"  # Remove trailing slash and specific paths
]

# Add CORS middleware BEFORE any routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Include routers
app.include_router(disease_routes.router)
app.include_router(demographic_routes.router)
app.include_router(resource_routes.router)
app.include_router(nlq_routes.router, prefix="/nlq")
app.include_router(auth_routes.router, prefix="/auth")
app.include_router(prediction_routes.router, prefix="/predictions")  # Add with prefix