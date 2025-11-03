from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF
import docx2txt
import io

app = Flask(__name__)
CORS(app)

@app.route("/ocr", methods=["POST"])
def ocr():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No se envió ningún archivo"}), 400

        archivo = request.files['file']
        filename = archivo.filename.lower()

        texto = ""

        if filename.endswith(".pdf"):
            doc = fitz.open(stream=archivo.read(), filetype="pdf")
            for page in doc:
                texto += page.get_text()
        elif filename.endswith(".docx"):
            texto = docx2txt.process(io.BytesIO(archivo.read()))
        else:
            return jsonify({"error": "Formato no soportado. Solo PDF o DOCX"}), 400

        return jsonify({"texto": texto})

    except Exception as e:
        print("Error en OCR:", e)
        return jsonify({"error": "Error al procesar el archivo", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
