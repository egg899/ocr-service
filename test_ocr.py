from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import fitz  # PyMuPDF
import tempfile
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # ✅ permite peticiones desde otros dominios (React, Node, etc.)

@app.route('/ocr', methods=['POST'])
def ocr():
    try:
        logger.info("📩 Petición recibida en /ocr")

        # ✅ Verificar que se haya subido un archivo
        if 'file' not in request.files:
            logger.error("No se envió ningún archivo")
            return jsonify({'error': 'No se envió ningún archivo'}), 400

        file = request.files['file']

        # ✅ Guardar el archivo temporalmente
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
            file.save(temp.name)
            temp_path = temp.name

        logger.info(f"📄 Archivo guardado temporalmente en: {temp_path}")

        # ✅ Procesar el archivo PDF
        text = ""
        with fitz.Document(temp_path) as doc:
            logger.info(f"Documento abierto con {len(doc)} páginas")
            for page_num, page in enumerate(doc):
                logger.info(f"Procesando página {page_num + 1}")
                text += page.get_text()

        # ✅ Eliminar el archivo temporal
        os.remove(temp_path)
        logger.info("🗑️ Archivo temporal eliminado")

        # ✅ Enviar resultado
        logger.info(f"Texto extraído (longitud: {len(text)})")
        return jsonify({'texto': text})

    except Exception as e:
        logger.error(f"❌ Error en OCR: {str(e)}", exc_info=True)
        return jsonify({'error': 'Error al procesar el archivo', 'details': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))  # ✅ Render asigna el puerto
    logger.info(f"🚀 Iniciando servicio OCR en puerto {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
