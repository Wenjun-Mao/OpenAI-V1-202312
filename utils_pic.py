from PIL import Image
import os

def create_expanded_and_mask_images(base_image_path, res):
    """
    Function to create an expanded image with a white background and a mask image.
    
    Parameters:
    - base_image_path: str, the path to the base image.
    - res: int, resolution of the output images, can be 256, 512, or 1024.
    
    Returns:
    - expanded_image_path: str, the path to the expanded image.
    - correct_mask_image_path: str, the path to the mask image.
    """
    # Validate the resolution
    if res not in [256, 512, 1024]:
        raise ValueError("Resolution must be one of 256, 512, or 1024.")
    
    # Load the image
    base_image = Image.open(base_image_path)

    # Extract the base filename without the extension and directory of the input file
    base_filename = os.path.splitext(os.path.basename(base_image_path))[0]
    input_dir = os.path.dirname(base_image_path)

    # Create a new image with white background and the specified resolution
    new_image = Image.new("RGB", (res, res), "white")
    new_image.paste(base_image, (int((res - base_image.width) / 2), int((res - base_image.height) / 2)))

    # Save the new image as PNG in the same directory as the input file
    expanded_image_path = os.path.join(input_dir, f'{base_filename}_expanded_{res}.png')
    new_image.save(expanded_image_path, "PNG")

    # Create a mask with transparent areas where the original image is not present
    base_mask = base_image.split()[-1].point(lambda x: 255 if x > 0 else 0)
    correct_mask = Image.new("RGBA", (res, res), (0, 0, 0, 0))
    correct_mask.paste(base_mask, (int((res - base_image.width) / 2), int((res - base_image.height) / 2)), mask=base_mask)

    # Save the correct mask image in the same directory as the input file
    correct_mask_image_path = os.path.join(input_dir, f'{base_filename}_mask_{res}.png')
    correct_mask.save(correct_mask_image_path, "PNG")
    
    return expanded_image_path, correct_mask_image_path
