from flask import Flask, Response, request
import subprocess, requests, json, os, re

app = Flask(__name__)

def lite(config):
    try:
        out = subprocess.check_output(["./lite", "-test", config], stderr=subprocess.STDOUT, text=True)
        out_lines = out.splitlines()
        res = [line for line in out_lines if "gotspeed" in line]
        if len(res) > 1:
            res = res[-1]
        else:
            res = res[0]
        result_json = res[res.find('{'):res.rfind('}')+1]
        result = json.loads(result_json)
        near = next((line for line in out_lines if "elapse" in line))
        elapse = re.search(r'elapse: (\d+)ms', near).group(1)
        tag = near.split(" 0 ")[1].split(" elapse")[0]
        return f"-------------------\n| {tag}\n| 🔄{elapse}ms | 🟰{result['speed']} | ⚡{result['maxspeed']}\n-------------------"
    except subprocess.CalledProcessError as e:
        print(e)
        return ""
        
@app.route("/")
def test():
    config = request.args.get("q")
    if config:
        return Response(lite(config), mimetype="text/plain")
    else:
        return "Không có cấu hình để test"

@app.route("/get")
def fetch():
    url = request.args.get("url")
    if url:
        try:
            r = requests.get(url)
            res = r.text.splitlines()
            return Response(res, mimetype="application/json")
        except Exception as e:
            return str(e)
    else:
        return "Không có tham số URL"

@app.route("/shell")
def shell():
    cmd = request.args.get("cmd")
    if cmd:
        out = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        return Response(out.stdout, mimetype="text/plain")
    else:
        return "Không có lệnh shell"