from flask import Flask, request, render_template, redirect
import get_students_work
import Drive
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == "POST":
        req = request.form
        email = req['email']
        file = get_students_work.main(teacherEmail=email)
        fileId = Drive.upload(file, email)
        Drive.share(fileId=fileId, role='reader', email=email)
        return redirect(f'/processing/{email}')
    return render_template("form.html")

@app.route('/processing/<email>')
def processing(email):
    return f"Request received. A file will be shared with {email} as soon as processing is complete. This may take a few minutes."