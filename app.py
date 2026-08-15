import json
import os
import socket
from pathlib import Path

import torch
import torch.nn as nn
from flask import Flask, jsonify, render_template, request
from transformers import AutoTokenizer, DistilBertModel

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["JSON_SORT_KEYS"] = False

BASE_DIR = Path(__file__).resolve().parent


def find_existing_path(*relative_parts):
    for candidate in [BASE_DIR.joinpath(*relative_parts), BASE_DIR.joinpath("models", *relative_parts)]:
        if candidate.exists():
            return candidate
    return BASE_DIR.joinpath(*relative_parts)


MODEL_DIR = find_existing_path("model")
TOKENIZER_DIR = find_existing_path("tokenizer")
MODEL_STATE_PATH = find_existing_path("model_state_dict.pth")
LABELS_PATH = find_existing_path("labels.json")

if not MODEL_STATE_PATH.exists():
    raise FileNotFoundError("Model weights file not found. Expected model_state_dict.pth in the project root or models folder.")
if not TOKENIZER_DIR.exists():
    raise FileNotFoundError("Tokenizer directory not found. Expected a tokenizer folder in the project root or models folder.")
if not LABELS_PATH.exists():
    raise FileNotFoundError("Labels file not found. Expected labels.json in the project root or models folder.")


class ToxicCommentClassifier(nn.Module):
    """Custom multi-label classifier built on top of DistilBERT."""

    def __init__(self):
        super().__init__()
        self.bert = DistilBertModel.from_pretrained("distilbert-base-uncased")
        self.dropout = nn.Dropout(0.3)
        self.classifier = nn.Linear(self.bert.config.hidden_size, 4)

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        hidden_state = outputs.last_hidden_state
        cls_output = hidden_state[:, 0]
        cls_output = self.dropout(cls_output)
        logits = self.classifier(cls_output)
        return logits


def load_labels(path):
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if isinstance(payload, dict):
        labels = payload.get("labels") or payload.get("class_labels") or []
    elif isinstance(payload, list):
        labels = payload
    else:
        labels = []

    return labels if isinstance(labels, list) else []


DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
TOKENIZER = AutoTokenizer.from_pretrained(str(TOKENIZER_DIR), local_files_only=True)
MODEL = ToxicCommentClassifier().to(DEVICE)
MODEL.eval()

LABELS = load_labels(LABELS_PATH)
LABEL_DISPLAY_NAMES = {
    "toxic": "Toxic",
    "severe_toxic": "Severe Toxic",
    "hate_speech": "Hate Speech",
    "offensive": "Offensive",
}


def load_model_weights():
    checkpoint = torch.load(MODEL_STATE_PATH, map_location=DEVICE)

    if isinstance(checkpoint, dict):
        if "state_dict" in checkpoint:
            checkpoint = checkpoint["state_dict"]
        elif "model_state_dict" in checkpoint:
            checkpoint = checkpoint["model_state_dict"]

    if not isinstance(checkpoint, dict):
        raise TypeError("The model checkpoint is not a dictionary and could not be loaded.")

    cleaned_state_dict = {}
    for key, value in checkpoint.items():
        cleaned_key = key.replace("module.", "").replace("model.", "")
        cleaned_state_dict[cleaned_key] = value

    incompatible = MODEL.load_state_dict(cleaned_state_dict, strict=False)
    if incompatible.missing_keys or incompatible.unexpected_keys:
        print(f"Loaded model with missing keys: {incompatible.missing_keys}")
        print(f"Loaded model with unexpected keys: {incompatible.unexpected_keys}")


load_model_weights()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json(silent=True) or {}
    text = (payload.get("text") or "").strip()

    if not text:
        return jsonify({"error": "Please enter a comment before scanning."}), 400

    inputs = TOKENIZER(
        text,
        max_length=128,
        padding="max_length",
        truncation=True,
        return_tensors="pt",
    )

    input_ids = inputs["input_ids"].to(DEVICE)
    attention_mask = inputs["attention_mask"].to(DEVICE)

    with torch.inference_mode():
        logits = MODEL(input_ids=input_ids, attention_mask=attention_mask)
        probabilities = torch.sigmoid(logits).squeeze(0).cpu().tolist()

    if len(LABELS) != len(probabilities):
        return jsonify({"error": "Model output shape does not match the expected label count."}), 500

    results = {}
    for label, probability in zip(LABELS, probabilities):
        display_name = LABEL_DISPLAY_NAMES.get(label, label.replace("_", " ").title())
        results[display_name] = round(probability * 100, 2)

    return jsonify(results)


def find_available_port(start_port=5000, max_attempts=20):
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(("0.0.0.0", port))
                return port
            except OSError:
                continue
    raise RuntimeError("No available port found for Flask server.")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", find_available_port()))
    app.run(host="0.0.0.0", port=port, debug=False)
