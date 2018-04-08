from flask import Flask, request, redirect, render_template
import cgi
import re
import os


app = Flask(__name__)
app.config['DEBUG']= True


def validate_field(inputfield):
    error_message = ""
    if len(inputfield) <3 :
        error_message ="field length cannot be less than 3."
    if len(inputfield) >20:
        error_message=" field length cannot be greater than 20."
    if ' 'in inputfield :
        error_message ="field cannot have space."
    return error_message

def email_validation(email):
    if not email:
        return ""

    error_msg = validate_field(email)
    counter = email.count('@')    
    if counter != 1 :
        error_msg = error_msg + "Email must contain one @ " 

    counter = email.count('.')
    if counter != 1 :
        error_msg = error_msg + "Email must contain one ." 
   
    return error_msg

    
@app.route("/", methods=['POST'])
def user_signup():
    username = request.form['username']
    password = request.form['password']
    verifypassword = request.form['verifypassword']
    email = request.form['email']

    username_error = ''
    password_error = ''
    verifypassword_error = ''
    email_error = ''
    
    #Validation 1:
    if (not username) or (username.strip() == ""):
        username_error = "Please specify username. "
    if (not password) or (password.strip() == ""):
        password_error = "Please specify the password. "
    if (not verifypassword) or (verifypassword.strip() == ""):
        verifypassword_error = "Please verify password."

    #error = error_msg1  + error_msg2 + error_msg3
    #if len(error) > 0:
        #return redirect("/?error=" + error)

    #Validation 2:
    if not username_error:
        username_error = validate_field(username)
    if not password_error:
        password_error = validate_field(password)

    #error = error_msg1 + error_msg2
    #if len(error) > 0:
        #return redirect("/?error=" + error)

    #Validation 3
    if not verifypassword_error:
        if verifypassword != password:
            verifypassword_error ="Passwords do not match."
        #return redirect("/?error=" + error)

    # Validate 4  
    email_error = email_validation(email)
    #if len(error_msg4)>0:
        #return redirect("/?error=" + error_msg4)

    if not username_error and not password_error and  not verifypassword_error and  not email_error:
       #message = "Welcome," + username
       return redirect('/welcome?user={0}'.format(username))
    else:
        return render_template('userform.html',username_error=username_error,password_error=password_error,verifypassword_error=verifypassword_error,email_error=email_error,email=email,username=username)  

@app.route("/")
def index():
        # combine all the pieces to build the content of our response
    return render_template('userform.html') 
 
   

@app.route('/welcome')
def welcome():
    username= request.args.get('user')
    return render_template ('welcome.html',username=username)
app.run()
