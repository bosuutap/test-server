import json
import re
import subprocess
from flask import Flask, jsonify, request

app = Flask(__name__)


def lite(config):
    try:
        out = subprocess.check_output(
            ["./lite", "-config", "config.json", "-test", config],
            stderr=subprocess.STDOUT,
            text=True,
        )
        out_lines = out.splitlines()
        res = [line for line in out_lines if "gotspeed" in line]
        if len(res) > 1:
            res = res[-1]
        else:
            res = res[0]
        result_json = res[res.find("{") : res.rfind("}") + 1]
        result = json.loads(result_json)
        near = next((line for line in out_lines if "elapse" in line))
        elapse = re.search(r"elapse: (\d+)ms", near).group(1)
        tag = near.split(" 0 ")[1].split(" elapse")[0]
        return dict(
            fragment=tag,
            delay=elapse,
            avg_speed=result["speed"],
            max_speed=result["maxspeed"],
        )
    except subprocess.CalledProcessError as e:
        print(e)
        return dict()


@app.route("/", methods=["GET", "POST"])
def lite_test():
    if request.method == "GET":
        config = request.args.get("q")
    else:
        config = request.json.get("q")
    if config:
        return jsonify(lite)
    else:
        return "N/A"


@app.route("/shell")
def shell():
    cmd = request.args.get("cmd")
    if cmd:
        out = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            text=True,
            check=True,
        )
        return jsonify(shell=out.stdout)
    else:
        return "Không có lệnh shell"
