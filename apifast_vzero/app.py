from http import HTTPStatus

from fastapi import FastAPI

from apifast_vzero.apifast_vzero.schemas import Message, UserSchema

app = FastAPI(
    title='API Fast VZero',
    description='API de exemplo para o curso de FastAPI',
    version='0.1.0',
)


# por padrão, o FastAPI retorna um JSON
@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello World!'}


@app.post('/users/')
def create_user(user: UserSchema):
    return user
