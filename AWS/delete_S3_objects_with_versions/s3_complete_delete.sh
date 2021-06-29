#!/bin/bash

# Empty array for all ticket numbers
buckets=()
input="s3list.txt"

while IFS= read -r line
do
    buckets+=("$line")
done < "$input"

for bucket in "${buckets[@]}"
do

    aws s3api put-bucket-versioning --bucket ${bucket} --versioning-configuration Status=Suspended
    aws s3 rm s3://${bucket} --recursive
    python3 s3_delete.py "$bucket"
    aws s3api put-bucket-versioning --bucket ${bucket} --versioning-configuration Status=Enabled
done
