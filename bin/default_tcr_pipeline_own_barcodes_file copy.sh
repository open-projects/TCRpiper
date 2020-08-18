
echo "USAGE: ./default_tcr_pipeline.sh <dir_name> <run_name>"
echo "the <dir_name> director should contain barcodes and sample info files"
echo "they should be named 'barcodes_<run_name>'.txt and 'sample_info_<run_name>'.txt"

##############you can change path auxiliary scripts dir here#######
script_dir=./
###################################################################

#enter run dir
cd $1

# make init files 
barcodes="barcodes_"$2".txt"
sample_info="sample_info_"$2".txt"
sample_info_unix="sample_info_"$2".unix.txt"
tr '\r' '\n' < $sample_info > $sample_info_unix
#awk 'BEGIN {FS="\t";OFS="\t";} { print $1,$3,"",$4,$5}' "$sample_info_unix" | tail -n +2 | sort | uniq > "$barcodes"
#cut -f-1,3-6 < "$sample_info_unix" | tail -n +2 | sort | uniq > "$barcodes" 

# define output dirs
checkout="checkout"
histogram="histogram"
assemble="assemble"
analyze="analyze"
vdj="vdj"
enr="ENR"
qc="runQC"


# migec
migec CheckoutBatch -cute $barcodes $checkout
migec Histogram $checkout $histogram
Rscript ../migec_histogram_batch.R histogram
migec AssembleBatch -c $checkout $histogram $assemble
#migec AssembleBatch -c --force-overseq 1 $checkout $histogram $assemble"_m1"

# mixcr using chain from info file
mkdir "$analyze"
rm analyze/*.report
mkdir "$vdj"
j=1
while IFS='' read -r line || [[ -n "$line" ]]; do
    test $j -eq 1 && ((j=j+1)) && continue
    echo "Text read from file: $line"
    IFS=$'\t' read -ra ADDR <<< "$line"
    sample="${ADDR[0]}"
    chain="${ADDR[1]}"
    echo $sample "$chain"
    mixcr analyze amplicon -s hsa --starting-material rna --5-end no-v-primers --3-end c-primers --adapters no-adapters --receptor-type "$chain" "$assemble"/"$sample"_R1.*.fastq.gz "$assemble"/"$sample"_R2.*fastq.gz "$analyze"/"$sample"
    vdjtools Convert -S mixcr "$analyze"/"$sample".clonotypes."$chain".txt "$vdj"/vdj
    vdjtools FilterNonFunctional "$vdj"/vdj."$sample".clonotypes."$chain".txt "$vdj"/nc
    python3 "$script_dir"/tcr_to_mysql.py "$vdj"/nc.vdj."$sample".clonotypes."$chain".txt $2 $sample $chain
done < "$sample_info_unix"

# run qC script
echo "now run quality control"
mkdir "$qc"
Rscript "$script_dir"/runQualityControl.R "$sample_info_unix" "$qc"

# run enr script using baseline column from info file
#echo "now performing ENRICHMENT"
#j=1
#while IFS='' read -r line || [[ -n "$line" ]]; do
#    test $j -eq 1 && ((j=j+1)) && continue
#    echo "Text read from file: $line"
#    IFS=$'\t' read -ra ADDR <<< "$line"
#    sample="${ADDR[0]}"
#    chain="${ADDR[1]}"
#    baseline="${ADDR[5]}"
#    echo $sample "$chain"
#    if [ $baseline != "" ]
#    then
#      mkdir "$enr"
#      Rscript "$script_dir"/tcr_enr_dotplot.R -i "$vdj" -d "$enr" -o "$sample" -v nc.vdj."$sample".clonotypes."$chain".txt nc.vdj."$baseline".clonotypes."$chain".txt 
#    fi
#done < "$sample_info_unix"
