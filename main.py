#import cx_Oracle
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
import psycopg2
from pydantic import BaseModel

app = FastAPI()

class Categoria(BaseModel):
    id: int
    nome: str

def conexao_bd():
    #dsn = cx_Oracle.makedsn(host='oracle.fiap.com.br', port=1521, sid='ORCL')
    #conn = cx_Oracle.connect(user='rm97324', password='fiap23', dsn=dsn)
    
    conn = psycopg2.connect(host='drona.db.elephantsql.com', database='bvenwnsb', user='bvenwnsb', password='luVMPfUFPMunKnOsA4Zd11VqlEr1k86L')
    
    return conn

@app.post("/incluir_categoria", status_code=status.HTTP_201_CREATED)
def incluir_usuario(categoria: Categoria):
    try:
        conn = conexao_bd()
        cursor = conn.cursor()

        sql = f"INSERT INTO TB_CATEGORIA (ID, NOME) VALUES ({categoria.id}, '{categoria.nome}')"
        
        cursor.execute(sql)
        conn.commit()

        return {"message": "Categoria incluída com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Erro ao inserir categoria - " + str(e))
    finally:
        cursor.close()
        conn.close()

@app.put("/atualizar_categoria/{idCategoria}", status_code=status.HTTP_200_OK)
def atualizar_usuario(categoria: Categoria, idCategoria):
    try:
        conn = conexao_bd()
        cursor = conn.cursor()

        sql = f"UPDATE TB_CATEGORIA SET NOME='{categoria.nome}' WHERE ID={idCategoria}"

        cursor.execute(sql)
        conn.commit()

        return {"message": "Categoria atualizada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Erro ao atualizar a categoria - " + str(e))
    finally:
        cursor.close()
        conn.close()

@app.delete("/excluir_categoria/{idCategoria}", status_code=status.HTTP_200_OK)
def excluir_categoria(idCategoria):
    try:
        conn = conexao_bd()
        cursor = conn.cursor()

        sql = f"DELETE FROM TB_CATEGORIA WHERE ID={idCategoria}"

        cursor.execute(sql)
        conn.commit()

        return {"message": "Categoria excluída com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Erro ao excluir a categoria - " + str(e))
    finally:
        cursor.close()
        conn.close()

@app.get("/listar_categorias", status_code=status.HTTP_200_OK)
def listar_usuarios():
    try:
        conn = conexao_bd()
        cursor = conn.cursor()

        sql = "SELECT ID, NOME FROM TB_CATEGORIA ORDER BY ID"
        cursor.execute(sql)

        rows = cursor.fetchall()

        listaCategorias = []

        for row in rows:
            categoria = {"id": row[0], "nome": row[1]}
            listaCategorias.append(categoria)

        return listaCategorias
    except Exception as e:
        raise HTTPException(status_code=400, detail="Erro ao selecionar as categorias - " + str(e))
    finally:
        cursor.close()
        conn.close()

@app.get("/lista_categoria/{idCategoria}", status_code=status.HTTP_200_OK)
def lista_categoria(idCategoria: int):
    try:
        conn = conexao_bd()
        cursor = conn.cursor()

        sql = f"SELECT ID, NOME FROM TB_CATEGORIA WHERE ID={idCategoria}"
        cursor.execute(sql)

        rows = cursor.fetchall()

        categoria = None
        for row in rows:
            if (row[0] == idCategoria):
                categoria = {"id": row[0], "nome": row[1]}
                break

        if (not categoria):
            return JSONResponse(status_code=400, content={"message": "Categoria não existente!"})
        else:
            return categoria
    except Exception as e:
        raise HTTPException(status_code=400, detail="Erro ao selecionar a categoria - " + str(e))
    finally:
        cursor.close()
        conn.close()