# login_bp dependencies
from flask import current_app as app, flash
from flask import redirect, render_template, request, url_for, session
from flask_login import login_user, logout_user


from coyote.blueprints.login import login_bp
from coyote.blueprints.login.login import LoginForm, User
from coyote.extensions import login_manager, mongo, ldap_manager, store


users_collection = mongo.cx["coyote"]["users"]

# Login routes:

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == "POST" and form.validate_on_submit():
        username = str(form.username.data)
        password = str(form.password.data)
        if ldap_authenticate(username, password):
            app.logger.info("anything?")
            user_obj = store.user(username)
            user_obj = User(user_obj["_id"], user_obj["groups"])
            login_user(user_obj)
            return redirect(url_for("main_bp.main_screen"))
        else:
            app.logger.info("yes?")
            return render_template('login.html',form=form, error="Invalid credentials")

    return render_template("login.html", title="login", form=form)


@login_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login_bp.login"))


@login_manager.user_loader
def load_user(username):
    user = users_collection.find_one({"_id": username})
    if not user:
        return None
    return User(user["_id"], user["groups"])

def ldap_authenticate(username, password):
    authorized = False

    try:
        authorized = ldap_manager.authenticate(
            username=username,
            password=password,
            base_dn=app.config.get("LDAP_BASE_DN") or app.config.get("LDAP_BINDDN"),
            attribute=app.config.get("LDAP_USER_LOGIN_ATTR")
        )
    except Exception as ex:
        flash(ex, "danger")

    return authorized