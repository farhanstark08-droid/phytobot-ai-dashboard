from flask import Flask, request, jsonify, render_template, send_from_directory
from datetime import datetime, timezone
from pathlib import Path
import sqlite3, os, json, uuid
from model_training.disease_treatements import get_treatment

try:
    import numpy as np
    from PIL import Image
except Exception:
    np = None
    Image = None

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"
IMAGE_DIR = DATA_DIR / "images"
DB_PATH = DATA_DIR / "agribot.db"
MODEL_PATH = APP_DIR / "models" / "leaf_disease_model.keras"
LABELS_PATH = APP_DIR / "models" / "labels.json"
DATA_DIR.mkdir(exist_ok=True)
IMAGE_DIR.mkdir(parents=True, exist_ok=True)
(MODEL_PATH.parent).mkdir(exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024
_model = None
_model_error = None

def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")

def db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with db() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT,
            temperature REAL, humidity REAL, soil_moisture REAL,
            latitude REAL, longitude REAL, satellites INTEGER,
            ir_left INTEGER, ir_center INTEGER, ir_right INTEGER,
            obstacle INTEGER, battery REAL
        )""")
        con.execute("""CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT,
            image_name TEXT, result TEXT, confidence REAL, note TEXT
        )""")
init_db()

def load_model():
    global _model, _model_error
    if _model is not None:
        return _model
    if _model_error:
        return None
    if not MODEL_PATH.exists():
        _model_error = "No trained model found. Add models/leaf_disease_model.keras."
        return None
    try:
        from tensorflow.keras.models import load_model as keras_load
        _model = keras_load(str(MODEL_PATH))
        return _model
    except Exception as e:
        _model_error = str(e)
        return None
def classify_image(path):
    model = load_model()

    if model is None or np is None or Image is None:
        return "AI model not configured", None, _model_error or "AI dependencies missing"

    try:
        labels = json.loads(
            LABELS_PATH.read_text(encoding="utf-8")
        )

        img = Image.open(path).convert("RGB").resize((224, 224))
        arr = np.asarray(img, dtype="float32")

        arr = np.expand_dims(arr, axis=0)

        pred = model.predict(arr, verbose=0)[0]

        idx = int(np.argmax(pred))
        disease = labels[idx]
        confidence = round(float(pred[idx]) * 100, 2)

        treatment = get_treatment(disease)

        result = {
            "disease": disease,
            "status": treatment["status"],
            "symptoms": treatment["symptoms"],
            "treatment": treatment["treatment"],
            "prevention": treatment["prevention"]
        }

        return json.dumps(result, ensure_ascii=False), confidence, "PhytoBot AI automatic analysis"

    except Exception as e:
        return "Analysis error", None, str(e)

def index():
    return render_template("index.html")

@app.route("/api/telemetry", methods=["POST"])
def telemetry():
    payload = request.get_json(silent=True) or {}
    ts = now_iso()
    def val(k, cast=float):
        v = payload.get(k)
        if v in (None, ""): return None
        try: return cast(v)
        except (ValueError, TypeError): return None
    fields = ["temperature","humidity","soil_moisture","latitude","longitude","satellites",
              "ir_left","ir_center","ir_right","obstacle","battery"]
    values = [ts] + [val(k, int if k in ("satellites","ir_left","ir_center","ir_right","obstacle") else float) for k in fields]
    with db() as con:
        con.execute("""INSERT INTO telemetry (timestamp, temperature, humidity, soil_moisture,
            latitude, longitude, satellites, ir_left, ir_center, ir_right, obstacle, battery)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", values)
    return jsonify(ok=True, received_at=ts)

@app.route("/api/frame", methods=["POST"])
def frame():
    # ESP32-CAM sends raw JPEG bytes with Content-Type: image/jpeg.
    raw = request.get_data()
    if not raw and "image" in request.files:
        raw = request.files["image"].read()
    if not raw:
        return jsonify(ok=False, error="No image bytes received"), 400
    if len(raw) > 8 * 1024 * 1024:
        return jsonify(ok=False, error="Image too large"), 413
    name = datetime.now().strftime("%Y%m%d_%H%M%S_") + uuid.uuid4().hex[:6] + ".jpg"
    path = IMAGE_DIR / name
    path.write_bytes(raw)
    result, confidence, note = classify_image(path)
    ts = now_iso()
    with db() as con:
        con.execute("INSERT INTO scans (timestamp,image_name,result,confidence,note) VALUES (?,?,?,?,?)",
                    (ts, name, result, confidence, note))
    return jsonify(ok=True, image=name, result=result, confidence=confidence, note=note, timestamp=ts)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/api/status")
def status():
    with db() as con:
        t = con.execute("SELECT * FROM telemetry ORDER BY id DESC LIMIT 1").fetchone()
        s = con.execute("SELECT * FROM scans ORDER BY id DESC LIMIT 1").fetchone()
        history = con.execute("SELECT timestamp, temperature, humidity, soil_moisture FROM telemetry ORDER BY id DESC LIMIT 20").fetchall()
    return jsonify(
        telemetry=dict(t) if t else None,
        scan=dict(s) if s else None,
        history=[dict(x) for x in reversed(history)],
        server_time=now_iso(),
        ai_ready=MODEL_PATH.exists(),
        ai_message=_model_error if _model_error else ("Model file detected" if MODEL_PATH.exists() else "Add a trained CNN model to enable disease predictions")
    )

@app.route("/images/<path:name>")
def images(name):
    return send_from_directory(IMAGE_DIR, name)

@app.route("/health")
def health():
    return jsonify(ok=True, service="AgriBot dashboard")

if __name__ == "__main__":
    # Accessible to devices on the same Wi-Fi network.
    app.run(host="0.0.0.0", port=5000, debug=True)
