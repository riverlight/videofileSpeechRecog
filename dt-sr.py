import os
from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = '10751908'
API_KEY = 'WAfpD27380TGbVuOs92AySxk'
SECRET_KEY = 'R5OCC3jOpWNKfTarm44ZZ5EWCUcH0lQt'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def write_srtxt(txtFile, line):
    with open(txtFile, 'a+') as fp:
        fp.write(line)

def dt_sr(srcFile):
    speechSRate = 16000
    speechSAccu = 16
    buffer = get_file_content(srcFile)
    sizePerSec = int((speechSAccu / 8) * speechSRate)
    timeSec = int(len(buffer) / sizePerSec)
    timeMinute = int((timeSec + 59) / 60)
    print(timeMinute)

    for count in range(0, timeMinute):
        print(min((count + 1) * sizePerSec * 60, len(buffer)))
        speechBuffer = buffer[count * sizePerSec * 60: min((count + 1) * sizePerSec * 60, len(buffer))]
        result = client.asr(speechBuffer, 'pcm', 16000, {
            'lan': 'zh',
        })
        if (result['err_no'] == 0):
            print(result['result'])
            line = str(count)+':00'+"--"+str(count)+":59  " + result['result'][0] +'\n'
            write_srtxt(txtFile, line)
        else:
            # print(result)
            print("语音识别错误，错误码是: ", result['err_no'], " , 错误信息是：" + result['err_msg'])

dtVideoFile = "d:\\workroom\\testroom\\dt-program.mp4"
pcmFile = 'd:\\workroom\\testroom\\sr.raw'
txtFile = 'd:\\workroom\\testroom\\srtxt.txt'
cmd = "ffmpeg -i " + dtVideoFile + " -f s16le -ar 16000 -acodec pcm_s16le -b:a 16 -ac 1 -y " + pcmFile
os.system(cmd)
dt_sr(pcmFile)
