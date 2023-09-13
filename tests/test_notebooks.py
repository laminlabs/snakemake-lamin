from pathlib import Path

import nbproject_test as test


def test_notebooks():
    # assuming this is in the tests folder
    docs_folder = Path(__file__).parents[1] / "docs/"

    for check_folder in docs_folder.glob("./**"):
        if {"rna-seq-star-deseq2"} in check_folder:
            continue
        test.execute_notebooks(check_folder, write=True)
