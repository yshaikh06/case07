from flask import Flask, request, jsonify, render_template

## Add required imports
from azure.storage.blob import BlobServiceClient
import os

CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("CONTAINER_NAME", "lanternflyimages")  # fallback name

bsc = BlobServiceClient.from_connection_string(CONNECTION_STRING)
cc  = bsc.get_container_client(CONTAINER_NAME) # Replace with Container nam$
app = Flask(__name__)
@app.post("/api/v1/upload")
def upload():
    f = request.files["file"]
    blob_client = cc.get_blob_client(f.filename)
    blob_client.upload_blob(f, overwrite=True)

    return jsonify(ok=True, url=f"{cc.url}/{f.filename}")


## Add other API end points. (/api/v1/gallery)  and (/api/v1/health)

@app.get("/api/v1/health")
def health():
    return jsonify(status="ok")

@app.get("/api/v1/gallery")
def gallery():
    blobs = [b.name for b in cc.list_blobs()]
    urls = [f"{cc.url}/{b}" for b in blobs]
    return jsonify(ok=True, gallery=urls)

@app.get("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    # host="0.0.0.0" makes it accessible on your LAN
    app.run(debug=True, host="0.0.0.0", port=5000)