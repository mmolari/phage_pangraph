rule SC_mash:
    input:
        fa=expand(rules.gbk_to_fasta.output, acc=scov_accnums),
    output:
        "results/scov/mash_dist.csv",
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
        directory("results/scov/export/{opt}"),
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


rule SC_corealn:
    input:
        rules.SC_polish.output,
    output:
        "results/scov/tree/corealn-{opt}.fa",
    conda:
        "../conda_env/bioinfo.yml"
    shell:
        """
        python3 scripts/core_genome_aln.py \
            --pangraph {input} \
            --aln {output} 
        """


rule SC_coretree:
    input:
        rules.SC_corealn.output,
    output:
        "results/scov/tree/coretree-{opt}.nwk",
    conda:
        "../conda_env/bioinfo.yml"
    shell:
        """
        fasttree -gtr -nt {input} > {output}
        """


rule SC_fig_mash:
    input:
        mash=rules.SC_mash.output,
        tree=rules.SC_coretree.output,
    output:
        "figures/scov/{opt}-mash_dist.png",
    conda:
        "../conda_env/bioinfo.yml"
    shell:
        """
        python3 scripts/plot_mash_dist.py \
            --mash {input.mash} \
            --tree {input.tree} \
            --fig {output}
        """


rule SC_fig_mosaic:
    input:
        tree=rules.SC_coretree.output,
        pan=rules.SC_polish.output,
    output:
        "figures/scov/{opt}-mosaic.png",
    conda:
        "../conda_env/bioinfo.yml"
    shell:
        """
        python3 scripts/plot_mosaic.py \
            --tree {input.tree} \
            --pan {input.pan} \
            --fig {output}
        """


rule SC_all:
    input:
        rules.SC_mash.output,
        expand(rules.SC_export.output, opt=kernel.keys()),
        expand(rules.SC_coretree.output, opt=kernel.keys()),
        expand(rules.SC_fig_mash.output, opt=kernel.keys()),
        expand(rules.SC_fig_mosaic.output, opt=kernel.keys()),
