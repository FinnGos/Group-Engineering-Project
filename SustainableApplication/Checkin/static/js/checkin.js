var map = L.map('map'); // Initialize map

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

function showPosition(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    
    map.setView([lat, lon], 15); // Center map on user location
    L.marker([lat, lon]).addTo(map)
        .bindPopup("You're here!")
        .openPopup();
}

var marker = L.marker([50.7354611346658, -3.5339872116477524]).addTo(map)
    .bindPopup("Forum recycling point")
    .openPopup();

var circle = L.circle([50.744283404596366,  -3.54216391886783], {
    color: 'purple',
    fillColor: '#f03',
    fillOpacity: 0.5,
    radius: 500
}).addTo(map)
    .bindPopup("Duryard PV solar panels")
    .openPopup();

    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                showPosition(position);
    
                // Get task ID from the HTML element
                const taskElement = document.getElementById("taskData");
                const taskId = taskElement ? taskElement.dataset.taskId : "0";
    
                if (taskId === "0") {
                    alert("Task ID not found.");
                    return;
                }
    
                // Redirect to the Django URL with latitude & longitude
                window.location.href = `/get_location/${taskId}/?lat=${position.coords.latitude}&lon=${position.coords.longitude}`;
            });
        } else {
            alert("Geolocation is not supported by this browser.");
        }
    }
    
// Automatically get and show user's location on page load
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition, function (error) {
        alert("Geolocation failed: " + error.message);
    });
} else {
    alert("Geolocation is not supported by this browser.");
}
