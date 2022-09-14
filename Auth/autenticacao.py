from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from Auth.auth_handler import signJWT
from Auth.auth_bearer import JWTBearer
from Database.database import get_db
from sqlalchemy.orm import Session
import sqlalchemy

Route_autenticacao = APIRouter()

@Route_autenticacao.post("/autentica", status_code=200, tags=["Segurança"])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    try:
        strSQL = """
            SELECT id, nome 
            FROM "Clientes"
            WHERE email = '{email}' AND senha = '{senha}'
        """.format(email=form_data.username, senha=form_data.password)

        result = db.execute(sqlalchemy.text(strSQL)).fetchall()
        
        id = 0
        nome = ''
        print(result)

        for user in result:
            id= user.id    
            nome = user.nome
            print(user)
            
        print(id)
        if id == 0:
            raise HTTPException(status_code=401, detail="Falha na autenticação")
        else:
            return {"id": id,"nome": nome,"access_token": signJWT(form_data.username)}
            
    except Exception as e:
        print(e)