from flask import Flask, render_template, request
from flask_caching import Cache

import requests
import os

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 0
asset_url = "https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/"
cache = Cache(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/profile", methods=["GET"])
def profile():
    uid = request.args.get("uid")
    url = f"https://api.mihomo.me/sr_info_parsed/{uid}?lang=en"
    res = requests.get(url)
    data = res.json()
    uid = data["player"]["uid"]
    cache.set("data_" + uid, data)

    url2 = f"https://api.mihomo.me/sr_info_parsed/{uid}?lang=en&version=v1"
    res2 = requests.get(url2)
    data2 = res2.json()
    cache.set("data2_" + uid, data2)

    return render_template("profile.html", data=data, asset_url=asset_url)


@app.route("/character")
def character():
    uid = request.args.get("uid")
    chara = int(request.args.get("chara"))
    data = cache.get("data_" + uid)
    data2 = cache.get("data2_" + uid)

    return render_template(
        "character.html",
        data=data,
        data2=data2,
        chara=chara,
        asset_url=asset_url,
    )


if __name__ == "__main__":
    app.run()
