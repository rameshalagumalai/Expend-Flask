from connection import conn
from flask import session
import ibm_db

def getDataByDay(date):
    expenses = []
    totalExpense = 0
    categories = []
    sql = "SELECT expense.*, expense_category.name, expense_category.color FROM expense INNER JOIN expense_category ON expense.category_id = expense_category.id WHERE expense_category.user_id = ? AND expense.date = ?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, session['userId'])
    ibm_db.bind_param(stmt, 2, date)
    ibm_db.execute(stmt)
    tuple = ibm_db.fetch_tuple(stmt)
    while tuple != False:
        expenses.append(tuple)
        tuple = ibm_db.fetch_tuple(stmt)

    sql = "SELECT sum(expense.amount) FROM expense INNER JOIN expense_category ON expense.category_id = expense_category.id WHERE expense_category.user_id = ? AND expense.date = ?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, session['userId'])
    ibm_db.bind_param(stmt, 2, date)
    ibm_db.execute(stmt)
    tuple = ibm_db.fetch_tuple(stmt)
    if tuple != False:
        totalExpense = tuple[0]

    sql = "SELECT expense_category.id, expense_category.name, expense_category.color, sum(expense.amount) FROM expense_category INNER JOIN expense ON expense_category.id = expense.category_id WHERE expense_category.user_id = ? AND expense.date = ? GROUP BY expense_category.id, expense_category.name, expense_category.color"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, session['userId'])
    ibm_db.bind_param(stmt, 2, date)
    ibm_db.execute(stmt)
    tuple = ibm_db.fetch_tuple(stmt)
    while tuple != False:
        categories.append(tuple)
        tuple = ibm_db.fetch_tuple(stmt)

    return {
        "expenses": expenses,
        "totalExpense": totalExpense,
        "categories": categories
    }


def addNewExpense(data, date):
    sql = "INSERT INTO expense (name, amount, date, category_id) VALUES (?, ?, ?, ?)"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, data['name'])
    ibm_db.bind_param(stmt, 2, data['amount'])
    ibm_db.bind_param(stmt, 3, date)
    ibm_db.bind_param(stmt, 4, data['category'])
    ibm_db.execute(stmt)