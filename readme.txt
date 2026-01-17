### baga comenzile astea pe rand in terminals

```shell
python -m venv .venv
```

```shell
.venv/Scripts/activate
```



```shell
pip install -r requirements.txt
```


### start db
#### !!! porneste docker desktop inainte !!!
```shell
docker-compose up -d
```

### genereaza tablele in baza de date
python model/init_db.py

