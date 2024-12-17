import os
import eel
from engine.features import *
from engine.command import *

eel.init('www')
eel.start('index.html', mode='chrome', host='127.0.0.1', block=True)

playAssistantSound()
os.system('start chrome.exe --app="http://127.0.0.1:8000/www/index.html"')
