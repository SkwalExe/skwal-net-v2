from django.http import HttpResponse
import os
import hashlib
import hmac
from django.views.decorators.csrf import csrf_exempt


def verify_signature(payload_body, signature_header):
    # Verify that the payload was sent from GitHub
    # by validating SHA256.

    secret_token = os.getenv("GITHUB_SECRET")
    if not signature_header:
        return False
    hash_object = hmac.new(secret_token.encode(
        'utf-8'), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()
    return hmac.compare_digest(expected_signature, signature_header)


@csrf_exempt
def redeploy(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    data = request.body
    signature = request.headers.get("X-Hub-Signature-256")

    if not verify_signature(data, signature):
        return HttpResponse(status=403)
    file = open(os.path.join(os.path.dirname(
        __file__), "../../hooks/redeploy"), "w")
    file.write("Redeploy")
    file.close()
    return HttpResponse(status=200)
