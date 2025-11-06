import eyed3
import sys


def comparar_bytes(b1, b2):
    """Compara dos bytes y cuenta diferencias."""
    min_len = min(len(b1), len(b2))
    diff_bytes = sum(1 for i in range(min_len) if b1[i] != b2[i])
    diff_bytes += abs(len(b1) - len(b2))
    return diff_bytes

def comparar_frames(frame1, frame2):
    """Compara dos frames y devuelve lista de diferencias (vacía si iguales)."""
    diffs = []

    # Comparamos tipo de frame
    if type(frame1) != type(frame2):
        diffs.append(f"Tipos diferentes: {type(frame1)} vs {type(frame2)}")
        return diffs

    # Si es frame de imagen (APIC)
    if frame1.__class__.__name__ == "ImageFrame":
        if frame1.mime_type != frame2.mime_type:
            diffs.append(f"mime_type: {frame1.mime_type} != {frame2.mime_type}")
        if frame1.picture_type != frame2.picture_type:
            diffs.append(f"picture_type: {frame1.picture_type} != {frame2.picture_type}")
        if (frame1.description or "") != (frame2.description or ""):
            diffs.append(f"description: '{frame1.description}' != '{frame2.description}'")
        if frame1.image_data != frame2.image_data:
            diffs.append(f"image_data size: {len(frame1.image_data)} bytes != {len(frame2.image_data)} bytes")
        if frame1.image_data != frame2.image_data:
            size1 = len(frame1.image_data)
            size2 = len(frame2.image_data)
            diffs.append(f"image_data tamaño: {size1} bytes != {size2} bytes")
            diff_bytes = comparar_bytes(frame1.image_data, frame2.image_data)
            diffs.append(f"Diferencias en bytes de imagen: {diff_bytes} bytes")

    else:
        # Para frames texto u otros, comparamos su texto
        # Algunos frames pueden tener atributo 'text' o 'text' es lista
        attr_text_1 = getattr(frame1, "text", None)
        attr_text_2 = getattr(frame2, "text", None)
        if attr_text_1 != attr_text_2:
            diffs.append(f"text: {attr_text_1} != {attr_text_2}")

    return diffs

def comparar_tags(file1, file2):
    audio1 = eyed3.load(file1)
    audio2 = eyed3.load(file2)

    if not audio1.tag or not audio2.tag:
        print("Uno o ambos archivos no tienen tags ID3.")
        return

    tags1 = audio1.tag.frame_set
    tags2 = audio2.tag.frame_set

    keys1 = set(tags1.keys())
    keys2 = set(tags2.keys())

    todas_claves = keys1.union(keys2)

    for clave in todas_claves:
        frames_1 = tags1.get(clave, [])
        frames_2 = tags2.get(clave, [])

        if not frames_1:
            print(f"Frame {clave.decode(errors='replace')} solo en archivo 2.")
            continue
        if not frames_2:
            print(f"Frame {clave.decode(errors='replace')} solo en archivo 1.")
            continue

        # Comparamos número de frames
        if len(frames_1) != len(frames_2):
            print(f"Frame {clave.decode(errors='replace')}: diferente número de ocurrencias {len(frames_1)} vs {len(frames_2)}")

        # Comparamos cada frame uno a uno (hasta el mínimo)
        for i, (f1, f2) in enumerate(zip(frames_1, frames_2)):
            diffs = comparar_frames(f1, f2)
            if diffs:
                print(f"Diferencias en frame {clave.decode(errors='replace')} instancia {i+1}:")
                for d in diffs:
                    print(f"  - {d}")
                print()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python comparar_tags_detallado.py archivo1.mp3 archivo2.mp3")
    else:
        comparar_tags(sys.argv[1], sys.argv[2])
