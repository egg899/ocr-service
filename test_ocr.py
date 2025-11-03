from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # permite peticiones desde cualquier origen

@app.route('/ocr', methods=['POST'])
def ocr():
    try:
        logger.info("Recibida petición OCR")

        # Revisamos si llegó un archivo
        if 'file' not in request.files:
            return jsonify({'error': 'No se subió ningún archivo'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nombre de archivo inválido'}), 400

        logger.info(f"Procesando archivo: {file.filename}")

        # Abrimos el PDF directamente desde el objeto FileStorage
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()

        logger.info(f"Texto extraído, longitud: {len(text)}")
        return jsonify({'texto': text})

    except Exception as e:
        logger.error(f"Error en OCR: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5001))
    logger.info(f"Iniciando servicio OCR en puerto {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
