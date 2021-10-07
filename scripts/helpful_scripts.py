from brownie import network, accounts, config, MockV3Aggregator

from web3 import Web3


# форки сетей
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork-dev"]

# здесь мы устанавливаем наши сети, для которых используем моки, не используем верификацию (т.е. development)
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-me"]


# для конвертации валют
DECIMALS = 8  # т.к. в контракте мы можем указать только 8 decimals (конвертация всё доведёт до 18)
STARTING_PRICE = 2000 * (10 ** 8)  # сумма с 8 decimals (3000 * 10 ** 8)

# функция, которая возвращает нам нужный аккаунт, в зависимости от того, где мы деплоемся
def get_account():

    # проверяем что .show_active() - т.е. сеть на которой мы работаем
    # совпадает с именем development (зарезервированно для Ganache-CLI)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]

    # если нет, то берём наш акк из .env
    else:
        return accounts.add(config["wallets"]["from_key"])


# функция, которая деплоет mocks (в нашем случае фейковый контракт проверки валют)
def deploy_mocks():

    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")

    # т.к. временная (ganache ) сеть не имеет доступа к внешним oracle сетям (вроде chainlink)
    # мы деплоем спец контракт, который имитирует работу контракта-конвертора
    # если мы уже деплоели этот контракт, нет смысла его заново деплоить
    # проверяем список деплоев у этого контракта (объект контракта по сути своей работает как лист, если мы ничего не передаём ему)

    if len(MockV3Aggregator) <= 0:

        # этот mock требует передачи ему двух параметров - decimals (мы ставим 8, т.к. в нашем контракте предусмотрено максимально 8 decimals на входе)
        # а также саму стоимость eth за доллар (ставим 3000 + 8 нулей)
        # функция Web3.toWei( ethAmount: int (или float), "unit" (нужно указать валюту, например "ether") ) возвращает нам скастованный эфир в wei (т.е. добавляет 18 нулей)
        # здесь она нам не нужна, но нужно помнить, что она есть

        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})

    print("Mocks Deployed")
