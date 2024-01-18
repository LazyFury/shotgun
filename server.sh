# current dir
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo dir: $DIR

WORKDIR=$DIR/backend
export PYTHONPATH=$DIR
echo workdir: $WORKDIR

cd $WORKDIR
poetry install --no-root

DEFAULT_PORT=8000
# if env replace 
if [ -n "$PORT" ]; then
    DEFAULT_PORT=$PORT
fi
# poetry run python -m uvicorn backend.asgi:app --reload
uvicorn() {
    poetry run python -m uvicorn backend.asgi:app --reload --port ${DEFAULT_PORT}
}

runserver() {
    poetry run ./manage.py runserver
}

if [ "$1" == "uvicorn" ]; then
    uvicorn
    exit 0
fi

if [ "$1" == "dev" ]; then
    runserver
    exit 0
fi

# has no argument
if [ $# -eq 0 ]; then
    uvicorn
    exit 0
fi
