import subprocess

class CameraController:
    def __init__(self):
        self.preview_process = None  # To keep track of the preview subprocess

    def capture_image(self, filename):
        try:
            subprocess.run(["libcamera-still", "-o", filename], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error capturing image: {e}")

    def start_preview(self):
        print("Starting camera preview...")
        try:
            self.preview_process = subprocess.Popen(["libcamera-still", "-t", "0"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("Preview process started.")
        except Exception as e:
            print(f"Failed to start preview: {e}")

    def stop_preview(self):
        print("Stopping camera preview...")
        if self.preview_process:
            self.preview_process.terminate()
            print("Preview process terminated.")


