# Raspberry PiとOpenCVでWEB監視カメラを作成する

## はじめに

`Mac環境の記事ですが、Windows環境も同じ手順になります。環境依存の部分は読み替えてお試しください。`

### 目的

ブラウザにストリーミング動画を表示します。

この記事を最後まで読むと、次のことができるようになります。

| No.  | 概要     | キーワード |
| :--- | :------- | :--------- |
| 1    | REST API | Flask      |
| 2    | OpenCV   | cv2        |

### 完成イメージ

|                                                                     ストリーミング                                                                     |
| :----------------------------------------------------------------------------------------------------------------------------------------------------: |
| <img width="300" alt="IMG_4814.PNG" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/0360b91a-42c2-d94e-27ac-81ca9e09c1ad.png"> |

### 実行環境

| 環境                           | Ver.     |
| :----------------------------- | :------- |
| macOS Catalina                 | 10.15.6  |
| Raspberry Pi 4 Model B 4GB RAM | -        |
| Raspberry Pi OS (Raspbian)     | 10       |
| Python                         | 3.7.3    |
| Flask                          | 1.1.2    |
| opencv-python                  | 4.4.0.42 |

### ソースコード

実際に実装内容やソースコードを追いながら読むとより理解が深まるかと思います。是非ご活用ください。

[GitHub](https://github.com/nsuhara/raspi-streaming.git)

### 関連する記事

- [Raspberry PiのセットアップからPython環境のインストールまで](https://qiita.com/nsuhara/items/05a2b41d94ced1f54316)
- [Raspberry PiとPythonでリモコンカーを作成する](https://qiita.com/nsuhara/items/7970b5dfe95ea76c93d6)
- [Raspberry PiとPythonでLCD(16x2)ゲームを作成する](https://qiita.com/nsuhara/items/57105fd232feffbcd05c)

## Camera設定

### Raspberry Pi Software Configuration Tool起動

```command.sh
~$ sudo raspi-config
```

### Camera有効化

1. `5 Interfacing Options`を選択
2. `P1 Camera`を選択

### 再起動

```command.sh
~$ sudo reboot
```

## OpenCV依存関係

### HDF5

HDF5 is a file format and library for storing scientific data.

```command.sh
~$ sudo apt-get install -y libhdf5-dev libhdf5-serial-dev libhdf5-103
```

### ATLAS

ATLAS is an approach for the automatic generation and optimization of numerical software.

```command.sh
~$ sudo apt-get install -y libatlas-base-dev
```

### JasPer

JasPer is a collection of software (i.e., a library and application programs) for the coding and manipulation of images.

```command.sh
~$ sudo apt-get install -y libjasper-dev
```

## ハンズオン

### ダウンロード

```command.sh
~$ git clone https://github.com/nsuhara/raspi-streaming.git -b master
```

### セットアップ

```command.sh
~$ cd raspi-streaming
~$ python -m venv .venv
~$ source .venv/bin/activate
~$ pip install -r requirements.txt
~$ source config
```

### サービス起動

```command.sh
~$ flask run --host=0.0.0.0 --port=5000
```

### アクセス

```command.sh
~$ open "http://{host}:5000/raspi-streaming/api?process=front_end&request=app_form&secret_key=M7XvWE9fSFg3"
```

### サービス終了

```command.sh
~$ Control Key + C
```

## アプリ構成

```target.sh
/app
├── __init__.py
├── apis
│   ├── templates
│   │   └── app_form.html
│   └── views
│       ├── __init__.py
│       ├── back_end_handler.py
│       ├── camera.py
│       ├── front_end_handler.py
│       └── main_handler.py
├── common
│   ├── __init__.py
│   └── utility.py
├── config
│   ├── __init__.py
│   ├── localhost.py
│   └── production.py
└── run.py
```

## front-end

```target.sh
/app
└── apis
     ├── templates
     │   └── app_form.html
     └── views
         └── front_end_handler.py
```

### front-end制御

```front_end_handler.py
"""app/apis/views/front_end_handler.py
"""
from flask import jsonify, render_template

from app import secret_key


def handler(req):
    """handler
    """
    param1 = req.get('param1')
    param2 = req.get('param2')

    if param1 == 'app_form':
        return _app_form(req=param2)

    return jsonify({'message': 'no route matched with those values'}), 200


def _app_form(req):
    """_app_form
    """
    if req.get('secret_key', '') != secret_key:
        return jsonify({'message': 'no route matched with those values'}), 200
    return render_template('app_form.html', secret_key=req.get('secret_key', ''))
```

### front-endレイアウト

```app_form.html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>raspi-streaming</title>

    <style type="text/css">
        html,
        body {
            -webkit-user-select: none;
            width: 100%;
            height: 100%;
        }

        table {
            width: 100%;
            height: 100%;
        }

        table,
        td {
            border: 1px gray solid;
            padding: 10px;
        }

        img.img-option {
            width: 100%;
            /* height: 100%; */
        }
    </style>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script type="text/javascript">
    // nothing to do
    </script>
</head>

<body>
    <table>
        <tr height="5%">
            <td>
                <h1>raspi-streaming</h1>
            </td>
        </tr>
        <tr>
            <td>
                <img class="img-option"
                    src="{{ url_for('raspi-streaming.api', process='back_end', request='video_feed', secret_key=secret_key) }}">
            </td>
        </tr>
    </table>
</body>

</html>
```

## back-end

```target.sh
/app
└── apis
     └── views
         ├── back_end_handler.py
         └── camera.py
```

### back-end制御

```back_end_handler.py
"""app/apis/views/back_end_handler.py
"""
from flask import Response, jsonify

from app import secret_key
from app.apis.views.camera import Camera


def handler(req):
    """handler
    """
    param1 = req.get('param1')
    param2 = req.get('param2')

    if param1 == 'video_feed':
        return _video_feed(req=param2)

    return jsonify({'message': 'no route matched with those values'}), 200


def _video_feed(req):
    """_video_feed
    """
    if req.get('secret_key', '') != secret_key:
        return jsonify({'message': 'no route matched with those values'}), 200
    return Response(_generator(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')


def _generator(camera):
    """_generator
    """
    while True:
        frame = camera.frame()
        yield b'--frame\r\n'
        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
```

### カメラ制御

```camera.py
"""app/apis/views/camera.py
"""
import cv2


class Camera():
    """Camera
    """

    def __init__(self):
        self.video_capture = cv2.VideoCapture(-1)

    def __del__(self):
        self.video_capture.release()

    def frame(self):
        """frame
        """
        _, frame = self.video_capture.read()
        _, image = cv2.imencode('.jpeg', frame)
        return image.tobytes()
```
