from azure.storage.blob import BlobServiceClient
from backend.config import settings
import logging

logger = logging.getLogger(__name__)


class AzureBlobService:

    def __init__(self):
        connection_string = settings.AZURE_STORAGE_CONNECTION_STRING

        if not connection_string:
            raise ValueError(
                "Azure Blob Storage connection string is missing"
            )

        self.blob_service_client = (
            BlobServiceClient.from_connection_string(
                connection_string
            )
        )

        self.container_name = (
            settings.AZURE_STORAGE_CONTAINER_NAME
        )

        self.container_client = (
            self.blob_service_client.get_container_client(
                self.container_name
            )
        )

    def upload_file(self, file_path, blob_name):

        blob_client = self.container_client.get_blob_client(
            blob_name
        )

        with open(file_path, "rb") as file:
            blob_client.upload_blob(
                file,
                overwrite=True
            )

        logger.info("Uploaded file to Azure Blob Storage: %s", blob_name)

        return {
            "filename": blob_name,
            "container": self.container_name,
            "status": "uploaded"
        }