loom_dir=$1
tdigest_dir=$2
mkdir -p $tdigest_dir
for loom_file in $(ls $loom_dir); do
{  
    loom_filename=$(basename $loom_file)
    tdigest="${loom_filename%.*}.pickle"
    echo $tdigest
    python ./compute_tdigests.chunks.py $loom_dir/$loom_file $tdigest_dir/$tdigest 
} & 
done
wait 
