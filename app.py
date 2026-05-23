#Objetivo com 
# Passo 1. Criar um Modelo com Pydantic e autenticação
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
#Criar um Modelo com Pydantic -  Importar o Base Model "from pydantic import BaseModel" - OK
#importar "from fastapi.security import HTTPBasic,HTTPBasicCredentials"
#importar "import secrets"
#importar "Depends" from fastapi



from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import HTTPBasic,HTTPBasicCredentials
import secrets

app = FastAPI()

#Passo 1. Criar um Modelo com Pydantic -  Importar o Base Model "from pydantic import BaseModel" - OK
class Tarefa(BaseModel):
    nome : str
    descricao : str
    concluida : bool =False
    
#Criar um usuário e senha de teste 
USUARIO = "admin"
SENHA = "12345" 

security = HTTPBasic()

#criar uma função para autenticar o usuário
def autenticar_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    
    # VE SE AS CREDENCIAIS DE USUÁRIO(USERNAME) É IGUAL AO USUÁRIO(O CRIADO COMO EXEMPLO OU O USUÁRIO OU O QUE ESTÁ SENDO PASSADO)
    is_username_correct = secrets.compare_digest(credentials.username, USUARIO)
    
    # VE SE AS CREDENCIAIS DE SENHA(PASSWORD) É IGUAL A SENHA(O CRIADO COMO EXEMPLO OU A SENHA QUE ESTÁ SENDO PASSADO)
    is_password_correct = secrets.compare_digest(credentials.password, SENHA)
    
    #se um dos dois estiver errado not (usuário e senha) lança e exception
    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou Senha incorretos",
            headers={"WWW-Authenticate":"Basic"}
        )




#Definindo uma Lista de Tarefas
minhas_tarefas = []

    
#rota inicial/ Teste da API
@app.get("/")
def read_root():
    return {"Hello": "World, a API está ok!"}


# Rotas e endpoints

#Rota para ver  as Tarefa
@app.get("/tarefas")
def get_tarefas(page:int =1, limit:int=10, ordenar_por:str = "nome", ordem:str = "asc", credentials: HTTPBasicCredentials = Depends(autenticar_usuario) ):
    
    #se o numero da página for menor que 1 ou limite de itens na pagina < 1 
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400,detail="page ou limit estão com valores inválidos!!!")
    
    #se nao existir nada em minhas_tarefas
    if not minhas_tarefas:
        return{ "Message": "não existe tarefas"}
    
    #Verificação da ordenação
    
    if ordem not in ["asc","desc"]:
        raise HTTPException(status_code=400,detail="Ordem deve ser 'asc' ou 'desc'")
    
    if ordenar_por not in ["nome","descricao","status"]:
        raise HTTPException(status_code=400,detail="Ordenação  deve ser por'nome' ou 'descricao' ou 'status' ! ")
    
    #estruturação do inicio e fim da pagina
    #inicio será na pagina -(menos) 1
    inicio = (page -1 )* limit
    fim = inicio + limit
    
    # a nova lista vai receber o item de acordo com os parametros. sorted vai ordenar os itens da lista "minhas_tarefas" mantendo a original.
    # o que vai vir ordenado? que está dentro do sorted( como dentro da lista tem objetos, nao da pra retornar direto ordenado
    #key = vai receber o valor do parametro para ordenar ex:"nome""descr"...vai usar uma função lambda(uma função rapida tipo arrow function)
    #para cada tarefa, pegue algum valor para usar na ordenação
    #getattr  = getattr(objeto, "atributo"), vai pegar o atributo escolhido "nome" "descrição"    tarefa."parametro escolhido (nome)"
    #reverse controla asc ou desc.
    #sorted()Ordena a lista. // key= Define QUAL valor usar na ordenação. // lambda = Cria uma função rápida. // getattr() Pega um atributo dinamicamente.
        
    #)
    tarefas_ordenadas = sorted(minhas_tarefas, key=lambda tarefa: getattr(tarefa,ordenar_por ), reverse=True if ordem =="desc" else False)
    
    tarefas_paginadas = tarefas_ordenadas[inicio:fim]
    
    return {
        "page": page,
        "limit": limit,
        "ordem": ordem,
        "ordenar_por":ordenar_por,
        "total" : len(minhas_tarefas),
        "tarefas": tarefas_paginadas
    }
    


#Rota para adicionar as tarefas
@app.post("/adiciona")
def post_tarefa(tarefa:Tarefa, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    #para cada item na "lista" minhas_tarefas 
    for item in minhas_tarefas:
        #se o item da lista tiver o nome do parametro "nome" lança uma exception
        if item.nome == tarefa.nome:
            raise HTTPException(status_code = 400, detail = "Essa tarefa já existe !")
    #se nao, adiciona o objeto Tarefa na lista minhas tarefas e retorna a mensagem.    
    minhas_tarefas.append(tarefa)
    return { "Mensagem" : "Tarefa adicionada com sucesso!",
            "tarefa":tarefa
    }
    



#Rota para atualizar uma tarefa "Concluida", recebe um nome como parametro
@app.put("/atualiza/{nome}")
def put_tarefa(nome:str, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):   
    
    #para cada tarefa da lista(minhas_tarefas)
    for tarefa in minhas_tarefas:
        #se a o nome da tarefa for igual o nome do parametro (nome passado) seta concluido para true e retorna mensagem
        if tarefa.nome == nome:
            tarefa.concluida = True
            return { "message":f" Tarefa '{nome}' Foi concluida com sucesso!"}
            
    #se nao achar a tarefa lança a exception        
    raise HTTPException(status_code = 404, detail = "Essa tarefa não existe !")

    
    
       
    
#Rota para deletar a tarefa    
@app.delete("/delete/{nome}")
def delete_tarefa(nome:str, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    #para cada tarefa da lista (minhas_tarefas)
    for tarefa in minhas_tarefas:
        #se o nome da tarefa for igual o nome passado pelo parametro
        if tarefa.nome == nome:
            #removve a tarefa da lista
            minhas_tarefas.remove(tarefa)
            return{"message":"Esta tarefa foi deletada com sucesso"}
        
        
    #se nao achar a tarefa lança a exception 
    raise HTTPException(status_code = 404, detail = "Essa tarefa não existe !")
        
        
    