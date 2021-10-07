from brownie import FundMe

from .helpful_scripts import get_account


def fund():
    fund_me = FundMe[-1]

    account = get_account()

    # вызываем функцию, которая просто даёт нам минимально возможную сумму для внесения на аккаунт
    entrance_fee = fund_me.getEntranceFee()

    print(f"The current entry fee is {entrance_fee}")

    print("Funding...")

    # если мы хотим внести деньги в аккаунт, то при вызове функции, мы передаём помимо from, также и "value"!
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():

    fund_me = FundMe[-1]

    account = get_account()

    print("Withdrawing...")
    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()
