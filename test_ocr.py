from flask import Flask, request, jsonify
import fitz  # PyMuPDF

app = Flask(__name__)

def extraer_texto(file):
    # Abrir el archivo PDF desde un objeto en memoria
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    texto = ""
    for pagina in pdf:
        texto += pagina.get_text()
    return texto

@app.route("/ocr", methods=["POST"])
def ocr():
    if 'file' not in request.files:
        return jsonify({"error": "No se subió ningún archivo"}), 400

    file = request.files['file']
    
    try:
        texto = extraer_texto(file)
        return jsonify({"texto": texto})
    except Exception as e:
        return jsonify({"error": "Error al procesar el PDF", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
