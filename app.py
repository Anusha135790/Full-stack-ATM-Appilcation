from flask import Flask, render_template, redirect, request, session, url_for

app = Flask(__name__)
app.secret_key = "srinubabu@123"
@app.route('/')
def home():
    return render_template('home.html')
# {username:password}
accounts = {
    1234:1234,
    1235:1235,
    1236:1236

}
amounts = {
    1234:1000,
    1235:2000,
    1236:4000

}
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST': # check weather the request is post or not
        username = int(request.form['username']) # get form data into app
        password = int(request.form['password']) # get form data
        session['username'] = username # storning username in session component
        # data validation
        if username in accounts:
            if accounts[username] == password:
                return redirect(url_for("dashboard"))
            else:
                return render_template("login.html", msg = "Flash msg: Incorrect credentials" )
        else:
            return render_template("login.html", msg = "Flash msg: Account not found")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route("/balance")
def balance():
    if 'username' not in session:
        return redirect(url_for('login'))
    account = session['username'] # get account no. from session
    return render_template('balance.html', amount =amounts[account])

@app.route("/withdraw", methods = ['GET', 'POST'])
def withdraw():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        account = session['username']
        withdraw_amount = int(request.form['amount'])
        curr_amount = amounts[account]
        if curr_amount >= withdraw_amount:
            amounts[account] -= withdraw_amount
            return render_template("withdraw.html", \
                msg =f"Flash MSG: {withdraw_amount} withdraw successfull and \
                current balance is {curr_amount-withdraw_amount}")
        else:
            return render_template("withdraw.html", \
                msg =f"Flash MSG: Insufficient Funds")

    return render_template("withdraw.html")

@app.route('/deposite', methods=['GET','POST'])
def deposite():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        account = session['username']
        deposite_amount = int(request.form['amount'])
        
        amounts[account] += deposite_amount
        return render_template("deposite.html", \
                msg =f"Flash MSG: {deposite_amount} deposite successfull and \
                current balance is {amounts[account]}")
        

    return render_template("deposite.html")

@app.route("/transfer", methods=['GET','POST'])
def transfer():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        recieverAccount = int(request.form['recieverAccount'])
        tranfer_amount = int(request.form['amount'])
        account = session['username']
        curr_amount = amounts[account]
        if recieverAccount in accounts:
            if curr_amount >= tranfer_amount:
                amounts[account] -= tranfer_amount
                amounts[recieverAccount] += tranfer_amount
                return render_template("transfer.html", \
                    msg =f"Flash MSG: {tranfer_amount} transfer successfull and \
                    current balance is {curr_amount-tranfer_amount}")
            else:
                return render_template("transfer.html", \
                    msg =f"Flash MSG: Insufficient Funds")
        else:
            return render_template("transfer.html", \
                    msg =f"Flash MSG: Recieve Account not found")
    return render_template('transfer.html')


    
@app.route("/ministatement")
def ministatement():
    return "ministatement page underdevelopment process....."

@app.route("/logout")
def logout():
    session.pop('username')
    if 'username' not in session:
        return redirect(url_for('login'))
    
# main
if __name__ == '__main__':
    app.run(debug=True, port= 5003)