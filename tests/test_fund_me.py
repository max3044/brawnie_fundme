from brownie import network, accounts, exceptions
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account

import pytest
from scripts.deploy import deploy_fund_me


def test_can_fund_and_withdraw():

    # получаем аккаунт
    account = get_account()

    # получаем контракт
    fund_me = deploy_fund_me()

    # получаем мин. вступительный взнос (добавляем небольшое значение, на случай если комиссия всё сожрёт)
    entrance_fee = fund_me.getEntranceFee() + 100

    # совершаем транзакцию
    tx = fund_me.fund({"from": account, "value": entrance_fee})

    # ждем завершения блоков (1 - т.к. у нас всего одна транзакция)
    tx.wait(1)

    # addressToAmountFunded - mapping
    # но не смотря на это, мы должны обращаться к нему через account call
    # т.е. с (), а не [] и уже в скобках писать ключ, как аргумент функции!
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee

    # выводим деньги с аккаунта (логика такова, что выводятся деньги на аккаунт владельца, после чего обнуляются счётчики всех вложившихся)
    tx2 = fund_me.withdraw({"from": account})

    tx2.wait(1)

    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():

    # например, если нам нужно тестироваться только в локалке
    # мы можем использовать pytest чтобы скипануть тест:

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:

        # скипаем тест
        pytest.skip("only for local testing")

    account = get_account()
    fund_me = deploy_fund_me()

    # если не прописать в метод add(), вызванный на accounts
    # то аккаунт сгенерируется рандомно
    bad_actor = accounts.add()

    # если мы ожидаем, что будет вызвано исключение
    # т.е. тест будет провален, если переданное исключение не будет вызвано
    # VirtualMachineError - это ошибка, которую выкидывает контракт
    with pytest.raises(exceptions.VirtualMachineError):

        fund_me.withdraw({"from": bad_actor})
