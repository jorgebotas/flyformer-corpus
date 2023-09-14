from collections import defaultdict
import loompy as lp
import sys
import pickle
from tdigest import TDigest
from tqdm import tqdm


# Global variables
PICKLE_CHUNK_SIZE = 100

def main():
    processed_loom = sys.argv[1]

    # Initialize TDigests and TDigest file pointer
    tdigests = defaultdict(TDigest)
    tdigest_fp = open(sys.argv[2], "wb")

    with lp.connect(processed_loom) as adata:
        genes = list(adata.ra.var_names)
        for idx, gene in enumerate(tqdm(genes)):
            gene_data = adata[idx, :]
            # Filter out zero values
            gene_data = gene_data[gene_data > 0]
            # Update TDigest for gene if gene_data is not empty
            if len(gene_data):
                tdigests[gene].batch_update(gene_data)

            # Update TDigest for gene if gene_data is not empty
            if len(tdigests.keys()) > PICKLE_CHUNK_SIZE:
                pickle.dump(tdigests, tdigest_fp)
                tdigests = defaultdict(TDigest)
    
    # Write residual tdigests if any
    if len(tdigests):
        pickle.dump(tdigests, tdigest_fp)

    # Close tdigest
    tdigest_fp.close()
    print("\nDONE!\n")

if __name__ == "__main__":
    main()
