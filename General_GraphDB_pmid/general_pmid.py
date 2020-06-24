import requests
import io
import json
import sys
import time
import random

from pubmed_lookup import PubMedLookup
from pubmed_lookup import Publication


def web_request(method_name, url, dict_data, is_urlencoded=True, timeout_seconds=3):
    """Web GET or POST request를 호출 후 그 결과를 dict형으로 반환 """
    method_name = method_name.upper()  # 메소드이름을 대문자로 바꾼다
    if method_name not in ('GET', 'POST'):
        raise Exception('method_name is GET or POST plz...')

    if method_name == 'GET':  # GET방식인 경우
        response = requests.get(url=url, params=dict_data, timeout=timeout_seconds)
    elif method_name == 'POST':  # POST방식인 경우
        if is_urlencoded is True:
            response = requests.post(url=url, data=dict_data, \
                                     timeout=timeout_seconds,
                                     headers={'Content-Type': 'application/x-www-form-urlencoded'})
        else:
            response = requests.post(url=url, data=json.dumps(dict_data), \
                                     timeout=timeout_seconds, headers={'Content-Type': 'application/json'})

    dict_meta = {'status_code': response.status_code, 'ok': response.ok, 'encoding': response.encoding,
                 'Content-Type': response.headers['Content-Type']}
    if 'json' in str(response.headers['Content-Type']):  # JSON 형태인 경우
        return {**dict_meta, **response.json()}
    else:  # 문자열 형태인 경우
        return {**dict_meta, **{'text': response.text}}


def web_request_retry(num_retry=3, sleep_seconds=1, **kwargs):
    """timeout발생 시 sleep_seconds쉬고 num_retyrp번 재시도 한다"""
    for n in range(num_retry):
        try:
            return web_request(**kwargs)
        except requests.exceptions.Timeout:
            print(str(n + 1) + ' Timeout')
            time.sleep(sleep_seconds)
            continue
    return None


def SubmitPMIDList_BERN(Inputfile):
    json = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

    #
    # load pmids
    #
    f_in = open(Inputfile,"r")
    f2_out = open("error_log.txt", "w")
    cnt = 1
    f_out = open("General_pubmed_result.txt","w")
    while True:

        line = f_in.readline().rstrip("\n")
        if not line : break
        time.sleep(random.randint(10, 30))

        try:
            r = requests.get("https://bern.korea.ac.kr/pubmed/" + line + "/pubtator",headers = headers, timeout = 60)
        except requests.exceptions.Timeout:
            print('Timeout Error : ' + line)
            time.sleep(60)
            try:
                r = requests.get("https://bern.korea.ac.kr/pubmed/" + line + "/pubtator", headers=headers, timeout = 60)
            except requests.exceptions.Timeout:
                print('Timeout Error : ' + line)
                time.sleep(60)
                try:
                    r = requests.get("https://bern.korea.ac.kr/pubmed/" + line + "/pubtator", headers=headers, timeout=500)
                except requests.exceptions.Timeout:
                    print('Timeout Error : ' + line)
                    f2_out.write('Timeout Error : ' + line + '\n')
                    f2_out.flush()
                    print(cnt)
                    cnt = cnt + 1
                    continue
        if r.status_code != 200:
            print("[Error]: HTTP code " + str(r.status_code))
            f2_out.write("[Error]: HTTP code " + str(r.status_code) + ":" + line + '\n')
            f2_out.flush()
        else:
            f_out.write(r.text)
            f_out.write("!#$@!#$@!#$@!#$@\n")
            f_out.flush()
            print(cnt)
            cnt = cnt+1

    f_out.close()
    f_in.close()
    f2_out.close()
def SubmitPMIDList(Inputfile, Format = "pubtator", Bioconcept = ""):
    json = {}

    #
    # load pmids
    #
    with io.open(Inputfile, 'r', encoding="utf-8") as file_input:
        json = {"pmids": [pmid.strip() for pmid in file_input.readlines()]}


    f = open("pubtator_list.txt","w")
    #
    # load bioconcepts
    #
    if Bioconcept != "":
        json["concepts"] = Bioconcept.split(",")

    #
    # request
    #
    r = requests.post("https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/" + Format, json=json)
    if r.status_code != 200:
        print("[Error]: HTTP code " + str(r.status_code))
    else:
        text = r.text.split("\n")

        for i in text:
            f.write(i)
            f.write("\n")


    f.close()

def SubmitPMIDList_To_pubmed(Inputfile, Format = "pubtator", Bioconcept = ""):
    json = {}

    # load pmids

    f_in = open(Inputfile, "r")
    f2_out = open("error_log.txt", "w")
    cnt = 1
    f_out = open("General_pubmed_result.txt", "w")
    while True:

        line = f_in.readline().rstrip("\n")
        if not line: break
        time.sleep(random.randint(3, 10))

        # NCBI will contact user by email if excessive queries are detected
        email = 'kms0845@yonsei.ac.kr'
        url = 'http://www.ncbi.nlm.nih.gov/pubmed/'+ line


        try:
            lookup = PubMedLookup(url, email)
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

    f_out.close()
    f_in.close()
    f2_out.close()

if __name__ == "__main__":

    SubmitPMIDList_To_pubmed("./general_pmid_list", "pubtator", "")

    #SubmitPMIDList("./general_pmid_list", "pubtator", "")
    #SubmitPMIDList("./pmid_list_0325.txt", "pubtator", "")
    #
    # arg_count = 0
    # for arg in sys.argv:
    #     arg_count += 1
    # if arg_count < 2 or (sys.argv[2] != "pubtator" and sys.argv[2] != "biocxml" and sys.argv[2] != "biocjson"):
    #     print("\npython SubmitPMIDList.py [InputFile] [Format] [BioConcept]\n\n")
    #     print("\t[Inputfile]: a file with a pmid list\n")
    #     print("\t[Format]: pubtator (PubTator), biocxml (BioC-XML), and biocjson (JSON-XML)\n")
    #     print(
    #         "\t[Bioconcept]: gene, disease, chemical, species, proteinmutation, dnamutation, snp, and cellline. Default includes all.\n")
    #     print("\t* All input are case sensitive.\n\n")
    #     print("Eg., python SubmitPMIDList.py examples/ex.pmid pubtator gene,disease\n\n")
    # else:
    #     Inputfile = sys.argv[1]
    #     Format = sys.argv[2]
    #     Bioconcept = ""
    #     if arg_count >= 4:
    #         Bioconcept = sys.argv[3]
    #     #/home/yonsei/Documents/Corona19/ExampleCode.Python/examples/ex.pmid
    #     #SubmitPMIDList(Inputfile, Format, Bioconcept)
    #