from dataManager import dataManager
from flask import Flask, render_template, request

dm = dataManager()

app = Flask(__name__)
@app.route('/')
def loading():
    return render_template("home.html",table=None)

@app.route("/uploadfile", methods=["POST"])
def uploadFile():
    dm.setData(request.files["dataFile"])
    return render_template("home.html",table=dm.getHTML())





if __name__ == '__main__':
    app.run()



