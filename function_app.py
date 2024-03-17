import os
import azure.functions as func
import logging
import requests
from dotenv import load_dotenv
import segno
from io import BytesIO

load_dotenv()

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="image_bg_remover", methods=["POST"])
def image_bg_remover(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    image_url = req_body.get("url")
    if not image_url:
        return func.HttpResponse(
            "Please provide an image URL in the request body.", status_code=400
        )

    # Remove Background
    key = os.environ["REMOVE_BG_API_KEY"]
    response = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        data={"image_url": image_url, "size": "auto"},
        headers={"X-Api-Key": key},
    )

    if response.status_code == requests.codes.ok:
        return func.HttpResponse(response.content, mimetype="image/png")
    else:
        return func.HttpResponse(
            "Failed to process the image", status_code=response.status_code
        )


@app.route(route="generate_qr_code", methods=["POST"])
def generate_qr_code(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    url = req_body.get("url")
    if not url:
        return func.HttpResponse(
            "Please provide a URL in the request body.", status_code=400
        )

    qr = segno.make(url)
    buffer = BytesIO()
    qr.save(buffer, kind="png", scale=10, border=1, dark="black", light="white")
    buffer.seek(0)
    img = buffer.getvalue()

    return func.HttpResponse(img, mimetype="image/png")
