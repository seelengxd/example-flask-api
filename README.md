# sample flask api

## set up

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## running

```bash
# from folder just above backend
flask --app backend init-db
flask --app backend --debug run
```
