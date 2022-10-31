PG_config = config["pangraph"]
kernel = PG_config["kernel-options"]


wildcard_constraints:
    opt=f"({'|'.join(kernel.keys())})",


rule PG_build_pangraph:
    input:
        fa=lambda w: expand(rules.gbk_to_fasta.output.fa, acc=species_to_acc[w.species]),
    output:
        "results/pangraph/{species}/{opt}.json",
    params:
        opt=lambda w: kernel[w.opt],
    shell:
        """
        pangraph build {params.opt} {input.fa} > {output}
        """


rule PG_polish_pangraph:
    input:
        rules.PG_build_pangraph.output,
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


rule PG_all:
    input:
        expand(rules.PG_build_pangraph.output, species=species, opt=kernel.keys()),
        expand(rules.PG_polish_pangraph.output, species=species, opt=kernel.keys()),
