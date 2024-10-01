source .bashrc

# Create a storage bucket
# yc storage bucket create --name $BUCKET_NAME

# Create a service account
SA_ID=$(
    yc iam service-account create --name ${SA_NAME} \
        --description "Service account for DataProc" \
        --format json | jq -r .id
)

# Add the storage.editor role to the service account
yc resource-manager folder add-access-binding $FOLDER_ID \
    --role=storage.editor \
    --subject=serviceAccount:$SA_ID

# Create a key for the service account
yc iam access-key create --service-account-name=airflow-sa > airflow-sa.json