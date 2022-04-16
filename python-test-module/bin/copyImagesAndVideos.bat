aws s3 sync s3://asl-dictionary-uploads/uploads s3://asl-dictionary/media-storage --exclude "*" --include "*/image.jpeg"
aws s3 sync s3://asl-dictionary-uploads/uploads s3://asl-dictionary/media-storage --exclude "*" --include "*/video.webm"
