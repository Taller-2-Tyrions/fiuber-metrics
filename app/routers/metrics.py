from fastapi import APIRouter, status
from ..crud import crud
from ..database.mongo import db

router = APIRouter(
    prefix="/metrics",
    tags=['Metrics']
)

@router.post('/user')
def user_metric():
	# TODO: ok? O vamos a ms-users
	#check_block_permissions(user_caller)

	user_metric = crud.find_user_metric(db)

	return user_metric

