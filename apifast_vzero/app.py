from http import HTTPStatus
from fastapi.responses import HTMLResponse
from fastapi import FastAPI

from apifast_vzero.schemas import message


app = FastAPI()


#por padrão, o FastAPI retorna um JSON, mas podemos retornar HTML usando a classe HTMLResponse
@app.get(
        '/', status_code=HTTPStatus.OK,
          response_class=HTMLResponse,
          response_model=message
          )
def read_root():
    return {'message': 'Hello World!'}

"""@app.get(
    '/html', status_code=HTTPStatus.OK,
      response_class=HTMLResponse
      )
def read_html():
    return '<h1>Hello World!</h1>'"""
