import hashlib

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        # Read and update hash in chunks to avoid memory issues with large files
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# Corrected file path
file_path = r"C:\Users\Puneeth\Downloads\IMG20221005201039.jpg"

try:
    known_hash = calculate_sha256(file_path)
    print(f"Known SHA-256 Hash: {known_hash}")
except FileNotFoundError:
    print(f"Error: File not found at the specified path: {file_path}")
