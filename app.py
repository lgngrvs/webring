from flask import Flask, render_template, redirect
import json
import markdown
from random import randrange

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
    with open("readme.md", "r") as file: 
        return render_template("example.html", data = markdown.markdown(file.read()))

@app.route("/next/<host>")
def next(host): 
    member = get_host_by_url(host)
    member_index = member["index"]

    if get_host_by_url(host) is not None: 
        try: 
            return redirect("https://" + str(members[member_index + 1]["url"]), code=302)
        except IndexError: 
            return redirect("https://" + str(members[0]["url"]), code=302)
    
    return render_template('notinring.html')

@app.route("/prev/<host>")
def prev(host): 
    member = get_host_by_url(host)
    member_index = member["index"]

    if get_host_by_url(host) is not None: 
        try: 
            return redirect("https://" + str(members[member_index - 1]["url"]), code=302)
        except IndexError: 
            return redirect("https://" + str(members[-1]["url"]), code=302)


    return render_template('notinring.html')

@app.route("/random")
def random(): 
    rand_index = randrange(0, len(members))
    redirect_url = members[rand_index]["url"]
    return redirect("https://" + redirect_url, code=302)


@app.route("/component/<host>")
def generate_component(host): 
    member = get_host_by_url(host)
    return render_template("component.html", name=member["name"], url=member["url"], admin=member["site admin"])


if __name__ == '__main__':
    app.run(debug=False)