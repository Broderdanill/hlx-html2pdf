# hlx-html2pdf
Returns HTML-string as Base64 encoded string

# Build image
podman build -t hlx-html2pdf .

# Run container
podman run -e LOG_LEVEL=DEBUG -p 8080:8080 hlx-html2pdf
