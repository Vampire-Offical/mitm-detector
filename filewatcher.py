from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from plyer import notification

def notify_sender():
    notification.notify(
            title = 'Critical',
            message = 'unkown activity is detected in your network',
            app_icon = "/etc/mitm/error.ico",
            timeout = 10,
    )



class FileModifiedHandler(FileSystemEventHandler):

    def __init__(self, path, file_name, callback):
        self.file_name = file_name
        self.callback = callback

        # set observer to watch for changes in the directory
        self.observer = Observer()
        self.observer.schedule(self, path, recursive=False)
        self.observer.start()
        self.observer.join()

    def on_modified(self, event):
        # only act on the change that we're looking for
        if not event.is_directory and event.src_path.endswith(self.file_name):
            self.observer.stop() # stop watching
            self.callback() # call callback


from sys import argv, exit
import os

if __name__ == '__main__':
    while True:
        def callback():
            notify_sender()
            # os.system('notify-send "unkown activity is detected in your network"')
        FileModifiedHandler('/tmp', 'arp_detect.txt', callback)
