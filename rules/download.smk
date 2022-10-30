import pandas as pd

df_acc = pd.read_csv(config["accession"])
acc_list = df_acc["genbank_accession"].to_list()


rule download_gbk:
    output:
        "raw_data/gbk/{acc}.gbk",
    conda:
        "../conda_env/bioinfo.yml"
    shell:
        """
        ncbi-acc-download {wildcards.acc} -e all -F genbank
        mv {wildcards.acc}.gbk {output}
        """


rule download_all:
    input:
        expand(rules.download_gbk.output, acc=acc_list),
