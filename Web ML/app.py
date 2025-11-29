import os
import re
import sqlite3
import joblib
import subprocess
from flask import Flask, redirect, render_template, request, session, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "supersecretkey")
DB_PATH = "ctf.db"

# === ML Models ===
MODEL_FILES = {
    "sqli_model": "models/sqli_dt.joblib",
    "sqli_vec": "models/sqli_vec.joblib",
    "xss_model":  "models/xss_dt.joblib",
    "xss_vec":    "models/xss_vec.joblib"
}
THRESHOLDS = {"sqli": 0.50, "xss": 0.50}

def contains_real_flag(text):
    if not text: return False
    return "flag{" in str(text).lower() and "}" in str(text)

def safe_load(path):
    return joblib.load(path) if os.path.exists(path) else None

sqli_model = safe_load(MODEL_FILES["sqli_model"])
sqli_vec   = safe_load(MODEL_FILES["sqli_vec"])
xss_model  = safe_load(MODEL_FILES["xss_model"])
xss_vec    = safe_load(MODEL_FILES["xss_vec"])

# === DB Setup ===
def get_db():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        email TEXT,
        bio TEXT,
        role TEXT DEFAULT 'user'
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        attack_type TEXT,
        endpoint TEXT,
        input_name TEXT,
        input_text TEXT,
        score REAL,
        ts DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")

    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO users (username,password,email,bio,role) VALUES (?,?,?,?,?)",
                    ("admin", "real_admin_pass123", "admin@ctf.com", "Admin user", "admin"))
        for i in range(1, 12):
            cur.execute("INSERT INTO users (username,password,email,bio) VALUES (?,?,?,?)",
                        (f"dummy{i}", "dummy", f"dummy{i}@example.com", "Dummy bio"))
        cur.execute("INSERT INTO users (id,username,password,email,bio) VALUES (?,?,?,?,?)",
                    (313, "special_user", "pass313", "special@ctf.com", "Secret user"))
        conn.commit()
    conn.close()

init_db()

# === ML Detection + Flag Reveal ===
def predict_score(model, vec, text):
    try:
        X = vec.transform([str(text)])
        if hasattr(model, "predict_proba"):
            return float(model.predict_proba(X)[0][1])
        return float(model.predict(X)[0])
    except:
        return 0.0

def detect_all_on_inputs(inputs: dict):
    detections = {}

    for name, text in inputs.items():
        if not text or str(text).strip() == "":
            detections[name] = []
            continue

        s = str(text)

        # Skip real CTF flags
        if contains_real_flag(s):
            detections[name] = []
            continue

        found = []

        # SQLi Detection + Flag Reveal
        if sqli_model and sqli_vec:
            score = predict_score(sqli_model, sqli_vec, s)
            if score >= THRESHOLDS["sqli"]:
                found.append(("SQLi", score))
                log_detection(session.get("username","guest"), "SQLi", name, s, score)
                # REVEAL SQLi FLAG
                flash("SQLi Detected! Here's your reward: flag{SqL_inject10n_1s_fun}", "success")

        # XSS Detection + JavaScript Flag Alert
        if xss_model and xss_vec:
            score = predict_score(xss_model, xss_vec, s)
            if score >= THRESHOLDS["xss"]:
                found.append(("XSS", score))
                log_detection(session.get("username","guest"), "XSS", name, s, score)
                # REVEAL XSS FLAG via JS ALERT
                flash(f'<script>alert("XSS Detected! Flag: flag{{XSS_1s_tr1cky_but_fun}}")</script>', "warning")

        detections[name] = found

    return detections, 0

def log_detection(username, attack_type, input_name, input_text, score):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""INSERT INTO alerts (username, attack_type, endpoint, input_name, input_text, score)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (username, attack_type, request.path, input_name, input_text, score))
    conn.commit()
    conn.close()

# === Routes (Only detection part changed, rest same as your original) ===
@app.route("/")
def index():
    return redirect(url_for("login")) if "user_id" not in session else redirect(url_for("home"))

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username","")
        password = request.form.get("password","")
        detect_all_on_inputs({"username": username, "password": password})

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        row = cur.fetchone()
        conn.close()
        if row:
            session["user_id"] = row[0]
            session["username"] = row[1]
            session["role"] = row[5]
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        flash("Invalid credentials.", "error")
    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username","")
        password = request.form.get("password","")
        email = request.form.get("email","")
        bio = request.form.get("bio","")
        detect_all_on_inputs({"username":username, "password":password, "email":email, "bio":bio})

        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username,password,email,bio) VALUES (?,?,?,?)",
                    (username, password, email, bio))
        conn.commit()
        conn.close()
        flash("Registered successfully!", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/home", methods=["GET","POST"])
def home():
    if "user_id" not in session: return redirect(url_for("login"))

    search_result = ""
    ping_output = ""

    if "search" in request.args:
        q = request.args.get("search","")
        detect_all_on_inputs({"search": q})
        search_result = f"Search results for: {q}"

    if request.method == "POST" and "ip" in request.form:
        ip = request.form.get("ip","")
        detect_all_on_inputs({"ip": ip})
        if re.match(r"^[a-zA-Z0-9\.\-:]+$", ip):
            try:
                proc = subprocess.run(["ping", "-c", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=5)
                ping_output = proc.stdout
            except: ping_output = "Ping failed."

    return render_template("home.html", username=session.get("username"), search_result=search_result, ping_output=ping_output)

@app.route("/profile", methods=["GET","POST"])
def profile():
    if "user_id" not in session: return redirect(url_for("login"))

    uid = int(session["user_id"])
    rid = int(request.args.get("id", uid))

    if uid != rid and session.get("role") != "admin":
        flash("IDOR Detected!", "warning")
        log_detection(session["username"], "IDOR", "profile", f"id={rid}", 1.0)

    upload_message = ""
    if request.method == "POST" and "file" in request.files:
        f = request.files["file"]
        if f and f.filename:
            filename = os.path.basename(f.filename)
            detect_all_on_inputs({"filename": filename})
            safe_fn = re.sub(r"[^a-zA-Z0-9._-]", "_", filename)
            os.makedirs("uploads", exist_ok=True)
            f.save(os.path.join("uploads", safe_fn))
            upload_message = f"Uploaded: {safe_fn}"

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id=?", (rid,))
    row = cur.fetchone()
    conn.close()
    if not row:
        flash("User not found", "error")
        return redirect(url_for("home"))

    info = {"name": row[1], "email": row[3], "bio": row[4]}
    if rid == 313:
        info["idor_flag"] = "flag{IDOR_Found_1n_th3_m4tr1x}"

    return render_template("profile.html", profile_info=info, upload_message=upload_message)

@app.route("/admin/alerts")
def admin_alerts():
    if session.get("role") != "admin":
        flash("Admin only!", "error")
        return redirect(url_for("home"))
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT username, attack_type, endpoint, input_name, input_text, score, ts FROM alerts ORDER BY ts DESC")
    logs = cur.fetchall()
    conn.close()
    return render_template("alerts.html", logs=logs)

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    print("\nML-PROTECTED CTF APP READY!")
    print("SQLi → flag{SqL_inject10n_1s_fun}")
    print("XSS  → JavaScript alert with flag{XSS_1s_tr1cky_but_fun}")
    print("IDOR → /profile?id=313\n")
    app.run(debug=True, host="127.0.0.1", port=5000)