# Copyright (c) 2012 - Roberto Arista (http://robertoarista.it/)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# To use this script check the README file and the instruction folder

## Open modules
from pyPdf import PdfFileWriter, PdfFileReader
from AppKit import NSOpenPanel, NSOKButton
import os, sys, shutil as sh, datetime as dt

# Print author
print "Robo_imposer, developed by Roberto Arista, v.02"

# Number of signature
segn = 14
print "Number of signature:", segn

# Presenza dei segni di stampa (You can choose "True" or "False")
print_marks = False
print "Segni di stampa:", print_marks

# Color method
colormode(CMYK)
outputmode(CMYK)

## Functions

def select_file(title="Open", types=[]): # Copied from nodebox website (http://nodebox.net/code/index.php/shared_2008-03-07-00-20-32)
    filebrowser = NSOpenPanel.openPanel()
    filebrowser.setTitle_(title)
    result = filebrowser.runModalForDirectory_file_types_(None, None, types)
    if (result == NSOKButton):
        return filebrowser.filenames()

def crop_marks(x1,y1,x2,y2,x3,y3,x4,y4): # anti-clockwise
    ## Variables
    # Distance from cut
    dis = 2.5*mm
    
    # Length
    lung = 5*mm
    
    # White and black thickness
    th125 = 0.441*mm
    th25 = 0.088*mm
    
    # All whites
    stroke(0,0,0,0)
    strokewidth(th125)
    line(x1,y1-dis,x1,y1-dis-lung)
    line(x1-dis,y1,x1-dis-lung,y1)
    line(x2,y2+dis,x2,y2+dis+lung)
    line(x2-dis,y2,x2-dis-lung,y2)
    line(x3,y3+dis,x3,y3+dis+lung)
    line(x3+dis,y3,x3+dis+lung,y3)
    line(x4,y4-dis,x4,y4-dis-lung)
    line(x4+dis,y4,x4+dis+lung,y4)
    
    # All blacks
    stroke(1,1,1,1)
    strokewidth(th25)
    line(x1,y1-dis,x1,y1-dis-lung)
    line(x1-dis,y1,x1-dis-lung,y1)
    line(x2,y2+dis,x2,y2+dis+lung)
    line(x2-dis,y2,x2-dis-lung,y2)
    line(x3,y3+dis,x3,y3+dis+lung)
    line(x3+dis,y3,x3+dis+lung,y3)
    line(x4,y4-dis,x4,y4-dis-lung)
    line(x4+dis,y4,x4+dis+lung,y4)

def fold_marks(x, y1, y2):
    ## Fixed dimensions
    # Distance from cut
    dis = 0*mm
    
    # Lenght 
    lung = 2.0*mm
    
    # White thickness
    th125 = 0.441*mm
    
    # Black thickness
    th25 = 0.088*mm
    
    # All whites
    stroke(0,0,0,0)
    strokewidth(th125)
    line(x,y1-dis,x,y1-dis-lung)
    line(x,y2+dis,x,y2+dis+lung)
    
    # All blacks
    stroke(1,1,1,1)
    strokewidth(th25)
    line(x,y1-dis,x,y1-dis-lung)
    line(x,y2+dis,x,y2+dis+lung)
    
def comment(x, y, dim):
    # Date and time
    dh = str(dt.datetime.now())
    
    # Document title
    title = str(file_name[1])
    
    # Font, text dimension and strings
    font("Arial")
    fontsize(dim)
    path1 = textpath(dh, x, y)
    path2 = textpath(dh, x, y)
    path3 = textpath(title, x, y+dim*1.2)
    path4 = textpath(title, x, y+dim*1.2)
    
    # White text
    stroke(0,0,0,0)
    strokewidth(1)
    drawpath(path1)
    drawpath(path3)
    
    # Black text
    fill(1,1,1,1)
    strokewidth(0)
    drawpath(path2)
    drawpath(path4)


def registration_marks(x,y):
    cir_l = 3.527*mm
    line_l = 4.233*mm
    circ_int = 2.117*mm

    stroke(0,0,0,0)
    strokewidth(0.441*mm)
    nofill()
    oval(x-cir_l/2.0,y-cir_l/2.0,cir_l,cir_l)
    line(x,y-line_l/2.0,x,y+line_l/2.0)
    line(x-line_l/2.0,y,x+line_l/2.0,y)
    oval(x-circ_int/2.0,y-circ_int/2.0,circ_int,circ_int)

    stroke(1,1,1,1)
    strokewidth(0.088*mm)
    nofill()
    oval(x-cir_l/2.0,y-cir_l/2.0,cir_l,cir_l)
    line(x,y-line_l/2.0,x,y+line_l/2.0)
    line(x-line_l/2.0,y,x+line_l/2.0,y)

    fill(0,0,0)
    nostroke()
    oval(x-circ_int/2.0,y-circ_int/2.0,circ_int,circ_int)

    stroke(0,0,0,0)
    line(x,y-circ_int/2.0,x,y+circ_int/2.0)
    line(x-circ_int/2.0,y,x+circ_int/2.0,y)
    
    
