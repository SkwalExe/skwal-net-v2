$$("*[href]").forEach(element => {
    let href = element.getAttribute("href");
    element._onclick = (e) =>
        redirect(href, (e.ctrlKey || e.metaKey || e.button == 1))
    element._onauxclick = (e) => {
        if (e.button === 2)
            redirect(href, true);
    }
});

$$("*[_href]").forEach(element => {
    let href = element.getAttribute("_href");
    element.onmousedown = (e) => {
        if (e.button !== 2)
            redirect(href, true);
    }
});

$$("*[_href], *[href]").forEach(element => {
    let href = element.getAttribute("_href");
    element.oncontextmenu = () => {
        copy(href);
        toasteur.success("URL copied to clipboard", "Copied!");
        return false;
    }
});