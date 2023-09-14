import shutil
from pathlib import Path

import nbproject_test as test


def test_notebooks():
    # assuming this is in the tests folder
    docs_folder = Path(__file__).parents[1] / "docs/"

    for check_folder in docs_folder.glob("./**"):
        if "rna-seq-star-deseq2" in str(check_folder):
            continue
        test.execute_notebooks(check_folder, write=True)

    # Clean up unnecessary files
    shutil.rmtree(f"{docs_folder}/rna-seq-star-deseq2", ignore_errors=True)
