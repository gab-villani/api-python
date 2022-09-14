import email
from fastapi import APIRouter, Depends
from Database.database import get_db
from sqlalchemy.sql.elements import and_, or_
from sqlalchemy.orm import Session
from Database.funcionario_db_database import Funcionarios
from Models.funcionario_model import FuncionarioModel
from Models.cliente_model import ClienteModel
from fastapi.exceptions import HTTPException

Route_Funcionarios = APIRouter()

@Route_Funcionarios.get('/lista-funcionarios/{pagina}/{qtde}', status_code=200, tags=["Funcionarios"])
def lista_funcionarios(pagina: int, qtde: int, db: Session = Depends(get_db)):
    
    Data = db.query(Funcionarios).filter().limit(qtde).offset(pagina).all()

    QtdeRegistros = db.query(Funcionarios).filter().count()

    return {
        "QtdeRegistros": QtdeRegistros,
        "Data": Data
    }

@Route_Funcionarios.get('/lista-funcionarios-por-nome/{nome}', status_code=200, tags=["Funcionarios"])
def lista_nome_Funcionario(nome: str = "", db: Session = Depends(get_db)):
    
    Data = db.query(Funcionarios).filter(  
        Funcionarios.nome.ilike("%{}%".format(nome))
    ).all()

    QtdeRegistros = db.query(Funcionarios).filter(  
        Funcionarios.nome.ilike("%{}%".format(nome))
    ).count()

    return {
        "QtdeRegistros": QtdeRegistros,
        "Data": Data
    }

@Route_Funcionarios.post('/incluir-cliente/', status_code=200, tags=["Funcionarios"])
def incluir_Funcionarios(func:FuncionarioModel , db: Session = Depends(get_db)):

    try:
        incluir = Funcionarios(   
        nome = func.nome,
        email = func.email,
        senha = func.senha
        )

        db.add(incluir)
        db.commit()
        id = incluir.id
        db.close()

        return {"id_funcionario": id }

    except Exception as e:
        print(e)

@Route_Funcionarios.put('/alterar-funcionario', status_code=200, tags=["Funcionarios"])
def alterar_funcionarios(func: FuncionarioModel, db: Session = Depends(get_db)):

    alterou = db.query(Funcionarios).filter(Funcionarios.id == func.id).\
        update({
            "nome": func.nome
        })

    db.commit()
    db.close()

    if alterou > 0:
        return {"detail" : "Registro alterado com sucesso!!!"}
    else:
        raise HTTPException(status_code=500, detail="Funcionario não encontrado") 
   

@Route_Funcionarios.delete('/excluir-funcionario/{id}', status_code=200, tags=["Funcionarios"])
def excluir_funcionarios(idfunc: int, db: Session = Depends(get_db)):

    alterou = db.query(Funcionarios).filter(Funcionarios.id == idfunc).delete()
    db.commit()
    db.close()

    if alterou > 0:
        return {"detail": "Usuario Excluído com Sucesso!!!"}
    else:
        raise HTTPException(status_code=500, detail="Funcionario não encontrado")         