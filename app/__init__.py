from flask import Flask, request, render_template, redirect
from app import get_students_work, Drive
from multiprocessing import Process

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == "POST":
        req = request.form
        email = req['email']
        primary_only = req.get('primary_only')
        print(email, primary_only)
        if primary_only:
            primary_only = True
        else:
            primary_only = False
        print(email, primary_only)
        background_process = Process(target=check_upload_share, daemon=True, args=(email, primary_only))
        background_process.start()
        return redirect(f'/processing/{email}')
    return render_template("form.html")


@app.route('/checkbox-test', methods=['GET', 'POST'])
def checkbox_test():
    if request.method == "POST":
        req = request.form
        return f'{req.get("email"), req.get("primary_only")}'
    return render_template('form.html')

@app.route('/processing/<email>')
def processing(email):
    return render_template('processing.html', name=email)


def check_upload_share(email, primary_only:bool = True):
    file = get_students_work.main(teacherEmail=email, primary_only=primary_only)
    fileId = Drive.upload(file, email)
    Drive.share(fileId=fileId, role='reader', email=email)
