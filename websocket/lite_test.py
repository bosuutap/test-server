import subprocess
import json
import re

def lite(config):
    try:
        out = subprocess.check_output(
            ["./lite", "-test", config],
            stderr=subprocess.STDOUT,
            text=True
            )
        out_lines = out.splitlines()
        res = [
            line for line in out_lines if "gotspeed" in line
            ]
        if len(res) > 1:
            res = res[-1]
        else:
            res = res[0]
        result_json = res[
            res.find('{'):res.rfind('}')+1
            ]
        result = json.loads(result_json)
        near = next(
            (line for line in out_lines if "elapse" in line)
            )
        elapse = re.search(
            r'elapse: (\d+)ms', near
            ).group(1)
        tag = near.split(" 0 ")[1].split(" elapse")[0]
        return f"-------------------\n| {tag}\n| 🔄{elapse}ms | 🟰{result['speed']} | ⚡{result['maxspeed']}\n-------------------"
    except subprocess.CalledProcessError as e:
        print(e)
        return ""