#input handling to check for intent
from unstructured.partition.pdf import partition_pdf_or_image
from unstructured.staging.base import elements_to_text
from ..schemas.base import Student

def pdfInput(path):
    elements= partition_pdf_or_image(filename=path)
    return elements_to_text(elements)

def xlsInput(path):
    pass

def fileType(path:str):
    #extract file extension
    extension= path.split(".")[-1]

    #return extension type
    if extension=="xlsx" or extension=="xls":
        return "xls"
    supported_img=["jpeg", "jpg","png", "tiff","heic","bmp"]
    if extension=="pdf":
        return "pdf"
    
    return "not supported"

def inputHandler(path:str)-> Student|str:

    #find type
    type=fileType(path)

    #call corresponding input parser
    if type=="pdf":
        return pdfInput(path)
    elif type=="xls":
        return xlsInput(path)
    
    return "file type not supported"