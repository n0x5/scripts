# Watchdog script to create a post with an image in wordpress when a file is detected in upload directory

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from datetime import date


def process_new_file(path):
    print(f"New file: {path}")
    today = date.today()
    d2 = today.strftime("%B %d %Y, %I:%M%p")
    os.chdir("/home/coax/websites/secondsight/images")
    os.system('wp post create --post_status="publish" --post_category="13" --post_title="{}" --post_content="[gallery ids=\'$(wp media import {} --porcelain)\' size=\'medium\']"' .format('Image blog '+d2, path))


class Watcher:
    DIRECTORY_TO_WATCH = "/home/coax/websites/secondsight/images"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()

class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            time.sleep(5)
            process_new_file(event.src_path)

        elif event.event_type == 'modified':
            pass

if __name__ == '__main__':
    w = Watcher()
    w.run()

