import os
import magic
import detectIMG

from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
ALLOWED_MIME_TYPES = {'image/jpeg'}


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# 顯示網頁要跑的 html 介面
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return (
        '<!doctype html>'
        '<title>Upload File</title>'
        '<h1>以圖搜圖</h1>'
        '<form method="post" enctype="multipart/form-data" action="/upload">'
        '<input type="file" name="file">'
        '<input type="submit" value=" 搜尋">'
        '</form>'
    )


# 判斷上傳的檔案附檔名是否正確
def is_allowed_file(file):
    if '.' in file.filename:
        ext = file.filename.rsplit('.', 1)[1].lower()
    else:
        return False

    mime_type = magic.from_buffer(file.stream.read(), mime=True)
    if (
        mime_type in ALLOWED_MIME_TYPES and
        ext in ALLOWED_EXTENSIONS
    ):
        # move the cursor to the beginning
        file.stream.seek(0, 0)
        return True

    return False


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and is_allowed_file(file):
        # filename = secure_filename(file.filename)
        # file.save(os.path.join('/tmp', filename))
        result = detectIMG.detect(file.read())
        global imageResult
        imageResult = result.copy()   #複製result裡面的資料，如果result不見後  還是會有資料
        print(imageResult)

        return redirect(url_for('photo'))
    return redirect(url_for('index'))   #如過上面有東西有問題就會跑回去一開始的網頁


@app.route('/photo', methods=['GET'])
def photo():
    # 標題名稱
    titleName = '搜尋結果'
    srcHead = "static/tshirt/"      #圖片路徑位置

    # len()是要找公寓有幾層
    # imageResult[i]  是第幾層公寓
   
    for i in range(len(imageResult)):
        imageResult[i] = srcHead+imageResult[i]
        print(imageResult[i])   #用終端機看圖片路徑對不對

    return render_template('image2.html', len=len(imageResult), imageResult=imageResult, titleName=titleName)


# Main Function
if __name__ == "__main__":

    app.run(debug=True)  #執行index()在上面
