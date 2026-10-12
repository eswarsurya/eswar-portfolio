#!/usr/bin/env python3
"""Archive, upload, list and safely restore directory backups in S3."""
import argparse
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
from datetime import datetime, timezone

def aws(*args):
    return subprocess.run(['aws', *args], check=True, text=True, capture_output=True).stdout.strip()

def make_archive(source: Path, archive: Path):
    source = source.resolve()
    if not source.is_dir():
        raise ValueError(f'Source must be an existing directory: {source}')
    with tarfile.open(archive, 'w:gz') as tar:
        tar.add(source, arcname=source.name)

def safe_extract(archive: Path, destination: Path):
    destination.mkdir(parents=True, exist_ok=True)
    root = destination.resolve()
    with tarfile.open(archive, 'r:gz') as tar:
        for member in tar.getmembers():
            target = (root / member.name).resolve()
            if target != root and root not in target.parents:
                raise ValueError(f'Unsafe archive path: {member.name}')
        tar.extractall(root, filter='data')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    b = sub.add_parser('backup'); b.add_argument('source', type=Path)
    sub.add_parser('list')
    r = sub.add_parser('restore'); r.add_argument('key'); r.add_argument('destination', type=Path)
    args = parser.parse_args()
    bucket = os.environ.get('BACKUP_BUCKET')
    if not bucket: parser.error('Set BACKUP_BUCKET to your private S3 bucket name')
    try:
        if args.command == 'backup':
            stamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H%M%SZ')
            with tempfile.TemporaryDirectory() as tmp:
                archive = Path(tmp) / (args.source.name + '.tar.gz')
                make_archive(args.source, archive)
                key = f'backups/{stamp}/{archive.name}'
                aws('s3', 'cp', str(archive), f's3://{bucket}/{key}', '--sse', 'AES256')
            print(f'Uploaded s3://{bucket}/{key}')
        elif args.command == 'list':
            print(aws('s3', 'ls', f's3://{bucket}/backups/', '--recursive'))
        elif args.command == 'restore':
            with tempfile.TemporaryDirectory() as tmp:
                archive = Path(tmp) / 'backup.tar.gz'
                aws('s3', 'cp', f's3://{bucket}/{args.key}', str(archive))
                safe_extract(archive, args.destination)
            print(f'Restored into {args.destination.resolve()}')
    except (subprocess.CalledProcessError, OSError, ValueError) as exc:
        parser.exit(1, f'Error: {exc}\n')

if __name__ == '__main__':
    main()