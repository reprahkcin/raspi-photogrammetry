import os

class FileManager:
    def __init__(self, base_dir, stacks_per_revolution, shots_per_stack):
        self.base_dir = base_dir
        self.stacks_per_revolution = stacks_per_revolution
        self.shots_per_stack = shots_per_stack
        self.angle_increment = 360 // stacks_per_revolution

    def create_folders(self):
        for i in range(self.stacks_per_revolution):
            angle = i * self.angle_increment
            folder_name = f"Angle_{angle:03d}"
            folder_path = os.path.join(self.base_dir, folder_name)
            os.makedirs(folder_path, exist_ok=True)

    def get_shot_filename(self, stack_index, shot_index):
        angle = stack_index * self.angle_increment
        folder_name = f"Angle_{angle:03d}"
        file_name = f"Shot_{shot_index:02d}.jpg"
        return os.path.join(self.base_dir, folder_name, file_name)
