from PIL import Image
import pytesseract

def ocr(file):
    im = Image.open(file)
    text = pytesseract.image_to_string(im, lang = 'eng', config='--psm 6')
    
    return text
    #out_stream=open(file[:find_period(file)] + ".txt", 'w')
    #out_stream.write(text)
    #out_stream.close()

#def ocrs(files):
#    for i in files:
#        ocr(i)

#def find_period(s):
#    s=s[::-1]
#    return -s.find('.') - 1