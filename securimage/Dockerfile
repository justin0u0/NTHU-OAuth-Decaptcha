FROM php:7.4-apache

RUN apt-get update && apt-get install -y libpng-dev 
RUN apt-get install -y \
    libwebp-dev \
    libjpeg62-turbo-dev \
    libpng-dev libxpm-dev \
    libfreetype6-dev

RUN docker-php-ext-configure gd --with-freetype --with-jpeg

RUN docker-php-ext-install gd

COPY src/ /var/www/html/
EXPOSE 80
