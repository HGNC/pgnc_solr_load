echo "Transfer data to solr" 2>&1 | tee output.log
python ./data-update/main.py --clear 2>&1 | tee -a output.log
echo "Transfer data to dump file" 2>&1 | tee -a output.log
python ./data-update/main.py --dump 2>&1 | tee -a output.log