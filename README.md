# hlx-html2pdf
Returns HTML-string as Base64 encoded string

# Build image
podman build -t hlx-html2pdf .

# Run container
podman run -e LOG_LEVEL=DEBUG -p 8080:8080 hlx-html2pdf

# Test container
curl -X POST http://localhost:8080/generate-pdf -H "Content-Type: application/json" -d '{"html": "<html><body><h1>Hello base64 pdf string!</h1></body></html>"}'
