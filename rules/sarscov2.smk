rule SC_mash:
    input:
        fa=expand(rules.gbk_to_fasta.output, acc=scov_accnums),
    output:
        "results/scov/mash_dist.csv",
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


rule SC_build:
    input:
        fa=lambda w: expand(rules.gbk_to_fasta.output, acc=scov_accnums),
    output:
        temp("results/scov/pangraph/raw-{opt}.json"),
    params:
        opt=lambda w: kernel[w.opt],
    shell:
        """
        pangraph build {params.opt} {input.fa} > {output}
        """


rule SC_polish:
    input:
        rules.SC_build.output,
    output:
        "results/scov/pangraph/polished-{opt}.json",
    params:
        opt=config["pangraph"]["polish-options"],
    conda:
        "../conda_env/pangraph.yml"
    shell:
        """
        pangraph polish {params.opt} {input} > {output}
        """


rule SC_export:
    input:
        rules.SC_polish.output,
    output:
        directory("results/covid/export/{opt}"),
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


rule SC_all:
    input:
        rules.SC_mash.output,
        expand(rules.SC_export.output, opt=kernel.keys()),
