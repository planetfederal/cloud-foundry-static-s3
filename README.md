# Simple S3 backed static files server

Python implementation of a simple Cloud Foundry application that serves static
files from an S3 bucket.

## Features

The application provides a simple web server that proxies calls to an S3 bucket
in order to serve static files from the bucket.

The application automatically serves an `index.html` file if found in a folder
and has a simple directory index functionality.

## Prerequisites

An AWS S3 bucket and AWS credentials to access that bucket.

## Installation

You can either directly edit the `manifest.yml` file or use the `deploy.sh`
script provided in the main folder, the script replaces the bucket name and the
AWS credentials in the `manifest.yml` file and then pushes the application to
PCF:

```
Usage: deploy.sh S3_BUCKET_NAME AWS_ACCESS_KEY AWS_SECRET_KEY
```

## Caching

Caching is not yet implemented, but can be easily added by using memcached or
Redis cloud.
