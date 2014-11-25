import grequests
import requests
import subprocess
import time


class Broadcaster(object):

    def __init__(self, ips):
        self.ips = ips
        self.screenshot_file = 'screenshot.jpg'

    def send_picture(self, filename):
        reqs = []
        s = requests.Session()
        for ip in self.ips:
            print('picture for {}'.format(ip))
            reqs.append(grequests.put('http://{}:7000/photo'.format(ip), data=open(filename, 'rb'), session=s))
        grequests.map(reqs)

    def mirror_desktop(self):
        s = requests.Session()
        subprocess.call(['scrot', self.screenshot_file])
        while True:
            reqs = []
            for ip in self.ips:
                reqs.append(grequests.put('http://{}:7000/photo'.format(ip), data=open(self.screenshot_file, 'rb'),
                            session=s))
            grequests.map(reqs)
            time.sleep(1)
            subprocess.call(['scrot', '--quality=50', self.screenshot_file])
        self.stop = False

    def stop(self):
        reqs = []
        s = requests.Session()
        for ip in self.ips:
            reqs.append(grequests.post('http://{}:7000/stop'.format(ip), session=s))
        grequests.map(reqs)
