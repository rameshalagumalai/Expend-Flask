from connection import conn
from flask import session
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
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

    sql = "SELECT id, name FROM expense_category WHERE user_id = ?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, session['userId'])
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

    sql = "SELECT (SELECT limit FROM user WHERE id = ?), sum(expense.amount), (SELECT email FROM user WHERE id = ?), (SELECT name FROM user WHERE id = ?) FROM expense INNER JOIN expense_category ON expense.category_id = expense_category.id WHERE expense_category.user_id = ? AND expense.date = ?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, session['userId'])
    ibm_db.bind_param(stmt, 2, session['userId'])
    ibm_db.bind_param(stmt, 3, session['userId'])
    ibm_db.bind_param(stmt, 4, session['userId'])
    ibm_db.bind_param(stmt, 5, date)
    ibm_db.execute(stmt)
    tuple = ibm_db.fetch_tuple(stmt)
    if tuple != False:
        limit = tuple[0]
        total = tuple[1]
        email = tuple[2]
        name = tuple[3]
        print(email, name, limit, total)
        if total > limit:
            message = Mail(
                from_email='mail',
                to_emails=email,
                subject='Daily expense limit exceeded',
                html_content='<h2>Hello ' + name + '</h2><h3>This is to notify you that your daily expense limit of ' + str(limit) + ' has been exceeded</h3>')
            try:
                sg = SendGridAPIClient('key')
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e.message)    

def setLimit(limit):
    sql = "UPDATE user SET limit = ? WHERE id = ?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, limit)
    ibm_db.bind_param(stmt, 2, session['userId'])
    ibm_db.execute(stmt)
