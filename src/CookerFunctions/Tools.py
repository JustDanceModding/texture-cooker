
from .Converting import *
from .Utils import *
from os import makedirs
import subprocess
from shutil import rmtree

"This PY file is made for the Cooking functions."

def Cook(texture_input: str, output_path: str, platform: str = "nx", todds = True):
    makedirs("temp", exist_ok=True)
    platform = platform.lower()
    transparency = has_transparency(texture_input)

    ckd = texture_input.split(".")[0] + '.png.ckd' if transparency else texture_input.split(".")[0] + '.tga.ckd'

    output_texture = output_path + "\\" + ckd.replace("toCook\\", "").replace("toCook/", "")

    if platform == "nx": console_format = ".xtx"
    if platform == "wiiu": console_format = ".gtx"
    if platform == "ps3": console_format = ".gtf"
    if platform == "pc" or platform == "win": console_format = ".dds"
    if platform == "xone" or platform == "durango": console_format = ".dds"
    if platform == "scarlett": console_format = ".dds"
    if platform == "x360": console_format = ".tga"

    if (console_format==".dds"):
        convert_to(image_path=texture_input, output_texture="temp\\temp.dds", program="nvcompress", todds=todds)

        with open(output_texture, "wb") as cooked_texture:
            cooked_texture.write(UbiartHeader.create_header(image="temp\\temp.dds"))
            with open("temp\\temp.dds", "rb") as dds:
                cooked_texture.write(dds.read())

    if (console_format==".xtx"):
        convert_to(image_path=texture_input, output_texture="temp\\temp.dds", program="nvcompress", todds=todds)

        ConvertTexture.convert(image="temp\\temp.dds", outImage="temp\\temp.xtx", platform="nx")

        with open(output_texture, "wb") as cooked_texture:
            cooked_texture.write(UbiartHeader.create_header(image="temp\\temp.dds"))
            with open("temp\\temp.xtx", "rb") as xtx:
                cooked_texture.write(xtx.read())

    if (console_format==".gtx"):
        convert_to(image_path=texture_input, output_texture="temp\\temp.dds", program="nvcompress", todds=todds)

        ConvertTexture.convert(image="temp\\temp.dds", outImage="temp\\temp.gtx", platform="wiiu")

        with open(output_texture, "wb") as cooked_texture:
            cooked_texture.write(UbiartHeader.create_header(image="temp\\temp.dds"))
            with open("temp\\temp.gtx", "rb") as gtx:
                cooked_texture.write(gtx.read())

    if (console_format==".gtf"):
        convert_to(image_path=texture_input, output_texture="temp\\temp.dds", program="nvcompress", todds=todds)

        ConvertTexture.convert(image="temp\\temp.dds", outImage="temp\\temp.gtf", platform="ps3")

        with open(output_texture, "wb") as cooked_texture:
            cooked_texture.write(UbiartHeader.create_header(image="temp\\temp.dds"))
            with open("temp\\temp.gtf", "rb") as gtf:
                cooked_texture.write(gtf.read())

    if (console_format==".tga"):
        convert_to(image_path=texture_input, output_texture="temp\\temp.tga", program="nvcompress", todds=todds)

        RDF.make(image="temp\\temp.tga", imageOnRDF="temp\\temp.xpr", rdfOut="temp\\temp.rdf")
        ConvertTexture.convert(image="temp\\temp.dds", outImage="temp\\temp.rdf", platform="x360")

        with open(output_texture, "wb") as cooked_texture:
            cooked_texture.write(UbiartHeader.create_header(image="temp\\temp.dds"))
            with open("temp\\temp.xpr", "rb") as xpr:
                xpr.seek(0x2c)
                cooked_texture.write(xpr.read(0x34))
                xpr.seek(2060, 0)
                cooked_texture.write(xpr.read())

    rmtree("temp")

def UnCook(texture_input: str, output_path: str, platform: str = "nx", extension: str = "dds", binarypath: str = "bin", program: str = "magick"):
    makedirs("temp", exist_ok=True)
    platform = platform.lower()

    if program == "nvcompress":
        print("NVCompress cant be used with UnCooking!!!")
        raise Exception

    if platform == "nx": console_format = ".xtx"
    if platform == "wiiu": console_format = ".gtx"
    if platform == "ps3": console_format = ".gtf"
    if platform == "pc" or platform == "win": console_format = ".dds"
    if platform == "xone" or platform == "durango": console_format = ".dds"
    if platform == "scarlett": console_format = ".dds"
    if platform == "x360": console_format = ".tga"

    texture_output = output_path + "\\" + texture_input.split(".")[0] + "." + extension

    texture_cooked = open(texture_input, "rb")
    texture_console = open(f"temp\\temp{console_format}", "wb")

    texture_cooked.seek(0x8)
    offsetFlag = struct.unpack(">I", texture_cooked.read(4))[0]

    texture_cooked.seek(offsetFlag, os.SEEK_SET)
    texture_console.write(
        texture_cooked.read()
    )

    if (console_format==".xtx"):
        ConvertTexture.convert("temp\\temp.xtx", outImage="temp\\temp.dds", platform="nx")

    if (console_format==".gtx"):
        ConvertTexture.convert("temp\\temp.gtx", outImage="temp\\temp.dds", platform="wiiu")

    if (console_format==".gtf"):
        ConvertTexture.convert("temp\\temp.gtf", outImage="temp\\temp.dds", platform="ps3", ps3Decompress=True)

    if program ==  "magick":
        command = f'magick.exe convert "temp\\temp.dds" "{texture_output}"'
        subprocess.run(command)