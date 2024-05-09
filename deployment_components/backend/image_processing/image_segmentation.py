from fastsam import FastSAM, FastSAMPrompt
from PIL import Image
import numpy as np
# import argparse
model = FastSAM('./weights/FastSAM-s.pt')
IMAGE_PATH = '../data/input_images/table_clutter.jpg'
DEVICE = 'cpu'



def crop_image_using_tensor(tensor, image_path):
    """
    Crop an image using tensor slices as masks with transparent backgrounds.

    Parameters:
    - tensor: a tensor where each slice is a mask. Can be a numpy ndarray or a PyTorch tensor.
    - image_path (str): path to the image to be cropped.

    Returns:
    - List[Image.Image]: list of cropped image segments.
    """
    
    # Convert tensor to numpy if it's a PyTorch tensor
    if hasattr(tensor, "cpu") and hasattr(tensor, "numpy"):
        tensor = tensor.cpu().numpy()

    # Load image using PIL and convert to RGBA
    img = Image.open(image_path).convert('RGBA')
    original_area = img.width * img.height
    cropped_segments = []
    for mask_slice in tensor:


        # Convert tensor slice to numpy array and then to PIL Image
        mask = Image.fromarray((mask_slice * 255).astype(np.uint8)).resize(img.size).convert("L")
        
        mask_np = np.array(mask)
        mask_area = np.sum(mask_np > 0)


        if (0.011 * original_area <= mask_area) and (mask_area <= 0.5 * original_area):
            
            # Use a transparent image for compositing
            transparent_img = Image.new('RGBA', img.size, (0, 0, 0, 0))
            
            # Composite images
            cropped_segment = Image.composite(img, transparent_img, mask)
            
            # Find bounding box of the mask to further crop unnecessary parts
            bbox = mask.getbbox()
            if bbox:
                cropped_segment = cropped_segment.crop(bbox)
                cropped_segments.append(cropped_segment)
        else:
            print(f"Mask area {mask_area} is not within the desired range. Skipping...")

    return cropped_segments
from PIL import Image
import os

def save_cropped_segments(cropped_segments, output_directory, base_filename="segment_"):
    """
    Save cropped image segments to the specified directory.

    Parameters:
    - cropped_segments (List[Image.Image]): list of cropped image segments.
    - output_directory (str): path to the directory where the segments should be saved.
    - base_filename (str, optional): base name for the cropped files. Defaults to "segment_".
    
    Returns:
    - List[str]: list of file paths where segments are saved.
    """

    # Ensure output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    saved_files = []

    for idx, segment in enumerate(cropped_segments, 1):
        filename = f"{base_filename}{idx}.png"
        file_path = os.path.join(output_directory, filename)
        segment.save(file_path)
        saved_files.append(file_path)

    return saved_files





# Import your functions here
# from your_module import crop_image_using_tensor, save_cropped_segments

def main_segmentation(args):
    # Use the arguments passed to the script
    IMAGE_PATH = args.image_path
    weight=args.weight
    model = FastSAM(weight)
    result = model.predict(source=IMAGE_PATH)
    masks = result[0].masks.data
    cropped_segments = crop_image_using_tensor(masks, IMAGE_PATH)
    # Create an empty list to store the cropped segments as arrays
    cropped_segments_list = []
    image_list=[]

    # Iterate through the cropped segments and convert them to arrays
    for segment in cropped_segments:
        # Assuming crop_image_using_tensor returns PIL Images, you can convert them to arrays
        segment_array = np.array(segment)
        cropped_segments_list.append(segment_array)
    # Iterate through the cropped segments as arrays and display them
    for i, segment_array in enumerate(cropped_segments_list):
        # Convert the NumPy array back to a PIL Image
        segment_image = Image.fromarray(segment_array)
        
        # Display the PIL Image
        # segment_image.show()
        image_list.append(segment_image)
    # Now you have cropped_segments_list as a list of images (arrays)
    print("cropped_segment", len(cropped_segments_list))
    # Example Usage
    output_dir = args.output_dir
    saved_file_paths = save_cropped_segments(cropped_segments, output_dir)
    print(saved_file_paths)  # This will print out the paths where the segments were saved
    return image_list

# if __name__ == "__main__":
#     # Create an ArgumentParser object
#     parser = argparse.ArgumentParser(description="Description of your script.")

#     # Define the command-line arguments you want to accept
#     parser.add_argument("--weight", default='./weights/FastSAM-s.pt',required=False, help="Description of masks argument")
#     parser.add_argument("--image-path", default='./data/input_images/table_clutter.jpg',required=False, help="Description of image path argument")
#     parser.add_argument("--output-dir", default="./data/segmented_images",required=False, help="Description of output directory argument")

#     # Parse the command-line arguments
#     args = parser.parse_args()

#     # Call the main function with the parsed arguments
#     list_images=main(args)
#     print("list_of_images",list_images)
# data/input_images/table_clutter.jpg