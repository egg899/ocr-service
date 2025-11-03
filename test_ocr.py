from flask import Flask, request, jsonify
import fitz  # PyMuPDF
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

def extraer_texto(file):
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    texto = ""
    for pagina in pdf:
        texto += pagina.get_text()
    return texto

@app.route("/ocr", methods=["POST"])
def ocr():
    logging.info("📥 Petición OCR recibida")

    if 'file' not in request.files:
        logging.error("❌ No se subió ningún archivo")
        return jsonify({"error": "No se subió ningún archivo"}), 400

    file = request.files['file']
    logging.info(f"Archivo recibido: {file.filename}, tamaño: {len(file.read())} bytes")
    file.seek(0)  # Volvemos al inicio del archivo para leerlo de nuevo

    try:
        texto = extraer_texto(file)
        logging.info(f"Texto extraído, {len(texto)} caracteres")
        return jsonify({"texto": texto})
    except Exception as e:
        logging.exception("❌ Error al procesar el PDF")
        return jsonify({"error": "Error al procesar el PDF", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
