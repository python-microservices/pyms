import base64

from pyms.crypt.driver import CryptAbstract
from pyms.utils import check_package_exists, import_package


class Crypt(CryptAbstract):
    encryption_algorithm = "SYMMETRIC_DEFAULT"  # 'SYMMETRIC_DEFAULT' | 'RSAES_OAEP_SHA_1' | 'RSAES_OAEP_SHA_256'
    key_id = ""

    def __init__(self, *args, **kwargs):
        self._init_boto()
        super().__init__(*args, **kwargs)

    def encrypt(self, message):   # pragma: no cover
        ciphertext = self.client.encrypt(
            KeyId=self.config.key_id,
            Plaintext=bytes(message, encoding="UTF-8"),
        )
        return str(base64.b64encode(ciphertext["CiphertextBlob"]), encoding="UTF-8")

    def _init_boto(self):  # pragma: no cover
        check_package_exists("boto3")
        boto3 = import_package("boto3")
        boto3.set_stream_logger(name='botocore')
        self.client = boto3.client('kms')

    def _aws_decrypt(self, blob_text):  # pragma: no cover
        response = self.client.decrypt(
            CiphertextBlob=blob_text,
            KeyId=self.config.key_id,
            EncryptionAlgorithm=self.encryption_algorithm
        )
        return str(response['Plaintext'], encoding="UTF-8")

    def _parse_encrypted(self, encrypted):
        blob_text = base64.b64decode(encrypted)
        return blob_text

    def decrypt(self, encrypted):
        blob_text = self._parse_encrypted(encrypted)
        decrypted = self._aws_decrypt(blob_text)

        return decrypted
