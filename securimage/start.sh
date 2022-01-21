docker build -t secure-image-gen .

docker run -p 8080:80 secure-image-gen
