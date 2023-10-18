import struct, os, subprocess
from ..Utils import *
from PIL import Image

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
            header += (os.path.getsize(imageEncoded)).to_bytes(4, "big") # Image Size
        else:
            header += b'\x00\x40\x00\x80'
        header += struct.pack(">HH", width, height)

        if alpha:
            header += b'\x00\x01\x18\x00'
        else:
            header += b'\x00\x01\x20\x00'

        fileStream.seek(0)
        if isXPR:
            header += (os.path.getsize(imageEncoded)).to_bytes(4, "big") # Image Size
        else:
            header += b'\x00\x40\x00\x80'
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
    