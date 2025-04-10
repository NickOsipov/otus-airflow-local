source .bashrc

# Create a storage bucket
# yc storage bucket create --name $BUCKET_NAME

# Create a service account
SA_ID=$(
    yc iam service-account create --name ${SA_NAME} \
        --description "Service account for Storage" \
        --format json | jq -r .id
)

# Add the storage.editor role to the service account
yc resource-manager folder add-access-binding $FOLDER_ID \
    --role=storage.editor \
    --subject=serviceAccount:$SA_ID

# Create a key for the service account and get it in JSON format
yc iam access-key create --service-account-name=airflow-sa --format json > airflow-sa.json

# Extract access key and secret key from the JSON output directly using jq
ACCESS_KEY=$(jq -r .access_key.key_id airflow-sa.json)
SECRET_KEY=$(jq -r .secret airflow-sa.json)

# Create variables.json with the extracted values
cat > variables.json << EOL
{
  "YC_ACCESS_KEY": "$ACCESS_KEY",
  "YC_SECRET_KEY": "$SECRET_KEY",
  "YC_BUCKET_NAME": "$BUCKET_NAME"
}
EOL

yc storage bucket create --name $BUCKET_NAME
