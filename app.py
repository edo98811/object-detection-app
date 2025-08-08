import tkinter as tk
from PIL import ImageTk
from image_class import ImageData
import tkinter.messagebox 

class ImageCropperApp:
    def __init__(self, root):
        """Initialize the main application."""
        self.root = root
        self.root.title("Perspective correction tool")
        self.current_oval_id = None
        # self.text_ids: list = []
        self.objects_drawn: list = [] 
        
        # Create an ImageData instance
        self.image = ImageData()
        self.image.find_images_to_process()
        self.image.find_next_image()
        self.image.load_image()

        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        self.current_oval_id = None
        self.objects_drawn: list = [] 

        """Set up the UI with a structured layout using grid."""
        # Clear previous UI
        for widget in self.root.winfo_children():
            widget.grid_forget()

        # Create the main frame for top controls (input + buttons)
        top_frame = tk.Frame(self.root)
        top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        # Left: Input field + label
        input_frame = tk.Frame(top_frame)
        input_frame.grid(row=0, column=0, sticky="w")

        self.input_label = tk.Label(input_frame, text="Insert object name:", fg="white", font=("Arial", 10))
        self.input_label.grid(row=0, column=0, padx=5)

        self.input_field = tk.Entry(input_frame, width=30)
        self.input_field.grid(row=0, column=1, padx=5)

        # Right: Buttons (Reset Points, Reset All, Save Object, Next Image)
        button_frame = tk.Frame(top_frame)
        button_frame.grid(row=0, column=1, sticky="e", padx=10)

        # self.save_button = tk.Button(button_frame, text="Save Object", command=self.save_object)
        # self.save_button.grid(row=0, column=0, padx=5)
    
        self.reset_button = tk.Button(button_frame, text="Reset Last Object", command=self.reset_last_object)
        self.reset_button.grid(row=0, column=1, padx=5)

        self.reset_objects_button = tk.Button(button_frame, text="Reset All Objects", command=self.reset_all_objects)
        self.reset_objects_button.grid(row=0, column=2, padx=5)

        self.next_image_button = tk.Button(button_frame, text="Save and Next Image", command=self.next_image)
        self.next_image_button.grid(row=0, column=3, padx=5)

        # Create a Canvas for displaying the image (Center)
        self.canvas = tk.Canvas(self.root, width=800, height=800, bg="black")  # Set to 800x800 minimum
        self.canvas.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")  # Expand to center

        # Display the loaded image
        if self.image.image:
            self.tk_img = ImageTk.PhotoImage(self.image.image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

        self.canvas.bind("<Button-1>", self.select_point)
        self.input_field.bind("<Return>", self.save_object)

        # # Console-like text box at the bottom
        # self.console = tk.Text(self.root, height=6, wrap="word", state="disabled", bg="black", fg="white", font=("Courier", 10))
        # self.console.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="ew")  # Full-width at the bottom

        # Configure grid rows and columns for resizing
        self.root.grid_rowconfigure(0, weight=0)  # First row for input + buttons
        self.root.grid_rowconfigure(1, weight=1)  # Second row for canvas, expands to fill available space
        # self.root.grid_rowconfigure(2, weight=0)  # Third row for console
        self.root.grid_columnconfigure(0, weight=1)  # First column for content alignment
        self.root.grid_columnconfigure(1, weight=1)  # Second column for content alignment

    def get_center_coords(self, shape_id):
        """Returns the center (x, y) coordinates of a given shape ID."""
        coords = self.canvas.coords(shape_id)  # Get bounding box [x1, y1, x2, y2]
        if coords:
            center_x = (coords[0] + coords[2]) / 2  # Calculate center X
            center_y = (coords[1] + coords[3]) / 2  # Calculate center Y
            return center_x, center_y
        return None  # Return None if coords are invalid

    def select_point(self, event):
        """Handle point selection on the image."""
        
        if self.current_oval_id is not None:
          self.canvas.delete(self.current_oval_id)
          self.current_oval_id = None
          
        self.current_oval_id = self.canvas.create_oval(event.x - 3, event.y - 3, event.x + 3, event.y + 3, fill="red")
        # self.canvas.bind("<Button-1>", lambda event: None)

    def reset_last_object(self):
        if not self.objects_drawn:
            return

        oval_id, text_id, object_name = self.objects_drawn.pop()

        self.canvas.delete(oval_id)
        self.canvas.delete(text_id)

        self.image.delete_object(object_name)
        print(f"Deleted object: {object_name}")
        
    def reset_all_objects(self):
        for oval_id, text_id, _ in self.objects_drawn:
            self.canvas.delete(oval_id)
            self.canvas.delete(text_id)
        self.objects_drawn.clear()
        self.image.reset_all_objects()

    def save_object(self, event=None):
        """Apply perspective transformation and validate input."""
        user_input = self.input_field.get().strip()  # Get user input and remove extra spaces

        if not user_input or self.current_oval_id is None:  # If the input is empty or the length of oval ids is not one longer than text ids
            self.input_label.config(text="YOU HAVE TO INSERT OBJECT NAME", fg="red")  # Show warning in red
            return
          
        if self.current_oval_id is None:
            return  
          
        oval_id = self.current_oval_id  # Get the last oval ID
        center_x, center_y  = self.get_center_coords(oval_id)
        text_id = self.canvas.create_text(center_x + 10, center_y + 10, text=user_input, fill="black", font=("Arial", 12, "bold"))
        
        # Store both IDs and name together
        self.objects_drawn.append((oval_id, text_id, user_input))
        # Add the object to the image's object manager
        self.image.add_object(user_input, (center_x, center_y))  # Add the object to the image's object manager
        # self.print_to_console(f"User Input: {user_input}")  
        # self.image.add_object(user_input)

        # Reset the label text back to normal
        self.input_label.config(text="Insert object name:", fg="black")  
        self.input_field.delete(0, tk.END)
        # self.canvas.bind("<Button-1>", self.select_point)
 
    def next_image(self):
        """Save the transformed image and load a new one."""
        self.image.save_objects()
        next_image = self.image.find_next_image()
        if next_image is None:
            tk.messagebox.showinfo("End of Queue", "No more images to process.")
            self.root.destroy()
            return
        self.image.load_image()
        self.setup_ui()

# Run the Tkinter app
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCropperApp(root)
    root.mainloop()
