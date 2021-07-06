from flask import Flask,render_template,url_for,request,session,redirect
import psycopg2
import psycopg2.extras

app = Flask(__name__)
app.secret_key = 'secrect'
 
DB_HOST = "localhost"
DB_NAME = "sample"
DB_USER = "postgres"
DB_PASS = "venky@postgresql"
 
con = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
 

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin')
def admin():
    if session['username']:
        return render_template('admin.html',info=session['username'])
    return redirect(url_for('login'))

@app.route('/user')
def user():
    if session['username']:
        return render_template('user.html',info=session['username'])
    return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        name = request.form['username']
        pwd = request.form['password']
        cursor.execute("SELECT * FROM users WHERE username = %s",(name,))
        user = cursor.fetchone()
        if user:
            # cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s",(name,pwd))
            # pwd = cursor.fetchone()
            pwds = user['password']
            if pwds == pwd:
                session['username'] = user['username']
                # cursor.execute("SELECT role FROM users WHERE username = %s",(name,))
                # roles = cursor.fetchone()
                role = user['role']
                if role == "admin":
                    return redirect(url_for('admin'))
                else:
                    return redirect(url_for('user'))
            else:
                msg = "Password is incorret. Kindly check"
                return render_template('error.html',info=msg)        
        else:
            msg = "username is incorret. Kindly check"
            return render_template('error.html',info=msg)

    return render_template('login.html')

    

@app.route('/signup',methods=['GET','POST'])
def signup():
    cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        name = request.form['username']
        role = request.form['role']
        pwd = request.form['password']
        msg =  "Account created successfully"    
        cursor.execute("INSERT INTO users (username,password,role) VALUES (%s,%s,%s)", (name,pwd,role))
        con.commit()
        return render_template('error.html',info=msg)
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session['username'] = None
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)


