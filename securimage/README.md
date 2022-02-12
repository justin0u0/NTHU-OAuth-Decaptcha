# Securimage

Source: https://www.phpcaptcha.org/

To start the server, run `./start.sh`.

To configurate the captcha generated, change the settings in the file `./src/index.php` then restart the server.

Once the server starts, run `curl -v -X GET localhost:8080 --output ~/Downloads/captcha.png`,
and the captcha will be downloaded and the code will be shown in the response header `X-Captcha-Code`.
