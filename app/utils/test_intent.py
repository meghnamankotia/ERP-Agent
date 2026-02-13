#input handling to check for intent
import base64
from openai import OpenAI
from unstructured.partition.pdf import partition_pdf_or_image
from unstructured.partition.xlsx import partition_xlsx
from unstructured.staging.base import elements_to_text
from ..schemas.base import Student

def pdfInput(path):
    elements= partition_pdf_or_image(filename=path)
    return elements_to_text(elements)

def xlsInput(path):
    return elements_to_text(partition_xlsx(filename=path))

def imgInput(path):
    client=OpenAI()
    with open(path, "rb") as f:
        image_base64=base64.b64encode(f.read()).decode("utf-8")

    image_input = {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{image_base64}"
        }
    }

    response= client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role":"system","content": "Extract text info from the image in a structured format. Do not add supporting text, return only the information"},
            {"role":"user", "content":[image_input]}
        ]
    )

    return response.choices[0].message.content


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