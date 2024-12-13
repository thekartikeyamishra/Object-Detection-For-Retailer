from PIL import Image

def save_image(image_array, output_path):
    image = Image.fromarray(image_array)
    image.save(output_path)