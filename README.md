<h1>Projeto Full-Stack-Basico Back-End</h1> 

- Projeto que contempla o MVP para o primeiro modulo da PÓS GRADUAÇÃO de Engenharia de Software da PUC
- O MVP pensado nesse modulo é um projeto de cadastro de políticas
- O projeto consiste em cadastrar, atualizar e desativar regras, políticas e demais componentes


[![PyPI](https://img.shields.io/pypi/pyversions/apache-superset.svg?maxAge=2592000)](https://pypi.python.org/pypi/apache-superset)


> Status do Projeto: :heavy_check_mark: Concluido

... 

## Descrição do projeto 

<p align="justify">
  O problema que estamos abordando envolve o gerenciamento de políticas de crédito.
</p>

## Visão Geral da Solução

Na solução, foram criadas três elementos principais:

- Políticas
- Camadas
- Regras

Além disso, foram criados dois elementos auxiliares:

- Associação de Política com Camada
- Associação de Camada com Regra

## Pré-requisitos

:warning: [Python 3.11.3](https://www.python.org/downloads/release/python-3113/)

## Funcionalidades

:heavy_check_mark: Políticas: Criação | Edição | Delete | Busca

:heavy_check_mark: Camadas: Criação | Edição | Delete | Busca

:heavy_check_mark: Regras: Criação | Edição | Delete | Busca

No terminal, clone o projeto: 

```bash
# Clonar o projeto
git clone https://github.com/humbertoinfnet/desenvolvimento-fullstack-basico.git
```

Recomenda-se o uso de um ambiente virtual (virtualenv) para isolar as dependências do projeto. Para configurar e ativar um ambiente virtual, execute os seguintes comandos no terminal:
```bash
# Instalar o virtualenv, se ainda não estiver instalado
pip install virtualenv

# Criar um novo ambiente virtual
virtualenv venv

# Ativar o ambiente virtual (Windows)
venv\Scripts\activate

# Ativar o ambiente virtual (Linux/Mac)
source venv/bin/activate

# Instalação dos pacotes python
pip install -r requirements.txt
```

Rodando a aplicação: 

```bash
# No diretório raiz do poprojeto executar o comando
python app.py
```

## Estrutura do Projeto
| Diretorio       | Diretorio              | Diretorio       | Diretorio         | Descrição                                                      |  
|---------------|----------------------|---------------|-----------------|------------------------------------------------------------------------|
| src/          |                      |               |                 | Diretório raiz do projeto                                              |
|               | entities/            |               |                 | Entidades principais do projeto, como classes ou objetos               |
|               | external_interfaces/ |               |                 | Diretório relacionado a configurações de aplicações externas           |
|               |                      | database/     |                 | Código relacionado ao banco de dados                                   |
|               |                      |               | controllers/    | Lógica de execução das consultas SQL                                   |
|               |                      |               | models/         | Definição dos modelos de tabelas                                       |
|               |                      | flask_server/ |                 | Códigos relacionado ao Flask                                           |
|               |                      |               | routers/        | Definição das rotas da API                                             |
|               |                      |               | app             | Configurações do servidor Flask                                        |
|               |                      |               | register_route  | Código para registrar as rotas                                         |
|               | interface_adapters/  |               |                 | Códigos que fazem a interface entre casos de uso e aplicações externas |
|               | log/                 |               |                 | Configuração dos logs                                                  |
|               | use_case/            |               |                 | Casos de uso do projeto                                                |
|               |                      | motor/        |                 | Lógica dos casos de uso relacionados ao motor                          |
| app           |                      |               |                 | Arquivos específicos da aplicação principal                            |
| requirements  |                      |               |                 | Lista de dependências do projeto                                       |
| gitignore     |                      |               |                 | Arquivo para especificar arquivos e diretórios que devem ser ignorados pelo git |

