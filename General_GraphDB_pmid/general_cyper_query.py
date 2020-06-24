import requests
import io
import json
import sys
import time
import random

from pubmed_lookup import PubMedLookup
from pubmed_lookup import Publication

def SubmitPMIDList_To_pubmed(Input_PMID, Format = "pubtator", Bioconcept = ""):
    json = {}

    # load pmids


    time.sleep(random.randint(3, 10))

    # NCBI will contact user by email if excessive queries are detected
    email = 'kms0845@yonsei.ac.kr'
    url = 'http://www.ncbi.nlm.nih.gov/pubmed/'+ Input_PMID


    try:
        lookup = PubMedLookup(url, email)

        # publication = {}
        # publication['title'] = lookup.record['Title']
        # publication['Title'] = lookup.record['Title']
        publication = Publication(lookup)

        return publication
        # print(
        #     """
        #     TITLE:\n{title}\n
        #     AUTHORS:\n{authors}\n
        #     JOURNAL:\n{journal}\n
        #     YEAR:\n{year}\n
        #     MONTH:\n{month}\n
        #     DAY:\n{day}\n
        #     URL:\n{url}\n
        #     PUBMED:\n{pubmed}\n
        #     CITATION:\n{citation}\n
        #     MINICITATION:\n{mini_citation}\n
        #     ABSTRACT:\n{abstract}\n
        #     """
        #         .format(**{
        #         'title': publication.title,
        #         'authors': publication.authors,
        #         'journal': publication.journal,
        #         'year': publication.year,
        #         'month': publication.month,
        #         'day': publication.day,
        #         'url': publication.url,
        #         'pubmed': publication.pubmed_url,
        #         'citation': publication.cite(),
        #         'mini_citation': publication.cite_mini(),
        #         'abstract': repr(publication.abstract),
        #     }))
    except:
        print("pubmed error!")


if __name__ == '__main__':
    f = open("./pubtator_list.txt","r")
    f_out = open("./pubtator_list_cyper_query.txt","w", encoding="utf-8")


    f_pro = open("./pro_list.txt","r")

    pro_list = []
    while True:
        line = f_pro.readline()
        if not line : break

        pro_list.append(line.rstrip("\n").split(","))

    f_pro.close()


    pmid_temp = "aaaa"
    bioconcept_list = []
    while True:
        line = f.readline()
        if not line : break
        #29458023	35	44	HCoV-229E	gene	CUI-less

        if("|t|" in line or "|a|" in line) : continue
        if('\n' == line) : continue
        else:
            temp = line.rstrip("\n").split("\t")
            bioconcept_list.append([temp[-3],temp[-2],temp[-1],temp[0]])
        # elif("Severe Acute Respiratory Syndrome Coronavirus 2" in line):
        #     f_out.write(line)

    last_pmid = '-999'

    for i in bioconcept_list:
        # if(i[3] != '27470214') : continue
        if(i[1] == 'Gene'):
            i[2] = 'GeneID:' + i[2]
            for j in pro_list:
                if(j[0] == i[2]):
                    i[2] = j[1]
                    break

            if ('GeneID' in i[2]): continue

        if (i[1] == 'Species'):
            i[2] = 'TAXID:' + i[2]

        if (' ' in i[2]):
            continue
        if('-' in i[2] ):
            continue
    #    f_out.write("\""+str(i[2])+"\", ")

        #         'title': publication.title,
        #         'authors': publication.authors,
        #         'journal': publication.journal,
        #         'year': publication.year,
        #         'month': publication.month,
        #         'day': publication.day,
        #         'url': publication.url,
        #         'pubmed': publication.pubmed_url,
        #         'citation': publication.cite(),
        #         'mini_citation': publication.cite_mini(),
        #         'abstract': repr(publication.abstract),

        if(last_pmid != str(i[3])):
            pmid_info = SubmitPMIDList_To_pubmed(str(i[3]), "pubtator", "")
            last_pmid = str(i[3])
        try:
            print_temp = str(i[1]) + "," + str(i[0]) + "," + str(i[2]) + "," + str(pmid_info.title).replace(",","_") + "," + str(pmid_info.authors).replace(",","_") + "," + str(pmid_info.journal).replace(",","_") + "," + str(pmid_info.year).replace(",","_") + "," + str(pmid_info.month).replace(",","_") + "," + str(pmid_info.day).replace(",","_") + "," + str(pmid_info.pubmed_url) + "\n"
        except:
            # print("print_temp_failed!")
            continue
        print(print_temp)
        f_out.write(print_temp)
    f.close()
    f_out.close()