from main.utils import *


def handler400(request, exception):
    return error_page(request, "The request was malformed, please try again.", 400)


def handler403(request, exception):
    return error_page(request, "You do not have permission to access this resource, try logging into your account.", 403)


def handler404(request, exception):
    return error_page(request, "The requested resource was not found. If you typed the adress manually, check your spelling. If you clicked a link, it may be broken, please contact us with the link below.", 404)


def handler500(request):
    return error_page(request, "An internal server error occured, please try again later.", 500)


def unknown_subdomain(request):
    return error_page(request, "The requested subdomain was not found. If you typed the adress manually, check your spelling. If you clicked a link, it may be broken, please contact us with the link below.", 404)
