import requests
import os

def test_ocr_service():
    # Ruta de prueba con un archivo que sabemos que existe
    test_file_path = r"C:\Users\Admin\Desktop\prueba31\potentAI\api\uploads\cvs\856ffe10f4c9b8ba69fb101624fa704f"
    
    print(f"Probando con archivo: {test_file_path}")
    print(f"Archivo existe: {os.path.exists(test_file_path)}")
    
    try:
        response = requests.post('http://localhost:5001/ocr', 
                               json={'pdf_path': test_file_path},
                               timeout=30)
        
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Texto extraído (primeros 200 caracteres): {data.get('texto', '')[:200]}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Error en la petición: {e}")

if __name__ == "__main__":
    test_ocr_service() 