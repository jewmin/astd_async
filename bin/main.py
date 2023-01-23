# -*- coding: utf-8 -*-

import sys
import base64
import asyncio
import engine.Dump as Dump
import engine.LogManager as LogManager
from model.Account import Account
from model.enum.ServerType import ServerType


def ReadAccountConfig(filename) -> list[Account]:
    account_list = []
    with open(filename, "r", encoding="utf-8") as fs:
        lines: list[str] = fs.readlines()
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, _, value = line.partition("=")
            if not key or not value:
                continue
            if key.lower() != "account":
                continue
            contents = value.split(":")
            if len(contents) < 8:
                continue
            account = Account(eval(f"ServerType.{contents[0]}"), int(contents[1]), contents[2], base64.b64decode(contents[3]), contents[7])
            account_list.append(account)

    return account_list


def FindAccount(account_list: list[Account], username: str, rolename: str) -> Account:
    for account in account_list:
        if account.username == username and account.rolename == rolename:
            return account


def Run(accounts: list[Account]):
    loop = asyncio.get_event_loop()
    for account in accounts:
        loop.create_task(account.Login())
    loop.run_forever()
    loop.close()


def ParseArgs(args):
    import argparse
    parser = argparse.ArgumentParser(prog="astd", description="傲视天地小助手", usage="%(prog)s [options]")
    parser.add_argument('--user-name', default="", type=str, help="账号名，多个用逗号隔开")
    parser.add_argument('--role-name', default="", type=str, help="角色名，多个用逗号隔开")
    parser.add_argument('--config', default="./bin/account.ini", type=str, help="账号配置")
    return parser.parse_args(args)


def Main(argv):
    args = ParseArgs(argv[1:])
    Dump.SetDumpPath("./bin/dumps")
    LogManager.SetLoggerPath("./bin/logs")
    account_list = ReadAccountConfig(args.config)
    usernames = args.user_name.split(",")
    rolenames = args.role_name.split(",")
    accounts = []
    for username, rolename in zip(usernames, rolenames):
        account = FindAccount(account_list, username, rolename)
        if not account:
            continue
        accounts.append(account)
    Run(accounts)


if __name__ == "__main__":
    Main(sys.argv)
