# pythonUserSystem

Here I used python to make the auth system.

It contains email-sending and jwt-auth system.

## Run
```bash
#restful
poetry run dev

#grpc
poetry run it

#test
poetry run test
```

## Help
You may need to install `grpc` manually in m1 macbook:

```bash
export GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=1
export GRPC_PYTHON_BUILD_SYSTEM_ZLIB=1
python -m pip install grpcio grpcio-tools
python -m pip install --pre "betterproto[compiler]"
```