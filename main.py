import os, subprocess

import cv2
import pytesseract
import csv
import numpy as np

import fitz
from typing import Tuple



""" transparent_filename=[]
print("Converting PDF to PNGs")
subprocess.call(['convert','-density', '128',
            pdfPath,
            '-quality', '100',
            '-sharpen', '0x1.0',
            imagesPath]) """
#data= pytesseract.textonly_pdf(pdfPath)

def convert_pdf2img(inputFile: str, pages: Tuple= None): #Referent https://morioh.com/p/1cec6ebe1d67
    #Converts pdf to image and generates a file by page
    #Open the document
    pdfIn= fitz.open(inputFile)
    outputFiles= []
    # Iterate throughout the pages
    for pg in range(pdfIn.pageCount):
        #print(pg)
        if str(pages) != str(None):
            if str(pg) not in str(pages):
                continue
        # Select a page
        page= pdfIn[pg]
        rotate= 0
        # PDF Page is converted into a whole picture 1056*816 and then for each picture a screenshot is taken.
        # zoom = 1.33333333 -----> Image size = 1056*816
        # zoom = 2 ---> 2 * Default Resolution (text is clear, image text is hard to read)    = filesize small / Image size = 1584*1224
        # zoom = 4 ---> 4 * Default Resolution (text is clear, image text is barely readable) = filesize large
        zoomX= 2
        zoomY= 2
        # The zoom factor is equal to 2 in order to make text clear
        # Prerotate is to rotate if needed
        mat= fitz.Matrix(zoomX, zoomY).preRotate(rotate)
        pix= page.getPixmap(matrix= mat, alpha= False)

        #print(inputFile)                                        # EX .\data\IndiceLibroOpencv.pdf
        #print(os.path.basename(inputFile))                      # EX IndiceLibroOpencv.pdf
        #print(os.path.splitext(os.path.basename(inputFile))[0]) # EX IndiceLibroOpencv
        outputFile= f"{os.path.splitext(inputFile)[0]}_page{pg+1}.png" #splitext split the pathname path into a pair (root, ext)

        pix.writePNG(outputFile)
        outputFiles.append(outputFile)   #List of output files '.\\data\\IndiceLibroOpencv_page1.png'
    pdfIn.close()
    summary= {
        "File": inputFile, "Pages": str(pages), "Output File(s)": str(outputFiles)
    }
    # Printing summary
    """ print("#   Summary")
    print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
    print("#####") """
    return outputFiles  #List with name of files generated

def posH(img, maxIndex=30):
    imgDilate= cv2.dilate(img, None, iterations=1) #solo aplique una dilatacion
    boxes= pytesseract.image_to_data(imgDilate)
    positions=[]
    topBefore=0
    contador=0
    for x,b in enumerate(boxes.splitlines()):
        if x!=0:
            b= b.split()
            if len(b)==12:
                if int(b[5]) == 1 and abs(int(b[7]) - topBefore) > 6 :
                    pos= int(b[7])
                    topBefore= int(b[7])
                    if(contador < 2  or contador > maxIndex):
                        contador+= 1
                        positions.append(pos)
                        #print(f"Clave: {str(b[11])}, en la posicion {str(b[7])}, en el rango del contador")
                    else:
                        contador += 1
                        #verificar si es numero
                        try:
                            float(b[11])
                            positions.append(pos)
                            #print(f"Clave: {str(b[11])}, en la posicion {str(b[7])}")
                        except  ValueError:
                            print(f"No se pudo poner como clave {b[11]}")
    return positions

def detectingHeading(imgPath, headings, headingsKey):
    image= cv2.imread(imgPath)
    imageGray= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #imageGray
    positions= np.array(posH(imageGray))
    gray= cv2.dilate(imageGray, None, iterations=1) #solo aplique una dilatacion
    gray= cv2.erode(gray, None, iterations=1)
    #gray= cv2.dilate(gray, None, iterations=2)
    boxes= pytesseract.image_to_data(gray)
    value= None
    key= None
    withoutV= False
    topBefore= 0
    #se pone los valores de la cuenta en x
    for x,b in enumerate(boxes.splitlines()):
        #print(b)
        if x!=0:
            #print(b)            #one result 5       1       1       1       1       1       122     335     109     45      95  "Un
            b= b.split()
            if len(b)==12:
                indexcercano= abs(positions - int(b[7])).argmin()
                print(f"Posicion {indexcercano}, creo valor top {positions[indexcercano]} y b[5] es {str(b[5])} ")
                if (abs(int(b[7]) - positions[indexcercano]) <= 6) and int(b[5]) == 1:
                    np.delete(positions, indexcercano)   #Remove by index
                    topBefore= int(b[7])
                    key= str(b[11])
                    #topBefore= int(b[7])
                    #print(key)
                    withoutV= True

                elif abs(int(b[7]) - topBefore) <= 6:
                    #topBefore= int(b[7])
                    x,y,w,h= int(b[6]),int(b[7]),int(b[8]),int(b[9])  #(x,y) Top left corner, w width (anchura), h height (altura)
                    cv2.rectangle(gray,(x,y),(w+x,h+y),(0,0,139),2)
                    #veremos si los caracteres fuero detectados apropiadamente
                    cv2.putText(gray, b[11], (x,y), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0,0,139),1)
                    value= headings.get(key,'') + " "+ str(b[11]) #Get the the value by key, in case without value we put '' nothing
                    #print(value)
                    headings[key]= value
                    withoutV= False
            elif withoutV:
                value= key
                headings[key]= value
                x,y,w,h= int(b[6]),int(b[7]),int(b[8]),int(b[9])
                cv2.putText(gray, value, (x,y), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0,0,139),1)
                withoutV= False

            elif b[4] == 1 and b[5]== 0:
                value= None
    return gray, headings, headingsKey

#Paths
pdfPath= os.path.join('.','data','IndiceLibroOpencv.pdf')
csvOutPath= os.path.join('.','assets','output1.jpg')
imgOCRFolder= os.path.join('.','assets',)
csvFilePath= os.path.join('.','assets','newCsv.csv')

pytesseract.pytesseract.tesseract_cmd= 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' #full_path_to_your_tesseract_executable

generateFiles= convert_pdf2img(pdfPath)    #List with the pags png path

""" Testing
image= cv2.imread(generateFiles[0])
imageGray= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
imageGray= cv2.dilate(imageGray, None, iterations=1)
#cv2.imshow("Dilate Gray", imageGray)
imageGray= cv2.erode(imageGray, None, iterations=2)
#imageN= detectingWords(imageGray)
cv2.imwrite(imagesOCRPath,imageN) """

headings={}
headingsKey=[]
for pagPath in generateFiles:
    print(pagPath)
    imgN, headings, headingsKey= detectingHeading(pagPath, headings, headingsKey)
    
    #Save images with anotations
    basename= os.path.basename(pagPath) # Ex: IndiceLibroOpencv_page#.png
    outputFile= f"{os.path.join(imgOCRFolder,os.path.splitext(basename)[0])}OCR.png" #splitext split the pathname path into a pair (root, ext)
    cv2.imwrite(outputFile,imgN)

print(headings)
#Create the csv file
with open(csvFilePath, 'w') as csvFile:
    #print(headings.keys())
    wr= csv.DictWriter(csvFile, fieldnames= headings.keys())  #Writer that map dictionarios
    wr.writeheader()
    wr.writerow(headings)
    csvFile.close
