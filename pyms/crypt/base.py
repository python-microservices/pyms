from abc import ABC, abstractmethod


class CryptAbstract(ABC):

    @abstractmethod
    def encrypt(self, message):
        raise NotImplementedError

    @abstractmethod
    def decrypt(self, encrypted):
        raise NotImplementedError


class CryptNone(CryptAbstract):

    def encrypt(self, message):
        return message

    def decrypt(self, encrypted):
        return encrypted
