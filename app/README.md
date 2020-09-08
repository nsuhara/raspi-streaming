# raspi-streaming

## api

| service     | method | example                      |
| :---------- | :----- | :--------------------------- |
| healthcheck | get    | /raspi-streaming/healthcheck |
| api         | get    | /raspi-streaming/api         |

## front-end sample

| service  | method | example                                                                         |
| :------- | :----- | :------------------------------------------------------------------------------ |
| app form | get    | /raspi-streaming/api?process=front_end&request=app_form&secret_key=M7XvWE9fSFg3 |

## back-end sample

| service    | method | example                                                  |
| :--------- | :----- | :------------------------------------------------------- |
| video feed | get    | /raspi-streaming/api?process=back_end&request=video_feed |

## setup environment

```command_line.sh
source config
```

## check code

```command_line.sh
python -B -m pylint --rcfile=.pylintrc -f parseable `find app -name "*.py" -not -path "app/tests"`
```

## unit test

```command_line.sh
python -B -m unittest discover tests
```

## launch flask

```command_line.sh
source config
flask run --host=0.0.0.0 --port=5000
```
