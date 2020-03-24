from pyms.crypt.driver import CryptAbstract
from pyms.utils import check_package_exists, import_package


class Crypt(CryptAbstract):
    encryption_algorithm = "SYMMETRIC_DEFAULT"  # 'SYMMETRIC_DEFAULT' | 'RSAES_OAEP_SHA_1' | 'RSAES_OAEP_SHA_256'
    key_id = ""
    grant_tokens = []

    def __init__(self):
        check_package_exists("boto3")
        boto3 = import_package("boto3")
        self.client = boto3.client('kms')

    def encrypt(self, message):
        encrypted = message
        return encrypted

    def decrypt(self, encrypted):
        response = self.client.decrypt(
            CiphertextBlob=b'bytes',
            EncryptionContext={
                'string': encrypted
            },
            GrantTokens=self.grant_tokens,
            KeyId=self.key_id,
            EncryptionAlgorithm=self.encryption_algorithm
        )
        return response
