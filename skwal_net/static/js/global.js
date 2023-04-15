toasteur = new Toasteur("top-right", 5000, 'top');
Toultip.init(200, true);

$$(".markdown *[centered]").forEach(el => {
    el.classList.add("center");
});
$$(".markdown *[arrow]").forEach(el => {
    el.classList.add("arrow");
});
$$(".markdown *[double-arrow]").forEach(el => {
    el.classList.add("double-arrow");
});

$$(".markdown hr[breakbox]").forEach(el => {
    let parent = el.parentNode;
    let parentParent = parent.parentNode;
    if (parent.tagName != "DIV" || !parent.classList.contains("box"))
        return;

    let elements = {
        before: [],
        after: []
    }

    let current = parent.firstChild;
    while (current != el) {
        elements.before.push(current);
        current = current.nextSibling;
    }

    current = el.nextSibling;
    while (current != null) {
        elements.after.push(current);
        current = current.nextSibling;
    }

    let before = document.createElement("div");
    before.classList.add("markdown");
    before.classList.add("box");
    let after = document.createElement("div");
    after.classList.add("markdown");
    after.classList.add("box");

    elements.before.forEach(el => {
        before.appendChild(el);
    });

    elements.after.forEach(el => {
        after.appendChild(el);
    });
    parentParent.insertBefore(before, parent);
    parentParent.insertBefore(after, parent);
    remove(parent);
});