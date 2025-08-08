import json
import os
from pathlib import Path

class ObjectLocations:
    def __init__(self, image_name: str):
        if not image_name or not isinstance(image_name, str):
            raise ValueError("image_name must be a non-empty string")
        self.objects: dict = {}
        self.associated_image: str = image_name

    def add_object(self, name: str, coordinates: tuple):
        if not isinstance(name, str):
          raise TypeError("Object name must be a string")
        if not (isinstance(coordinates, tuple) and len(coordinates) == 2 and all(isinstance(c, (int, float)) for c in coordinates)):
          raise TypeError("Coordinates must be a tuple of two numbers")
        self.objects[name] = coordinates

    def delete_object(self, name: str):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        
        if name in self.objects:
            del self.objects[name]
        else:
            raise KeyError(f"Object '{name}' not found in the list.")
        
    def save_to_json(self, file_path: Path = None):
        print(f"Saving objects for image '{self.associated_image}' to {file_path}")

        if not isinstance(file_path, Path):
            raise TypeError("file_path must be a Path object")
        
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                existing_data = json.load(file)
            
            image_found = False
            for image in existing_data:
                if image['image_name'] == self.associated_image:
                    image['objects'].update(self.objects)
                    image_found = True
                    break
            
            if not image_found:
                existing_data.append({'image_name': self.associated_image, 'objects': self.objects})
            
            data_to_save = existing_data
        else:
            data_to_save = [{'image_name': self.associated_image, 'objects': self.objects}]
        
        with open(file_path, 'w') as file:
            json.dump(data_to_save, file, indent=4)

# Example usage:
# obj_loc = ObjectLocations()
# obj_loc.add_object("object1", (10, 20))
# obj_loc.save_to_json("/path/to/your/file.json")