import threading
import urllib.request
import time
from queue import Queue

class Downloader:
    def __init__(self, max_threads=4):
        self.max_threads = max_threads
        self.queue = Queue()
        self.lock = threading.Lock()

    def download_file(self, url, filename):
        """Download a single file and save it"""
        try:
            urllib.request.urlretrieve(url, filename)
            with self.lock:
                print(f"Downloaded {filename} from {url}")
        except Exception as e:
            with self.lock:
                print(f"Failed to download {url}: {str(e)}")

    def worker(self):
        """Worker thread that processes download tasks"""
        while True:
            url, filename = self.queue.get()
            self.download_file(url, filename)
            self.queue.task_done()

    def start_downloads(self, download_list):
        """Start the download process with multiple threads"""
        for url, filename in download_list:
            self.queue.put((url, filename))

        for _ in range(self.max_threads):
            t = threading.Thread(target=self.worker, daemon=True)
            t.start()

        self.queue.join()

if __name__ == "__main__":
    files_to_download = [
        ("https://example.com/file1.zip", "file1.zip"),
        ("https://example.com/file2.pdf", "file2.pdf"),
        ("https://example.com/image.jpg", "image.jpg"),
        ("https://example.com/document.docx", "document.docx"),
    ]

    print("Starting concurrent downloads...")
    start_time = time.time()

    downloader = Downloader(max_threads=4)
    downloader.start_downloads(files_to_download)

    end_time = time.time()
    print(f"All downloads completed in {end_time - start_time:.2f} seconds")