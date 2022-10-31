GC_config = config["genome-comparison"]


rule GC_mash_dist:
    input:
        fa=lambda w: expand(rules.gbk_to_fasta.output.fa, acc=species_to_acc[w.species]),
    output:
        "results/mash_triangle/{species}.txt",
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
        expand(rules.GC_mash_dist.output, species=species),
