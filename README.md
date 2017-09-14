# biomCtrlFiltering

Giving a list of Sample ID corresponding to control samples, it removes OTU (or feature) from a TSV biom file higher than a given threshold.


Remove OTU by raw abundance:
```bash
biomCtrlFiltering.py -i otu_table.tsv -c ctrl_sample_1 -c ctrl_sample_2 -c ... -n 10
```

Remove OTU by frequency:
```bash
biomCtrlFiltering.py -i otu_table.tsv -c ctrl_sample_1 -c ctrl_sample_2 -c ... -f 0.1
```

Python library:
- argparse
- csv
- logging
