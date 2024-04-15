from langchain.chains.openai_functions import create_extraction_chain_pydantic
from langchain_openai import ChatOpenAI
from langchain_community.llms import OpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
# Standard Helpers
import pandas as pd
import requests
import time
import json
from datetime import datetime
import os

# Text Helpers
from bs4 import BeautifulSoup
from markdownify import markdownify as md

# For token counting
from langchain_community.callbacks import get_openai_callback

def printOutput(output):
    print(json.dumps(output,sort_keys=True, indent=3))
# It's better to do this an environment variable but putting it in plain text for clarity
openai_api_key = 'api_key'

chat = ChatOpenAI(
    # model_name="gpt-3.5-turbo-0613", # Cheaper but less reliable
    model_name="gpt-4-0613",
    temperature=0,
    max_tokens=2000,
    openai_api_key=openai_api_key
)

from typing import Sequence
from langchain.pydantic_v1 import BaseModel, Field
import enum
from typing import List, Optional

class Kinderen(BaseModel):
    """Identifying information about a person's child."""

    name: str = Field(..., description="Name of the child mentioned")
    extra_info: str = Field(..., description="Extra info about that specific child such as:birth/death date/place, education and job.")


class PersonInfo(BaseModel):
    """Information about a person."""
    name: str = Field(..., description="Name of the person. each text can only contain one name")
    geb: str = Field(..., description="The birth date of the peron")
    gest: str = Field(..., description="The death date of the peron")
    opleiding: List[str] = Field(..., description="Education information")
    loopbaan: List[str] = Field(..., description="Career information")
    bijzonderheden: List[str] = Field(..., description="Additional details")
    echtgenote: Optional[str] = Field(None, description="Name of the spouse")
    kinderen: List[Kinderen] = Field(None, description="Names of the children")
    # kinderen: Sequence[str] = Field(None, description="Names of the children")


# Extraction
chain = create_extraction_chain_pydantic(pydantic_schema=PersonInfo, llm=chat)

# Run
text = """BONTIUS (BONDT, DE BONT) ,Gerardus(Geraert)

1.Geb. Rijswijk(Gld.) 7536
Gest.lLeiden 15-09-1599

20pleidings
-Les Adrianus Agrippa

Schoonhoven,

Delft ,Geldrop
-5tud.Med. Leuven
-Studiereis Italië
-Doct.Med., Padua

3eLoopbaans

-Arts Leiden

-Hoogleraar Medicijnen en Leiden 17-07-1575
vrije consten(wis- en
sterrekunde )

-Onderwijs Kruid-en Ont- Leiden -09-1587
leedkunde

-Toezicht Hortus Leiiden T0-70-1598

-Rector Magnificus Leiden 1582-83,15909

5 .Bijzonderheden:

-Woont op Gerecht,hoek Lengesteeg.

-Salaris: f300,-(1575),f400,-(1589),f500,-(1591),f600,-(1594).
-NVezijzinnig in religiosis,.

9.Echtgenote:

Jacoba Jansdr.,
11.Kimderen:s

1 .Agnes
2.Marie

3edan
Begr.Rotterdam 18/25-04-1632°
Arts en gemeenteontvanger Rotterdam
Getr.Rotterdam 20-06-17599 Lideroy van Goedereede

4.JacoMb
Geb. Leiden 1598
Gest.Nederlands-Indië 30-117-1637
Arts te Leiden,Inspecteur chirurgen Indi&

en Advocaat-Fiscaal Indië.
Getr.Leiden 22-01-1676 Agneta Jansdr.,

5eReinier (zie hierna)
Geb.Leiden 1576
Gest.Leiden 12-06-1623(T79) of 13-06-1623(20)
Hoogleraar Geneeskunde Leiden
Ondt.1. Leiden 02-06-16017 Leonora Fabiusdr.
Ondt.2.Leiden 02-04-1618 Clementia Willemsdr.-van der Aa

6.eWMilLLem
Gest.Leiden 16-710-1646
Hoogleraar Rechten Leiden,Schout Leiden
Ondt Leiden 05-06-1626 Maria van Dilsen

a) Bevolkingsregisteer 1581,GA Leiden
"""
output = chain.run(text)
print(output)
