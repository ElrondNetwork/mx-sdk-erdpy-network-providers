from typing import Any, Dict

from multiversx_sdk_core import Address

from multiversx_sdk_network_providers.interface import IAddress
from multiversx_sdk_network_providers.resources import EmptyAddress


class AccountOnNetwork:
    def __init__(self):
        self.address: IAddress = EmptyAddress()
        self.nonce: int = 0
        self.balance: int = 0
        self.code: bytes = b''
        self.username: str = ''

    @staticmethod
    def from_http_response(payload: Dict[str, Any]) -> 'AccountOnNetwork':
        result = AccountOnNetwork()

        address = payload.get('address', '')
        result.address = Address.from_bech32(address) if address else EmptyAddress()

        result.nonce = payload.get('nonce', 0)
        result.balance = int(payload.get('balance', 0))
        result.code = bytes.fromhex(payload.get('code', ''))
        result.username = payload.get('username', '')

        return result
    
    def to_dictionary(self) -> Dict[str, Any]:
        return{
            "address": self.address.bech32(),
            "nonce": self.nonce,
            "balance": self.balance,
            "code": self.code.hex(),
            "username": self.username
        }
