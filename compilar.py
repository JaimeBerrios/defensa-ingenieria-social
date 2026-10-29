#!/usr/bin/env python3
"""Punto de entrada: python3 compilar.py [opciones]."""
import sys
import subprocess
import tarfile
import zipfile
from herramientas.compilacion import main

if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError,
            StopIteration, tarfile.TarError, zipfile.BadZipFile) as error:
        print(f"\nERROR: {error}", file=sys.stderr)
        sys.exit(1)
