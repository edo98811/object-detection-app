import os
import json
import numpy as np
from PIL import Image, ImageTk
import pillow_heif
from pillow_heif import register_heif_opener
from objects_manager import ObjectLocations
from pathlib import Path

class ImageData:
    def __init__(self):
        """Initialize image data attributes."""
        self.image = None
        self.objects_manager:ObjectLocations = None
        self.image_name = None
        self.image_path = None
        self.source_folder: Path = None
        self.destination_file: Path = None
        self.images_to_process = []

        register_heif_opener()
        self.find_folders()

    def load_image(self):
        """Load image from the current image path."""
        if self.image_path is None:
            return
        
        print(self.image_path)
        if self.image_path.lower().endswith('.heic'):
            heif_file = pillow_heif.open_heif(self.image_path)
            self.image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data)
        else:
            self.image = Image.open(self.image_path)
        self.image.thumbnail((1000, 1000))  # Resize for display

    def save_objects(self) -> None:
      """
      Save object coordinates and name using the objects_manager.
      """
      self.objects_manager.save_to_json(self.destination_file)
    
    def reset_all_objects(self):
        """Reset all objects in the objects manager."""
        self.objects_manager = ObjectLocations(self.image_name)

    def add_object(self, object_name: str, coordinates: tuple) -> None:
        if not isinstance(object_name, str):
            raise TypeError("name must be a string")
        if not (isinstance(coordinates, tuple) and len(coordinates) == 2 and all(isinstance(coord, (int, float)) for coord in coordinates)):
            raise TypeError("coordinates must be a tuple of two numbers")
          
        self.objects_manager.add_object(object_name, coordinates)

    
    def delete_object(self, id: str):
        self.objects_manager.delete_object(id)
    
    def find_folders(self):
        """Find the next image from the source folder."""
        with open('source_folders.json') as json_data:
            folders = json.load(json_data)

        self.source_folder = Path(folders['source_folder'])
        self.destination_file = Path(folders['destination_file'])

    def find_images_to_process(self):
        all_files = os.listdir(self.source_folder)
        
        if os.path.exists(self.destination_file):
            try:
                with open(self.destination_file, 'r') as file:
                    existing_data = json.load(file)
                    processed_images = {image['image_name'] for image in existing_data}
                    all_files = [f for f in all_files if f not in processed_images]
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error reading or parsing {self.destination_file}: {e}")
                processed_images = set()
        
        if not all_files:
            print("No more images to process.")
            return None
        self.images_to_process = all_files
        
    def find_next_image(self):

        if not self.images_to_process:
            print("No more images to process.")
            return None
          
        file_name = self.images_to_process.pop()
        self.image_name = file_name
        self.objects_manager = ObjectLocations(self.image_name)
        self.image_path = os.path.join(self.source_folder, file_name)
        self.image = None
        self.points = []
        return file_name

