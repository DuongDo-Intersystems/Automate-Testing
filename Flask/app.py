from flask_mail import Mail
from flask_mail import Message
from threading import Thread
from flask import Flask, flash, redirect, render_template, url_for
from Flask.form_request_password import ResetPasswordRequestForm, ResetPasswordForm


app = Flask(__name__)
app.config['SECRET_KEY'] = "Online Learning"

# Mail config
app.config['MAIL_SERVER'] = "mail.iscinternal.com"
app.config['MAIL_USE_TLS'] = True

mail = Mail(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        # TO DO: need to check the email actually exist in database
        recipient = form.email.data
        send_password_reset_email(recipient)
        flash('Instructions to reset your password sent to {}'.format(recipient))
        return redirect(url_for('index'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)


def send_password_reset_email(recipient):
    recipients = [recipient]
    msg = Message('Reset Your Password', sender='Online.Training@intersystems.com', recipients=recipients)
    email_form = ResetPasswordRequestForm()
    email = email_form.email.data
    msg.html = render_template('reset_password_text.html', email=email)
    t = Thread(name="Send Email", target=send_async_email, args=(app, msg))
    t.start()


@app.route('/reset_password/<user>', methods=['GET', 'POST'])
def reset_password(user):
    # TO DO: need to validate user
    form = ResetPasswordForm()
    if form.validate_on_submit():
        new_password = form.password2.data
        set_password(user, new_password)
        flash('Password has been reset for {}.'.format(user))
        return redirect(url_for('index'))
    return render_template('reset_password_form.html', form=form)


def set_password(user, new_password):
    with open("user_credentials.txt", "r+") as f:
        lines = f.readlines()
        f.seek(0)
        for line in lines:
            line = ''.join(line.split())
            user_name, password = line.split(':')
            if user_name != user:
                f.write(line + "\n")
            if user_name == user:
                f.write("{}:{}\n".format(user_name, new_password))
        f.truncate()


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


@app.route('/email')
def send_mail():
    recipients = ['DUONG.DO@intersystems.com']
    msg = Message('test subject', sender='Online.Training@intersystems.com', recipients=recipients)
    msg.html = "<p>Welcome to your InterSystems IRIS Learning Lab. Insert marketing sentences here.</p>" \
               "<p> Please note that your instance will only run for 24 hours unless you verify your email. " \
               "Please click <a href='link provided by flask to SSO'>this link</a> to verify your email and extend your Learning Lab for 30 days. " \
               "If you want to return to your lab, you can use <a href='link to IDE from flask'>this link</a></p>"
    t = Thread(name="Send Email", target=send_async_email, args=(app, msg))
    t.start()
    return "Sent email about container successfully."


if __name__ == '__main__':
    app.run()