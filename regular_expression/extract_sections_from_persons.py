import re
from pprint import pprint

text = """
ALBIAUS, Bernhardus Siegfried

1.Geb. Frankfurt/Oder 24-02-1697 19)
Gest. Leiden 09-09-1770 (19)

2.Opleiding:

-Voorbereidend onderwijs door Leiden 0o ((149,2)
Sommerse Westerhnof

-Stud. Litt.h.c. Leiden 16-09-1709: --(20)

-Stud. Med., Leiden 1712

-Studiereis Frankrijk 1718

-Stud. Med. Parija -05-1729

-Doct.Med.hn.c. Leiden 19-09-1719

3.Boopbaan.:

-Lactor Ontleed- en Heelkunde Leiden 29-06-1716
O: --10-1719

-Hoogleraar Ontleed- en Heelkunde Leiden 18-10-1721
0319-11-1721

-Hoogleraar Geneeskunde en Leiden 30-08-1745
Physiologie 0:25-10-1746
-Rector Magnificus Leiden 19726/27,1738

5.Bijzonderheden :

-Hoogleraarschap Halle afgeslagen in 17d43.

-Hoogleraarschap Göttingen afgeslagen in 179592.

-Woont tot 1736 bij moeder in Steenschuur(gekocht
van trof. Boerhaave ),daarna met 2 zusters iLnt
Breestraat nr.42.

6.Ouders:(zie hiervoor)

Bernhardus Albinus(1653-1721),
hoogleraar geneeskunde Frankfurt/Oder en Leiden

Suzanna Catharina Ring(s)(1675-1745) (2,981

7.Ouders Vader:(zie hiervoor)

Christodorus Albinus(1622-1706), (70,83)
burgemeester Dessa.1

Rebecca Stieler(Stillers),gest. 1677 (70)

8.Ouders Moeder:(zie hiervoor)

Thomas Siegfried Ring(s)(1544-1707), (2)
hoogleraar rechten Frankfurt/Oder

Suzanna Maria von Scholtz von Hermensdorff
9,Echtgenote :

Clara Magdalena Dupeyrou

Geb. Amsterdam 19-04-1724

Gest. 30-10-1796

Getr.1.Lucas Dirksz.Trip

Getr.2.Bernhardus Siegfried Albinus in 17565
Getr.3.Mr.Gerrit Gerritsz.Hooft op 27-06-1773

10. Ouders Echtgenote:

Steven Andries Dupeyrou(1700-1761), koopman te
Amsterdam,reder ter walvisvangst

Margaretha Clara Muyssart(1702-1761)(haar vader
is Lid van de vreoedschap van Amsterdam)

a) Dossier Albiuus CBG
"""

# Define regular expressions for each part
name_pattern = r'^([^,]+(?:\s+\([^)]+\))?)(?:,\s*(.*?(?=\s+\(|,|$)))?'
birthdate_pattern = r'1\.Geb\..*?(\d{2}-\d{2}-\d{4})'
deathdate_pattern = r'Gest\..*?(\d{2}-\d{2}-\d{4})'
education_pattern = r'2\.Opleiding:(.*?)3\.Loopbaan:'
career_pattern = r'3\.Loopbaan:(.*?)4\.Nevenfunctie:'
extra_work_pattern = r'4\.Nevenfunctie:(.*?)5\. Bijzonderheden:'
additional_info_pattern = r'5\. Bijzonderheden:(.*)6\.Ouders:'
parents_pattern = r'6\.Ouders:(.*)7\.Ouders Vader:'
parents_father = r'7\.Ouders Vader:(.*)8\.Ouders Moeder:'
parents_mother = r'8\.Ouders Moeder:(.*)9\.Echtgenotes:'
spouses = r'9\.Echtgenotes:(.*)10\.Ouders Echtgenotes:'
parents_spouses = r'10\.Ouders Echtgenotes:(.*)11\Kinderen:'
children = r'11\Kinderen:(.*)'

# Extracting parts using regular expressions
first_name = re.search(name_pattern, text, re.MULTILINE | re.DOTALL)
last_name = re.search(name_pattern, text, re.MULTILINE | re.DOTALL)
birthdate = re.search(birthdate_pattern, text, re.MULTILINE | re.DOTALL)
deathdate = re.search(deathdate_pattern, text, re.MULTILINE | re.DOTALL)
education = re.search(education_pattern, text, re.MULTILINE | re.DOTALL)
career = re.search(career_pattern, text, re.MULTILINE | re.DOTALL)
extra_career = re.search(career_pattern, text, re.MULTILINE | re.DOTALL)
additional_info = re.search(additional_info_pattern, text, re.MULTILINE | re.DOTALL)

extracted_data = {}

# Storing extracted parts in the dictionary
if first_name:
    extracted_data["FirstName"] = first_name.group(2).strip()
if last_name:
    extracted_data["LastName"] = last_name.group(1).strip()
if birthdate:
    extracted_data["Birthdate"] = birthdate.group(1).strip()
if deathdate:
    extracted_data["Deathdate"] = deathdate.group(1).strip()
if education:
    extracted_data["Education"] = education.group(1).strip()
if career:
    extracted_data["Career"] = career.group(1).strip()
if additional_info:
    extracted_data["Additional Information"] = additional_info.group(1).strip()

# Returning the dictionary containing extracted data
pprint(extracted_data)
