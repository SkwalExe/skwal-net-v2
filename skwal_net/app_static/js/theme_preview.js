$("select[name='theme']").onchange = e => {
    theme = e.target.value;
    $("#theme").href = `/static/css/themes/${theme}.css`;
}