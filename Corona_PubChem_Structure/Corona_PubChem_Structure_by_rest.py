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
    f_out = open("Corona_drug_structure_rest.txt","w")
    while True:

        line = f_in.readline().rstrip("\n")
        if not line : break

        query_text = line.split('@#$')[0]
        r = requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/" + query_text + "/cids/TXT")
        f_out.write(line.rstrip('\n')+'@#$')
        if r.status_code != 200:
            print("[Error]: HTTP code " + str(r.status_code))
            f_out.write("[Error]: HTTP code " + str(r.status_code))
            f_out.write("\n")
            f_out.flush()
        else:
            f_out.write(r.text.split('\n')[0])
            #only first best match of names
            f_out.write("\n")
            f_out.flush()
            print(cnt)
            cnt = cnt+1

    f_out.close()
    f_in.close()
if __name__ == "__main__":
    SubmitPMIDList_BERN("./bern_drug_cui_sorted.txt")
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