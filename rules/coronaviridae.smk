
rule CV_mash:
    input:
        fa=expand(rules.gbk_to_fasta.output, acc=cov_accnums),
    output:
        "results/covid/mash_dist.csv",
    conda:
        "../conda_env/bioinfo.yml"
    params:
        opt=GC_config["mash-opt"],
    shell:
        """
        mash triangle {params.opt} {input.fa} > {output}.temp
        python3 scripts/mash_to_csv.py --mash_tri {output}.temp --csv {output}
        rm {output}.temp
        """


kernel = config["pangraph"]["kernel-options"]


rule CV_build:
    input:
        fa=lambda w: expand(rules.gbk_to_fasta.output, acc=cov_genus_acc[w.genus]),
    output:
        temp("results/covid/pangraph/{genus}-raw-{opt}.json"),
    params:
        opt=lambda w: kernel[w.opt],
    shell:
        """
        pangraph build {params.opt} {input.fa} > {output}
        """


rule CV_polish:
    input:
        rules.CV_build.output,
    output:
        "results/covid/pangraph/{genus}-polished-{opt}.json",
    params:
        opt=config["pangraph"]["polish-options"],
    conda:
        "../conda_env/pangraph.yml"
    shell:
        """
        pangraph polish {params.opt} {input} > {output}
        """


rule CV_export:
    input:
        rules.CV_polish.output,
    output:
        directory("results/covid/export/{genus}-{opt}"),
    conda:
        "../conda_env/pangraph.yml"
    shell:
        """
        pangraph export \
            --no-duplications \
            --output-directory {output} \
            --prefix export \
            {input}
        """


rule CV_all:
    input:
        rules.CV_mash.output,
        expand(rules.CV_export.output, opt=kernel.keys(), genus=cov_genus_acc.keys()),
