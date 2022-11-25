from erdpy_core import Address
from erdpy_network.api_network_provider import ApiNetworkProvider
from erdpy_network.proxy_network_provider import ProxyNetworkProvider, ContractQuery


class TestApi:
    api = ApiNetworkProvider('https://devnet-api.elrond.com', ProxyNetworkProvider('https://devnet-gateway.elrond.com'))

    def test_get_network_stake_statistic(self):
        result = self.api.get_network_stake_statistics()

        assert result.total_validators > 0
        assert result.active_validators > 0
        assert result.total_staked > 0

    def test_get_general_statistics(self):
        result = self.api.get_network_general_statistics()

        assert result.shards == 3
        assert result.rounds_per_epoch == 1200
        assert result.refresh_rate == 6000
        assert result.epoch >= 2864
        assert result.rounds_passed >= 0
        assert result.transactions >= 4330650
        assert result.accounts >= 92270

    def test_get_account(self):
        address = Address.from_bech32('erd1testnlersh4z0wsv8kjx39me4rmnvjkwu8dsaea7ukdvvc9z396qykv7z7')
        result = self.api.get_account(address)

        assert result.address.bech32() == 'erd1testnlersh4z0wsv8kjx39me4rmnvjkwu8dsaea7ukdvvc9z396qykv7z7'
        assert result.username == ''

    def test_get_fungible_token_of_account(self):
        address = Address.from_bech32('erd1testnlersh4z0wsv8kjx39me4rmnvjkwu8dsaea7ukdvvc9z396qykv7z7')
        result = self.api.get_fungible_token_of_account(address, 'ABC-10df96')

        assert result.identifier == 'ABC-10df96'
        assert result.balance == 50

    def test_get_nonfungible_token_of_account(self):
        address = Address.from_bech32('erd1testnlersh4z0wsv8kjx39me4rmnvjkwu8dsaea7ukdvvc9z396qykv7z7')
        result = self.api.get_nonfungible_token_of_account(address, 'ASDASD-510041', 2)

        assert result.balance == 0
        assert result.nonce == 2
        assert result.collection == 'ASDASD-510041'
        assert result.identifier == 'ASDASD-510041-02'
        assert result.type == 'NonFungibleESDT'

    def test_get_mex_pairs(self):
        result = self.api.get_mex_pairs()
        first_pair = result[0]

        assert len(result) >= 0
        assert first_pair.address.bech32() == 'erd1qqqqqqqqqqqqqpgquu5rsa4ee6l4azz6vdu4hjp8z4p6tt8m0n4suht3dy'
        assert first_pair.name == 'EGLDMEXLP'
        assert first_pair.symbol == 'EGLDMEX'
        assert first_pair.state == 'active'
        assert first_pair.type == 'core'

    def test_get_transaction(self):
        result = self.api.get_transaction('2cb813be9d5e5040abb2522da75fa5c8d94f72caa510ff51d7525659f398298b')

        assert result.hash == '2cb813be9d5e5040abb2522da75fa5c8d94f72caa510ff51d7525659f398298b'
        assert result.nonce == 828
        assert result.is_completed
        assert result.sender.bech32() == 'erd1testnlersh4z0wsv8kjx39me4rmnvjkwu8dsaea7ukdvvc9z396qykv7z7'
        assert result.receiver.bech32() == 'erd1c8tnzykaj7lhrd5cy6jap533afr4dqu7uqcdm6qv4wuwly9lcsqqm9ll4f'
        assert result.value == '10000000000000000000'

    def test_get_transaction_status(self):
        result = self.api.get_transaction_status('2cb813be9d5e5040abb2522da75fa5c8d94f72caa510ff51d7525659f398298b')

        assert result.status == 'success'

    def test_query_contract(self):
        query = ContractQuery(Address.from_bech32('erd1qqqqqqqqqqqqqpgquykqja5c4v33zdmnwglj3jphqwrelzdn396qlc9g33'),
                              'getSum', 0, [])
        result = self.api.query_contract(query)

        assert len(result.return_data) == 1

    def test_get_definition_of_fungible_token(self):
        result = self.api.get_definition_of_fungible_token('ABC-10df96')

        assert result.identifier == 'ABC-10df96'
        assert result.owner.bech32() == 'erd1testnlersh4z0wsv8kjx39me4rmnvjkwu8dsaea7ukdvvc9z396qykv7z7'
        assert result.can_upgrade
        assert not result.can_freeze
        assert result.decimals == 1
        assert result.supply == 5

    def test_get_definition_of_token_collection(self):
        result = self.api.get_definition_of_token_collection('ASDASD-510041')

        assert result.collection == 'ASDASD-510041'
        assert result.owner.bech32() == 'erd1testnlersh4z0wsv8kjx39me4rmnvjkwu8dsaea7ukdvvc9z396qykv7z7'
        assert result.type == 'NonFungibleESDT'
        assert result.decimals == 0
        assert result.can_freeze
        assert not result.can_pause

    def test_get_non_fungible_token(self):
        result = self.api.get_non_fungible_token('ASDASD-510041', 2)

        assert result.type == 'NonFungibleESDT'
        assert result.nonce == 2
        assert result.identifier == 'ASDASD-510041-02'
        assert result.collection == 'ASDASD-510041'
        assert result.creator.bech32() == 'erd1testnlersh4z0wsv8kjx39me4rmnvjkwu8dsaea7ukdvvc9z396qykv7z7'
        assert result.balance == 0
        assert result.royalties != 0
        assert result.timestamp != 0