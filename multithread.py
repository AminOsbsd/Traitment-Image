import os
import time
import pytesseract
from PIL import Image
import concurrent.futures
import threading

# Configure pytesseract to use the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract' 

def load_images_from_folder(folder):
    """Load images from a specified folder."""
    images = []
    for filename in os.listdir(folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(folder, filename)
            try:
                img = Image.open(img_path)
                img.info['dpi'] = (300, 300)
                images.append((filename, img))
            except Exception as e:
                print(f"Error loading image {img_path}: {e}")
    return images

lock = threading.Lock()

def process_image(image_data):
    """Process a single image to extract text."""
    filename, img = image_data
    try:
        text = pytesseract.image_to_string(img)
        with lock: 
            
            pass
        return filename, text
    except Exception as e:
        print(f"Error processing image {filename}: {e}")
        return filename, ""

def process_images_in_parallel(images):
    """Process multiple images concurrently using multithreading."""
    num_workers = min(4, len(images))
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_image = {executor.submit(process_image, image_data): image_data for image_data in images}
        for future in concurrent.futures.as_completed(future_to_image):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Error during processing: {e}")
    return results

def save_results(results, output_folder):
    """Save the extracted text results to files in the specified output folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for filename, text in results:
        try:
            with open(os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt"), 'w') as f:
                f.write(text)
        except Exception as e:
            print(f"Error saving file {filename}: {e}")

def main(input_folder, output_folder):
    """Main function to run the entire process."""
    start_time = time.time()
    
    images = load_images_from_folder(input_folder)
    print(f"Loaded {len(images)} images.")
    
    results = process_images_in_parallel(images)
    print(f"Processed {len(results)} images.")
    
    save_results(results, output_folder)
    
    end_time = time.time()
    print(f"Multithreading execution time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    input_folder = '/home/khouloud/Desktop/SEA/Input/'
    output_folder = '/home/khouloud/Desktop/SEA/Output/multi/'
    main(input_folder, output_folder)

