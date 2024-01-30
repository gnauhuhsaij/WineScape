// script.js
document.getElementById('wineForm').onsubmit = function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const params = new URLSearchParams();
    let wineName = "";

    for (const [key, value] of formData.entries()) {
        if (key === "wineName") {
            if (value === ""){
                const newValue = "Wine sample";
                wineName = encodeURIComponent(newValue);
            }
            else{
                wineName = encodeURIComponent(value);
            }
            ; // Ensure the name is URL-encoded
            continue;
        }
        const inputValue = value === '' ? '-100' : Math.min(Math.max(parseInt(value, 10), -100), 100).toString();
        params.append(key, inputValue);
    }
    // Construct the URL for wine_details with query parameters
    const wineDetailsUrl = `/wine_details/${wineName}/${params.toString()}`;
    window.location.href = wineDetailsUrl; // Redirect to the constructed URL
};