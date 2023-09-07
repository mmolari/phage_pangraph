rule FL_mash:
    input:
        fa=expand(rules.gbk_to_fasta.output, acc=flu_accnums),
    output:
        "results/flu/mash_dist.csv",
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


rule FL_build:
    input:
        fa=lambda w: expand(rules.gbk_to_fasta.output, acc=flu_accnums),
    output:
        temp("results/flu/pangraph/raw-{opt}.json"),
    params:
        opt=lambda w: kernel[w.opt],
    shell:
        """
        pangraph build {params.opt} {input.fa} > {output}
        """


rule FL_polish:
    input:
        rules.FL_build.output,
    output:
        "results/flu/pangraph/polished-{opt}.json",
    params:
        opt=config["pangraph"]["polish-options"],
    conda:
        "../conda_env/pangraph.yml"
    shell:
        """
        pangraph polish {params.opt} {input} > {output}
        """


rule FL_export:
    input:
        rules.FL_polish.output,
    output:
        directory("results/flu/export/{opt}"),
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


rule FL_fig_bandage:
    input:
        rules.FL_export.output,
    output:
        "figures/flu/{opt}-bandage.png",
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


rule FL_corealn:
    input:
        rules.FL_polish.output,
    output:
        "results/flu/tree/corealn-{opt}.fa",
    conda:
        "../conda_env/bioinfo.yml"
    shell:
        """
        python3 scripts/core_genome_aln.py \
            --pangraph {input} \
            --aln {output} 
        """


rule FL_coretree:
    input:
        rules.FL_corealn.output,
    output:
        "results/flu/tree/coretree-{opt}.nwk",
    conda:
        "../conda_env/bioinfo.yml"
    shell:
        """
        fasttree -gtr -nt {input} > {output}
        """


rule FL_fig_mash:
    input:
        mash=rules.FL_mash.output,
        tree=rules.FL_coretree.output,
    output:
        "figures/flu/{opt}-mash_dist.png",
    conda:
        "../conda_env/bioinfo.yml"
    shell:
        """
        python3 scripts/plot_mash_dist.py \
            --mash {input.mash} \
            --tree {input.tree} \
            --fig {output}
        """


rule FL_fig_mash_simple:
    input:
        mash=rules.FL_mash.output,
    output:
        "figures/flu/{opt}-mash_dist_simple.png",
    conda:
        "../conda_env/bioinfo.yml"
    shell:
        """
        python3 scripts/plot_mash_simple.py \
            --mash {input.mash} \
            --fig {output}
        """


rule FL_fig_mosaic:
    input:
        tree=rules.FL_coretree.output,
        pan=rules.FL_polish.output,
    output:
        "figures/flu/{opt}-mosaic.png",
    conda:
        "../conda_env/bioinfo.yml"
    shell:
        """
        python3 scripts/plot_mosaic.py \
            --tree {input.tree} \
            --pan {input.pan} \
            --fig {output}
        """


rule FL_all:
    input:
        rules.FL_mash.output,
        expand(rules.FL_export.output, opt=kernel.keys()),
        expand(rules.FL_coretree.output, opt=kernel.keys()),
        expand(rules.FL_fig_mash.output, opt=kernel.keys()),
        expand(rules.FL_fig_mash_simple.output, opt=kernel.keys()),
        expand(rules.FL_fig_mosaic.output, opt=kernel.keys()),
        expand(rules.FL_fig_bandage.output, opt=kernel.keys()),
