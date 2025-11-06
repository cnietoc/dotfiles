import eyed3
import shutil
import os

# Archivo original
MP3_ORIGINAL = "original.mp3"

# Frames a eliminar uno por uno
frames_a_eliminar = [b"TDRC", b"POPM", b"TSSE", b"TENC", b"WOAS", b"TCOP", b"USLT"]

# Carpeta salida
OUTPUT_DIR = "output_sin_frames"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def eliminar_frames(input_file, frames_to_remove, output_file):
    shutil.copyfile(input_file, output_file)
    audio = eyed3.load(output_file)
    if not audio.tag:
        audio.initTag()
    for frame_id in frames_to_remove:
        if frame_id in audio.tag.frame_set:
            del audio.tag.frame_set[frame_id]
    audio.tag.title= os.path.basename(output_file).replace(".mp3", "")
    audio.tag.save(version=(2, 3, 0))
    print(f"Generado {output_file} sin frames: {[f.decode() for f in frames_to_remove]}")

# 1. Generar archivos eliminando un frame cada vez
for frame in frames_a_eliminar:
    salida = os.path.join(OUTPUT_DIR, f"sin_{frame.decode()}.mp3")
    eliminar_frames(MP3_ORIGINAL, [frame], salida)

# 2. Generar archivo eliminando todos los frames listados
salida_todos = os.path.join(OUTPUT_DIR, "sin_todos_los_frames.mp3")
eliminar_frames(MP3_ORIGINAL, frames_a_eliminar, salida_todos)
