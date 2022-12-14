import base64
from typing import Any, Dict

from multiversx_sdk_core import Address

from multiversx_sdk_network_providers.contract_results import ContractResults
from multiversx_sdk_network_providers.interface import IAddress
from multiversx_sdk_network_providers.resources import EmptyAddress
from multiversx_sdk_network_providers.transaction_completion_strategy import (
    TransactionCompletionStrategyOnApi, TransactionCompletionStrategyOnProxy)
from multiversx_sdk_network_providers.transaction_logs import TransactionLogs
from multiversx_sdk_network_providers.transaction_receipt import TransactionReceipt
from multiversx_sdk_network_providers.transaction_status import TransactionStatus


class TransactionOnNetwork:
    def __init__(self):
        self.is_completed: bool = False
        self.hash: str = ''
        self.type: str = ''
        self.nonce: int = 0
        self.round: int = 0
        self.epoch: int = 0
        self.value: int = 0
        self.receiver: IAddress = EmptyAddress()
        self.sender: IAddress = EmptyAddress()
        self.gas_limit: int = 0
        self.gas_price: int = 0
        self.data: str = ''
        self.signature: str = ''
        self.status: TransactionStatus = TransactionStatus()
        self.timestamp: int = 0

        self.block_nonce: int = 0
        self.hyperblock_nonce: int = 0
        self.hyperblock_hash: str = ''

        self.receipt: TransactionReceipt = TransactionReceipt()
        self.contract_results: ContractResults = ContractResults([])
        self.logs: TransactionLogs = TransactionLogs()

    def get_status(self) -> TransactionStatus:
        return self.status

    @staticmethod
    def from_api_http_response(tx_hash: str, response: Dict[str, Any]) -> 'TransactionOnNetwork':
        result = TransactionOnNetwork.from_http_response(tx_hash, response)
        result.contract_results = ContractResults.from_api_http_response(response.get('results', []))
        result.is_completed = TransactionCompletionStrategyOnApi().is_completed(result)

        return result

    @staticmethod
    def from_proxy_http_response(tx_hash: str, response: Dict[str, Any]) -> 'TransactionOnNetwork':
        result = TransactionOnNetwork.from_http_response(tx_hash, response)

        result.contract_results = ContractResults.from_proxy_http_response(response.get('smartContractResults', []))
        result.is_completed = TransactionCompletionStrategyOnProxy().is_completed(result)

        return result

    @staticmethod
    def from_http_response(tx_hash: str, response: Dict[str, Any]) -> 'TransactionOnNetwork':
        result = TransactionOnNetwork()

        result.hash = tx_hash
        result.type = response.get('type', '')
        result.nonce = response.get('nonce', 0)
        result.round = response.get('round', 0)
        result.epoch = response.get('epoch', 0)
        result.value = response.get('value', 0)

        sender = response.get('sender', '')
        result.sender = Address.from_bech32(sender) if sender else EmptyAddress()

        receiver = response.get('receiver', '')
        result.receiver = Address.from_bech32(receiver) if receiver else EmptyAddress()

        result.gas_price = response.get('gasPrice', 0)
        result.gas_limit = response.get('gasLimit', 0)

        data = response.get('data', '') or ""

        result.data = base64.b64decode(data).decode()
        result.status = TransactionStatus(response.get('status'))
        result.timestamp = response.get('timestamp', 0)

        result.block_nonce = response.get('blockNonce', 0)
        result.hyperblock_nonce = response.get('hyperblockNonce', 0)
        result.hyperblock_hash = response.get('hyperblockHash', '')

        result.receipt = TransactionReceipt.from_http_response(response.get('receipt', {}))
        result.logs = TransactionLogs.from_http_response(response.get('logs', {}))

        return result

    def to_dictionary(self) -> Dict[str, Any]:
        return {
            "isCompleted": self.is_completed,
            "hash": self.hash,
            "type": self.type,
            "nonce": self.nonce,
            "round": self.round,
            "epoch": self.epoch,
            "value": self.value,
            "receiver": self.receiver.bech32(),
            "sender": self.sender.bech32(),
            "gasLimit": self.gas_limit,
            "gasPrice": self.gas_price,
            "data": self.data,
            "signature": self.signature,
            "status": self.status.status,
            "timestamp": self.timestamp,
            "blockNonce": self.block_nonce,
            "hyperblockNonce": self.hyperblock_nonce,
            "hyperblockHash": self.hyperblock_hash
        }
