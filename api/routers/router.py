from fastapi import APIRouter
from api.confs.settings import settings


router = APIRouter(
    prefix=settings.APP_PREFIX
)
