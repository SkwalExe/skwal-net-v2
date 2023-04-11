$$("*[href]").forEach(element => {
    let href = element.getAttribute("href");
    element.onclick = (e) =>
        redirect(href, (e.ctrlKey || e.metaKey || e.button == 1))
    element.onauxclick = (e) => {
        if (e.button === 1)
            redirect(href, true);
    }
});

$$("*[_href]").forEach(element => {
    let href = element.getAttribute("_href");
    element.onclick = element.onauxclick = () =>
        redirect(href, true);
});