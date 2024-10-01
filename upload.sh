source .bashrc

# Upload the dataset for inference
s3cmd put /data/dataset.csv s3://${BUCKET_NAME}/dataset.csv

# Upload the model for inference
s3cmd put /models/model.joblib s3://${BUCKET_NAME}/model.joblib