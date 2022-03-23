# pythonUserSystem

Here I used python to make the auth system.

It contains email-sending and jwt-auth system.

## Run
```bash
#restful
poetry run dev

#test
poetry run test
```

## Build
```bash
docker build --tag weloveparty_accountservice .

docker run --rm --name weloveparty_accountservice \
--mount type=bind,source="$(pwd)"/o365_token.txt,target=/code/o365_token.txt \
--volume $(pwd)/data:/code/data \
weloveparty_accountservice
```