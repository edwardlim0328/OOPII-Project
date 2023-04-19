from flask import Blueprint, render_template, request, flash, jsonify, redirect
from gingerit.gingerit import GingerIt
from flask_login import login_required, current_user
from .models import User
from . import db
import json

views = Blueprint('views', __name__)
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/my_info', methods=['GET', 'POST'])
@login_required
def account():
    user = User.query.filter_by(id=current_user.id).first()
    return render_template("account.html", user=current_user)

@views.route('/spell_checker', methods=['GET', 'POST'])
@login_required
def spellChecker():
    if request.method == 'POST':
        text = request.form["SENT"]
        parser = GingerIt()
        print(parser.parse(text)['corrections'])
        result=parser.parse(text)['result']
        return render_template('spellcheck.html', user=current_user, output1=result)
        
    return render_template("spellcheck.html", user=current_user)

@views.route('/calculator', methods=['GET', 'POST'])
@login_required
def calculator():
    if request.method == 'POST':
        num1 = request.form.get('num1')
        num2 = request.form.get('num2')
        num3 = request.form.get('num3')
        result = None

        num1 = float(num1)
        num2 = float(num2)
        num3 = float(num3)
        
        if num1 ==0 or num2 == 0 or num3 == 0:
            flash('Please enter valid numbers for the interest rate and loan term.', category='error')
        else:
            result = round(((num1*(num2/100/12.0))*((1+(num2/100/12.0))**(num3*12)))/((((1+(num2/100/12.0))**(num3*12)))-1),2)        
        return render_template("calculator.html", user=current_user, result=result)
    return render_template("calculator.html", user=current_user)


