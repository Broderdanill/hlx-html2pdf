# hlx-html2pdf
Returns HTML-string as Base64 encoded string
This can be useful for example in BMC Helix to send a html-string to this container and the collect the answer in a innovation studio application that have possibility to save a base64-encoded string as an attachment directly.
So this makes it possible to generate a pdf-file in BMC Helix.

# Build image
podman build -t hlx-html2pdf .

# Run container
podman run -e LOG_LEVEL=DEBUG -p 8080:8080 hlx-html2pdf

> [!TIP]
> Test the container with command:
> curl -X POST http://localhost:8080/generate-pdf -H "Content-Type: application/json" -d '{"html": "YOUR HTML-CODE AS STRING"}'