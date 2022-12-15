GC_config = config["genome-comparison"]


rule GC_mash_dist:
    input:
        fa=lambda w: expand(rules.gbk_to_fasta.output.fa, acc=species_to_acc[w.species]),
    output:
        "results/mash_triangle/{species}.csv",
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


# rule genome_size:


rule GC_all:
    input:
        expand(rules.GC_mash_dist.output, species=species),
