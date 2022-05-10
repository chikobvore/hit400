from datetime import datetime
import numpy as np
import pandas as pd
import pymongo
from flask import Flask, redirect, render_template, request, session, url_for,jsonify
from bson import json_util
import json
import ssl
import mysql.connector
import requests
import dbh,api
import time

app = Flask(__name__)

# client = pymongo.MongoClient("mongodb+srv://ladsroot:ladsroot@lads.f97uh.mongodb.net/tau?retryWrites=true&w=majority")
# db = client.tau


@app.route('/') 
def index():
    return render_template('index.html')

@app.route('/api',methods=["post"])
def chatmenu():
    print('message received')
    payload = request.get_json()

    sender = payload['data']['from'].split('@')[0]

    senderName = payload['data']['from'].split('@')[0]
    # message_id = payload['messages'][0]['id']
    response = payload['data']['body']
    
    if sender == '263771067779':
        return '', 200

        existance = dbh.db['Senders'].count_documents({"Sender": sender}) 

    #check if session exist
    if existance < 1:
        #create new session
        record = {
            "Sender": sender,
            "Timestamp": datetime.datetime.now(),
            "session_type": "0",
            "Status": "0"
            }
        dbh.db['Senders'].insert_one(record)
        # -*- coding: utf-8 -*-
        caption = "Hello "+ senderName +" 🙋🏽‍♂ , \nThank you for contacting HIT CLINIC,I'm Tau, i'm a virtual assistant,\nFor any emergency 👇 \n📞 Dial Number: +263202060823 \n\nPlease visit our clinic first to be registered for this service"
        attachment_url = 'https://www.africa2trust.com/WBA/Logos/HIT316410143.jpg'
        api.send_attachment(sender,attachment_url,caption)
        return '', 200
    else:

        response = response
        state = dbh.db['Senders'].find_one({"Sender": sender})

        date2 = datetime.datetime.now()
        date1 = state['Timestamp']

        time_delta = (date2 - date1)

        total_seconds = time_delta.total_seconds()

        minutes = total_seconds/60
        if minutes > 10:
            sh.session_status(sender,'0','0')
            message =  "*Previous session expired*\nHello *"+ senderName +"* 🙋🏽‍♂,\nPlease select one of the following options 👇\n\n"+ str('1️⃣') +"*USS OBSTETRICS*\n\n"+ str('2️⃣') +" *USS PELVIS*\n\n"+str('0️⃣') +" *Cancel*\n\n""
            api.reply_message(sender,message)
            return '', 200

        if state['session_type'] == "0":
            if response == "1":
                return obstetrics(reference)
            elif response == "2":
                return pelvis(reference)
            else:
                
                message =  "*Invalid Response*\nHello *"+ senderName +"* 🙋🏽‍♂,\nPlease select one of the following options 👇\n\n"+ str('1️⃣') +"*USS OBSTETRICS*\n\n"+ str('2️⃣') +" *USS PELVIS*\n\n"+str('0️⃣') +" *Cancel*\n\n""
                api.reply_message(sender,message)
                return '', 200




@app.route('/new-patient',methods=['POST','GET']) 
def addpatient():

    if request.method == 'GET':

        return render_template('newpatient.html')

    else:
        name = request.form['name']
        surname = request.form['surname']
        sex = request.form['sex']
        dob = request.form['dob']
        address = request.form['address']
        email = request.form['email']
        contact = request.form['contact']

        num = dbh.db['Patients'].count_documents({"status":"Pending"})
        w_no = 100 + num
        
        patient = {
            "name": name,
            "surname": surname,
            "sex": sex,
            "dob": dob,
            "address": address,
            "email": email,
            "contact": contact,
            "scan_type": " ",
            "waiting_list_no": w_no,
            "status": "Pending"
            }
        dbh.db['Patients'].insert(patient)

        patient = dbh.db['Patients'].find_one({"contact": contact})

        record = {
            "Sender": sender,
            "Timestamp": datetime.datetime.now(),
            "session_type": "1",
            "Status": "0"
            }
        dbh.db['Senders'].insert_one(record)

        caption = "Hello "+ str(patient['name'])+ " "+ str(patient['surname'])+"\nThank you for visiting HIT CLINIC\n. Please follow our orderly queue, your waiting list:" + str(w_no) +". You ll be notified once your turn have come,\n*Thank You*"
        attachment_url = 'https://www.africa2trust.com/WBA/Logos/HIT316410143.jpg'
        api.send_attachment(contact,attachment_url,caption)

        time.sleep(30)

        message =  "Hello *"+ senderName +"* 🙋🏽‍♂,\nPlease select one of the following options 👇\n\n"+ str('1️⃣') +"*USS OBSTETRICS*\n\n"+ str('2️⃣') +" *USS PELVIS*\n\n"+str('0️⃣') +" *Cancel*\n\n""
        api.reply_message(sender,message)
        
        return redirect('/manage')

@app.route('/manage') 
def manage():
    
    mypatients = []
    patients = dbh.db['Patients'].find().limit(500)
    
    for patient in patients:
        mypatients.append(patient)

    return render_template('manage.html',patients = mypatients)

@app.route('/uss-obstetrics/<reference>') 
def obstetrics(reference):

    message = '''*Prerequisites USS OBSTETRICS*\n1. Wear comfortable, loose-fitting clothing. You may need to remove all clothing and jewelry in the area to be examined. You may need to change into a gown for the procedure.\n
    2. You do not need to fast for this exam (eat all meals as usual on the day of the exam)\n
    3. Take all medications as usual\n
    4. Drink 1 liter of fluid (water, juice or soda) within 15 minutes, one hour prior to your appt time.\n
    5. Do not empty your bladder prior to having this exam (bladder must be full)'''
    api.reply_message(reference,message)

    time.sleep(30)


    message = "Hello,Thank you for following our orderly queue. Please come to room 31 for examination\nThank you"
    api.reply_message(reference,message)
    sh.session_status(sender,'0','0')

    return '',200

@app.route('/uss-pelvis/<reference>') 
def pelvis(reference):
    

    message = '''*Prerequisites USS PELVIS*1. You may eat and drink anything you like on the day of your exam.\n
    2. 2 hours before your scheduled appointment time you should start drinking 1 quart of clear liquid (i.e. soda, water, juice or coffee).\n
    3. The liquid should be finished 1 hour before the exam.\n
    3. Once you have started drinking, you should not empty your bladder.\n
    4. You may experience some discomfort when your bladder fills. Unfortunately, we need you to have a full bladder for this exam.\n
    5. This exam will take approximately 15 minutes if your bladder is full. (It will take longer if we have to wait for your bladder to fill).\n
    6. Please let the radiographer/receptionist know if your bladder feels too full to tolerate. They will try to make you as comfortable as possible.'''
    api.reply_message(reference,message)

    time.sleep(30)


    message = "Hello,Thank you for following our orderly queue. Please come to room 31 for examination\nThank you"
    api.reply_message(reference,message)

    return '',200



if __name__ == '__main__':
   app.secret_key = 'super secret key'
   app.config['SESSION_TYPE'] = 'filesystem'
   app.run(debug = True,port='5000')
