source .bashrc

s3cmd get s3://$BUCKET_NAME/predictions.csv data/predictions.csv --force
