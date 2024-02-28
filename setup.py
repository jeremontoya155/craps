import sys
from cx_Freeze import setup, Executable
import os
# Reemplaza '<USER>' con tu nombre de usuario en Windows
os.environ['TCL_LIBRARY'] = r'C:\Users\Administrador\AppData\Roaming\Python\Python311\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Administrador\AppData\Roaming\Python\Python311\tcl\tk8.6'

include_files = [
    r"C:\Users\Administrador\AppData\Roaming\Python\Python311\DLLs\tcl86t.dll",
    r"C:\Users\Administrador\AppData\Roaming\Python\Python311\DLLs\tk86t.dll"
]

packages = ["tkinter", "os"  # Agrega otros paquetes según sea necesario
            # ... ]
]

build_exe_options = {
    "includes": ["tkinter"],
    "include_files": include_files,
    "packages": packages
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Si tu aplicación es una GUI, utiliza "Win32GUI"

setup(
    name="NombreEjecutable",
    version="1.0",
    description="Descripción del programa",
    options={"build_exe": build_exe_options},
    executables=[Executable("Scrapper.py", base=base)]
)
