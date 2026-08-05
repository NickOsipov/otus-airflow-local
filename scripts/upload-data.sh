#!/bin/bash

source .env

s3cmd put --recursive data/test.csv s3://$BUCKET_NAME/test.csv
