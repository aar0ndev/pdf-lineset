import glob
import os
import shutil

RED = '\x1b[0;31m'
BLK = '\x1b[0m;'

def convert_to_svg(filename):
  os.system(f'inkscape.exe --export-type="svg" {filename}')

def modify_svg(filename):
  with open(filename, 'r') as finput:
    data = finput.read()
  output = data.replace('stroke-width:7;', 'stroke-width:3;')
  with open(filename, 'w') as foutput:
    foutput.write(output)

def convert_to_pdf(filename):
  os.system(f'inkscape.exe --export-type="pdf" {filename}')

if __name__ == '__main__':

  os.system('color')

  if not os.path.exists('temp/old'):
    os.makedirs('temp/old')

  files = glob.glob('OLD_FILES/*.pdf')
  for file in files:
    print(f'converting {file}...')

    path, basename = os.path.split(file)
    root, ext = os.path.splitext(basename)

    temp_pdf_path = 'temp/' + basename
    os.replace(file, temp_pdf_path)
    convert_to_svg(temp_pdf_path)

    temp_svg_path = 'temp/' + root + '.svg'
    if not os.path.exists(temp_svg_path):
      print(f'  {RED}-> Problem converting to SVG!{BLK}')
      continue
    modify_svg(temp_svg_path)

    os.replace(temp_pdf_path, 'temp/old/' + basename)
    convert_to_pdf(temp_svg_path)
    if not os.path.exists(temp_pdf_path):
      print('  {RED}-> Problem converting to PDF!{BLK}')
      continue

    os.replace(temp_svg_path, 'temp/old/' + root + '.svg')
    os.replace(temp_pdf_path, basename)
