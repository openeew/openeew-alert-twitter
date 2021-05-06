# openeew-alert-twitter

This repository contains a Dockerfile that can be used for local development.

To build an a docker image, from the root directory run the following:

```
docker build --tag alert-twitter:dev .
```

Modify the .env file with relevant information.

To then run this docker image execute the following command:

```
docker run \
  --interactive \
  --detach \
  --env-file .env \
  --name alert-twitter \
  alert-twitter:dev
```

**Formatter**

This repository is written in Python and runs Black on all Pull Request.

To install and run black formatter:

```
pip install black
black /path/to/file
```
