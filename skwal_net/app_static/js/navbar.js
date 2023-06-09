// Show/Hide navbar buttons on mobile
function toggleButtons() {
    let navbarButtons = $("#navbar-buttons");
    navbarButtons.dataset.active = navbarButtons.dataset.active === "true" ? "false" : "true";
}

document.addEventListener('DOMContentLoaded', function() {
    let navButtons = $("#navbar-buttons");
    let navbarTop = $("#navbar-top");
    let navbar = $("#navbar");
    let navbarLogo = $("#navbar-logo");
    let minWidth = navButtons.offsetWidth + navbarTop.offsetWidth + 100;

    // Show the buttons or put them in the dropdown menu if the window is too small when resizing
    window.addEventListener("resize", () => navbar.dataset.mobile = window.innerWidth < minWidth);
    // Call resize event to force the navbar
    // to adjust to the window size when the page is loaded
    window.dispatchEvent(new Event("resize"));
    // Copy the website URL to the clipboard when clicking on the logo
    navbarLogo.oncontextmenu = function(e) {
        e.preventDefault();
        e.stopPropagation();
        copy("https://skwal.net")
        toasteur.success("Website URL to clipboard!", "Copied!")
    }
});