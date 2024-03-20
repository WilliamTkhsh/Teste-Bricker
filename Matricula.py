from typing import Optional
from langchain.pydantic_v1 import BaseModel, Field

class Matricula(BaseModel):
    expedition_date: str = Field(description = "a data de emissão do presente documento. IMPORTANTE: Retorne no formato dd/MM/yyyy")
    responsible_registry: str = Field(description = "nome do cartório que emitiu o documento")
    registration_number: str = Field(description = "Número da matrícula do imóvel")
    property_type: str = Field(description = "Tipo do imóvel (lote, prédio residencial, apartamento, terreno, vaga de garagem) IMPORTANTE: converta 'terreno urbano' é a mesma coisa que 'terreno' então retorne 'terreno' se o tipo for 'terreno urbano'; IMPORTANTE: no caso de prédio e respectivo terreno sempre retorne prédio;")
    batch: str = Field(description = "apenas o lote do terreno, indique se é o lote inteiro ou se é partes ou parte do lote;")
    block: str = Field(description = "a quadra do imóvel (se houver, somente número/nome da quadra)")
    street: str = Field(description = "A primeira rua do imóvel, escrever no começo se é rua, avenida, etc")
    street_2: str = Field(description = "A segunda rua do imóvel, escrever no começo se é rua, avenida, etc")
    property_number: str = Field(description = "sempre que houver, pegar o primeiro número do endereço do imóvel")
    property_number_2: str = Field(description = "sempre que houver, pegar o segundo número do endereço do imóvel")
    address_complement: str = Field(description = "o número do apartamento, número do bloco ou número da vaga de garagem. IMPORTANTE: SOMENTE o número;")
    neighborhood: str = Field(description = "pegar APENAS o bairro onde fica localizado o imóvel")
    city: str = Field(description = "pegar APENAS a cidade onde fica localizado o imóvel")
    state: str = Field(description = "estado onde o imóvel fica localizado retorne o nome COMPLETO do estado")
    property_footage: str = Field(description = "pegar APENAS o primeiro tamanho do imóvel que encontrar e remover a unidade de medida")
    owners_quantity: str = Field(description = "Quantidade de donos ATUAIS do imóvel, retorne como número")
    owner_1: str = Field(description = "Nome Completo do primeiro proprietário")
    owner_2: str = Field(description = "Nome Completo do segundo proprietário (se houver)")
    document_owner_1: str = Field(description = "CPF ou CNPJ do proprietário principal (PADRÃO CPF: 000.000.000-00) (PADRÃO CNPJ: 00.000.000/0000-00)")
    document_owner_2: str = Field(description = "CPF ou CNPJ do proprietário secundário (se houver) (PADRÃO CPF: 000.000.000-00) (PADRÃO CNPJ: 00.000.000/0000-00)")
    mortgage: str = Field(description = "Indique se o imóvel está em hipoteca (sim ou não) retorne sim ou não")
    mortgage_owner_name: str = Field(description = "Nome do dono da hipoteca (se houver)")
    mortgage_owner_document: str = Field(description = "CPF ou CNPJ do proprietário da hipoteca (se houver)")
    fiduciary_alienation: str = Field(description = "Indique se o imóvel está em alienação fiduciária (sim ou não) retorne sim ou não")
    fiduciary_alienation_owner_name: str = Field(description = "Nome do dono da alienação fiduciária (se houver)")
    fiduciary_alienation_owner_document: str = Field(description = "CPF ou CNPJ do proprietário da alienação fiduciária (se houver) (PADRÃO CPF: 000.000.000-00) (PADRÃO CNPJ: 00.000.000/0000-00)")
    garnishment: str = Field(description = "Indique se o imóvel está em penhora (sim ou não) retorne sim ou não")

    def __init__(self, **data):
        for field in self.__fields__:
            if field in data and data[field] is None:
                data[field] = "n/a"
        super().__init__(**data)