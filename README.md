# Projeto 10 — Mapa de Focos de Calor com Flask, Leaflet e PostGIS

## Sobre o projeto

Esta aplicação exibe focos de calor do programa Queimadas do INPE em um mapa utilizando Leaflet no front-end e Flask no back-end.

O usuário pode desenhar uma área no mapa e a aplicação realiza um cruzamento geoespacial diretamente no PostgreSQL utilizando PostGIS para retornar a quantidade de focos de calor presentes dentro da região selecionada.

---

# Tecnologias utilizadas

* Python
* Flask
* PostgreSQL
* PostGIS
* Leaflet
* Leaflet Draw
* Pandas
* SQLAlchemy
* Jupyter Notebook

---

# Pré-requisitos

Antes de executar o projeto, instale:

## 1. Python

Baixe e instale:

[https://www.python.org/downloads/](https://www.python.org/downloads/)

Durante a instalação marque:

```text
Add Python to PATH
```

Teste no terminal:

```bash
python --version
```

---

## 2. PostgreSQL

Baixe e instale:

[https://www.postgresql.org/download/](https://www.postgresql.org/download/)

Durante a instalação:

* usuário padrão: `postgres`
* escolha uma senha
* porta padrão: `5432`

---

## 3. PostGIS

Baixe a versão compatível com sua versão do PostgreSQL:

[https://postgis.net/install/](https://postgis.net/install/)

Depois da instalação, abra o pgAdmin e execute:

```sql
CREATE EXTENSION postgis;
```

Teste:

```sql
SELECT PostGIS_Version();
```

---

## 4. Jupyter Notebook

Instale pelo terminal:

```bash
pip install notebook
```

---

# Clonando o projeto

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta:

```bash
cd nome-do-projeto
```

---

# Instalando dependências Python

No terminal:

```bash
pip install flask pandas sqlalchemy psycopg2-binary notebook
```

---

# Estrutura do projeto

```text
Projeto10/
│
├── app.py
├── focos_mensal_br_202604.csv
├── Untitled.ipynb
├── templates/
│   └── index.html
└── static/
```

---

# Criando o banco de dados

Abra o pgAdmin.

Crie um banco chamado:

```sql
CREATE DATABASE focosdb;
```

Conecte-se ao banco `focosdb` e execute:

```sql
CREATE EXTENSION postgis;
```

---

# Criando a tabela

Execute no Query Tool:

```sql
CREATE TABLE focos (
    id UUID PRIMARY KEY,
    lat DOUBLE PRECISION,
    lon DOUBLE PRECISION,
    data_hora_gmt TIMESTAMP,
    municipio VARCHAR(100),
    estado VARCHAR(100),
    bioma VARCHAR(100),
    geom GEOMETRY(Point, 4326)
);
```

---

# Importando os dados do CSV

Abra o Jupyter Notebook:

```bash
jupyter notebook
```

Abra o notebook do projeto.

---

## 1. Ler o CSV

```python
import pandas as pd

df = pd.read_csv("focos_mensal_br_202604.csv")
```

---

## 2. Selecionar colunas utilizadas

```python
df_reduzido = df[['id', 'lat', 'lon', 'data_hora_gmt', 'municipio', 'estado', 'bioma']]
```

---

## 3. Converter data

```python
df_reduzido['data_hora_gmt'] = pd.to_datetime(df_reduzido['data_hora_gmt'])
```

---

## 4. Conectar ao PostgreSQL

Troque `SUA_SENHA` pela senha utilizada na instalação do PostgreSQL.

```python
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:SUA_SENHA@localhost:5432/focosdb")
```

---

## 5. Inserir dados na tabela

```python
df_reduzido.to_sql(
    "focos",
    engine,
    if_exists="append",
    index=False
)
```

---

# Criando a geometria espacial

No pgAdmin execute:

```sql
UPDATE focos
SET geom = ST_SetSRID(ST_MakePoint(lon, lat), 4326);
```

---

# Executando a aplicação

No terminal execute:

```bash
python app.py
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:5000
```

---

# Como utilizar

1. Abra o mapa no navegador.
2. Utilize a ferramenta de desenho no canto superior esquerdo.
3. Desenhe um polígono ou retângulo.
4. A aplicação enviará a área para o Flask.
5. O PostgreSQL/PostGIS realizará o cruzamento geoespacial.
6. Um alerta exibirá a quantidade de focos de calor encontrados na área selecionada.

---

# Consulta espacial utilizada

O cruzamento geoespacial é realizado utilizando:

```sql
ST_Contains(
    ST_GeomFromText(...),
    geom
)
```

---

# Fonte dos dados

Dados obtidos do programa Queimadas do INPE:

[https://terrabrasilis.dpi.inpe.br/queimadas/portal/pages/secao_downloads/dados-abertos/#da-focos](https://terrabrasilis.dpi.inpe.br/queimadas/portal/pages/secao_downloads/dados-abertos/#da-focos)

---

# Autor

Projeto acadêmico desenvolvido utilizando Flask, Leaflet e PostGIS.
