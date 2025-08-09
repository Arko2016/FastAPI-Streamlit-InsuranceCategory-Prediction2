# Benefits of using --no-cache-dir with pip install in Dockerfile
Normally, pip caches downloaded package files (like .whl files) and built wheels in a dedicated cache directory, thereby avoiding subsequent  re-downloads and re-builds

However, the **--no-cache-dir** flag bypasses this caching behavior, meaning:
1) No downloaded files are stored: pip will not save a copy of the downloaded package files in its cache.
2) No locally built wheels are stored: If pip builds a wheel from a source distribution, that built wheel will not be added to the cache for future use

Reasons for using --no-cache-dir:
1) Reducing Docker image size:
In containerized environments like Docker, using --no-cache-dir prevents pip from adding cached files to the image layers, resulting in smaller, more efficient container images.
2) Ensuring fresh downloads:
It can be used to guarantee that pip always downloads the latest available versions of packages, even if older versions are present in a local cache

## Docker Commands to build, run, push and pull images
1) Ensure you are signed in to Dockerhub as well as Docker Desktop using same profile ID

2) Build the Docker Image (*in your local system*):
```
docker build -t <name of docker profile>/<name of the image> .
```
"-t": required to specify the tag for the image
"." enusres the images is bulit using the Dockerfile present
providing docker profile name at the start is recommended format to ensure uniqueness of the image created

3) Run the Docker Image to create Container (which is static instance of the Docker image)
```
docker run -d -p <docker app port as specified in Dockerfile>:<external port> <name of docker profile>/<name of the image> (*same as mentioned in step 2 above*)
``` 

"-d" ensures the applications runs in detached mode,  similar to a daemon process on a Linux system
"-p" tag to specify ports

4) Push the Docker Image to Docker Hub/ Registry:
- Login to Dockerhub
```
docker login
```
- Push the Image
```
docker push <name of docker profile>/<name of the image>
```

5) Pull the Docker Image from Dicker Hub:
```
docker pull <name of docker profile>/<name of the image>
```