print = console.log;

function $(selector) {
    return document.querySelector(selector);
}

function $$(selector) {
    return document.querySelectorAll(selector);
}

function redirect(href, new_tab = false) {
    if (new_tab)
        window.open(href, "_blank");
    else
        document.location.href = href;
}

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min
}

function copy(text) {
    navigator.clipboard.writeText(text);
}