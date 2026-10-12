# AWS S3 Backup & Restore Lab

A Python utility to archive a local directory, upload the compressed archive to an Amazon S3 bucket with server-side encryption, list backups, and restore a selected archive.

## Requirements
- Python 3.11+
- AWS CLI v2 configured with a least-privilege identity
- A private S3 bucket with Block Public Access enabled

## Run
```bash
export BACKUP_BUCKET='your-private-bucket'
python backup_s3.py backup ./sample-data
python backup_s3.py list
python backup_s3.py restore 'backups/EXACT_KEY/sample-data.tar.gz' ./restore-output
python -m unittest -v
```

## Design & safety
- Uses a timestamped gzip tar archive and AWS CLI.
- Uploads with SSE-S3; use SSE-KMS and a suitable key policy where required.
- Does not create public buckets or embed AWS keys.
- Restore validates archive paths before extraction to mitigate path traversal.
- Configure lifecycle expiration/versioning in the bucket to suit retention requirements.
- AWS storage, requests and transfer may incur charges. Test with small data in a disposable bucket.

## Status
Starter project committed to source control. Before describing this as a verified live AWS deployment, run the unit tests and perform an end-to-end test in your own AWS account. Add redacted evidence of the run after validation.