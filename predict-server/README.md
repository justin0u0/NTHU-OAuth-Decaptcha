# Local Development

To start server locally, run:

```bash
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r requirements.txt

export FLASK_APP=server
export FLASK_ENV=development
flask run
```

# Deploy to Heroku

Since our server is inside subdirectory of a Git repository. So we need a little more works to deploy the APP to Heroku.

References:
- https://realpython.com/flask-by-example-part-1-project-setup/
- https://github.com/timanovsky/subdir-heroku-buildpack
- https://stackoverflow.com/questions/39197334/automated-heroku-deploy-from-subfolder

```bash
heroku create nthu-oauth-decaptcha
```

Also, `tensorflow` is too big for a Heroku application that will exceed the 500MB limit of the slug size. So need to install `tensorflow-cpu` instead.

Reference:
- https://stackoverflow.com/questions/61191925/install-tensorflow-2-x-only-for-cpu-using-pip
- https://devcenter.heroku.com/articles/slug-compiler#slug-size
- https://www.tensorflow.org/install/pip#package-location
