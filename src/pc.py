import os, shutil, json
from unittest import TestResult
from CookerFunctions.UbiHeader import UbiartHeader
from PIL import Image, UnidentifiedImageError

# Took this from ChatGPT
"""def convert_image_to_dds(image_path, output_path, binPath="bin"):
    # Check if the image has transparency
    transpacency = has_transparency(image_path)

    # Set the compression format based on transparency
    compression = "dxt5" if transpacency else "dxt1"

    # Convert the image to DDS using nvcompress
    command = f"{binPath}\\nvcompress.exe -bc1" if compression == "dxt1" else f"{binPath}\\nvcompress -bc3"
    command += f" {image_path} {output_path}"
    os.system(command)"""

def convert_to_dds(image_path, output_path):
    img = Image.open(image_path)
    img.save(output_path)
    
# And also this
def has_transparency(image_path):
    try:
        with Image.open(image_path) as image:
            # Check if the image has an alpha channel
            if image.mode == 'RGBA' or (image.mode == 'P' and 'transparency' in image.info):
                return True
            else:
                return False
    except UnidentifiedImageError:
        return 0

def main():
    print("texture-cooker PC")
    
    config = json.load(open("CookerConfig.json"))

    os.makedirs("toCook", exist_ok=True)
    os.makedirs("cooked\\pc", exist_ok=True)

    for image in os.listdir("toCook"):
        print(image)
        os.makedirs("temp", exist_ok=True)
        dds = image.split(".") [0] + '.dds'

        transparency = has_transparency(f"toCook/{image}")
        if transparency == 0:
            Conv = False
            transparency = True
            path = f"toCook/{image}"
        else:
            Conv = True
            path = f"temp/{image}"

        if config["DontUseCookerExtension"]:
            ckd = image.split(".")[0] + config["NewExtension"] + ".ckd"
        else:
            ckd = image.split(".")[0] +'.png.ckd' if transparency else image.split(".")[0] + '.tga.ckd'
        
        if Conv:
            convert_to_dds(f"toCook/{image}", f"temp/{dds}")

            MakeHeader = UbiartHeader.create_header

            header = MakeHeader(f"temp/{dds}", isDDS=True)

        else:
            header = b'\x00\x00\x00\x09\x54\x45\x58\x00\x00\x00\x00\x2C\x00\x40\x00\x80\x00\x08\x00\x04\x00\x01\x18\x00\x00\x40\x00\x80\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\xCC\xCC'

        with open(f"cooked/pc/{ckd}", "wb") as final:
            final.write(header)
            with open(path, "rb") as temp:
                final.write(temp.read())

    shutil.rmtree("temp")

if __name__ == "__main__":
    main()