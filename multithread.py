import os
import time
import pytesseract
from PIL import Image
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

def process_image(image_data, results, lock):
    """Process a single image to extract text."""
    filename, img = image_data
    try:
        text = pytesseract.image_to_string(img)
        with lock:
            results.append((filename, text))
    except Exception as e:
        print(f"Error processing image {filename}: {e}")
        with lock:
            results.append((filename, ""))

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
    
    results = []
    threads = []
    lock = threading.Lock()
    
    for image in images:
        thread = threading.Thread(target=process_image, args=(image, results, lock))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print(f"Processed {len(results)} images.")
    
    save_results(results, output_folder)
    
    end_time = time.time()
    print(f"Multithreading execution time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    input_folder = '/home/aminos/Images'
    output_folder = '/home/aminos/output/multi'
    main(input_folder, output_folder)
