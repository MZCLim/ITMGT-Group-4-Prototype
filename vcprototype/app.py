from flask import  Flask, render_template, redirect, request, flash, session
import database as db
import feedmanagement as fm
import purchasemanagement as pm
import authentication
import logging



app = Flask(__name__)

app.secret_key = b's@g@d@c0ff33!'

logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.INFO)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.route('/tiers')
def tiers():
    tier_list = db.get_tiers()
    return render_template('tiers.html', page="Teams", tier_list=tier_list)

@app.route('/confirmpurchase')
def confirmpurchase():
    code = request.args.get('code', '')
    tier = db.get_tier(int(code))

    return render_template('confirmpurchase.html', code=code, tier=tier)

@app.route('/purchasetier')
def purchase():
    code = request.args.get('code', '')
    tier = db.get_tier(int(code))
    item = dict()

    item["code"] = code
    item["name"] = tier["name"]
    item["subtotal"] = tier["price"]

    if(session.get("cart") is None):
        session["cart"]={}

    cart = session["cart"]
    cart[code] = item
    session["cart"] = cart

    return redirect('/purchase')

@app.route('/purchase')
def cart():
    return render_template('purchase.html')

@app.route('/paymentmethod', methods = ['POST'])
def paymentmethod():
    code = request.form.get('code', '')
    tier = db.get_tier(int(code))
    payment = request.form.get('payment')

    cart = session["cart"]

    for item in cart.values():
        if item["code"] == code:
            item["subtotal"] = tier["price"]
            item["payment"] = payment
            cart = session["cart"]
            cart[code] = item
            session["cart"] = cart
    return render_template('purchase.html', code=code, tier=tier, payment=payment)

@app.route('/checkout')
def checkout():
    pm.create_tier_purchase()
    session.pop("cart",None)

    return redirect('/purchasecomplete')

@app.route('/purchasecomplete')
def purchasecomplete():
    return render_template('purchasecomplete.html')

@app.route("/purchasehistory", methods=["GET"])
def purchasehistory():
    purchase_history = db.view_purchase_history()

    return render_template("purchasehistory.html", purchase_history=purchase_history)

@app.route('/organization')
def organization():
    team_list = db.get_teams()
    return render_template('organization.html', page="Organization", team_list=team_list)

@app.route("/organizationfeed", methods=["GET", "POST"])
def organizationfeed():
    code = request.args.get('code', '')
    team = db.get_team(int(code))
    history = db.view_message_history()
    message_history = reversed(history)

    return render_template("organizationfeed.html", code=code, team=team)

@app.route('/teams')
def teams():
    team_list = db.get_teams()
    return render_template('team.html', page="Teams", team_list=team_list)

@app.route('/teamdetails')
def teamsdetails():
    code = request.args.get('code', '')
    team = db.get_team(int(code))

    return render_template('teamdetails.html', code=code, team=team)

@app.route('/')
def index():
    return render_template('login.html', page="Login")

@app.route('/home', methods = ['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route("/addmessages", methods=["GET", "POST"])
def addmessages():
    fm.create_message_feed()
    history = db.view_message_history()
    message_history = reversed(history)

    return render_template("index.html", message_history=message_history)

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop("user",None)
    session.pop("cart",None)
    return redirect('/')

@app.route('/auth', methods = ['GET', 'POST'])
def auth():
    username = request.form.get('username')
    password = request.form.get('password')

    is_successful, user = authentication.login(username, password)
    app.logger.info('%s', is_successful)
    if(is_successful):
        session["user"] = user
        return redirect('/home')
    else:
        flash('Invalid username or password. Please try again')
        return redirect('/login')

@app.route("/profile/changepassword", methods=["GET","POST"])
def changepassword():
    username = session["user"]["username"]
    password = db.get_password(username)
    currentpassword = request.form.get("oldpassword")
    newpassword = request.form.get("newpassword")
    checkpassword = request.form.get("checkpassword")
    changepassword = None
    error = None

    if currentpassword == None:
        error = None

    elif newpassword == "":
        error = "No new password was given."

    elif currentpassword != password:
        error = "Current password is incorrect."

    elif currentpassword == newpassword:
        error = "Your new password cannot be the same as your old password "

    elif newpassword != checkpassword:
        error = "New passwords did not match."

    elif currentpassword == password:
        if newpassword == checkpassword:
            changepassword = db.change_password(username,newpassword)

    return render_template("changepassword.html", page="Change Password", changepassword=changepassword, error=error)
