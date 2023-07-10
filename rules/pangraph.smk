import os

PG_config = config["pangraph"]
kernel = PG_config["kernel-options"]


wildcard_constraints:
    opt=f"({'|'.join(kernel.keys())})",


rule PG_mash:
    input:
        fa=lambda w: expand(rules.gbk_to_fasta.output.fa, acc=species_to_acc[w.species]),
    output:
        "results/mash_triangle/{species}.csv",
    conda:
        "../conda_env/bioinfo.yml"
    params:
        opt=config["mash-opt"],
    shell:
        """
        mash triangle {params.opt} {input.fa} > {output}.temp
        python3 scripts/mash_to_csv.py --mash_tri {output}.temp --csv {output}
        rm {output}.temp
        """


rule PG_build:
    input:
        fa=lambda w: expand(rules.gbk_to_fasta.output.fa, acc=species_to_acc[w.species]),
    output:
        temp("results/pangraph/{species}/{opt}.json"),
    params:
        opt=lambda w: kernel[w.opt],
    shell:
        """
        pangraph build --circular {params.opt} {input.fa} > {output}
        """


rule PG_polish:
    input:
        rules.PG_build.output,
    output:
        "results/pangraph/{species}/{opt}-polished.json",
    params:
        opt=PG_config["polish-options"],
    conda:
        "../conda_env/pangraph.yml"
    shell:
        """
        pangraph polish {params.opt} {input} > {output}
        """


rule PG_export:
    input:
        rules.PG_polish.output,
    output:
        directory("results/gfa/{species}/{opt}"),
    conda:
        "../conda_env/pangraph.yml"
    shell:
        """
        pangraph export \
            --no-duplications \
            --edge-minimum-length 0 \
            --output-directory {output} \
            --prefix export \
            {input}
        """


rule PG_fig_bandage:
    input:
        rules.PG_export.output,
    output:
        "figures/pangraph/{species}/{opt}-bandage.png",
    conda:
        "../conda_env/bioinfo.yml"
    shell:
        """
        bandage image \
            {input}/export.gfa \
            {output} \
            --scope entire \
            --colour depth \
        """


rule PG_corealn:
    input:
        rules.PG_polish.output,
    output:
        "results/pangraph/{species}/corealn-{opt}.fa",
    conda:
        "../conda_env/bioinfo.yml"
    shell:
        """
        python3 scripts/core_genome_aln.py \
            --pangraph {input} \
            --aln {output} 
        """


rule PG_coretree:
    input:
        rules.PG_corealn.output,
    output:
        "results/pangraph/{species}/coretree-{opt}.nwk",
    conda:
        "../conda_env/bioinfo.yml"
    shell:
        """
        fasttree -gtr -nt {input} > {output}
        """


rule PG_fig_mash:
    input:
        mash=rules.PG_mash.output,
        tree=rules.PG_coretree.output,
    output:
        "figures/pangraph/{species}/{opt}-mash_dist.png",
    conda:
        "../conda_env/bioinfo.yml"
    shell:
        """
        python3 scripts/plot_mash_dist.py \
            --mash {input.mash} \
            --tree {input.tree} \
            --fig {output}
        """


rule PG_fig_mosaic:
    input:
        tree=rules.PG_coretree.output,
        pan=rules.PG_polish.output,
    output:
        "figures/pangraph/{species}/{opt}-mosaic.png",
    conda:
        "../conda_env/bioinfo.yml"
    shell:
        """
        python3 scripts/plot_mosaic.py \
            --tree {input.tree} \
            --pan {input.pan} \
            --fig {output}
        """


rule PG_all:
    input:
        expand(rules.PG_mash.output, species=species),
        expand(rules.PG_polish.output, species=species, opt=kernel.keys()),
        expand(rules.PG_export.output, species=species, opt=kernel.keys()),
        expand(rules.PG_coretree.output, species=species, opt=kernel.keys()),
        expand(rules.PG_fig_mash.output, species=species, opt=kernel.keys()),
        expand(rules.PG_fig_mosaic.output, species=species, opt=kernel.keys()),
        expand(rules.PG_fig_bandage.output, species=species, opt=kernel.keys()),
