from flask import Flask, request, render_template, redirect
from get_students_work import main
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == "POST":
        req = request.form
        email = req['email']

        return redirect(f'/processing/{email}')
    return render_template("form.html")

@app.route('/processing/<email>')
def processing(email):
    return f"Request received. A file will be shared with {email} as soon as processing is complete. This may take a few minutes."