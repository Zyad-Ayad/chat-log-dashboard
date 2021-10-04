from flask import Flask, redirect, render_template, request, session, flash
from datetime import timedelta
from functions import apology, auth, get_user_data, get_user_guilds, get_channels
from functools import wraps
from flask_session import Session




# Configure application
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SECRET_KEY'] = "@#$@$#123$FDGFDT$%%Rkr ewr ewrefdsqwe2 s"
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=30)
app.url_map.strict_slashes = False



def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None or session.get("user") is None or session.get("guilds") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        return render_template("index.html", user=session["user"], servers=session["guilds"])
    
    if request.method == "POST":
        if request.form.get("server") is None:
            return apology("You didn't select any server", session["user"])
        else:
            serverId = request.form.get("server")
    return redirect(f"/dashboard/{serverId}")




@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        return redirect("https://discord.com/api/oauth2/authorize?client_id=879273611603619881&redirect_uri=https%3A%2F%2Fchat-log-dashboard.herokuapp.com%2Floggedin&response_type=code&scope=identify%20guilds")

@app.route('/loggedin')
def loggedin():
    auth_key = {}
    code = request.args.get("code")
    if not code:
        session.clear()
        return apology("No codes provided! please use login button")
    else:
        auth_key = auth(code)
        if auth_key == "ERROR: 1":
            session.clear()
            return apology("Couldn't get auth token. Please re-login")

    user = get_user_data(auth_key)
    if user == "ERROR: 2":
        session.clear()
        return apology("Couldn't get user data. Please re-login")

    session["user_id"] = user["id"]
    session["user"] = user
    

    user_guilds = get_user_guilds(auth_key)
    if user_guilds == "ERROR: 3":
        return apology("Couldn't get user_guilds data. Please re-login", session["user"])

    session["guilds"] = user_guilds
    return redirect('/')

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/dashboard/<server_id>", methods=["GET", "POST"])
@login_required
def dashboard(server_id):
    if request.method == "GET":
        if session["guilds"].get(server_id) is None:
            return apology("Couldn't open this server dashboard.!\nDo you have [ADMINISTRATOR] permission in this server ?", user=session["user"])
        else:

            channels = get_channels(server_id)
            server = session["guilds"][server_id]
            return render_template("dashboard.html", user=session["user"], channels=channels, server=server)
    
    if request.method == "POST":
        flash("This future is OFF now!")
        return redirect(request.url)
    


@app.route("/dashboard")
def dashboard1():
    return redirect("/")


@app.route("/dashboard")
def dashboard1():
    return redirect("/")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500




if __name__ == '__main__':
    app.run()