def color_bars(x,y):
    # Lenght
    side = 4.939*mm
    
    # List of colors (CMYK)
    lista_colori = [(0,0,1,0),(0,1,0,0),(1,0,0,0),(1,1,0,0),(1,0,1,0),(0,1,1,0),(0,0,0,1),(0,0,0.5,0),(0,0.5,0,0),(0.5,0,0,0),(0,0,0,0.5)]
    
    # outstroke
    stroke(0.65,0.65,0.65,0.65)
    strokewidth(0.353*mm)
    
    # Square positioning
    for indice, quad in enumerate(lista_colori):
        fill(quad)
        rect(x+side*indice,y,side,side)


def gray_bars(x,y):
    # Lenght
    side = 4.939*mm
    
    lista_colori = []
    
    for i in range(1,11,1):
        lista_colori.append((0.1*i,0.1*i,0.1*i,0.1*i))
    
    # Gestione traccia contorno
    stroke(0.65,0.65,0.65,0.65)
    strokewidth(0.353*mm)
    
    # Ciclo for di posizionamento dei quadrati
    for indice, quad in enumerate(lista_colori):
        fill(quad)
        rect(x+side*indice,y,side,side)
        

# Check input and output folders
if os.path.exists("output") is False:
    os.makedirs("output")

# Make work directories
for sg in range(1,segn+1,1):
    os.makedirs('work/'+str("%#04d" % sg)+'/single')
    os.makedirs('work/'+str("%#04d" % sg)+'/spread')

## Split the pdf in single pages
# Open input file
sel_path = select_file("Select Aim File", ["pdf"])
input1 = PdfFileReader(file(str(sel_path[0])))

# File name
file_name = os.path.split(sel_path[0])

# Pages document number
pagine = int(input1.getNumPages())
print "The pdf has", pagine, "pages."

# Pages number per signature
pg_sg = pagine/segn
print "Pages number per signature:", pg_sg

# Check the correct number of pages
if pagine/segn%4 == 0:
    print "Pages amount correct!"
else:
    print "Pages amount is not correct. It has to be multiple of 4."
    sh.rmtree('work')
    sys.exit()

# Page variable
page1 = input1.getPage(0) 

# Distance from the origin
scst = 0*mm

# Size of canvas, dependent from spread
size(float(page1.bleedBox[2])*2+scst, float(page1.bleedBox[3])+scst*2) 

# Ordered list of the pages
lista_pagine = range(1,pagine+1)

# 1 signature
if segn == 1:
    # Splitting loop
    for pag in range(0,pagine,1):
        # Output creation
        output = PdfFileWriter()
        output.addPage(input1.getPage(pag))
    
        # Save and close
        outputStream = file("work/"+str(segn)+"/single/"+str(pag+1)+".pdf", "wb")
        output.write(outputStream)
        outputStream.close()

# More signature
else:
    # Last page at precedent loop
    ult = 0
    
    for sg in range(1,segn+1,1):
        for pag in range(ult+1,ult+pg_sg+1,1):
            
            # Output creation
            output = PdfFileWriter()
            output.addPage(input1.getPage(pag-1))
            
            # Save and close
            outputStream = file("work/"+str("%#04d" % sg)+"/single/"+str(pag)+".pdf", "wb")
            output.write(outputStream)
            outputStream.close()
        
        # Last page at precedent loop
        ult = pg_sg*sg

# List of the folders present in 'work'
lista_sg = os.listdir('work')
ds = '.DS_Store' in lista_sg
if ds is True:
    del lista_sg[0]
    
