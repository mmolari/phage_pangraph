rule download_gbk:
    output:
        "raw_data/gbk/{acc}.gbk",
    conda:
        "../conda_env/bioinfo.yml"
    params:
        api=api_key,
    shell:
        """
        ncbi-acc-download {wildcards.acc} -e all -F genbank {params.api}
        mv {wildcards.acc}.gbk {output}
        """


rule gbk_to_fasta:
    input:
        gbk=rules.download_gbk.output,
    output:
        fa="raw_data/fa/{acc}.fa",
    conda:
        "../conda_env/bioinfo.yml"
    shell:
        """
        python3 scripts/gbk_to_fa.py --gbk {input.gbk} --fa {output.fa}
        """


rule download_all:
    input:
        expand(rules.gbk_to_fasta.output, acc=acc_list),
        expand(rules.gbk_to_fasta.output, acc=cov_accnums),
        expand(rules.gbk_to_fasta.output, acc=scov_accnums),
