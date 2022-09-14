from typing import Optional, List
import pyodbc, json, collections, uvicorn, requests, sys
from datetime import datetime
from fastapi import FastAPI, Body, Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
# from auth.auth_handler import signJWT
from Controllers.usuarios import Route_Usuarios
# from Controllers.spi_sensor import Route_Sensor_Spi
# from auth.autenticacao import Route_Autenticacao

server = '127.0.0.1' 
database = 'gabrielaAprendizagem' 
username = 'postgres' 
password = '123' 

erro = ''

print(pyodbc.drivers())

try:
    conn = pyodbc.connect('DRIVER={PostgreSQL Unicode};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password+';PORT=5432;autocommit=True;autosave=always')
    erro = 'Api-SPI100 Online.'
except pyodbc.Error as ex:
    sqlstate = ex.args[1]
    erro = sqlstate 
    print(erro)

app = FastAPI(title="Apis gabriela",
    description="minhas apis em python",
    version="1.0.0",)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/autentica")


origins = [
    "http://salaoday.com.br",
    "http://spi100.s3-website-us-east-1.amazonaws.com/",
    "https://salaoday.com.br",
    "https://app-spi.web.app",
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8580",
    "http://localhost:8080",
    "http://localhost:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Route_Usuarios, prefix='/api/usuarios')
# app.include_router(Route_Cidades, prefix='/api/cidades')
# app.include_router(Route_Custo_Fixo, prefix='/api/custo-fixo')
# app.include_router(Route_Funcionarios, prefix='/api/funcionarios')