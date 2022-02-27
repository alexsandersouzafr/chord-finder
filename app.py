from flask import Flask, redirect, render_template, request
from helpers import chordfinder, NOTES

app = Flask(__name__)

choices = []
for i in NOTES:
    if int(i) > 12: break
    for item in NOTES[i]:
        choices.append(item)
choices.sort()
print(choices)

@app.route("/")
def index():

    return render_template("/layout.html", choices=choices)

@app.route("/found")
def found():
    if request.method == "GET":
        root = request.args.get("root")
        b = request.args.get("b")
        c = request.args.get("c")
        d = request.args.get("d")
        if d == 'none':
            d = None
        if chordfinder(root, b, c, d):
            chord = chordfinder(root, b, c, d)
            if 'None' in chord:
                chord = "Invalid Notes"
        else:
            chord = "Invalid Notes"
        return render_template("/found.html", chord=chord, choices=choices)
    else:
        return redirect("/")