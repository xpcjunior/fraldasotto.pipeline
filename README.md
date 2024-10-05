# Fraldas Otto Pipeline

Pipeline ETL para ingestão de dados de abas de uma planilha do Google Sheet e carregamento de informações obtidas a partir do tratamento destes em uma base de dados NoSQL, o Google Firestore. Estes dados são de registros de ganho, compra e utilização de fraldas do meu primeiro filho, Otto, em sua jornada até o desfraldamento.

![image](/readme_itens/diagrama.gif)

## Requisitos:

Para conseguir executar esta aplicação, você precisará de:

- Uma conta no [Astronomer.io](https://cloud.astronomer.io/) ou AirFlow instalado;
- Possuir o astronomer CLI instalado em seu ambiente, caso tenha optado pelo Astronomer;
- Uma aplicação no [Firebase](https://console.firebase.google.com) com uma base de dados Firestore habilitada;
- Python;

## Configuração

1. Duplique e renomeie a duplicata do aquivo [firebase-adminsdk.example.json](/firebase-adminsdk.example.json) para **firebase-adminsdk.json**. Substitua os valores contidos no arquivo pelos valores obtidos no seu Firebase Console. Este arquivo é responsável pela conexão com sua base de dados Firestore.

2. Esta aplicação necessita de algumas informações sigilosas, por isso utilizei variáveis do Airflow para protegê-las, as quais você deve preencher com suas próprias informações. Em seu Astronomer ou Airflow configure as seguintes variáveis:

```properties
ID_G_SHEET = Este é o ID da sua planinha no Google Sheets
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

## Astronomer

O Astronomer é uma ferramenta web online grátis para utilização do Airflow. Através dela é possível criar seus pipelines online, fazendo a gestão pela própria interface do Astronomer ou do Airflow. Ela foi utilizada neste projeto e você pode saber mais sobre em [Getting started tutorial](https://www.astronomer.io/docs/learn/get-started-with-airflow).

## Visualizando o resultado deste pipeline

Este projeto possui uma aplicação frontend em Angular que exibe as informações tratadas da base de dados Firestore. 

- Confira [aqui](https://github.com/xpcjunior/fraldasotto.frontend) o código-fonte dela
- Confira [aqui](https://fraldas-otto.web.app/) a aplicação rodando