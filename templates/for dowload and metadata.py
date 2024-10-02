import os
import hashlib
from PIL import Image
from PIL.ExifTags import TAGS
import PyPDF2

def extract_image_metadata(image_path):
    """Extract EXIF metadata from an image file and perform hash comparison."""
    try:
        if not os.path.isfile(image_path):
            print("Error: The specified path is not a valid file. Please check the path and try again.")
            return

        print(f"Checking image file at path: {image_path}")

        # Open image and get EXIF data
        image = Image.open(image_path)
        exif_data = image._getexif()

        # Calculate file SHA-256 hash
        sha256_hash = hashlib.sha256()
        with open(image_path, 'rb') as file:
            sha256_hash.update(file.read())
        image_hash = sha256_hash.hexdigest()

        # Display file hash
        print(f"File SHA-256 Hash: {image_hash}")

        # Display EXIF metadata if available
        if not exif_data:
            print("No EXIF metadata found.")
        else:
            print("\nEXIF Metadata:")
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                print(f"{tag:25}: {value}")

        # Compare the file's hash with a known SHA-256 hash
        known_hash = input("Enter the known SHA-256 hash to compare (or press Enter to skip): ")
        if known_hash:
            compare_hashes(image_hash, known_hash)
        else:
            print("No known hash provided for comparison.")
    except Exception as e:
        print(f"Error processing image: {e}")

def extract_pdf_metadata(pdf_path):
    """Extract metadata from a PDF file and perform hash comparison."""
    try:
        if not os.path.isfile(pdf_path):
            print("Error: The specified path is not a valid file. Please check the path and try again.")
            return

        print(f"Checking PDF file at path: {pdf_path}")

        # Open PDF file and extract metadata
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            metadata = reader.metadata

        # Calculate file SHA-256 hash
        sha256_hash = hashlib.sha256()
        file.seek(0)  # Ensure the pointer is at the start of the file
        sha256_hash.update(file.read())
        file_hash = sha256_hash.hexdigest()

        # Display file hash
        print(f"File SHA-256 Hash: {file_hash}")

        # Display PDF metadata if available
        if metadata is None:
            print("No metadata found in the PDF.")
        else:
            print("\nPDF Metadata:")
            for key, value in metadata.items():
                print(f"{key:25}: {value}")

        # Compare the file's hash with a known SHA-256 hash
        known_hash = input("Enter the known SHA-256 hash to compare (or press Enter to skip): ")
        if known_hash:
            compare_hashes(file_hash, known_hash)
        else:
            print("No known hash provided for comparison.")
    except Exception as e:
        print(f"Error processing PDF: {e}")

def compare_hashes(calculated_hash, known_hash):
    """Compare the calculated hash with a known hash."""
    if calculated_hash == known_hash:
        print("Hashes match. No tampering detected.")
    else:
        print("Warning: Hashes do not match. File may be tampered with.")

def analyze_whatsapp_image(image_path):
    """Analyze basic information about a WhatsApp image."""
    try:
        if not os.path.isfile(image_path):
            print("Error: The specified path is not a valid file.")
            return

        print(f"Checking file at path: {image_path}")

        # WhatsApp often strips metadata, but we can get file modification time
        modification_time = os.path.getmtime(image_path)
        print(f"Image modification time: {modification_time}")
        print("Note: This might not reflect the original capture time due to WhatsApp processing.")
        
    except Exception as e:
        print(f"Error analyzing WhatsApp image: {e}")

def main():
    """Main function to run the file analysis tool."""
    print("Choose an option to analyze:")
    print("1. Analyze an image (EXIF metadata)")
    print("2. Analyze a PDF file")
    print("3. Analyze a WhatsApp image")

    choice = input("Enter your choice (1/2/3): ")

    if choice == "1":
        image_path = input("Enter the path of the image to analyze: ")
        if image_path.lower().endswith((".jpg", ".jpeg", ".png")):
            extract_image_metadata(image_path)
        else:
            analyze_whatsapp_image(image_path)  # For WhatsApp images (no EXIF data)

    elif choice == "2":
        pdf_path = input("Enter the path of the PDF to analyze: ")
        extract_pdf_metadata(pdf_path)

    elif choice == "3":
        image_path = input("Enter the path of the WhatsApp image: ")
        analyze_whatsapp_image(image_path)

    else:
        print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()
