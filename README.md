

### Setting up the environment and running the application

1. Check version of pip (version 3.6 and perhaps some lower versions should be fine)

``` bash
pip --version
```

2. Install `virtualenv`

``` bash
pip install virtualenv
```

3. Navigate into project directory and set up virtual environment

``` bash
virtualenv venv
```

4. Activate environment

``` bash
source venv/bin/activate
```

5. Install requirements

``` bash
pip install -r requirements.txt
```

6. Run application file

``` bash
python wsgi.py
```

