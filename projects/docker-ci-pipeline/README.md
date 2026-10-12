# Docker + GitHub Actions CI Pipeline

A small Python web service packaged with Docker and checked automatically by GitHub Actions. The workflow runs unit tests and builds a container image on pushes and pull requests.

## Local run
```bash
python -m unittest -v
docker build -t sample-health-api .
docker run --rm -p 8000:8000 sample-health-api
curl http://localhost:8000/health
```

## Pipeline
- Checkout source
- Set up Python
- Run unit tests
- Set up Docker Buildx
- Build the container image

The workflow builds the image but does not publish it to a registry or deploy to production. Registry publishing can be added later using repository secrets and least-privilege credentials.

## Validation
Run the commands above locally and inspect the GitHub Actions run after pushing to GitHub. Do not claim a successful workflow run until GitHub reports it passed.

## Security notes
- Uses a non-root container user.
- No credentials are committed.
- The container image is a demo and should be further hardened and scanned before production use.