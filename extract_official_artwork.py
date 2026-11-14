#!/usr/bin/env python3
"""Extract original map and 46 shop panels from the official Uozu Karnival 2026 PDF.
No shop copy or geographic details are generated or rewritten."""
import pathlib, urllib.request, fitz
ROOT=pathlib.Path(__file__).resolve().parent
OUT=ROOT/"assets"
(OUT/"shops").mkdir(parents=True,exist_ok=True)
URL="https://www.uozu-kanko.jp/uozu-bar/img/map.pdf"
req=urllib.request.Request(URL,headers={"User-Agent":"Mozilla/5.0 (compatible; UozuMapArchive/1.0)"})
with urllib.request.urlopen(req,timeout=90) as response:
    pdf=response.read()
if not pdf.startswith(b"%PDF"): raise ValueError("Official source did not return a PDF")
doc=fitz.open(stream=pdf,filetype="pdf")
if len(doc)!=2: raise ValueError("Unexpected official PDF page count")
# Coordinates are points on the unmodified official A3 landscape artwork.
# The cropped maps match the top and bottom sections in page one's right-hand half.
maps={
  "map_area.png":(600,255,1173.6,554.6),
  "map_station.png":(615,553,1170.2,800.2),
}
for filename,box in maps.items():
    doc[0].get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=fitz.Rect(*box),alpha=False).save(OUT/filename)
# Shop panels in source page two, retaining artwork without textual reconstruction.
cols=[(19.5,207.2),(212,400.7),(405.5,593.2),(596,783.7),(786.5,975.8),(978.5,1171.2)]
rows=[(110,198.3),(200.5,287.2),(289.5,375.2),(377.5,464.8),
      (467,554.3),(556.5,643.2),(645.5,732.8),(735,822.3)]
n=1
for row,(top,bottom) in enumerate(rows):
    for col,(left,right) in enumerate(cols):
        if row==0 and col==0: continue
        if row==7 and col==5: continue
        doc[1].get_pixmap(matrix=fitz.Matrix(3,3),
          clip=fitz.Rect(left,top,right,bottom),alpha=False).save(OUT/"shops"/f"{n:02}.png")
        n+=1
assert n==47, f"Expected 46 shop cards, extracted {n-1}"
for f in [OUT/"map_area.png",OUT/"map_station.png"]+list((OUT/"shops").glob("*.png")):
    if f.stat().st_size<1000: raise ValueError(f"Unexpected empty image: {f}")
print("Extracted original artwork from official source: 2 maps and 46 shop cards")
