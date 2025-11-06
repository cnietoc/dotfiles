import eyed3
import shutil
import os

MP3_ORIGINAL = "original.mp3"
OUTPUT_DIR = "output_tags_separados"
os.makedirs(OUTPUT_DIR, exist_ok=True)

audio = eyed3.load(MP3_ORIGINAL)
if not audio.tag:
    print("El archivo no tiene etiquetas ID3.")
    exit()

frames = audio.tag.frame_set

frames_keys = list(frames.keys())
frames_imagen = [f for f in frames_keys if f.startswith(b"APIC")]
frames_otros = [f for f in frames_keys if not f.startswith(b"APIC")]


def guardar_con_frames(frame_list, filename, titulo):
    shutil.copyfile(MP3_ORIGINAL, filename)
    audio_mod = eyed3.load(filename)
    if not audio_mod.tag:
        audio_mod.initTag()
    # Borrar todos los frames
    for f in list(audio_mod.tag.frame_set.keys()):
        del audio_mod.tag.frame_set[f]
    # Añadir solo los frames indicados (copiarlos desde original)
    for f in frame_list:
        if f in frames:
            for frame in frames[f]:
                audio_mod.tag.frame_set[f] = frame
    # Actualizar título para identificar el caso
    for img_frame in audio_mod.tag.images:
        if img_frame.picture_type == eyed3.id3.frames.ImageFrame.FRONT_COVER:
            portada_bytes = img_frame.image_data
            mime_type = img_frame.mime_type

            # Eliminar todas las imágenes
            audio_mod.tag.images.remove(img_frame.description)

            # Insertar nuevamente sin descripción
            audio_mod.tag.images.set(
                eyed3.id3.frames.ImageFrame.FRONT_COVER,
                portada_bytes,
                mime_type
            )

            print(f"✅ Imagen portada reinsertada sin descripción")
        else:
            print("⚠️ No se encontró una imagen de tipo FRONT_COVER")

    audio_mod.tag.title = titulo
    audio_mod.tag.save(version=(2, 3, 0))
    print(f"Generado {filename} con frames: {[f.decode() for f in frame_list]} y título '{titulo}'")


# 1) Archivo con solo imagen(es)
if frames_imagen:
    out_img = os.path.join(OUTPUT_DIR, "solo_imagenes.mp3")
    guardar_con_frames(frames_imagen, out_img, "Solo imagen")
else:
    print("No hay frames de imagen en el archivo original.")

# 2) Archivos con solo un frame (no imagen) cada uno
for f in frames_otros:
    titulo = f"Solo {f.decode(errors='replace')}"
    out_f = os.path.join(OUTPUT_DIR, f"solo_{f.decode(errors='replace')}.mp3")
    guardar_con_frames([f] + frames_imagen, out_f, titulo)
