# -*- coding: utf-8 -*-
from flask import flash,render_template, url_for, redirect, Flask, request
from apps import app,mailbox,db
from apps.models import Scholarship, User
from flask.ext.email import EmailMessage

import logging,codecs,copy

def check_grade(row, personal_inform):
    check = [0,0,0]

    for x in range(0,3):
        if x == 0:
            if(row.all_grade != None):
                check[0] +=1
            else:
                continue
        if x == 1:
            if(row.prev1_grade != None):
                check[1] +=1
            else:
                continue
        if x == 2:
            if(row.prev2_grade != None):
                check[2] +=1
            else:
                continue

    sum = check[0]+check[1]+check[2]
    logging.debug(sum)
    if sum == 0:
        return row

    if sum==1:
        if check[0] == 1:
            if personal_inform.user_all_grade >= row.all_grade:
                return row
        if check[1] == 1:
            if personal_inform.user_prev1_grade >= row.prev1_grade:
                return row
        if check[2] == 1:
            if personal_inform.user_prev2_grade >= row.prev2_grade:
                return row

    if sum==2:
        if check[0] and check[1] == 1:
            if personal_inform.user_all_grade >= row.all_grade or personal_inform.user_prev1_grade >= row.prev1_grade:
                return row
        if check[0] and check[2] == 1:
            if personal_inform.user_all_grade >= row.all_grade or personal_inform.user_prev2_grade >= row.prev2_grade:
                return row
        if check[1] and check[2] == 1:
            if personal_inform.user_prev1_grade >= row.prev1_grade or personal_inform.user_prev2_grade >= row.prev2_grade:
                return row

def match(input):
    result = []
    a = Scholarship.query.filter(Scholarship.area_state != None)
    b = Scholarship.query.filter(Scholarship.area_state == "")
    for row in a:
            if row.area_city != "":
                if input.user_area_state != row.area_state:
                    continue
                else:
                    if input.user_area_city != row.area_city:
                        continue
                    else:
                        #check grade conditions and print
                        if row.all_grade or row.prev1_grade or row.prev2_grade != None:
                            result.append(check_grade(row,input))
                        else:
                            #if there are no grade conditions and print
                            result.append(row)
            #if there is not row['area_state']
            else:
                if input.user_area_state != row.area_state:
                    continue
                else:
                #check grade conditions and print
                    if row.all_grade or row.prev1_grade or row.prev2_grade != None:
                        result.append(check_grade(row,input))
                #if there are no grade conditions and print
                    else:
                        result.append(row)
    for row in b:
        if row.all_grade or row.prev1_grade or row.prev2_grade != None:
            result.append(check_grade(row,input))
        else:
            #if there are no grade conditions and print
            result.append(row)

    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html')
    elif request.method == 'POST':
        personal = User(
            user_student_num = request.form['student_num'],
            user_prev1_grade = request.form['prev1_grade'],
            user_prev2_grade = request.form['prev2_grade'],
            user_all_grade = request.form['all_grade'],
            user_grade_condition = request.form['grade_condition'],
            user_area_state = request.form['area_state'],
            user_area_city = request.form['area_city']
        )
        db.session.add(personal)
        db.session.commit()

        return redirect(url_for('result', id=request.form['student_num']))

@app.route('/result:<string:id>', methods=['GET'])
def result(id):
    if request.method == 'GET':
        data = User.query.get(id)
        find_scholar = []
        result = match(data)
        for x in result:
            if x != None:
                find_scholar.append(x)
        return render_template('result.html', result=find_scholar)

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'GET':
        return render_template('report.html')
    elif request.method == 'POST':
        report_inform = {}
        report_inform['name'] = request.form['name']
        report_inform['email'] = request.form['email']
        report_inform['message'] = request.form['message']
        email = EmailMessage(
            'Scholarship Modification by %s'%report_inform['name'],
            report_inform['message'],
            report_inform['email'],
            ['cronos91@naver.com'],
            headers={'From':report_inform['email']}
        )
        test = EmailMessage(
            'Subject',
            'Content',
            'lxmcdonald@naver.com',
            ['cronos91@naver.com'],
            headers={'From': 'lxmcdonald@example.com'}
        )
        test.send(mailbox)
        email.send(mailbox)
        #send_email('장학금 수정사항 by %s'%report_inform['name'], report_inform['message'],report_inform['email'],['cronos91@naver.com'] )
        flash(u'이메일을 성공적으로 보냈습니다', 'success')
        return redirect(url_for('report'))
