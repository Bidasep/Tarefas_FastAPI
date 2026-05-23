#Objetivo com 
# Passo 1. Criar um Modelo com Pydantic
#Crie uma aplicação simples utilizando FastAPI para gerenciar um conjunto de tarefas. A aplicação deve permitir as seguintes operações:

#Adicionar uma nova tarefa com um nome e uma descrição.

#Listar todas as tarefas cadastradas.

#Marcar uma tarefa como concluída.

#Remover uma tarefa.

#Passo a Passo:
#Criação da Aplicação FastAPI
#Crie um arquivo Python chamado app.py e inicialize a aplicação FastAPI. Para isso, importe a classe FastAPI e crie uma instância da aplicação.

#Definindo uma Lista de Tarefas
#Crie uma lista de dicionários para armazenar as tarefas. Cada tarefa será representada como um dicionário com os campos "nome", "descrição" e "concluída" (inicialmente como False).

#Rota para Adicionar uma Tarefa
#Crie uma rota do tipo POST que permita adicionar uma nova tarefa. A rota deverá receber um corpo JSON com os campos "nome" e "descrição" e adicionar a tarefa à lista.

#rota para Listar as Tarefas
#Crie uma rota do tipo GET que exiba todas as tarefas. A resposta deve incluir o nome, a descrição e se a tarefa foi concluída ou não.

#Rota para Marcar uma Tarefa como Concluída
#Crie uma rota do tipo PUT que permita marcar uma tarefa como concluída. Para isso, a rota deve receber o nome da tarefa e alterar o valor do campo "concluída" para True se a tarefa existir.

#Rota para Remover uma Tarefa
#Crie uma rota do tipo DELETE que permita remover uma tarefa da lista. A rota deve receber o nome da tarefa e removê-la da lista se existir.

#Testando a Aplicação
#Após implementar as rotas, utilize o Insomnia ou Postman para testar as funcionalidades. Envie requisições POST para adicionar tarefas, GET para listar, PUT para marcar tarefas como concluídas e DELETE para remover tarefas.#

# 1 INSTALAR PACOTES E DEPENDENCIAS:
#1 - poetry init -> NOME DO PROJETO (sem espaços)
#2 - poetry shell -> iniciar o gerenciador de dependencias
#3 - para iniciar o servidor virtual : poetry add fastapi[standard]
#4 - em seguida fastapi dev "main.py" main sem aspas, é o nome do arquivo principal.
#INSTALANDO O SQL LITE
#poetry add sqlalchemy aiosqlite  //  SÃO DOIS ARQUIVOS ALCHEMY E SQLITE

#após podemos inicar o projeto



from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


#Passo 1. Criar um Modelo com Pydantic OK
class Tarefa(BaseModel):
    nome : str
    descricao : str
    concluida : bool =False
    




app = FastAPI()


minhas_tarefas = []

#Definindo uma Lista de Tarefas
    

@app.get("/")
def read_root():
    return {"Hello": "World, a API está ok!"}


# Rotas e endpoints

#Rota para ver  as Tarefa
@app.get("/tarefas")
def get_tarefas():
    if not minhas_tarefas:
        return{ "Message": "não existe tarefas"}
    else:
        return{"tarefas": minhas_tarefas}
    



@app.post("/adiciona")
def post_tarefa(tarefa:Tarefa):

    for item in minhas_tarefas:
        if item.nome == tarefa.nome:
            raise HTTPException(status_code = 400, detail = "Essa tarefa já existe !")
        
    minhas_tarefas.append(tarefa)
    return { "Mensagem" : "Tarefa adicionada com sucesso!",
            "tarefa":tarefa
    }
    




@app.put("/atualiza/{nome}")
def put_tarefa(nome:str):   
    
    
    for tarefa in minhas_tarefas:
        if tarefa.nome == nome:
            tarefa.concluida = True
            return { "message":f" Tarefa '{nome}' Foi concluida com sucesso!"}
            
            
    raise HTTPException(status_code = 404, detail = "Essa tarefa não existe !")

    
    
       
    
    
@app.delete("/delete/{nome}")
def delete_tarefa(nome:str):

    for tarefa in minhas_tarefas:
        if tarefa.nome == nome:
            minhas_tarefas.remove(tarefa)
            return{"message":"Esta tarefa foi deletada com sucesso"}
    
    raise HTTPException(status_code = 404, detail = "Essa tarefa não existe !")
        
        
    