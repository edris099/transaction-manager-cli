import json
import sys
import os
import csv
import time
import datetime
import functools
import colorama
from colorama import Fore

colorama.init(autoreset=True)


class InvalidChoice(Exception):
    pass


class ThisNumberExists(Exception):
    pass


class ListEmpty(Exception):
    pass


report_by_category_list = []

transactions_file = 'transactions.jsonl'
report_by_category_file = 'report_by_category.csv'

print(Fore.LIGHTBLACK_EX + 'Program Begin!')

CATEGORIES = [
    ("Dairy", "لبنیات"),
    ("Meat & Poultry", "گوشت و مرغ"),
    ("Fruits & Vegetables", "میوه و سبزیجات"),
    ("Bakery", "نان و شیرینی"),
    ("Beverages", "نوشیدنی"),
    ("Snacks", "تنقلات"),
    ("Electronics", "الکترونیک"),
    ("Clothing", "پوشاک"),
    ("Footwear", "کفش"),
    ("Home & Kitchen", "خانه و آشپزخانه"),
    ("Personal Care", "بهداشت شخصی"),
    ("Stationery", "لوازم‌التحریر"),
    ("Other", "سایر")
]


def log_actions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        func_name = func.__name__
        print(Fore.LIGHTYELLOW_EX + f'\n[{date}] Running: {func_name}')
        return func(*args, **kwargs)

    return wrapper


def slow(s, d=0.0):
    for c in s:
        print(c, end='', flush=True)
        time.sleep(d)
    print()


def load_json():
    try:
        if os.path.exists(transactions_file):
            with open(transactions_file, 'r', encoding='utf-8') as file_transactions:
                for line_num, line in enumerate(file_transactions, 1):
                    try:
                        yield json.loads(line)
                    except json.decoder.JSONDecodeError:
                        print(f"Skipping corrupted line {line_num}")
                        continue
        else:
            raise FileNotFoundError('File Not Found.')
    except FileNotFoundError:
        print(Fore.RED + 'Transactions file not found.', end='')
        time.sleep(1)
        print(Fore.YELLOW + '\rCreating New Transaction File', end='')
        slow('...', 0.205)
        time.sleep(2)
        with open(transactions_file, 'w', encoding='utf-8'):
            pass
        print(Fore.GREEN + '\rSuccessfully created new transactions file.')


transactions_list = list(load_json())

try:
    if os.path.exists(report_by_category_file):
        with open(report_by_category_file, 'r', encoding='utf-8') as file_report_by_category:
            reader = csv.DictReader(file_report_by_category)
            if reader.fieldnames:
                for row in reader:
                    report_by_category_list.append(row)
    else:
        raise FileNotFoundError('File Not Found.')
except FileNotFoundError:
    with open(report_by_category_file, 'w', encoding='utf-8'):
        pass


