from main.utils import *


def handler400(request, exception):
    return error_page(request, 400, "The request was malformed, please try again.")


def handler403(request, exception):
    return error_page(request, 403, "You do not have permission to access this resource, try logging into your account.")


def handler404(request, exception):
    return error_page(request, 404, "The requested resource was not found. If you typed the adress manually, check your spelling. If you clicked a link, it may be broken, please contact us with the link below.")


def handler500(request):
    return error_page(request, 500, "An internal server error occured, please try again later.")
