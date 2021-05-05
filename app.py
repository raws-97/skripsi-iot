from flask import Flask, render_template, url_for, request
from engine import read_finger_data, get_finger_image, searchDosen, registerFingerAPI
import time
import math

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/scanning')
def finger_image():
    get_finger_image()
    return render_template("get_finger.html")

@app.route('/finger')
def get_finger():
    
    result = read_finger_data()
    data = result['data']
    code = data['kode']
    name = data['nama_dosen']
    date = data['tanggal']
    hour = data['jam']
    msg  = data['pesan']

    jadwal = data['jadwal']
    periode = jadwal['periode']
    nama_hari = jadwal['nama_hari']
    tanggal_mengajar = jadwal['tanggal_mengajar']
    kode_semester = jadwal['kode_semester']
    kelas = jadwal['kelas']
    nama_matakuliah = jadwal['nama_matakuliah']
    nama_kampus = jadwal['nama_kampus']
    ruang = jadwal['ruang']
    keterangan_jam = jadwal['keterangan_jam']
    absen_telat = jadwal['absen_telat']

    finger = result['finger']
    photo = result['lecturer_photo']

    if msg == "Sidik jari tidak ditemukan. Apakah anda ada jadwal hari ini ?":
        return render_template('not_found.html')
    else :
        return render_template('check.html', kode=code, nama_dosen=name, tanggal=date, jam=hour, pesan=msg,
         periode=periode, nama_hari=nama_hari, tanggal_mengajar=tanggal_mengajar,
        kode_semester=kode_semester, kelas=kelas, nama_matakuliah=nama_matakuliah, nama_kampus=nama_kampus,
        ruang=ruang, keterangan_jam=keterangan_jam, absen_telat=absen_telat,photo=photo)


@app.route('/register', methods=['GET'])
def register():
    return render_template('searchDosen.html')


@app.route('/search', methods=['POST'])
def loadTable():
    dosenId = request.form['id']

    req = searchDosen(dosenId)
    result = req['data']
    return render_template('listDosen.html', result=result)


@app.route('/result')
def loadForm():
    dosenId = request.args.get('id')

    req = searchDosen(dosenId)
    result = req['data'][0]
    kode = result['id_dosen']
    nama = result['nama_dosen']
    fakultas = result['nama_fakultas']
    prodi = result['nama_prodi']
    return render_template('registration.html', kode=kode, nama=nama, fakultas=fakultas, prodi=prodi)

@app.route('/daftarFinger', methods=['GET','POST'])
def inputData():
    dosenId = request.form['id']
    req = searchDosen(dosenId)
    result = req['data'][0]
    nama = result['nama_dosen']

    commit = registerFingerAPI(result)


    return render_template('successRegister.html', nama=nama)

@app.route('/success')
def successPage():
    return render_template('404.html')

@app.route('/shutdown', methods=['GET'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return render_template('shutdown.html')

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.errorhandler(405)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('405.html'), 405

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')