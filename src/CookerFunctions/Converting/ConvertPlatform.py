from os import system
from os.path import isfile

class ConvertTexture:
    def convert(image, outImage=None, platform="nx", binPath="bin", ps3Decompress = False):
        if platform == "wii":
            system(f"{binPath}\\wimgt.exe ENCODE \"{image}\" --transform tpl.cmpr --overwrite --strip --dest \"{outImage}\"")
        
        if platform == "wiiu":
            system(f"{binPath}\\TexConv2.exe -i \"{image}\" -o \"{outImage}\"")
        
        if platform == "ps3":
            if ps3Decompress:
                system(f"{binPath}\\gtf2dds.exe \"{image}\" -o \"{outImage}\"")
            if not ps3Decompress:
                system(f"{binPath}\\dds2gtf.exe \"{image}\" -o \"{outImage}\"")   

        if platform == "nx":
            _ = isfile(f"{binPath}\\xtx_extract.exe")
            if _:
                xtx_ext = "xtx_extract.exe"
                arg = ""
            
            if not _:
                xtx_ext = "xtx_extract.py"
                arg = "python "

            system(f"{arg}{binPath}\\{xtx_ext} -o \"{outImage}\" \"{image}\"")

        if platform == "x360":
            system(f"{binPath}\\Bundler.exe \"{image}\"")