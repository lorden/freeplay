import sys
from PyQt4 import QtGui, QtCore
from broadcaster import Broadcaster
from zeroconf import ServiceBrowser, Zeroconf
import socket


class DeviceListener(object):

    devices = []

    def __init__(self, ui_app):
        self.ui_app = ui_app

    def addService(self, zeroconf, type, name):
        info = zeroconf.getServiceInfo(type, name)
        if info:
            name = info.getServer().split('.')[0]
            ip = socket.inet_ntoa(info.getAddress())
            print('{} => {}'.format(name, ip))
            self.devices.append((name, ip))
            self.ui_app.add_device(name, ip)


class MirrorThread(QtCore.QThread):
    def __init__(self, broadcaster):
        self.broadcaster = broadcaster
        QtCore.QThread.__init__(self)

    def run(self):
        self.broadcaster.mirror_desktop()


class BroadcasterUI(QtGui.QMainWindow):

    def __init__(self, devices={}):
        super(BroadcasterUI, self).__init__()
        self.devices = devices
        self.combo = QtGui.QComboBox(self)
        self.selected_device = None
        self.broadcaster = None
        self.mirrorThread = None

        self.initUI()

    def initUI(self):

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('FreePlay')
        self.setWindowIcon(QtGui.QIcon('tower.png'))
        self.center()

        btnPicture = QtGui.QPushButton('Picture', self)
        btnPicture.resize(btnPicture.sizeHint())
        btnPicture.move(120, 0)
        btnPicture.clicked.connect(self.select_picture)

        btnMirror = QtGui.QPushButton('Mirror', self)
        btnMirror.resize(btnMirror.sizeHint())
        btnMirror.move(120, 30)
        btnMirror.clicked.connect(self.mirror_screen)

        btnStop = QtGui.QPushButton('Stop', self)
        btnStop.resize(btnStop.sizeHint())
        btnStop.move(120, 60)
        btnStop.clicked.connect(self.stop)

        btnScan = QtGui.QPushButton('Scan', self)
        btnScan.resize(btnPicture.sizeHint())
        btnScan.move(120, 90)
        btnScan.clicked.connect(self.scan_devices)

        self.combo.addItem('Select device')
        self.combo.addItem('All')
        for dev in self.devices:
            self.combo.addItem(dev[0])
        self.combo.move(0, 0)

        self.statusBar().showMessage('Scanning...', 5000)
        self.show()

    def add_device(self, name, ip):
        self.devices[name] = ip
        self.combo.addItem(name, ip)

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def select_picture(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '~/Pictures')
        device_name = '{}'.format(self.combo.currentText())
        print(device_name)
        if device_name == 'All':
            device_ips = self.devices.values()
            bc = Broadcaster(device_ips)
        else:
            device_ip = self.devices[device_name]
            bc = Broadcaster([device_ip])
        bc.send_picture(filename)
        self.statusBar().showMessage('Picture sent')
        self.broadcaster = bc

    def init_device_combo(self):
        self.combo.clear()
        self.combo.addItem('Select device')
        self.combo.addItem('All')

    def scan_devices(self):
        self.statusBar().showMessage('Scanning...', 5000)
        self.init_device_combo()
        zeroconf = Zeroconf()
        listener = DeviceListener(self)
        ServiceBrowser(zeroconf, "_airplay._tcp.local.", listener)

    def mirror_screen(self):
        device_name = '{}'.format(self.combo.currentText())
        print(device_name)
        if device_name == 'All':
            device_ips = self.devices.values()
            bc = Broadcaster(device_ips)
        else:
            device_ip = self.devices[device_name]
            bc = Broadcaster([device_ip])
        self.statusBar().showMessage('Mirroring')
        self.mirrorThread = MirrorThread(bc)
        self.broadcaster = bc
        self.mirrorThread.start()

    def stop(self):
        print('terminating...')
        self.broadcaster.send_picture('/dev/null')
        self.mirrorThread.terminate()
        self.broadcaster.stop()

    def add(self):
        print('add')


def main():

    app = QtGui.QApplication(sys.argv)

    bc_ui = BroadcasterUI()
    zeroconf = Zeroconf()
    listener = DeviceListener(bc_ui)
    ServiceBrowser(zeroconf, "_airplay._tcp.local.", listener)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
