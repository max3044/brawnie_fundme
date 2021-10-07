from brownie import FundMe, network, config, MockV3Aggregator

from .helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, deploy_mocks, get_account

from web3 import Web3


def deploy_fund_me():

    # получаем аккаунт
    account = get_account()

    # как мы помним, в транзакционные функции (а функция deploy именно такая)
    # мы передаём реквизиты

    # publish_source=True - означает, что мы публикуем наш контракт

    # также, мы должны передать адресс контракта, отвечающего за конвертацию

    # небольшая функция, которая береёт адрес конвертора для активной сети из конфига
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]

    else:
        # вызываем функцию, которая деплоет фейковый контракт для проверки курса валют

        deploy_mocks()

        # получаем адрес нашего фейкового контракта для конвертации
        # берём его у последней вересии задеплоенного контракта
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        # получаем режим верификакции (true или false - устанавливаем в конфиге)
        publish_source=config["networks"][network.show_active()].get("verify"),
    )

    # свойство address у контракта - даёт нам адрес самого контракта
    print(f"Contract deployed to {fund_me.address}")

    # возвращаем ново-задеплоенный контракт
    return fund_me


def main():
    deploy_fund_me()
