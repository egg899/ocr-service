from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF
import docx2txt
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# CORS abierto (para permitir llamadas desde tu frontend)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Carpeta temporal para subir archivos
UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/ocr", methods=["POST"])
def ocr():
    try:
        # Verificar que venga un archivo
        if "file" not in request.files:
            return jsonify({"error": "No se envió ningún archivo"}), 400

        archivo = request.files["file"]
        filename = secure_filename(archivo.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        archivo.save(filepath)

        texto = ""

        # Detectar tipo de archivo
        if filename.lower().endswith(".pdf"):
            doc = fitz.open(filepath)
            for page in doc:
                texto += page.get_text()
            doc.close()
        elif filename.lower().endswith(".docx"):
            texto = docx2txt.process(filepath)
        else:
            os.remove(filepath)
            return jsonify({"error": "Formato no soportado"}), 400

        # Borrar archivo temporal
        os.remove(filepath)

        return jsonify({"texto": texto})

    except Exception as e:
        print("❌ Error en OCR:", e)
        return jsonify(
            {"error": "Error al procesar el archivo", "details": str(e)}
        ), 500


if __name__ == "__main__":
    # Render usa el puerto de la variable de entorno PORT
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
