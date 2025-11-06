import eyed3
import sys

def get_apic_raw_bytes(audio):
    """
    Extrae los bytes crudos del frame APIC (imagen) del tag ID3.
    Ojo: eyed3 no expone directamente los bytes completos del frame,
    así que vamos a leer el tag ID3 directamente del fichero.
    """
    # Cargamos tag raw desde el archivo
    with open(audio.path, "rb") as f:
        raw_data = f.read()

    # Buscamos la posición del tag ID3v2 al inicio
    if not raw_data.startswith(b"ID3"):
        print(f"No se encontró tag ID3 en {audio.path}")
        return None

    # Tamaño del tag ID3 (bytes 6 a 9), syncsafe integer de 4 bytes
    size_bytes = raw_data[6:10]
    size = (
            (size_bytes[0] & 0x7F) << 21
            | (size_bytes[1] & 0x7F) << 14
            | (size_bytes[2] & 0x7F) << 7
            | (size_bytes[3] & 0x7F)
    )
    tag_end = 10 + size

    tag_data = raw_data[:tag_end]

    # Buscamos el frame APIC (identificado por b'APIC')
    # El ID3v2.3/2.4 los frames empiezan justo después del header de 10 bytes
    pos = 10
    while pos < tag_end:
        frame_id = tag_data[pos:pos+4]
        if frame_id == b'\x00\x00\x00\x00' or frame_id == b'':
            break
        frame_size_bytes = tag_data[pos+4:pos+8]
        # En ID3v2.4 el tamaño es syncsafe, en 2.3 no
        # Aquí asumimos ID3v2.3 (entero normal)
        frame_size = int.from_bytes(frame_size_bytes, byteorder='big')
        frame_flags = tag_data[pos+8:pos+10]

        frame_data = tag_data[pos:pos+10+frame_size]

        if frame_id == b'APIC':
            return frame_data

        pos += 10 + frame_size

    print("No se encontró frame APIC en el tag.")
    return None

def comparar_bytes(b1, b2):
    min_len = min(len(b1), len(b2))
    diff_bytes = sum(1 for i in range(min_len) if b1[i] != b2[i])
    diff_bytes += abs(len(b1) - len(b2))
    return diff_bytes

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python comparar_apic_raw.py archivo1.mp3 archivo2.mp3")
        sys.exit(1)

    file1, file2 = sys.argv[1], sys.argv[2]

    audio1 = eyed3.load(file1)
    audio2 = eyed3.load(file2)

    apic1 = get_apic_raw_bytes(audio1)
    apic2 = get_apic_raw_bytes(audio2)

    if apic1 is None or apic2 is None:
        print("No se pudo extraer el frame APIC de uno o ambos archivos.")
        sys.exit(1)

    print(f"APIC tamaño archivo1: {len(apic1)} bytes")
    print(f"APIC tamaño archivo2: {len(apic2)} bytes")

    if apic1 == apic2:
        print("Los frames APIC son idénticos byte a byte.")
    else:
        diff = comparar_bytes(apic1, apic2)
        print(f"Diferencias en frame APIC: {diff} bytes")

        # Opcional: mostrar primeros bytes distintos (hasta 64 bytes)
        max_show = 64
        print("Diferencias byte a byte (posición: archivo1 vs archivo2):")
        for i in range(min(len(apic1), len(apic2), max_show)):
            if apic1[i] != apic2[i]:
                print(f"  {i}: {apic1[i]:02X} vs {apic2[i]:02X}")
