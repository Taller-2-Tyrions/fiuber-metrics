from fastapi import APIRouter
from ..services import metric_services
from ..database.mongo import db

from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
    prefix="/metrics",
    tags=['Metrics']
)


@router.get('/users')
async def users_metric():
    # TODO: ok? O vamos a ms-users
    # check_block_permissions(user_caller)
    # print("in users")
    metric = metric_services.find_users_metric(db)
    return metric


@router.get('/payments')
async def payments_metric():
    metric = metric_services.find_payments_metric(db)
    return metric


@router.get('/voyages')
async def voyages_metric():
    metric = metric_services.find_voyages_metric(db)
    return metric
