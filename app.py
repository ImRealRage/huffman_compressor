import os
import glob
from flask import Flask, render_template, request, send_file

# Configure Application
app = Flask(__name__)

# Global variables
filename = ""
ftype = ""

@app.route("/")
def home():
    # Delete old files
    for file_list in [glob.glob('uploads/*'), glob.glob('downloads/*')]:
        for f in file_list:
            os.remove(f)
    return render_template("home.html")

app.config["FILE_UPLOADS"] = "/home/shubh/Desktop/test_0/Huffman_Coding/uploads"

@app.route("/compress", methods=["GET", "POST"])
def compress():
    global filename, ftype

    if request.method == "GET":
        return render_template("compress.html", check=0)
    else:
        up_file = request.files["file"]

        if len(up_file.filename) > 0:
            filename = up_file.filename
            up_file.save(os.path.join(app.config["FILE_UPLOADS"], filename))
            os.system('./c uploads/{}'.format(filename))
            filename = filename[:filename.index(".", 1)]
            ftype = "-compressed.bin"

            while True:
                if 'uploads/{}-compressed.bin'.format(filename) in glob.glob('uploads/*-compressed.bin'):
                    os.system('mv uploads/{}-compressed.bin downloads/'.format(filename))
                    break

            return render_template("compress.html", check=1)
        else:
            print("ERROR")
            return render_template("compress.html", check=-1)

@app.route("/decompress", methods=["GET", "POST"])
def decompress():
    global filename, ftype

    if request.method == "GET":
        return render_template("decompress.html", check=0)
    else:
        up_file = request.files["file"]

        if len(up_file.filename) > 0:
            filename = up_file.filename
            up_file.save(os.path.join(app.config["FILE_UPLOADS"], filename))
            os.system('./d uploads/{}'.format(filename))
            with open('uploads/{}'.format(filename), 'rb') as f:
                ftype = "-decompressed." + f.read(int(f.read(1))).decode("utf-8")
            filename = filename[:filename.index("-", 1)]

            while True:
                if 'uploads/{}{}'.format(filename, ftype) in glob.glob('uploads/*-decompressed.*'):
                    os.system('mv uploads/{}{} downloads/'.format(filename, ftype))
                    break

            return render_template("decompress.html", check=1)
        else:
            print("ERROR")
            return render_template("decompress.html", check=-1)

@app.route("/home/shubh/Desktop/test_0/Huffman_Coding/downloads")
def download_file():
    global filename, ftype
    path = "/home/shubh/Desktop/test_0/Huffman_Coding/downloads" + filename + ftype
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

