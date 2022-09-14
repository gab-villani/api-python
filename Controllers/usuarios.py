from fastapi import APIRouter, Depends
from Database.database import get_db
from sqlalchemy.sql.elements import and_, or_
from sqlalchemy.orm import Session
from Database.usuario_db_database import Usuario
from Models.usuario_model import UsuarioModel
from fastapi.exceptions import HTTPException

Route_Usuarios = APIRouter()

@Route_Usuarios.get('/lista-usuario/{pagina}/{qtde}', status_code=200, tags=["Usuarios"])
def lista_usuario(pagina: int, qtde: int, db: Session = Depends(get_db)):
    
    Data = db.query(Usuario).filter().limit(qtde).offset(pagina).all()

    QtdeRegistros = db.query(Usuario).filter().count()

    return {
        "QtdeRegistros": QtdeRegistros,
        "Data": Data
    }

@Route_Usuarios.get('/lista-usuario-por-nome/{nome}', status_code=200, tags=["Usuarios"])
def lista_nome_usuario(nome: str = "", db: Session = Depends(get_db)):
    
    Data = db.query(Usuario).filter(  
        Usuario.nome.ilike("%{}%".format(nome))
    ).all()

    QtdeRegistros = db.query(Usuario).filter(  
        Usuario.nome.ilike("%{}%".format(nome))
    ).count()

    return {
        "QtdeRegistros": QtdeRegistros,
        "Data": Data
    }

@Route_Usuarios.post('/incluir-usuario/', status_code=200, tags=["Usuarios"])
def incluir_usuarios(usuario: UsuarioModel, db: Session = Depends(get_db)):

    try:
        incluir = Usuario(   
            nome = usuario.nome
        )

        db.add(incluir)
        db.commit()
        id = incluir.id
        db.close()

        return {"id_usuario": id }

    except Exception as e:
        print(e)

@Route_Usuarios.put('/alterar-usuario', status_code=200, tags=["Usuarios"])
def alterar_usuarios(usuario: UsuarioModel, db: Session = Depends(get_db)):

    alterou = db.query(Usuario).filter(Usuario.id == usuario.id).\
        update({
            "nome": usuario.nome
        })

    db.commit()
    db.close()

    if alterou > 0:
        return {"detail" : "Registro alterado com sucesso!!!"}
    else:
        raise HTTPException(status_code=500, detail="Usuario não encontrado") 
   

@Route_Usuarios.delete('/excluir-usuario/{id}', status_code=200, tags=["Usuarios"])
def excluir_usuarios(idusuario: int, db: Session = Depends(get_db)):

    alterou = db.query(Usuario).filter(Usuario.id == idusuario).delete()
    db.commit()
    db.close()

    if alterou > 0:
        return {"detail": "Usuario Excluído com Sucesso!!!"}
    else:
        raise HTTPException(status_code=500, detail="Usuario não encontrado")         