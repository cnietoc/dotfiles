import eyed3
import shutil
import os

RUTA_ORIGINAL = "solo_imagenes.mp3"
RUTA_NUEVO = "solo2.mp3"

# Copiar el archivo original a uno nuevo
shutil.copyfile(RUTA_ORIGINAL, RUTA_NUEVO)

# Cargar el archivo nuevo
audio = eyed3.load(RUTA_NUEVO)
if not audio.tag:
    audio.initTag()

# Buscar la portada existente
for img_frame in audio.tag.images:
    if img_frame.picture_type == eyed3.id3.frames.ImageFrame.FRONT_COVER:
        portada_bytes = img_frame.image_data
        mime_type = img_frame.mime_type

        # Eliminar todas las imágenes
        audio.tag.images.remove(img_frame.description)

        # Insertar nuevamente sin descripción
        audio.tag.images.set(
            eyed3.id3.frames.ImageFrame.FRONT_COVER,
            portada_bytes,
            mime_type
        )

        print(f"✅ Imagen portada reinsertada sin descripción en: {RUTA_NUEVO}")
        break
else:
    print("⚠️ No se encontró una imagen de tipo FRONT_COVER")

# Guardar el nuevo archivo
audio.tag.save(version=(2, 3, 0))
