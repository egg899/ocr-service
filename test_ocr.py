# ocr_service.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF

app = Flask(__name__)
CORS(app)  # Permite solicitudes desde cualquier origen (frontend)

@app.route("/ocr", methods=["POST"])
def ocr():
    try:
        # Verificamos que haya un archivo en la request
        if 'file' not in request.files:
            return jsonify({"error": "No se envió ningún archivo"}), 400

        archivo = request.files['file']

        # Abrimos el PDF desde memoria
        doc = fitz.open(stream=archivo.read(), filetype="pdf")

        # Extraemos texto
        texto = ""
        for page in doc:
            texto += page.get_text()

        return jsonify({"texto": texto})

    except Exception as e:
        print("Error en OCR:", e)
        return jsonify({"error": "Error al procesar el PDF", "details": str(e)}), 500

if __name__ == "__main__":
    # Cambiá el puerto si Render te asigna otro
    app.run(host="0.0.0.0", port=5001)
