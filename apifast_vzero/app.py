from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from apifast_vzero.models import User

from .database import get_session
from .schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI(
    title='API Fast VZero',
    version='0.0.0',
)


# por padrão, o FastAPI retorna um JSON
@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello World!'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):

    query = select(User).where(
        (User.username == user.username) | (User.email == user.email)
    )
    db_user = session.scalar(query)
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Username já existe'
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Email já existe'
            )

    db_user = User(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user  # O FastAPI já converte para UserPublic automaticamente

    # user_with_id = UserDB(
    #   **user.model_dump(),
    #    id=len(database) + 1,)
    # database.append(user_with_id)
    # return user_with_id"""


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    limit: int = 10,  # limit e offset para paginação
    offset: int = 10,
    session: Session = Depends(get_session),
):

    users = session.scalars(select(User).limit(limit).offset(offset)).all()
    return {'users': users}


@app.put('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    try:
        user_db.username = user.username
        user_db.email = user.email
        user_db.password = user.password

        session.add(user_db)
        session.commit()
        session.refresh(user_db)

        return user_db
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Username ou email já existe'
        ) from None


@app.delete('/users/{user_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )
    session.delete(user_db)
    session.commit()
    return {'message': 'Usuário deletado com sucesso'}


@app.get('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    return user_db
