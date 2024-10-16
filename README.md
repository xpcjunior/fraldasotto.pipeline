# Fraldas Otto Pipeline

Pipeline ETL para ingestão de dados de abas de uma planilha do Google Sheet e carregamento de informações obtidas a partir do tratamento destes em uma base de dados NoSQL, o Google Firestore. Estes dados são de registros de ganho, compra e utilização de fraldas do meu primeiro filho, Otto, em sua jornada até o desfraldamento.

![image](/readme_itens/diagrama.gif)

## Requisitos:

Para conseguir executar esta aplicação, você precisará de:

- AirFlow instalado;
- Uma aplicação no [Firebase](https://console.firebase.google.com) com uma base de dados Firestore habilitada;
- Python;

## Configuração

1. Adicione à sua lista de Connections do Airflow uma nova conexão chamada _"fraldas_otto_firestore"_, ela é do tipo Google Cloud. Esta conexão irá conter as credenciais para acesso da sua base Firestore obtidas no seu Firebase Console. O JSON de conexão deve ser colocado por completo no campo _"Keyfile JSON"_.

1. Adicione à sua lista de Connections do Airflow uma nova conexão chamada _"fraldas_otto_gsheet"_, ela é do tipo HTTP. Esta conexão armazena a URL base para acesso à planilha que contém os dados brutos sobre as fraldas.

2. Esta aplicação necessita de algumas informações sigilosas, por isso utilizei variáveis do Airflow para protegê-las, as quais você deve preencher com suas próprias informações. Em Airflow Variables configure as seguintes variáveis:

```properties
ID_TAB_G_SHEET_GANHADAS = Este é o ID da aba onde estão as fraldas ganhadas
ID_TAB_G_SHEET_COMPRADAS = Este é o ID da aba onde estão as fraldas compradas
ID_TAB_G_SHEET_UTILIZADAS = Este é o ID da aba onde estão as fraldas utilizadas
FIRESTORE_COLLECTION_NAME = Este é o nome da coleção no Firestore onde os dados tratados serão salvos
FIRESTORE_DOCUMENT_ID = Este é o nome do documento que será sempre atualizado no Firestore
```

3. Recomendo fortemente que você crie um ambiente virtual do Python em sua máquina (venv) e execute o comando a baixo para instalar todas as dependências necessárias para o funcionamento do pipeline:

```bash
pip install -r requirements.txt
```

## Visualizando o resultado deste pipeline

Este projeto possui uma aplicação frontend em Angular que exibe as informações tratadas da base de dados Firestore. 

- Confira [aqui](https://github.com/xpcjunior/fraldasotto.frontend) o código-fonte dela
- Confira [aqui](https://fraldas-otto.web.app/) a aplicação rodando

## Dados brutos

Os dados brutos deste pipeline são oriundos de uma planilha salva em Cloud.

- Clique [aqui](https://docs.google.com/spreadsheets/d/1alaeZRchzrXYqNJ_WGEk8DkcjRkIOn-BXtkCqqGMXBM) e confira a planilha.