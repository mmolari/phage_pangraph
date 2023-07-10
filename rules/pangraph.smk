import os

PG_config = config["pangraph"]
kernel = PG_config["kernel-options"]


wildcard_constraints:
    opt=f"({'|'.join(kernel.keys())})",


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
            --output-directory {output} \
            --prefix export \
            {input}
        """


rule PG_all:
    input:
        expand(rules.PG_polish.output, species=species, opt=kernel.keys()),
        expand(rules.PG_export.output, species=species, opt=kernel.keys()),
