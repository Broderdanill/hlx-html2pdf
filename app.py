import os
import tempfile
import base64
import subprocess
import logging
from flask import Flask, request, jsonify

# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    logger.info("Received PDF generation request")

    try:
        html_content = request.json.get("html", "")
        if not html_content:
            logger.warning("No HTML content found in the request")
            return jsonify({"error": "Missing HTML content"}), 400

        # Create temporary HTML and PDF files
        with tempfile.TemporaryDirectory() as tmpdir:
            html_path = os.path.join(tmpdir, "input.html")
            pdf_path = os.path.join(tmpdir, "output.pdf")

            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            logger.debug(f"HTML written to: {html_path}")

            # Run Microsoft Edge in headless mode
            cmd = [
                "microsoft-edge",
                "--headless",
                "--disable-gpu",
                "--no-sandbox",
                f"--print-to-pdf={pdf_path}",
                f"file://{html_path}"
            ]

            logger.debug(f"Executing command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True)

            if result.returncode != 0:
                logger.error(f"Edge process failed: {result.stderr.decode()}")
                return jsonify({
                    "error": "Failed to generate PDF",
                    "stderr": result.stderr.decode()
                }), 500

            # Read PDF file and encode it in Base64
            with open(pdf_path, "rb") as f:
                pdf_base64 = base64.b64encode(f.read()).decode("utf-8")

            logger.info("PDF successfully generated and encoded to Base64")
            return jsonify({"pdf_base64": pdf_base64})

    except Exception as e:
        logger.exception("Unexpected error occurred during PDF generation")
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    logger.debug("Health check request received")
    return "PDF Generator is up!", 200

if __name__ == "__main__":
    logger.info(f"Starting server with log level: {LOG_LEVEL}")
    app.run(host="0.0.0.0", port=8080)
