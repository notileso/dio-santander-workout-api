from fastapi import APIRouter
from app.modules import athlete, category, training_center

router = APIRouter()

router.include_router(athlete.router, prefix="/athletes", tags=["athletes"])
router.include_router(category.router, prefix="/categories", tags=["categories"])
router.include_router(training_center.router, prefix="/training-centers", tags=["training-centers"])

@router.get("/")
async def root():
    return {"message": "Hello World"}
