GC_config = config["genome-comparison"]


rule GC_mash_dist:
    input:
        fa=expand(rules.gbk_to_fa.output.fa, acc=acc_list),
    output:
        "results/genome_comparisons/mash_triangle.txt",
    conda:
        "../conda_env/bioinfo.yml"
    params:
        opt=GC_config["mash-opt"],
    shell:
        """
        mash triangle {params.opt} {input.fa} > {output}
        """


# rule genome_size:


rule GC_all:
    input:
        rules.GC_mash_dist.output,
