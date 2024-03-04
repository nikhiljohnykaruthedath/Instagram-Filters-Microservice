# Instagram Filters Microservice

Features: 
- User can authenticate themselves using MySQL and JWT
- User can then upload an image along with the instagram filter they would want to apply
- When the editing is complete, the user will receive a email notification to a link id
- User can then use that link id and download the edited image

## Setup
### 1. Setup docker, kubernetes, minikube
### 2. Deploy each microservice to docker hub
### 3. Setup minikube and kubernetes to pull docker images and apply the manifests

## Usage
Run the below commands in sequence:
```
curl -X POST http://editimage.com/login -u <Email>:<Password>
```
```
curl -X POST -F 'file=@./picture1.jpg' -H 'Authorization: Bearer <JWT Token>' http://editimage.com/upload?filter_type=aden
```
```
curl -X POST -F 'file=@./picture2.jpg' -H 'Authorization: Bearer <JWT Token>' http://editimage.com/upload?filter_type=dogpatch
```
```
curl --output picture2_dogpatch.jpg -X GET -H 'Authorization: Bearer <JWT Token>' http://editimage.com/download?fid=<Email Link ID>
```
