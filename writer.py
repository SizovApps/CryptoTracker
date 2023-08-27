import csv

import pandas as pd

HEADER_LINE = ['Адрес', 'Итого в долларах', 'Итого в ETH', 'Итого вход', 'Итого выход',
               'Количество успешных', 'Количество неуспешных', 'Win rate', 'PNL']

TOKENS_HEADER = ['Token:', 'Вход', 'Выход', 'Профит в %', 'Профит в ETH',
                 'Профит в долларах', 'Денег осталось']

RESULTS_FOLDER_NAME = "../results/"


def write_full_stats(address, result_in_dollar, result_in_altcoine, full_enter, full_exit, count_of_profit,
                     count_of_loss, tokens):
    with open(RESULTS_FOLDER_NAME + address + '.csv', 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=';',
                            quotechar=';', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(HEADER_LINE)
        writer.writerow(
            [address, result_in_dollar, result_in_altcoine, full_enter, full_exit, count_of_profit, count_of_loss])

        writer.writerow(TOKENS_HEADER)
        for token in tokens:
            val = token.to_row()
            writer.writerow(val)


def write_header_wallets_stats(token_name):
    with open(RESULTS_FOLDER_NAME + token_name + '.csv', 'w', newline='', encoding="utf-8") as all_file:
        all_writer = csv.writer(all_file, delimiter=';', quotechar=';', quoting=csv.QUOTE_MINIMAL)
        all_writer.writerow(HEADER_LINE)
        all_writer.writerow("")


def write_wallet(wallet, token_name):
    with open(RESULTS_FOLDER_NAME + token_name + '.csv', 'a', newline='', encoding="utf-8") as all_file:
        all_writer = csv.writer(all_file, delimiter=';', quotechar=';', quoting=csv.QUOTE_MINIMAL)
        all_writer.writerow(
            [wallet.address, wallet.profit_in_dollar, wallet.profit_in_ETH, wallet.full_enter, wallet.full_exit,
             wallet.count_of_profit, wallet.count_of_loss, wallet.win_rate, wallet.pnl])


def create_excel(token_name, wallets):
    token_file = pd.read_csv(RESULTS_FOLDER_NAME + token_name + '.csv', sep=';', encoding="utf-8")
    token_file.to_excel(RESULTS_FOLDER_NAME + token_name + ".xlsx", index=None, header=True)

    with pd.ExcelWriter(RESULTS_FOLDER_NAME + token_name + ".xlsx", engine='openpyxl', mode='a') as writer:
        for wallet in wallets:
            token_file = pd.read_csv(RESULTS_FOLDER_NAME + wallet.address + '.csv', sep=';')
            token_file.to_excel(writer, sheet_name=wallet.address)

