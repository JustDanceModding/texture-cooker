from os import system

class ConvertTexture:
    def convert(image, outImage, platform, binPath="bin"):
        if platform == "wii":
            system(f"{binPath}\\wimgt.exe ENCODE \"{image}\" --transform tpl.cmpr --overwrite --strip --dest \"{outImage}\"")
        
        if platform == "wiiu":
            system(f"{binPath}\\TexConv2.exe -i \"{image}\" -o \"{outImage}\"")
        
        if platform == "ps3":
            system(f"{binPath}\\dds2gtf.exe \"{outImage}\" -o \"{outImage}\"")

        if platform == "nx":
            system(f"{binPath}\\xtx_extract.exe -o \"{outImage}\" \"{image}\"")

        if platform == "x360":
            system(f"{binPath}\\Bundler.exe \"{image}\"")