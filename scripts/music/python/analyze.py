from PIL import Image
from io import BytesIO
import os
import eyed3
import piexif

def analizar_jpeg_binario(imagen_bytes):
    def leer_segmentos(data):
        i = 0
        while i < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i+1]
            if marker == 0xD9:  # EOI
                print("🛑 Fin de imagen (EOI) encontrado")
                break
            elif marker == 0xD8:  # SOI
                print("🟢 Inicio de imagen (SOI)")
                i += 2
            elif 0xD0 <= marker <= 0xD7:  # RST markers (no length)
                print(f"🔸 Reinicio (RST{marker - 0xD0})")
                i += 2
            else:
                length = (data[i+2] << 8) + data[i+3]
                marker_name = f"APP{marker - 0xE0}" if 0xE0 <= marker <= 0xEF else f"Marker 0x{marker:02X}"
                print(f"🔹 {marker_name} - longitud: {length}")
                i += 2 + length

    print("🔍 Análisis binario JPEG:")
    leer_segmentos(imagen_bytes)

# Por cada mp3 de la carpeta actual, extrae las imágenes embebidas y las analiza
for file in os.listdir('.'):
    if not file.endswith('.mp3'):
        continue

    print(f"🔍 Procesando {file}...")
    # Cargar el archivo MP3
    audio = eyed3.load(file)
    if not audio.tag:
        print("❌ No hay etiqueta ID3 en el archivo.")
        exit()
    print("\n🧩 Otros frames:")
    otros_frames = [
        f for f in audio.tag.frame_set.items()
        if not f[0] in [
            b'TIT2', b'TPE1', b'TALB', b'TYER', b'COMM', b'APIC', b'TCON', b'TRCK', b'TPOS', b'TDAT', b'TORY', b'TSRC',
        b'TXXX', b'TMED', b'TPE2', b'TSO2', b'TSOP', b'UFID']
    ]

    if not otros_frames:
        print("  ✔️ No hay frames extraños.")
    else:
        for fid, frames in otros_frames:
            print(f"  ⚠️ Frame {fid}: {len(frames)} ocurrencia(s)")


        if not audio.tag or not audio.tag.images:
            print("❌ No se encontró ninguna imagen embebida.")
            exit()

    ## var dump de imágenes embebidas

    for img_frame in audio.tag.images:
        img_bytes = img_frame.image_data
        img_mime = img_frame.mime_type

        # Analizar con PIL
        with Image.open(BytesIO(img_bytes)) as img:
            print("✅ Imagen embebida encontrada:")
            print("-" * 40)
            print(f"Formato       : {img.format}")
            print(f"MIME          : {img_mime}")
            print(f"Resolución    : {img.size[0]}x{img.size[1]}")
            print(f"Modo de color : {img.mode}")
            print(f"Tamaño (KB)   : {len(img_bytes) / 1024:.2f} KB")
            print(f'Tipo de imagen : {img_frame.picture_type}')
            print(f"Descripción   : {img_frame.description if img_frame.description else 'N/A'}")
            print(f"ID de imagen  : {img_frame.id if img_frame.id else 'N/A'}")


            # Comprobar perfil ICC / EXIF
            icc_profile = img.info.get("icc_profile")
            if icc_profile:
                print("Perfil ICC        : ✅ Presente (podría causar problemas)")
            else:
                print("Perfil ICC        : ❌ No presente")

            # Revisar EXIF si es JPEG
            if img.format == "JPEG":
                try:
                    exif_dict = piexif.load(img_frame.image_data)
                    if exif_dict and any(exif_dict[tag] for tag in exif_dict):
                        print("Metadatos EXIF    : ✅ Presentes (podrían causar errores)")
                    else:
                        print("Metadatos EXIF    : ❌ Vacíos o no presentes")
                except Exception as e:
                    print(f"Metadatos EXIF    : ❌ No legibles ({e})")
            else:
                print("Metadatos EXIF    : N/A (no JPEG)")

            print("-" * 40)
            # print(f"🧪 Análisis avanzado:")
            # analizar_jpeg_binario(img_frame.image_data)