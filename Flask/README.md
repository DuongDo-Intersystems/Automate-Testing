# Reset password

## Contents

### Python files

1. `form_request_password.py`: Contain 2 Flask Forms: Enter Email, and Reset Password
2. `app.py`: Contain the following functions:
    * `index()`
    * `reset_password_request()`: Send email for user to reset password.
    * `send_password_reset_email()`: helper function for `reset_password_reset`. Contain sender, recipients, messages content.
    * `reset_password(user)`: Set new password for given user.
    * `set_password(user, new_password)`: helper function for `reset_password`. Write user and new password to `user_credentials.txt` file.
    * `send_async_email()`: Send asynchronous email.
    * `send_mail():` Send email about container info.

### Template HTML files

1. `base.html`: for fun
2. `index.html`: Main page, contain links to send container information and reset password for user.
3. `reset_password_form.html`: Contain two boxes: Enter password, and confirm password.
4. `reset_password_request.html`: Contain 1 box to enter email for sending reset link.
5. `reset_password_text.html`: Text to send for user.

## How to run

1. Add your email and a fake password into `user_credentials.txt`
2. `python app.py`
3. Go to [http://127.0.0.1:5000](http://127.0.0.1:5000), and select **Click here to reset password**
4. Enter your email
5. Click on the link from your email to reset password. Type in a new password, for example, **hello**
6. For now, I don't have database, so I make a fake database in `user_credentials.txt`.

Before reset password, `user_credentials.txt`:

    duong.do@intersystems.com:pass1
    dhdo@csbsju.edu:pass2
    dohoangduong95@gmail.com:pass3

After reset password, you can see the password for your email in `user_credentials.txt` has been change.