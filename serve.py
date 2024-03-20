#!/usr/bin/env python
import os
import boto3
import time
from Matricula import Matricula

from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
BUCKET = os.environ.get("BUCKET")
PROMPT_MATRICULA = """
    Obtenha informações deste texto retirado de um documento de matrícula de imóvel.
    {query}
    {format_instructions}
    """

# Recebe o resultado do Job assíncrono após ter completado
# Retorna o número de páginas do documento
def get_job_results(client, job_id):
    pages = []
    time.sleep(1)
    response = client.get_document_text_detection(JobId=job_id)
    pages.append(response)
    print("Resultset page received: {}".format(len(pages)))
    next_token = None
    if 'NextToken' in response:
        next_token = response['NextToken']

    while next_token:
        time.sleep(1)
        response = client.\
            get_document_text_detection(JobId=job_id, NextToken=next_token)
        pages.append(response)
        print("Resultset page received: {}".format(len(pages)))
        next_token = None
        if 'NextToken' in response:
            next_token = response['NextToken']

    return pages

# Operção assíncrona de OCR obtendo arquivo no S3 bucket
# Retorna Id do job assíncrono
def start_job(client, s3_bucket_name, object_name):
    response = None
    response = client.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': s3_bucket_name,
                'Name': object_name
            }})

    return response["JobId"]

# Verifica a cada segundo o status do job assíncrono
# Retorna o status caso seja diferente de 'IN_PROGRESS'
def is_job_complete(client, job_id):
    time.sleep(1)
    response = client.get_document_text_detection(JobId=job_id)
    status = response["JobStatus"]
    print("Job status: {}".format(status))

    while(status == "IN_PROGRESS"):
        time.sleep(1)
        response = client.get_document_text_detection(JobId=job_id)
        status = response["JobStatus"]
        print("Job status: {}".format(status))

    return status
    
if __name__ == "__main__":

    fileName = input("Digite o nome do arquivo : ")

    # 1. OCR para extração do texto.
    # Client da AWS para utilizar o serviço Amazon Textract
    client = boto3.client('textract')

    jobId = start_job(client, BUCKET, fileName)

    print("Iniciando OCR com Amazon Textract com JobId: {}".format(jobId))

    if is_job_complete(client, jobId):
        response = get_job_results(client, jobId)

    text_prompt = ""
    # Armazena o resultado string do OCR numa variável
    for result_page in response:
        for item in result_page["Blocks"]:
            if item["BlockType"] == "LINE":
                text_prompt += item["Text"] + " "

    print("Texto extraído com sucesso. Iniciando leitura de texto com Gemini")

    # 2. Análise do resultado com LLM.
    gemini_llm = ChatGoogleGenerativeAI(google_api_key=os.environ.get("GOOGLE_API_KEY"),model="gemini-pro")
    parser = PydanticOutputParser(pydantic_object=Matricula)

    prompt = PromptTemplate(
        template=PROMPT_MATRICULA,
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | gemini_llm | parser

    output = chain.invoke({"query": text_prompt})

    print(output)