import os
import sys
import eyed3
from PIL import Image
import io

MAX_SIZE_KB = 100
MAX_DIMENSION = 500

def cumple_requisitos(img):
    if img.mime_type != "image/jpeg":
        return False
    if len(img.image_data) > MAX_SIZE_KB * 1024:
        return False
    try:
        with Image.open(io.BytesIO(img.image_data)) as im:
            w, h = im.size
            if w > MAX_DIMENSION or h > MAX_DIMENSION:
                return False
    except Exception as e:
        print(f"⚠️ Error al abrir imagen: {e}")
        return False
    return True



def convertir_portada(imagen_data):
    with Image.open(io.BytesIO(imagen_data)) as img:
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.thumbnail((MAX_DIMENSION, MAX_DIMENSION))

        calidad = 100
        while calidad > 30:
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=calidad)
            size = buffer.tell()
            if size <= MAX_SIZE_KB:
                break
            calidad -= 5

        if calidad <= 10:
            print(f"⚠️ No se pudo comprimir lo suficiente")

        return buffer.getvalue()

def procesar_mp3(file_path):
    audio = eyed3.load(file_path)
    if not audio or audio.tag is None:
        print(f"❌ {file_path}: sin metadatos.")
        return

    portada = None
    for img in audio.tag.images:
        if img.picture_type == eyed3.id3.frames.ImageFrame.FRONT_COVER:
            portada = img
            break

    if not portada:
        print(f"❌ {file_path}: sin portada.")
        return

    if cumple_requisitos(portada):
        return

    print(f"🔁 {file_path}: portada no compatible. Procesando...")
    nueva_portada = convertir_portada(portada.image_data)

    audio.tag.images.remove(portada.description)
    audio.tag.images.set(
        eyed3.id3.frames.ImageFrame.FRONT_COVER,
        nueva_portada,
        "image/jpeg",
        u"Cover"
    )
    audio.tag.version = (2, 3, 0)
    audio.tag.save(version=(2, 3, 0))
    print(f"✅ {file_path}: portada convertida y reemplazada.")

def main():
    if len(sys.argv) < 2:
        print("Uso: python procesar_portadas_mp3.py /ruta/a/la/carpeta")
        return

    carpeta = sys.argv[1]
    if not os.path.isdir(carpeta):
        print(f"❌ Ruta inválida: {carpeta}")
        return

    for archivo in os.listdir(carpeta):
        if archivo.lower().endswith(".mp3"):
            ruta_archivo = os.path.join(carpeta, archivo)
            try:
                procesar_mp3(ruta_archivo)
            except Exception as e:
                print(f"⚠️ Error procesando {archivo}: {e}")

if __name__ == "__main__":
    main()
