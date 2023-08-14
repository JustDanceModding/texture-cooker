from os import system

class ConvertTexture:
    def convert(image, outImage=None, platform="nx", binPath="bin"):
        if platform == "wii":
            system(f"{binPath}\\wimgt.exe ENCODE \"{image}\" --transform tpl.cmpr --overwrite --strip --dest \"{outImage}\"")
        
        if platform == "wiiu":
            system(f"{binPath}\\TexConv2.exe -i \"{image}\" -o \"{outImage}\"")
        
        if platform == "ps3":
            system(f"{binPath}\\dds2gtf.exe \"{image}\" -o \"{outImage}\"")

        if platform == "nx":
            try:
                # Mechanism to detect if theres exe version or python one.
                xtx_ext = open(f"{binPath}\\xtx_extract.py", "rb")
                xtx_ext = "xtx_extract.py"
            except FileNotFoundError:
                pass
            # Two try and except are needed for avoiding errors on the except.
            try:
                # Mechanism to detect if theres exe verion of python one.
                xtx_ext = open(f"{binPath}\\xtx_extract.exe", "rb")
                xtx_ext = "xtx_extract.exe"
            except FileNotFoundError:
                pass
            
            if xtx_ext.endswith(".py"):
                arg = "py "
            else:
                arg = ""
            system(f"{arg}{binPath}\\{xtx_ext} -o \"{outImage}\" \"{image}\"")

        if platform == "x360":
            system(f"{binPath}\\Bundler.exe \"{image}\"")