#!/usr/bin/env python3
import os
import pickle
from flask import Flask, request

app = Flask(__name__)

BANNER = """
==========================
   Mini Vulnerable App
        CTF Demo
==========================
"""

@app.route("/")
def index():
    return BANNER + "\nRoutes: /run?cmd= , /read?file= , /load "

# --- VULN 1: Command Injection ---
@app.route("/run")
def run_cmd():
    cmd = request.args.get("cmd", "")
    # Vulnerable: executes raw user input
    output = os.popen(cmd).read()
    return f"Command output:\n{output}"

# --- VULN 2: Path Traversal ---
@app.route("/read")
def read_file():
    filename = request.args.get("file", "")
    try:
        with open(filename, "r") as f:
            return f.read()
    except Exception as e:
        return str(e)

# --- VULN 3: Insecure Deserialization ---
@app.route("/load", methods=["POST"])
def load_pickle():
    data = request.data
    try:
        obj = pickle.loads(data)   # Dangerous: loads attacker-controlled pickle
        return f"Loaded object: {obj}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    app.run(debug=True)
