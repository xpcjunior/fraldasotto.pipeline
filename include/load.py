import os
from google.cloud import firestore
from google.oauth2 import service_account

class Load:
    def __init__(self):
        caminho_json = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), # pwd
            '..',
            "firebase-adminsdk.json"
        )

        credentials = service_account.Credentials.from_service_account_file(caminho_json)
        self.db = firestore.Client(credentials=credentials, project=credentials.project_id)

    def atualizar_documento(self, collection_name, document_id, dados_atualizados):
        """
        Atualiza um documento por ID em uma coleção específica.
        
        :param collection_name: Nome da coleção no Firestore
        :param document_id: ID do documento a ser atualizado
        :param dados_atualizados: Dicionário com os campos e valores a serem atualizados
        :return: Nenhum valor é retornado, mas uma exceção pode ser lançada se ocorrer um erro
        """
        try:
            doc_ref = self.db.collection(collection_name).document(document_id)
            doc_ref.update(dados_atualizados)
            print(f"Documento com ID '{document_id}' atualizado com sucesso.")
        except Exception as e:
            print(f"Erro ao atualizar documento: {e}")
