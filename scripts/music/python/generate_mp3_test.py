import os
import io
import shutil
from PIL import Image
import eyed3

MP3_ORIGINAL = "Test.mp3"
SALIDA_DIR = "output"
RESOLUCIONES = [100, 128, 256, 300, 450, 480, 500, 600, 750, 800]
PESOS_KB = [10, 25, 50, 64, 75, 100, 128, 200, 300, 400, 500]

if not os.path.exists(SALIDA_DIR):
    os.makedirs(SALIDA_DIR)

def generar_imagen_bajo_limite(imagen, tamaño, peso_kb, formato):
    """
    Redimensiona la imagen a tamaño x tamaño y la guarda en bytes ajustando la calidad
    para que el tamaño esté justo por debajo de peso_kb (en KB).
    """
    imagen_red = imagen.copy()
    imagen_red.thumbnail((tamaño, tamaño), Image.LANCZOS)

    calidad_min = 10
    calidad_max = 95
    mejor_bytes = None

    # Función para guardar en buffer en el formato deseado
    def guardar_bytes(calidad):
        buf = io.BytesIO()
        if formato.lower() == "jpeg":
            imagen_red.save(buf, format="JPEG", quality=calidad)
        elif formato.lower() == "png":
            # Para PNG la compresión es diferente, no usamos calidad igual que JPEG
            # Pero Pillow acepta 'optimize' y 'compress_level'
            imagen_red.save(buf, format="PNG", optimize=True, compress_level=calidad//10)
        else:
            raise ValueError(f"Formato no soportado: {formato}")
        return buf.getvalue()

    # Búsqueda binaria para ajustar calidad y tamaño
    while calidad_min <= calidad_max:
        calidad_media = (calidad_min + calidad_max) // 2
        data = guardar_bytes(calidad_media)
        tamaño_kb = len(data) / 1024
        if tamaño_kb > peso_kb:
            calidad_max = calidad_media - 1
        else:
            mejor_bytes = data
            calidad_min = calidad_media + 1

    return mejor_bytes

def generar_combinaciones(mp3_base):
    total = 0
    print("\n💽 Generando combinaciones con JPEG y PNG...")

    audio_original = eyed3.load(mp3_base)
    if not audio_original or not audio_original.tag:
        print("❌ No se pudieron leer los metadatos del archivo original.")
        return

    imagen_original = None
    for img in audio_original.tag.images:
        if img.picture_type == eyed3.id3.frames.ImageFrame.FRONT_COVER:
            imagen_original = Image.open(io.BytesIO(img.image_data))
            break
    if imagen_original is None:
        print("❌ No se encontró portada FRONT_COVER en el archivo original.")
        return

    for formato in ["jpeg", "png"]:
        for res in RESOLUCIONES:
            for peso in PESOS_KB:
                portada_bytes = generar_imagen_bajo_limite(imagen_original, res, peso, formato)
                if portada_bytes is None:
                    print(f"❌ No se pudo generar imagen {res}x{res} ≤ {peso}KB formato {formato.upper()}")
                    continue

                actual_kb = len(portada_bytes) / 1024
                nombre = f"test_{formato}_{res}x{res}_{int(actual_kb)}kb"
                salida_mp3 = os.path.join(SALIDA_DIR, f"{nombre}.mp3")

                shutil.copy(mp3_base, salida_mp3)  # Copiar el MP3 original a la salida
                # Cargar original en memoria
                audio = eyed3.load(mp3_base)
                if audio.tag is None:
                    audio.initTag()

                tag = audio.tag
                # Copiar metadatos básicos

                # Modificar título y portada
                tag.title = nombre
                tag.images.set(
                    eyed3.id3.frames.ImageFrame.FRONT_COVER,
                    portada_bytes,
                    f"image/{formato}"
                )

                # Guardar nuevo archivo
                tag.save(salida_mp3, version=(2, 3, 0))

                tamaño_mp3_kb = os.path.getsize(salida_mp3) / 1024
                print(f"✅ {nombre}.mp3 → MP3: {tamaño_mp3_kb:.1f} KB | Portada: {actual_kb:.1f} KB")

                total += 1

    print(f"\n🎯 Total de archivos generados: {total}")

if __name__ == "__main__":
    generar_combinaciones(MP3_ORIGINAL)
