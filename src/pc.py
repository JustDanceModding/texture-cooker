import subprocess
from os import listdir, makedirs
from shutil import rmtree
from CookerFunctions.UbiHeader import UbiartHeader

def convert_to_dds_MAGICK(image_path, output_dds, binary_path="bin"):
    alpha = has_transparency(image_path)
    compression = 'DXT5' if alpha else "DXT1"
    subprocess.run(
        f'''{binary_path}\\magick.exe convert -define dds:compression={compression} "{image_path}" "{output_dds}"''',
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )

def convert_to_dds(image_path, output_dds, binary_path="bin"):
    alpha = has_transparency(image_path)
    compression = '-bc3' if alpha else "-bc1"

    command = f"{binary_path}\\nvcompress.exe {compression}"
    command += f' "{image_path}" "{output_dds}"'
    subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        text=True
    )

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

def main():
    print("Texture Cooker for PC")

    makedirs("toCook", exist_ok=True)
    makedirs("cooked\\pc", exist_ok=True)

    for image in listdir("toCook"):
        print(image)
        makedirs("temp", exist_ok=True)
        dds = image.split(".") [0] + '.dds'

        transparency = has_transparency(f"toCook/{image}")

        ckd = image.split(".")[0] + '.png.ckd' if transparency else image.split(".")[0] + '.tga.ckd'
        
        convert_to_dds_MAGICK(f"toCook/{image}", f"temp/{dds}")

        MakeHeader = UbiartHeader.create_header

        header = MakeHeader(f"temp/{dds}")

        with open(f"cooked/pc/{ckd}", "wb") as final:
            final.write(header)
            with open(f"temp/{dds}", "rb") as temp:
                final.write(temp.read())

    rmtree("temp")

if __name__ == "__main__":
    main()