@log_actions
def save(data=None):
    if data is None:
        with open(transactions_file, 'w', encoding='utf-8') as file_transaction:
            for t in transactions_list:
                json.dump(t, file_transaction, ensure_ascii=False)
                file_transaction.write('\n')
        if report_by_category_list:
            fieldnames = list(report_by_category_list[0].keys())
            print(Fore.LIGHTGREEN_EX + 'Successfully find header')
        else:
            fieldnames = ["category", "transaction_count", "total_sales"]
            print(Fore.LIGHTRED_EX + 'Can\'t find header create new header', end='')
            time.sleep(2)
        with open(report_by_category_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(report_by_category_list)
        print(Fore.GREEN + '\rSuccessfully saved new reports document in file.')
    else:
        with open(transactions_file, 'a', encoding='utf-8') as file_transaction:
            json.dump(data, file_transaction, ensure_ascii=False)
            file_transaction.write('\n')
    print(Fore.LIGHTGREEN_EX + 'Successfully saved new transactions document in file.')


@log_actions
def main_menu():
    while True:
        print(Fore.CYAN + '\n' + '=' * 15 + Fore.WHITE + ' Main Menu ' + Fore.CYAN + '=' * 15)
        print(Fore.LIGHTBLUE_EX + '1. ' + Fore.WHITE + 'Transactions Menu')
        print(Fore.LIGHTBLUE_EX + '2. ' + Fore.WHITE + 'Show Reports')
        print(Fore.LIGHTBLUE_EX + '3. ' + Fore.WHITE + 'Save and Exit')

        try:
            choose = int(input(Fore.RED + '\nPlease choose an option: '))
            if choose not in [1, 2, 3]:
                raise InvalidChoice(Fore.RED + "Choose an option between 1 and 3.")
        except ValueError:
            print(Fore.RED + 'Please Enter Something!')
            time.sleep(2)
            continue
        except InvalidChoice as err:
            print(err)
            time.sleep(2)
            continue

        match choose:
            case 1:
                transaction_menu()
            case 2:
                show_reports()
            case 3:
                print(Fore.GREEN + '\nGoodbye Sir/Ma\'am')
                sys.exit()


@log_actions
def transaction_menu():
    while True:
        print(Fore.CYAN + '\n' + '=' * 15 + Fore.WHITE + ' Transaction Menu ' + Fore.CYAN + '=' * 15)
        print(Fore.LIGHTBLUE_EX + '1. ' + Fore.WHITE + 'Add New Transaction')
        print(Fore.LIGHTBLUE_EX + '2. ' + Fore.WHITE + 'Show All Transactions')
        print(Fore.LIGHTBLUE_EX + '3. ' + Fore.WHITE + 'Edit Transaction')
        print(Fore.LIGHTBLUE_EX + '4. ' + Fore.WHITE + 'Remove Transaction')
        print(Fore.LIGHTBLUE_EX + '5. ' + Fore.WHITE + 'Search Transactions')
        print(Fore.LIGHTMAGENTA_EX + '6. ' + Fore.WHITE + 'Back Main Menu')

        try:
            choose = int(input(Fore.RED + '\nPlease choose an option: '))
            if choose not in [1, 2, 3, 4, 5, 6]:
                raise InvalidChoice(Fore.RED + "Choose an option between 1 and 6.")
        except ValueError:
            print(Fore.RED + 'Please Enter Something!')
            time.sleep(2)
            continue
        except InvalidChoice as err:
            print(err)
            time.sleep(2)
            continue

        match choose:
            case 1:
                add_new_transaction()
            case 2:
                show_all_transaction()
            case 3:
                edit_transaction()
            case 4:
                remove_transaction()
            case 5:
                search_transaction()
            case 6:
                break


@log_actions
def add_new_transaction():
    print(Fore.CYAN + '\n' + '=' * 15 + Fore.WHITE + ' Add New Transaction ' + Fore.CYAN + '=' * 15)

    while True:
        try:
            product_id = int(input(Fore.MAGENTA + 'Please enter product id: '))
            if any(p["product_id"] == product_id for p in transactions_list):
                raise ThisNumberExists(Fore.RED + 'That product id already exists.')
            else:
                break
        except (ValueError, ThisNumberExists) as error:
            print(Fore.RED + f'Error: {type(error).__name__}: {error}')
            time.sleep(2)

    while True:
        try:
            product_name = input(Fore.MAGENTA + 'Please enter product name: (Must Letter) ').strip()
            if product_name.isalpha():
                break
            else:
                raise ValueError('Name must contain letters only')
        except ValueError as error:
            print(Fore.RED + f'Error: {type(error).__name__}: {error}')
            time.sleep(2)

    while True:
        try:
            unit_price = float(input(Fore.MAGENTA + 'Please enter unit price: '))
            if unit_price <= 0:
                raise ValueError('Unit price must be positive')
            else:
                break
        except ValueError as error:
            print(Fore.RED + f'Error: {type(error).__name__}: {error}')
            time.sleep(2)

    while True:
        try:
            quantity = int(input(Fore.MAGENTA + 'Please enter quantity: '))
            if quantity <= 0:
                raise ValueError('Quantity must be positive')
            else:
                break
        except ValueError as error:
            print(Fore.RED + f'Error: {type(error).__name__}: {error}')
            time.sleep(2)

    while True:
        try:
            print(Fore.CYAN + '\n--- Categories ---')
            for i, (en, fa) in enumerate(CATEGORIES, 1):
                print(Fore.BLUE + f"{i:2}. {en:<22} → {fa}")
            category = int(input(Fore.MAGENTA + '\nPlease enter category number: '))
            if not 1 <= category <= len(CATEGORIES):
                raise ValueError(f'Must be between 1 and {len(CATEGORIES)}')
            category = CATEGORIES[category - 1][0]
            break
        except ValueError as error:
            print(Fore.RED + f'Error: {type(error).__name__}: {error}')
            time.sleep(2)

    time_now = datetime.datetime.now()
    time_now = time_now.strftime("%y-%m-%d %H:%M")

    data = {
        "product_id": product_id,
        "product_name": product_name,
        "unit_price": unit_price,
        "quantity": quantity,
        "category": category,
        "registered": time_now
    }

    transactions_list.append(data)

    print(Fore.YELLOW + '\nchecking product ID', end='')
    slow('...', 0.5)
    print(Fore.GREEN + 'Successful')
    time.sleep(0.5)

    print(Fore.YELLOW + 'checking product name', end='')
    slow('...', 0.5)
    print(Fore.GREEN + 'Successful')
    time.sleep(0.5)

    print(Fore.YELLOW + 'checking product quantity', end='')
    slow('...', 0.5)
    print(Fore.GREEN + 'Successful')
    time.sleep(0.5)

    print(Fore.YELLOW + 'checking other thing', end='')
    slow('...', 0.5)
    print(Fore.GREEN + 'Successful\n')
    time.sleep(1)

    print(
        Fore.BLUE + f'Product ID: {product_id} | Name: {product_name} | Unit Price: {unit_price} | Qty: {quantity} | Category: {category} | Registered: {time_now}')
    save(data)


@log_actions
def show_all_transaction():
    try:
        if not transactions_list:
            raise ListEmpty(Fore.LIGHTRED_EX + 'We Don\'t have any transactions.')

        print(
            Fore.LIGHTWHITE_EX + f"\n{'#':<4} | {'ID':<5} | {'Name':<15} | {'Price':<10} | {'Qty':<4} | {'Category':<18} | {'Registered':<15}")
        print(Fore.LIGHTBLACK_EX + '-' * 80)

        for idx, t in enumerate(transactions_list, start=1):
            print(
                Fore.BLUE + f"{idx:<4} | {t['product_id']:<5} | {t['product_name']:<15} | {t['unit_price']:<10} | {t['quantity']:<4} | {t['category']:<18} | {t['registered']:<15}")
    except ListEmpty as error:
        print(Fore.RED + f'Error: {type(error).__name__}: {error}')


@log_actions
def edit_transaction():
    if not transactions_list:
        print(Fore.RED + 'No transactions to edit.')
        return

    show_all_transaction()
    print()

    while True:
        try:
            choose = int(input(Fore.RED + f'Please Choose Number 1 To {len(transactions_list)}: '))
            if not choose or choose < 1 or choose > len(transactions_list):
                raise ValueError(Fore.RED + f'Number Must Between 1 and {len(transactions_list)}!')
            choice = transactions_list[choose - 1]
            break
        except ValueError as error:
            print(Fore.RED + f'Error: {type(error).__name__}: {error}')
            time.sleep(2)

    print(Fore.CYAN + '\n--- Enter New Details ---')

    while True:
        try:
            print(Fore.LIGHTBLUE_EX + f'Current Name: {choice["product_name"]}')
            product_name = input(Fore.MAGENTA + 'Please enter new product name: (Must Letter) ').strip()
            if not product_name.isalpha():
                raise ValueError('Name must contain letters only')
            else:
                break
        except ValueError as error:
            print(Fore.RED + f'Error: {type(error).__name__}: {error}')
            time.sleep(2)

    while True:
        try:
            print(Fore.LIGHTBLUE_EX + f'Current Price: {choice["unit_price"]}')
            unit_price = float(input(Fore.MAGENTA + 'Please enter new unit price: '))
            if unit_price <= 0:
                raise ValueError('Unit price must be positive')
            else:
                break
        except ValueError as error:
            print(Fore.RED + f'Error: {type(error).__name__}: {error}')
            time.sleep(2)

    while True:
        try:
            print(Fore.LIGHTBLUE_EX + f'Current Quantity: {choice["quantity"]}')
            quantity = int(input(Fore.MAGENTA + 'Please enter new quantity: '))
            if quantity <= 0:
                raise ValueError('Quantity must be positive')
            else:
                break
        except ValueError as error:
            print(Fore.RED + f'Error: {type(error).__name__}: {error}')
            time.sleep(2)

    while True:
        try:
            print(Fore.LIGHTBLUE_EX + f'Current Category: {choice["category"]}')
            print(Fore.CYAN + '--- Categories ---')
            for i, (en, fa) in enumerate(CATEGORIES, 1):
                print(Fore.BLUE + f"{i:2}. {en:<22} → {fa}")
            category = int(input(Fore.MAGENTA + '\nPlease enter new category number: '))
            if not 1 <= category <= len(CATEGORIES):
                raise ValueError(f'Must be between 1 and {len(CATEGORIES)}')
            category = CATEGORIES[category - 1][0]
            break
        except ValueError as error:
            print(Fore.RED + f'Error: {type(error).__name__}: {error}')
            time.sleep(2)

    product_id = choice['product_id']
    time_now = choice['registered']
    data = {
        "product_id": product_id,
        "product_name": product_name,
        "unit_price": unit_price,
        "quantity": quantity,
        "category": category,
        "registered": time_now
    }

    transactions_list[choose - 1] = data

    print(Fore.YELLOW + '\nchecking product ID', end='')
    slow('...', 0.5)
    print(Fore.GREEN + 'Successful')
    time.sleep(0.5)

    print(Fore.YELLOW + 'checking product name', end='')
    slow('...', 0.5)
    print(Fore.GREEN + 'Successful')
    time.sleep(0.5)

    print(Fore.YELLOW + 'checking product quantity', end='')
    slow('...', 0.5)
    print(Fore.GREEN + 'Successful')
    time.sleep(0.5)

    print(Fore.YELLOW + 'checking other thing', end='')
    slow('...', 0.5)
    print(Fore.GREEN + 'Successful\n')
    time.sleep(1)

    print(
        Fore.BLUE + f'Product ID: {product_id} | Name: {product_name} | Unit Price: {unit_price} | Qty: {quantity} | Category: {category} | Registered: {time_now}')
    save()


@log_actions
def remove_transaction():
    if not transactions_list:
        print(Fore.RED + 'No transactions to remove.')
        return

    show_all_transaction()
    print()

    while True:
        try:
            choose = int(input(Fore.RED + f'Please Choose Number 1 To {len(transactions_list)}: '))
            if not choose or choose < 1 or choose > len(transactions_list):
                raise ValueError(Fore.RED + f'Number Must Between 1 and {len(transactions_list)}!')
            show = transactions_list[choose - 1]
            del transactions_list[choose - 1]
            print(
                Fore.GREEN + f'\nWe Have Deleted This Transaction! -> ID: {show["product_id"]} | Name: {show["product_name"]}')
            break
        except ValueError as error:
            print(Fore.RED + f'Error: {type(error).__name__}: {error}')
            time.sleep(2)
    save()


@log_actions
def search_transaction():
    if not transactions_list:
        print(Fore.RED + 'No transactions to Search.')
        return

    while True:
        print(Fore.YELLOW + '\nIf you don\'t want to search, please write (NOT)')
        choose = input(Fore.RED + 'Please enter ID or product name: ')
        if choose == 'NOT':
            return
        if choose.isdigit():
            choose = int(choose)
            result = [t for t in transactions_list if t['product_id'] == choose]
            break
        elif choose.isalpha():
            result = [t for t in transactions_list if choose.lower() in t['product_name'].lower()]
            break
        else:
            print(Fore.RED + 'Please write only letter or number')
            time.sleep(2)

    if result:
        print(
            Fore.LIGHTWHITE_EX + f"\n{'ID':<5} | {'Name':<15} | {'Price':<10} | {'Qty':<4} | {'Category':<18} | {'Registered':<15}")
        print(Fore.LIGHTBLACK_EX + '-' * 80)
        for t in result:
            print(
                Fore.BLUE + f"{t['product_id']:<5} | {t['product_name']:<15} | {t['unit_price']:<10} | {t['quantity']:<4} | {t['category']:<18} | {t['registered']:<15}")
    else:
        print(Fore.RED + 'Nothing found.')
        time.sleep(2)
        return


def show_reports(perm = False):
    if not transactions_list:
        print(Fore.RED + 'No transactions to generate reports.')
        return

    sort_category = {cat_en: 0 for cat_en, _ in CATEGORIES}
    sort_category1 = dict(sort_category)

    for t in transactions_list:
        sort_category[t["category"]] += t["quantity"] * t["unit_price"]
        sort_category1[t["category"]] += 1

    report_by_category_list.clear()
    for cat in sort_category:
        data = {
            "category": cat,
            "transaction_count": sort_category1[cat],
            "total_sales": sort_category[cat]
        }
        report_by_category_list.append(data)
    if perm:
        return

    result = []

    count_quantity = {"count": 0, "count_all": 0, "total": 0}
    for t in transactions_list:
        count_quantity["count_all"] += t["quantity"]
        count_quantity["total"] += t["quantity"] * t["unit_price"]
        count_quantity["count"] += 1

    c_q = (Fore.CYAN + 'Total transactions & Total revenue:\n' +
           Fore.WHITE + f"Total Transactions: {count_quantity['count']}\n" +
           f"Total Quantity: {count_quantity['count_all']}\n" +
           f"Total Price: {count_quantity['total']:,.2f} Toman")
    result.append(c_q)

    s_c_lines = [Fore.CYAN + "Revenue by category:\n"]
    for cat, total in sort_category.items():
        if total > 0:
            s_c_lines.append(Fore.WHITE + f"{cat}: {total:,.2f} Toman")
    s_c = "\n".join(s_c_lines)
    result.append(s_c)

    name_product = {}
    for t in transactions_list:
        name_product[t["product_name"]] = name_product.get(t["product_name"], 0) + t["quantity"]
    best_product = max(name_product, key=lambda k: name_product[k])
    n_p = (Fore.CYAN + 'Best-selling product:\n' +
           Fore.WHITE + f"{best_product} With {name_product[best_product]} sells!")
    result.append(n_p)

    daily = {}
    for t in transactions_list:
        daily[t["registered"].split(" ")[0]] = daily.get(t["registered"].split(" ")[0], 0) + t["quantity"] * t[
            "unit_price"]

    daily_report_lines = [Fore.CYAN + "Daily report:\n"]
    for date in sorted(daily.keys()):
        daily_report_lines.append(Fore.WHITE + f"{date}: {daily[date]:,.2f} Toman")

    d_r = "\n".join(daily_report_lines)
    result.append(d_r)

    print(Fore.CYAN + '\n' + '=' * 40 + Fore.WHITE + ' REPORTS ' + Fore.CYAN + '=' * 40)
    for d in result:
        print(d)
        print(Fore.LIGHTBLACK_EX + '-' * 80)

    print(Fore.CYAN + '\n--- CSV Data (report_by_category) ---')
    for report in report_by_category_list:
        print(
            Fore.WHITE + f"Category: {report['category']:<20} | Count: {report['transaction_count']:<5} | Total Sales: {report['total_sales']:,.2f} Toman")


if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        print(Fore.RED + '\nProgram done by user.', end='')
        time.sleep(2)
    except SystemExit:
        print(Fore.RED + '\nProgram done by user.', end='')
        time.sleep(2)
    finally:
        print('\r\n')
        print(Fore.GREEN + 'Save Everything...', end='')
        time.sleep(2)
        print('\r')
        show_reports(True)
        save()
        print(Fore.GREEN + 'Closing transactions App...')
        time.sleep(2)
        print('\n')
        print(Fore.BLUE + 'Program done.')