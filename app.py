from crypt import methods
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, 'mydatabase.db'))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, nullable = False, primary_key = True)
    date = db.Column(db.String(50), nullable = False)
    expensename = db.Column(db.String(100), nullable = False)
    amount = db.Column(db.Integer, nullable = False)
    category = db.Column(db.String(50), nullable = False)


@app.route('/')
def add_form():
    return render_template('/addform.html')

# create/add database expense table 
@app.route('/addexpense', methods=['POST'])
def add_expense():
    getdate = request.form['date']
    getexpenseName = request.form['expense']
    getamount = request.form['amount']
    getcategory = request.form['category']
    expenses = Expense(date=getdate, expensename=getexpenseName, amount=getamount, category=getcategory)
    db.session.add(expenses)
    db.session.commit()
    return redirect('/expenses')



# update/edit the info of database b
@app.route('/edit/<int:id>')
def edit_expense(id):
    expenseID = Expense.query.filter_by(id=id).first()
    return render_template('/editform.html', expenses = expenseID)


@app.route('/editexpense', methods=['POST'])
def edit():
    id = request.form['id']
    newdate = request.form['date']
    newexpenseName = request.form['expense']
    newamount = request.form['amount']
    newcategory = request.form['category']

    expenses = Expense.query.filter_by(id=id).first()
    expenses.date = newdate
    expenses.expensename = newexpenseName
    expenses.amount = newamount
    expenses.category = newcategory
    db.session.commit()

    return redirect('/expenses')

# read expense info 
@app.route('/expenses')
def expenses():
    getAllexpenses = Expense.query.all()
    total = 0
    t_food_amount = 0
    t_entertainment_amount = 0
    t_other_amount = 0
    t_business_amount = 0 
    for expense in getAllexpenses:
        total += expense.amount
        if expense.category == 'food':
            t_food_amount += expense.amount
        elif expense.category == 'business':
            t_business_amount += expense.amount
        elif expense.category == 'entertainment':
            t_entertainment_amount += expense.amount
        elif expense.category == 'other':
            t_other_amount += expense.amount

    return render_template('/expenses.html', expenses = getAllexpenses, t_food=t_food_amount, t_business=t_business_amount, 
    t_entertainment=t_entertainment_amount, t_other=t_other_amount, t_total=total) 

# delete the info from database 
@app.route('/delete/<int:id>')
def delete(id):
    expenseID = Expense.query.filter_by(id=id).first()
    db.session.delete(expenseID)
    db.session.commit()
    return redirect('/expenses')


# adding view for both methods POST and GET
@app.route('/addview', methods=['GET', 'POST'])
def add_view():
    if request.method == 'POST':
        getdate = request.form['date']
        getexpenseName = request.form['expense']
        getamount = request.form['amount']
        getcategory = request.form['category']
        expenses = Expense(date=getdate, expensename=getexpenseName, amount=getamount, category=getcategory)
        db.session.add(expenses)
        db.session.commit()
        return redirect('/addview')

    if request.method == 'GET':
        getAllexpenses = Expense.query.all()
        total = 0
        t_food_amount = 0
        t_entertainment_amount = 0
        t_other_amount = 0
        t_business_amount = 0 
        for expense in getAllexpenses:
            total += expense.amount
            if expense.category == 'food':
                t_food_amount += expense.amount
            elif expense.category == 'business':
                t_business_amount += expense.amount
            elif expense.category == 'entertainment':
                t_entertainment_amount += expense.amount
            elif expense.category == 'other':
                t_other_amount += expense.amount
                

    return render_template('/addview.html', expenses = getAllexpenses, t_food=t_food_amount, t_business=t_business_amount, 
    t_entertainment=t_entertainment_amount, t_other=t_other_amount, t_total=total) 
        


if __name__ == '__main__':
    app.run(debug=True)