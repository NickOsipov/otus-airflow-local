source .bashrc

s3cmd put --recursive models/model.joblib s3://$BUCKET_NAME/model.joblib
