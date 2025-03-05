rm -f /usr/src/app/output/done.flag solr.json
echo "Transfer data to solr" 2>&1 | tee output.log
python ./data-update/main.py --clear 2>&1 | tee -a output.log
echo "Transfer data to dump file" 2>&1 | tee -a output.log
python ./data-update/main.py --dump 2>&1 | tee -a output.log

if [ $? -eq 0 ]; then
  echo "Python script completed successfully."
  touch /usr/src/app/output/done.flag  # Create success flag
else
  echo "Python script failed."
fi

echo "Waiting for solr-client to complete..."
while [ ! -f /usr/src/app/output/solr-client-done.flag ]; do
  sleep 5
done

echo "solr-client completed. Stopping python container..."
exit 0  # Exits the container
