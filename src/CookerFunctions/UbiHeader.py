import struct, os, subprocess
from PIL import Image

def has_transparency(image_path, binary_path="bin"):
    completed_process = subprocess.Popen(
        f'''{binary_path}\\magick.exe identify -format '%[channels]' "{image_path}"''',
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        shell=True,
        text=True
    )

    stdout_output, stderr_output = completed_process.communicate()

    if completed_process.returncode == 0:
        output = stdout_output
    else:
        output = stderr_output

    if "srgba" in output:
        return True
    elif "srgb" in output and "srgba" not in output:
        return False
    elif "rgba" in output:
        return True
    elif "rgb" in output and "rgba" not in output:
        return False
    elif "p" in output:
        return True

class UbiartHeader:
    def create_header(image, hasSSD=False, imageEncoded=None, isXPR=False):
        os.getcwd()
        if isXPR:
            fileStream = open(imageEncoded, "rb")
        else:
            fileStream = open(image, "rb")
        imageStream = Image.open(image)
        alpha = has_transparency(image)
        width, height = imageStream.size
        header = b''

        header += b'\x00\x00\x00\x09' # Version
        header += b'TEX\x00' # Magic
        header += b'\x00\x00\x00\x2C' # Offset Flags
        if isXPR:
            header += (os.path.getsize(imageEncoded)).to_bytes(3, "big") # Image Size
        else:
            header += b'\x00\x40\x00'
        header += b'\x80' # ???
        header += struct.pack(">HH", width, height)

        if alpha:
            header += b'\x00\x01\x18\x00'
        else:
            header += b'\x00\x01\x20\x00'

        fileStream.seek(0)
        if isXPR:
            header += (os.path.getsize(imageEncoded)).to_bytes(3, "big") # Image Size
        else:
            header += b'\x00\x40\x00'
        header += b'\x80' # ???
        header += b'\x00\x00\x00\x00'
        header += b'\x00\x04\x00\x00'
        header += b'\x00\x00\x00\x00'
        header += b'\x00\x00\x00\x00'

        fileStream.close()
        imageStream.close()

        if hasSSD:
            fileStream = open(imageEncoded, "rb")
            imageStream = Image.open(image)
            fileStream.seek(0x14)
            width, height = struct.unpack(">HH", fileStream.read(4), fileStream.read(4))

            header += b' SSD'
            header += b'\x00\x00\x00\x7C'
            header += b'\x00\x08\x10\x07'
            header += struct.pack(">II", height, width)
            header += b'\x00\x00\x08\x00'
            header += b'\x00\x00\x00\x00'
            header += b'\x00\x00\x00\x00'
            header += b'\x00\x00\x00\x00'
            header += b'\x00\x00\x00\x00'
            header += b'\x00\x00\x00\x00'
            header += b'\x00\x00\x00\x00'
            header += b'\x00\x00\x00\x00'
            header += b'\x00\x00\x00\x00'
            header += b'\x00\x00\x00\x00'
            header += b'\x00\x00\x00\x00'
            header += b'\x00\x00\x00\x00'
            header += b'TTVN'
            header += b'\x00\x02\x00\x07'
            header += b'\x00\x00\x00\x20'
            header += b'\x00\x00\x00\x04'

            if alpha:
                header += b'APMC'
            else:
                header += b'1TXD'
                
            header += b'\x00\x00\x00\x00'
            header += b'\x00\x00\x00\x00'
            header += b'\x00\x00\x00\x00'
            header += b'\x00\x00\x00\x00'
            header += b'\x00\x00\x00\x00'
            header += b'\x00\x00\x10\x00'
            header += b'\x00\x00\x00\x00'
            header += b'\x00\x00\x00\x00'
            header += b'\x00\x00\x00\x00'
            header += b'\x00\x00\x00\x00'

        return header
    