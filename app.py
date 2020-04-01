from flask import Flask, request, render_template, redirect
import get_students_work
import Drive
from multiprocessing import Process

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == "POST":
        req = request.form
        email = req['email']
        background_process = Process(target=check_upload_share, daemon=True, args=(email,))
        background_process.start()
        return redirect(f'/processing/{email}')
    return render_template("form.html")

@app.route('/processing/<email>')
def processing(email):
    return render_template('processing.html', name=email)


def check_upload_share(email):
    file = get_students_work.main(teacherEmail=email)
    fileId = Drive.upload(file, email)
    Drive.share(fileId=fileId, role='reader', email=email)
