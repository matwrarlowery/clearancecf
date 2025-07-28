import subprocess
import re
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class InputData(BaseModel):
    cookies_file: str
    url: str

@app.post("/run")
async def run_script(data: InputData):
    try:
        cmd = [
            "python", "main.py",
            "-f", data.cookies_file,
            data.url
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)

        # Buscar el valor de cf_clearance en la salida stderr
        match = re.search(r'cf_clearance=([\w\-_.]+)', result.stderr)
        if match:
            cf_clearance = match.group(1)
            return {"cf_clearance": cf_clearance}
        else:
            return {"error": "cf_clearance not found", "log": result.stderr}

    except Exception as e:
        return {"error": str(e)}
