from flask import Flask, request, current_app, send_from_directory
import hashlib
import pymysql.cursors
from werkzeug.utils import secure_filename

import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "storage"
# Connect to the database
connection = pymysql.connect(host='0.0.0.0',
                             user='root',
                             password='Nek55tos',
                             database='vezdekod',
                             cursorclass = pymysql.cursors.DictCursor)

@app.route('/get/', methods=['GET'])
def get_image():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `url` FROM `images` WHERE `image_id`=%s"
            cursor.execute(sql, (request.args["image_id"]))
            result = cursor.fetchone()
            print(result)
            return send_from_directory(directory=current_app.root_path, path=result["url"])
    except Exception:
        return "Image not found"


@app.route('/upload/', methods=['POST'])
def upload_image():
    try:
        file = request.files['file']

        data = request.files['file'].read()
        m = hashlib.sha1(data)

        if "image" not in file.content_type:
            return "File not is image"

        hash_key_file = m.hexdigest()

        path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(hash_key_file + "." + file.content_type.split("/")[1]))
        file.seek(0)
        file.save(path)

        with connection.cursor() as cursor:
            sql_getImageId = "SELECT `url` FROM `images` WHERE `image_id`=%s"
            cursor.execute(sql_getImageId, (hash_key_file))
            result = cursor.fetchone()
            if result is None:
                sql = "INSERT INTO `images` (`image_id`, `url`) VALUES (%s, %s)"
                cursor.execute(sql, (hash_key_file, path))
                connection.commit()
        return hash_key_file
    except Exception:
        return "File upload error"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
