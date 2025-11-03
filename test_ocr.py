# ocr_service.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF
import docx2txt
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/ocr", methods=["POST"])
def ocr():
    try:
        # Verificar que venga un archivo
        if 'file' not in request.files:
            return jsonify({"error": "No se envió ningún archivo"}), 400

        archivo = request.files['file']
        filename = secure_filename(archivo.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        archivo.save(filepath)

        texto = ""

        # Detectar tipo de archivo
        if filename.lower().endswith(".pdf"):
            doc = fitz.open(filepath)
            for page in doc:
                texto += page.get_text()
        elif filename.lower().endswith(".docx"):
            texto = docx2txt.process(filepath)
        else:
            return jsonify({"error": "Formato no soportado"}), 400

        # Borrar archivo temporal
        os.remove(filepath)

        return jsonify({"texto": texto})

    except Exception as e:
        print("❌ Error en OCR:", e)
        return jsonify({"error": "Error al procesar el archivo", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
