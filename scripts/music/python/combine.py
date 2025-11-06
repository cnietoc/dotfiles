import eyed3
import shutil
import os

# Entradas
MP3_1 = "original.mp3"
MP3_2 = "Test.mp3"

# Salidas
MP3_1_WITH_PORTADA2 = "original_portada_ok.mp3"
MP3_2_WITH_PORTADA1 = "Test_portada_ko.mp3"

def extraer_portada(mp3_path):
    audio = eyed3.load(mp3_path)
    if not audio.tag:
        return None
    return next(
        (img for img in audio.tag.images if img.picture_type == eyed3.id3.frames.ImageFrame.FRONT_COVER),
        None
    )

def combinar(audio_path, portada_img, salida_path):
    # Copiar base
    shutil.copyfile(audio_path, salida_path)
    audio_final = eyed3.load(salida_path)
    if not audio_final.tag:
        audio_final.initTag()

    # Eliminar imágenes previas
    for image in list(audio_final.tag.images):  # Hacemos una copia con list() para evitar problemas al modificar durante la iteración
        audio_final.tag.images.remove(image.description)

    # Pone el nombre descriptivo como titulo
    audio_final.tag.title = os.path.basename(salida_path).replace(".mp3", "")
    # Insertar imagen nueva sin descripción
    audio_final.tag.images.set(
        eyed3.id3.frames.ImageFrame.FRONT_COVER,
        portada_img.image_data,
        portada_img.mime_type
    )

    audio_final.tag.save(version=(2, 3, 0))
    print(f"✅ Generado: {salida_path}")

# Extraer portadas
portada1 = extraer_portada(MP3_1)
portada2 = extraer_portada(MP3_2)

if not portada1 or not portada2:
    print("❌ No se pudieron extraer ambas portadas")
else:
    combinar(MP3_1, portada2, MP3_1_WITH_PORTADA2)
    combinar(MP3_2, portada1, MP3_2_WITH_PORTADA1)
