---
execute_via: python
---

# Snakemake

```{warning}
This notebook is a demo for Python scripting that you could run before and after Snakemake runs.
Typically, you would include lamindb directly within your Snakemake workflow.
```

[Snakemake](https://snakemake.readthedocs.io) is a popular workflow manager in bioinformatics. This guide is based on the example of the [rna-seq-star-deseq2](https://github.com/snakemake-workflows/rna-seq-star-deseq2) pipeline.

First we clone the Snakemake pipeline with git. Because the test datasets come with the repo and, for simplicity, we want to avoid moving them into another directory, we initialize a LaminDB instance in the same directory.

```python
# pip install lamindb snakemake
!git clone https://github.com/snakemake-workflows/rna-seq-star-deseq2 --single-branch --branch v3.1.0
!lamin init --storage ./rna-seq-star-deseq2
```

```python
import lamindb as ln
```

## Registering inputs

```python
root_dir = "rna-seq-star-deseq2"
sample_sheet = ln.Artifact(f"{root_dir}/.test/config_basic/samples.tsv").save()
input_fastqs = ln.Artifact.from_dir(f"{root_dir}/.test/ngs-test-data/reads/")
ln.save(input_fastqs)
```

## Track a Snakemake run

Track the Snakemake workflow & run:

```python
transform = ln.Transform(
    key="snakemake-rna-seq-star-deseq2",
    version="2.0.0",
    type="pipeline",
    reference="https://github.com/snakemake-workflows/rna-seq-star-deseq2",
)
ln.track(transform)
```

If we call `cache()` on the input artifacts, they’ll be downloaded into a cache and tracked as run inputs. In this test case however, no download happened because the files are already available locally.

```python
input_sample_sheet_path = sample_sheet.cache()
input_paths = [input_fastq.cache() for input_fastq in input_fastqs]
```

Let's run the pipeline.

```python
!snakemake \
    --directory rna-seq-star-deseq2/.test \
    --snakefile rna-seq-star-deseq2/workflow/Snakefile \
    --configfile rna-seq-star-deseq2/.test/config_basic/config.yaml \
    --use-conda \
    --show-failed-logs \
    --cores 2 \
    --conda-frontend conda \
    --conda-cleanup-pkgs cache
```

## Registering outputs

<!-- #region pycharm={"name": "#%% md\n"} -->

Quality control.

<!-- #endregion -->

```python
multiqc_file = ln.Artifact(f"{root_dir}/.test/results/qc/multiqc_report.html").save()
```

<!-- #region -->

:::{dropdown} How would I register all QC files?

```python
multiqc_results = ln.Artifact.from_dir(f"{root_dir}/results/qc/multiqc_report_data/")
ln.save(multiqc_results)
```

:::

<!-- #endregion -->

<!-- #region pycharm={"name": "#%% md\n"} -->

Count matrix.

<!-- #endregion -->

```python
count_matrix = ln.Artifact(f"{root_dir}/.test/results/counts/all.symbol.tsv")
count_matrix.save()
```

## Visualize

View data lineage:

```python
count_matrix.view_lineage()
```

# Appendix

## Linking biological entities

To make the count matrix queryable by biological entities (genes, experimental metadata, etc.), we can now proceed with: {doc}`docs:bulkrna`

<!-- #region pycharm={"name": "#%% md\n"} -->

## Linking a Snakemake run ID

<!-- #endregion -->

Snakemake does not have an easily accessible ID that is associated with a run.
Therefore, we need to extract it from the log files.

```python
import pathlib
from datetime import datetime

PATH_TO_DOT_SNAKEMAKE_LOG = "rna-seq-star-deseq2/.test/.snakemake/log"
log_files_file_names = list(
    map(
        lambda lf: str(lf).split("/")[-1],
        list(pathlib.Path(PATH_TO_DOT_SNAKEMAKE_LOG).glob("*.snakemake.log")),
    )
)

timestamps = [
    datetime.strptime(filename.split(".")[0], "%Y-%m-%dT%H%M%S")
    for filename in log_files_file_names
]
snakemake_id = log_files_file_names[timestamps.index(max(timestamps))].split(".")[1]
```

Let us add the information about the session ID to our run record:

```python
run = ln.context.run  # let's grab the global run record
run.reference = snakemake_id
run.reference_type = "snakemake_id"
run.save()
```
