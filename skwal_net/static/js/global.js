toasteur = new Toasteur("top-right", 5000, 'top');
Toultip.init(200, true);

// Call resize event to force the navbar and 
// other elements to adjust to the window size
window.dispatchEvent(new Event("resize"));