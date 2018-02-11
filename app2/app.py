import os

from flask import Flask, render_template
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField


app = Flask(__name__)
app.config['SECRET_KEY'] = 'some hard word'
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()

# 初始化
photos = UploadSet('photos', IMAGES)
# 注册
configure_uploads(app, photos)
# patch_request_class(app, 32 * 1024 * 1024)  文件上传最大size, 默认16
patch_request_class(app)


class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, '只能上传图片!'), FileRequired('文件未选择')])
    submit = SubmitField('上传')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
    else:
        file_url = None
    return render_template('index.html', form=form, file_url=file_url)


if __name__ == '__main__':
    app.run()
