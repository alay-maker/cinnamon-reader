import os
import re
import unicodedata

# --- CONFIGURACIÓN DE RUTAS ---
# Subimos un nivel desde la carpeta 'src' para llegar a la raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')

def ensure_directories():
    """Crea las carpetas de datos si no existen."""
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)

def remove_diacritics(text):
    """
    Descompone los caracteres Unicode para separar la letra base de sus acentos.
    Ejemplo: 'ά' se convierte en 'α' + '´'. Luego eliminamos los acentos.
    """
    # NFD separa las letras de sus marcas diacríticas
    normalized = unicodedata.normalize('NFD', text)
    # Filtramos para quedarnos solo con lo que no es una marca ('Mn' = Mark, Nonspacing)
    cleaned = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
    return cleaned

def clean_to_scriptio_continua(text):
    """
    Transforma el texto griego al formato del papiro original de Herculano.
    """
    # 1. Quitar acentos y espíritus
    text = remove_diacritics(text)
    
    # 2. Convertir todo a mayúsculas
    text = text.upper()
    
    # 3. Usar Regex para eliminar todo lo que NO sea una letra griega mayúscula.
    # El rango Unicode [\u0391-\u03A9] cubre de la Alfa (Α) a la Omega (Ω).
    text = re.sub(r'[^Α-Ω]', '', text)
    
    return text

def create_sample_text():
    """Genera un texto de prueba si no tienes nada descargado."""
    filepath = os.path.join(RAW_DIR, 'epicurus_sample.txt')
    if not os.path.exists(filepath):
        # Fragmento de Epicuro con acentos, espacios y puntuación
        sample_greek = """
        τὸ φρικωδέστατον οὖν τῶν κακῶν ὁ θάνατος οὐθὲν πρὸς ἡμᾶς, 
        ἐπειδήπερ ὅταν μὲν ἡμεῖς ὦμεν, ὁ θάνατος οὐ πάρεστιν, 
        ὅταν δὲ ὁ θάνατος παρῇ, τόθ' ἡμεῖς οὐκ ἐσμέν.
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(sample_greek)
        print(f"[*] Archivo de prueba creado en: {filepath}")
    return filepath

def main():
    print("Iniciando Cinnamon Data Cleaner...")
    ensure_directories()
    
    # Aseguramos que haya un archivo para procesar
    input_file = create_sample_text()
    output_file = os.path.join(PROCESSED_DIR, 'corpus_limpio.txt')
    
    # Leemos el archivo crudo
    with open(input_file, 'r', encoding='utf-8') as f:
        raw_text = f.read()
        
    print(f"[*] Texto original cargado ({len(raw_text)} caracteres).")
    
    # Limpiamos los datos
    cleaned_text = clean_to_scriptio_continua(raw_text)
    
    # Guardamos el muro de texto
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)
        
    print(f"[*] Limpieza completada con éxito.")
    print(f"[*] Texto procesado guardado en: {output_file} ({len(cleaned_text)} caracteres).")
    
    # Mostramos un fragmento para comprobar visualmente
    print("\n--- VISUALIZACIÓN DEL SCRIPTIO CONTINUA ---")
    print(cleaned_text[:100] + "...")
    print("-------------------------------------------\n")

if __name__ == "__main__":
    main()