for indice, segnatura in enumerate(lista_sg):
    
    # Creation of alist with the pages of each signature
    lista_pg_files = os.listdir("work/"+str(segnatura)+"/single/")
    ds = '.DS_Store' in lista_pg_files
    if ds is True:
        del lista_pg_files[0]
    
    # Ordered list of the signature
    lista_pg = range((pg_sg*indice)+1, (pg_sg*indice)+pg_sg+1, 1)
        
    ## Composition of the spreads
    for spread in range(0, pg_sg/2,1):
        
        ## Spread Retro
        if spread%2 == True:
            # Page left - page right
            sx = lista_pg.pop(0)
            dx = lista_pg.pop(-1)
    
            # Putting pages on canvas, saving and closing
            image("work/"+segnatura+"/single/"+str(sx)+".pdf", 0*mm, 0*mm)
            image("work/"+segnatura+"/single/"+str(dx)+".pdf", float(page1.cropBox[2]), 0*mm)

            ## Segni di stampa
            if print_marks is True:
	            # registration_marks
	            registration_marks(float(page1.bleedBox[2])+scst, float(page1.bleedBox[1])+scst/2) # Top
	            registration_marks(float(page1.bleedBox[2])+scst, float(page1.bleedBox[3])+scst*1.5) # Down
	            registration_marks(float(page1.bleedBox[0])+scst/2, float(page1.bleedBox[3])/2) # Left
	            registration_marks(float(page1.bleedBox[2])*2+scst/2, float(page1.bleedBox[3])/2) # Right
	
	            # segni angoli artbox + bleedbox (2 volte)
	            crop_marks(float(page1.bleedBox[0])+scst, float(page1.bleedBox[1])+scst, float(page1.bleedBox[0])+scst, float(page1.bleedBox[3])+scst, float(page1.bleedBox[2])*2, float(page1.bleedBox[3])+scst, float(page1.bleedBox[2])*2, float(page1.bleedBox[1])+scst)
	            crop_marks(float(page1.artBox[0])+scst, float(page1.artBox[1])+scst, float(page1.artBox[0])+scst, float(page1.artBox[3])+scst, float(page1.artBox[2])*2+scst/2, float(page1.artBox[3])+scst, float(page1.artBox[2])*2+scst/2, float(page1.artBox[1])+scst)
	            
	            # Segni di piega (only bleedbox)
	            fold_marks(float(page1.bleedBox[2])+scst, float(page1.bleedBox[1])+scst, float(page1.bleedBox[3])+scst)
	            
	            # commento
	            comment(float(page1.bleedBox[2])*1.5+scst, float(page1.bleedBox[1])+scst/2.0, 8)
	    
	            ## barre colore e grigio
	            gray_bars(float(page1.bleedBox[2])*0.5+scst,float(page1.bleedBox[1])+scst*0.4)
	            color_bars(float(page1.bleedBox[2])*0.5+scst,float(page1.bleedBox[3])+scst*1.2)
            
            # Salvataggio e pulizia della tavola
            canvas.save("work/"+segnatura+"/spread/"+str(spread+1)+'.pdf')
            canvas.clear()

        ## Spread front
        else:
            # Page left - page right
            sx = lista_pg.pop(-1)
            dx = lista_pg.pop(0)
            
            # Putting pages on canvas, saving and closing
            image("work/"+segnatura+"/single/"+str(sx)+".pdf", 0*mm, 0*mm)
            image("work/"+segnatura+"/single/"+str(dx)+".pdf", float(page1.cropBox[2]), 0*mm)

            ## registration_marks
            if print_marks is True:
	            registration_marks(float(page1.bleedBox[2])+scst, float(page1.bleedBox[1])+scst/2) # Top
	            registration_marks(float(page1.bleedBox[2])+scst, float(page1.bleedBox[3])+scst*1.5) # Down
	            registration_marks(float(page1.bleedBox[0])+scst/2, float(page1.bleedBox[3])/2) # Left
	            registration_marks(float(page1.bleedBox[2])*2+scst/2, float(page1.bleedBox[3])/2) # Right
	
	            # segni angoli artbox + bleedbox (2 volte)
	            crop_marks(float(page1.bleedBox[0])+scst, float(page1.bleedBox[1])+scst, float(page1.bleedBox[0])+scst, float(page1.bleedBox[3])+scst, float(page1.bleedBox[2])*2, float(page1.bleedBox[3])+scst, float(page1.bleedBox[2])*2, float(page1.bleedBox[1])+scst)
	            crop_marks(float(page1.artBox[0])+scst, float(page1.artBox[1])+scst, float(page1.artBox[0])+scst, float(page1.artBox[3])+scst, float(page1.artBox[2])*2+scst/2, float(page1.artBox[3])+scst, float(page1.artBox[2])*2+scst/2, float(page1.artBox[1])+scst)
	            
	            # Segni di piega (only bleedbox)
	            fold_marks(float(page1.bleedBox[2])+scst, float(page1.bleedBox[1])+scst, float(page1.bleedBox[3])+scst)
	            
	            # commento
	            comment(float(page1.bleedBox[2])*1.5+scst, float(page1.bleedBox[1])+scst/2.0, 8)
	    
	            ## barre colore e grigio
	            gray_bars(float(page1.bleedBox[2])*0.5+scst,float(page1.bleedBox[1])+scst*0.4)
	            color_bars(float(page1.bleedBox[2])*0.5+scst,float(page1.bleedBox[3])+scst*1.2)
            
            canvas.save("work/"+segnatura+"/spread/"+str(spread+1)+'.pdf')
            canvas.clear()

## Grouping spread in signatures
# Dynamic navigation of work folders
for sg in range(0, segn, 1):
    
    # Output creation
    output_def = PdfFileWriter()
    for spread in range(0,pg_sg/2,1):
        input3 = PdfFileReader(file("work/"+str("%#04d" % (sg+1))+"/spread/"+str(spread+1)+".pdf", "rb"))
        output_def.addPage(input3.getPage(0))

    # Save and close
    outputStream = file("output/imposed_segn"+str("%#04d" % (sg+1))+"_"+file_name[1], "wb")
    output_def.write(outputStream)
    outputStream.close()

# Remove of work folders
sh.rmtree('work')
print "Imposition completed!"
print