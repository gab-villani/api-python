import email
from fastapi import APIRouter, Depends
from Database.cliente_db_database import Clientes
from Database.database import get_db
from sqlalchemy.sql.elements import and_, or_
from sqlalchemy.orm import Session
from Database.usuario_db_database import Usuario
from Models.usuario_model import UsuarioModel
from Models.cliente_model import ClienteModel
from fastapi.exceptions import HTTPException

Route_Clientes = APIRouter()

@Route_Clientes.get('/lista-clientes/{pagina}/{qtde}', status_code=200, tags=["Clientes"])
def lista_cliente(pagina: int, qtde: int, db: Session = Depends(get_db)):
    
    Data = db.query(Clientes).filter().limit(qtde).offset(pagina).all()

    QtdeRegistros = db.query(Clientes).filter().count()

    return {
        "QtdeRegistros": QtdeRegistros,
        "Data": Data
    }

@Route_Clientes.get('/lista-clientes-por-nome/{nome}', status_code=200, tags=["Clientes"])
def lista_nome_cliente(nome: str = "", db: Session = Depends(get_db)):
    
    Data = db.query(Clientes).filter(  
        Clientes.nome.ilike("%{}%".format(nome))
    ).all()

    QtdeRegistros = db.query(Clientes).filter(  
        Clientes.nome.ilike("%{}%".format(nome))
    ).count()

    return {
        "QtdeRegistros": QtdeRegistros,
        "Data": Data
    }

@Route_Clientes.post('/incluir-cliente/', status_code=200, tags=["Clientes"])
def incluir_clientes(clientes: ClienteModel, db: Session = Depends(get_db)):

    try:
        incluir = Clientes(   
            nome = clientes.nome,
            email = clientes.email,
            senha = clientes.senha
        )

        db.add(incluir)
        db.commit()
        id = incluir.id
        db.close()

        return {"id_cliente": id }

    except Exception as e:
        print(e)

@Route_Clientes.put('/alterar-cliente', status_code=200, tags=["Clientes"])
def alterar_clientes(cliente: ClienteModel, db: Session = Depends(get_db)):

    alterou = db.query(Clientes).filter(Clientes.id == cliente.id).\
        update({
            "nome": cliente.nome
        })

    db.commit()
    db.close()

    if alterou > 0:
        return {"detail" : "Registro alterado com sucesso!!!"}
    else:
        raise HTTPException(status_code=500, detail="Cliente não encontrado") 
   

@Route_Clientes.delete('/excluir-cliente/{id}', status_code=200, tags=["Clientes"])
def excluir_clientes(idcliente: int, db: Session = Depends(get_db)):

    alterou = db.query(Clientes).filter(Clientes.id == idcliente).delete()
    db.commit()
    db.close()

    if alterou > 0:
        return {"detail": "Usuario Excluído com Sucesso!!!"}
    else:
        raise HTTPException(status_code=500, detail="Cliente não encontrado")         