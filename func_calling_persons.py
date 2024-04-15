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


class Kind(BaseModel):
    """Identifying information about a person."""

    naam: str = Field(..., description="Name of the person mentioned")
    geb: Optional[str] = Field(..., description="The birth date of the peron")
    geb_plaats: str = Field(..., description="The birth place of the peron")
    gest: str = Field(..., description="The death date of the peron")
    gest_plaats: str = Field(..., description="The place where this person has died")
    extra_info: str = Field(..., description="Extra info about that specific person such as education and job.")


class Echtgenote(BaseModel):
    """Identifying information about a person."""

    naam: str = Field(..., description="Name of the person mentioned")
    geb: str = Field(..., description="The birth date of the peron")
    geb_plaats: str = Field(..., description="The birth place of the peron")
    gest: str = Field(..., description="The death date of the peron")
    gest_plaats: str = Field(..., description="The place where this person has died")
    marriage: str = Field(..., description="which marriage is this. ex: getr. 1")
    extra_info: str = Field(..., description="Extra info about that specific person such as education and job.")


class Ouder(BaseModel):
    """Identifying information about a person's father or mother inlaw."""

    naam: str = Field(..., description="Name of the person mentioned")
    extra_info: str = Field(..., description="Extra info about that specific person such as birth/death date education and job.")


class Persoon(BaseModel):
    """Information about a person."""
    naam: str = Field(..., description="Name of the person. each text can only contain one name")
    geb: str = Field(..., description="The birth date of the peron")
    geb_plaats: str = Field(..., description="The birth place of the peron")
    gest: str = Field(..., description="The death date of the peron")
    gest_plaats: str = Field(..., description="The place where this person has died")
    opleiding: List[str] = Field(..., description="Education information")
    loopbaan: List[str] = Field(..., description="Career information")
    nevenfuncties: Optional[str] = Field(None, description="volunteer work information")
    bijzonderheden: List[str] = Field(..., description="Additional details")
    ouders: Optional[Ouder] = Field(None, description="Names of the parents")
    ouders_vader: Optional[Ouder] = Field(None, description="Names of the grandparents")
    ouders_moeder: Optional[Ouder] = Field(None, description="Names of the grandparents")
    echtgenote: Optional[Echtgenote] = Field(None, description="Name of the spouse")
    ouders_echtgenote: Optional[Ouder] = Field(None, description="Names of the father and mother in law")
    kinderen: Optional[Kind] = Field(None, description="Names of the children")
    # kinderen: Sequence[str] = Field(None, description="Names of the children")


# Extraction
chain = create_extraction_chain_pydantic(pydantic_schema=Persoon, llm=chat)

# Run
text = """DECKERS (DEKKERS), Fredericus

1.Geb.’s Hertogenbosch 23-12-1648
Gest.Leiden 03-11-1720

2.Opleiding:

-Voorbereidend onderwijs ’s Hertogenbosch
-Stud.Med. Leiden 05-12-1664
-Doct.Med., Leiden 01-02-1668

3.Loopbaans:

-Arts Leiden 1668
-Hoogleraar practische Leiden 15-11-1694
Geneeskunde 0:20-712-71694

-Hoogleraar collegium Leiden 18-05-1697
practicum-medicum

-Hmeritus: 177

-Rector Magnificus Leiden 1700/01,1707/08,

1715/16
4eNevenfonncties

-Secretaris van de Senaa:t
BeBijzonderheden:

-Diss.De capitis dolore bij prof.Schacht

-Woont Oude Rijn(1670) ,Steenschuur(17017)

-Salaris: f1600,- (än 1694)

-Hij is de derde voor de vacature Pitcairne} voor hem wezen
Cyprianus(hoogleraar Franeker) en Brunner(lijfarts van de
keurvorst van de Palts)het aanbod af.

6.Ouders:
Hubertus Dekkers

9.Echtgenotess

Maria Breyne(Brayns) (2,a)
Gest.23-04-1700
Getr.Leiden 16-05-1670

Adriana van Aeckeren (2,29, a)
Ged. Leiden 25-12-1649

Gest.Leiden 26-12-1703

Getr.l.Matteus Pollenaer,lid vroedschap Leiden op 13-12-1667

Getr.2. 02-07-1670 Dirk Verhagen,notaris en schatmeester

van de prinselijke domeinen in Zoeterwoude

Getre3.Leiden 24-07-1701
10.Ouders Echtgenotes:

Pieter Mattijsz.Braine ,koopman,geboren te Keulen
Sarah de Koorn (1651-1700)

dan Meindertsz.van Aeckeren

Haesje Jansdr.van Rijn

11.Kinderen:(allen uit eerste huwelijk)

13arah
Ged. Leiden 08-02-1677

2.Hubertus
Ged. Leriden 20-11-1672
Gest.eLeiden 02-11-1720
stadsarts: Leiden
ondt.Leiden 22-08-1697 Johanna Jacoba Verhagen (dochter uit tweede
huwelijk van zijn aanstaande stiefmoeder)

3.dareh
Ged. Leiden 08-05-1674

4.Johanna

Ged. Leiden 10-12-1675
59eserrahn

Ged. Leiden 70-05-1678
6G.Meria

Ged. Leiden 18-06-17680

7.5Sarah
Ged. Leiden 26-04-1682

8.Jacoba

Ged. Leiden 05-11-11683
9.Sarah

Ged. Leiden 07-04-1686

T0.Johannes Hendecik
Gest. 02-17:-11720
Arts tes Hamburg:

a) DTB GA Leiden
"""
output = chain.run(text)
print(output)
