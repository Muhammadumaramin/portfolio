"""Build the resume-only PDF in the user-provided LaTeX design.
Requires pdflatex, Latin Modern, and the packages used by resume-source/*.tex.
"""
from pathlib import Path
import shutil
import subprocess
import tempfile
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'resume-source/Muhammad_Umar_Amin_Resume.tex'
OUTPUT=ROOT/'output/pdf/Muhammad_Umar_Amin_Resume.pdf'
OUTPUT.parent.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory(prefix='umar-resume-') as build:
 result=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',f'-output-directory={build}',str(SOURCE)],capture_output=True,text=True)
 if result.returncode:
  raise RuntimeError(result.stdout[-6000:])
 shutil.copy2(Path(build)/SOURCE.with_suffix('.pdf').name,OUTPUT)
print(OUTPUT)
