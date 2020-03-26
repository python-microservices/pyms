import base64

from pyms.crypt.driver import CryptAbstract
from pyms.utils import check_package_exists, import_package


class Crypt(CryptAbstract):
    encryption_algorithm = "SYMMETRIC_DEFAULT"  # 'SYMMETRIC_DEFAULT' | 'RSAES_OAEP_SHA_1' | 'RSAES_OAEP_SHA_256'
    key_id = ""
    grant_tokens = []

    def __init__(self, *args, **kwargs):
        check_package_exists("boto3")
        boto3 = import_package("boto3")
        boto3.set_stream_logger(name='botocore')
        self.client = boto3.client('kms')
        super().__init__(*args, **kwargs)

    def encrypt(self, message):
        encrypted = message
        return encrypted

    def decrypt(self, encrypted):
        blob_text = base64.b64decode(encrypted)
        response = self.client.decrypt(
            CiphertextBlob=blob_text,
            KeyId=self.config.key_id,
            EncryptionAlgorithm=self.encryption_algorithm
        )
        return str(response['Plaintext'], encoding="UTF-8")
