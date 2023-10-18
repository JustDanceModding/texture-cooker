import subprocess
from os import makedirs

def convert_to(image_path, 
               output_texture, 
               binary_path="bin",  
               program="magick",
               todds=False):
    
    alpha = has_transparency(image_path)
    if program == "nvcompress": compression = '-bc3' if alpha else "-bc1"
    else: compression = "DXT3" if alpha else "DXT1"

    makedirs("temp", exist_ok=True)
    
    if todds: subprocess.run(
        f'''{binary_path}\\magick.exe convert "{image_path}" "temp\\temp.png"''',
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )

    command = f"{binary_path}\\{program}.exe {compression}"
    if todds: command += f' "temp\\temp.png" "{output_texture}"'
    else: command += f' "{image_path}" "{output_texture}"'
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