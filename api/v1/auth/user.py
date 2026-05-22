from auth import auth

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or user.verify_passwd(password):
        print("verify..")
        return False
    g.user = user
    return True
