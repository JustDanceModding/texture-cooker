import os, shutil, json
from CookerFunctions.UbiHeader import UbiartHeader
from PIL import Image

# Took this from ChatGPT
def convert_image_to_dds(image_path, output_path, binPath="bin"):
    # Check if the image has transparency
    transpacency = has_transparency(image_path)

    # Set the compression format based on transparency
    compression = "dxt5" if transpacency else "dxt1"

    # Convert the image to DDS using nvcompress
    command = f"{binPath}\\nvcompress.exe -bc1" if compression == "dxt1" else f"{binPath}\\nvcompress -bc3"
    command += f" {image_path} {output_path}"
    os.system(command)
    
# And also this
def has_transparency(image_path):
    with Image.open(image_path) as image:
        # Check if the image has an alpha channel
        if image.mode == 'RGBA' or (image.mode == 'P' and 'transparency' in image.info):
            return True
        else:
            return False

def main():
    print("texture-cooker XONE")

    config = json.load(open("CookerConfig.json"))

    os.makedirs("toCook", exist_ok=True)
    os.makedirs("cooked\\durango", exist_ok=True)

    for image in os.listdir("toCook"):
        print(image)
        os.makedirs("temp", exist_ok=True)
        dds = image.split(".") [0] + '.dds'

        transparency = has_transparency(f"toCook/{image}")

        if config["DontUseCookerExtension"]:
            ckd = config["NewExtension"]
        else:
            ckd = image.split(".")[0] +'.png.ckd' if transparency else image.split(".")[0] + '.tga.ckd'
        convert_image_to_dds(f"toCook/{image}", f"temp/{dds}")

        MakeHeader = UbiartHeader.create_header

        header = MakeHeader(f"temp/{dds}", isDDS=True)

        with open(f"cooked/durango/{ckd}", "wb") as final:
            final.write(header)
            with open(f"temp/{dds}", "rb") as temp:
                final.write(temp.read())

    shutil.rmtree("temp")

if __name__ == "__main__":
    main()