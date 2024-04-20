<h1>Projeto Full-Stack-Basico Back-End</h1> 

- Projeto que contempla o MVP para o primeiro modulo da PÓS GRADUAÇÃO de Engenharia de Software da PCU
- O MVP pensado nesse modulo é um projeto de cadastro de políticas em um motor de análise de crédito
- O projeto consiste em cadastrar, atualizar e desativar regras, políticas e demais componentes


[![PyPI](https://img.shields.io/pypi/pyversions/apache-superset.svg?maxAge=2592000)](https://pypi.python.org/pypi/apache-superset)


> Status do Projeto: :heavy_check_mark: :warning: (concluido, em desenvolvimento, etc)

### Tópicos 

:small_blue_diamond: [Descrição do projeto](#descrição-do-projeto)

:small_blue_diamond: [Visão Geral da Solução](#visao-geral-da-solucao)

:small_blue_diamond: [Funcionalidades](#funcionalidades)

:small_blue_diamond: [Pré-requisitos](#pré-requisitos)

... 

Insira os tópicos do README em links para facilitar a navegação do leitor

## Descrição do projeto 

<p align="justify">
  O problema que estamos abordando envolve o gerenciamento de políticas de crédito.
</p>

## Visão Geral da Solução

Na solução, foram criadas três elementos principais:

- Política
- Camadas
- Regras

Além disso, foram criados dois elementos auxiliares:

- Associação de Política com Camada
- Associação de Camada com Regra

## Pré-requisitos

- Python 3.11.3
- pip (gerenciador de pacotes Python)

## Funcionalidades

:heavy_check_mark: Funcionalidade 1  

:heavy_check_mark: Funcionalidade 2  

:heavy_check_mark: Funcionalidade 3  

:heavy_check_mark: Funcionalidade 4  

Se ainda não houver deploy, insira capturas de tela da aplicação ou gifs

## Pré-requisitos

:warning: [Node](https://nodejs.org/en/download/)

No terminal, clone o projeto: 

```bash
# Clonar o projeto
git clone https://github.com/humbertoinfnet/full-stack-basico-front-end.git
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