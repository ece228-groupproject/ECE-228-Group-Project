import kagglehub

# Download latest version
path = kagglehub.dataset_download("dataanalyst001/all-capital-cities-in-the-world")

print("Path to dataset files:", path)