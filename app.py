from flask import Flask, render_template, redirect
import json

app = Flask(__name__)

with open("ring.json", "r") as file: 
    global members 
    members = json.load(file) 

def get_host_by_url(host):
    index_flag_var = 0
    for member in members: 
        if member["url"] == host:
            return {"name": member["name"], "url": member["url"], "site admin": member["site admin"], "index": index_flag_var}
        index_flag_var += 1
    return None

@app.route("/")
def home(): 
    return render_template("example.html")

@app.route("/next/<host>")
def next(host): 
    member = get_host_by_url(host)
    member_index = member["index"]

    if get_host_by_url(host) is not None: 
        return redirect("https://" + str(members[member_index + 1]["url"]), code=302)

    return render_template('notinring.html')

@app.route("/prev/<host>")
def prev(host): 
    member = get_host_by_url(host)
    member_index = member["index"]

    if get_host_by_url(host) is not None: 
        return redirect("https://" + str(members[member_index - 1]["url"]), code=302)

    return render_template('notinring.html')


@app.route("/component/<host>")
def generate_component(host): 
    member = get_host_by_url(host)
    return render_template("component.html", name=member["name"], url=member["url"], admin=member["site admin"])


if __name__ == '__main__':
    app.run(debug=False)