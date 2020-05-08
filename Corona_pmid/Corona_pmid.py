import requests
import io
import json
import sys

def SubmitPMIDList_BERN(Inputfile):
    json = {}

    #
    # load pmids
    #
    f_in = open(Inputfile,"r")
    cnt = 1
    f_out = open("bern_niclosamide_results.txt","w")
    while True:
        line = f_in.readline().rstrip("\n")
        if not line : break

        r = requests.get("https://bern.korea.ac.kr/pubmed/" + line + "/pubtator")
        if r.status_code != 200:
            print("[Error]: HTTP code " + str(r.status_code))
        else:
            f_out.write(r.text)
            f_out.write("!#$@!#$@!#$@!#$@\n")
            f_out.flush()
            print(cnt)
            cnt = cnt+1

    f_out.close()
    f_in.close()
def SubmitPMIDList(Inputfile, Format, Bioconcept):
    json = {}

    #
    # load pmids
    #
    with io.open(Inputfile, 'r', encoding="utf-8") as file_input:
        json = {"pmids": [pmid.strip() for pmid in file_input.readlines()]}


    f = open("Chemical_result.txt","w")
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
            if("Chemical" in i ):
                f.write(i)
                f.write("\n")

    f.close()
if __name__ == "__main__":
    SubmitPMIDList_BERN("./pmid_list_niclosamide")
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