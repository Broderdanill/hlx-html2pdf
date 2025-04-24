import os
import tempfile
import base64
import subprocess
import logging
from flask import Flask, request, jsonify

# Sätt upp loggning
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    logger.info("Mottog PDF-genereringsförfrågan")

    try:
        html_content = request.json.get("html", "")
        if not html_content:
            logger.warning("Ingen HTML hittades i begäran")
            return jsonify({"error": "Missing HTML content"}), 400

        with tempfile.TemporaryDirectory() as tmpdir:
            html_path = os.path.join(tmpdir, "input.html")
            pdf_path = os.path.join(tmpdir, "output.pdf")

            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            logger.debug(f"HTML skriven till: {html_path}")

            cmd = [
                "microsoft-edge",
                "--headless",
                "--disable-gpu",
                "--no-sandbox",
                f"--print-to-pdf={pdf_path}",
                f"file://{html_path}"
            ]

            logger.debug(f"Kör kommando: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True)

            if result.returncode != 0:
                logger.error(f"Edge-processen misslyckades: {result.stderr.decode()}")
                return jsonify({
                    "error": "Failed to generate PDF",
                    "stderr": result.stderr.decode()
                }), 500

            with open(pdf_path, "rb") as f:
                pdf_base64 = base64.b64encode(f.read()).decode("utf-8")

            logger.info("PDF genererad och kodad till Base64")
            return jsonify({"pdf_base64": pdf_base64})

    except Exception as e:
        logger.exception("Ett oväntat fel inträffade")
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    logger.debug("Hälsokontrollsförfrågan mottagen")
    return "PDF Generator is up!", 200

if __name__ == "__main__":
    logger.info(f"Startar server med loggnivå: {LOG_LEVEL}")
    app.run(host="0.0.0.0", port=8080)
