# 🧾 Transaction Manager CLI

A simple, colorful **command-line transaction management app** built with Python.
Add, edit, remove, search and report transactions — all from your terminal, with
bilingual (English / فارسی) category support and colored output.

---

## ✨ Features

- ➕ Add new transactions (product id, name, unit price, quantity, category)
- 📋 Show all transactions in a clean table
- ✏️ Edit an existing transaction
- 🗑️ Remove a transaction
- 🔍 Search by product ID or name
- 📊 Generate reports:
  - Total transactions, quantity and revenue
  - Revenue per category
  - Best-selling product
  - Daily revenue report
- 💾 Persistent storage: `transactions.jsonl` + `report_by_category.csv`
- 🌈 Colored output via `colorama`
- 🈯 13 bilingual categories (English / Persian)

---

## Requirements

- Python 3.10+
- colorama

## Installation

```bash
git clone https://github.com/edris099/transaction-manager-cli.git
cd transaction-manager-cli
pip install -r requirements.txt
