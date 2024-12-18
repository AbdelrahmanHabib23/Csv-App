Toastify({
    text: "{{ message }}",  // Pass the message content
    duration: 4000,          // Duration the toast will be visible (in milliseconds, 4 seconds here)
    close: true,             // Allow closing the toast by clicking the close button
    gravity: "top",          // Positioning from top of the screen
    position: "right",       // Align the toast to the right of the screen
    backgroundColor: getToastBackgroundColor("{{ message.tags }}"), // Dynamically change the background color based on message type
    className: "custom-toast",  // Apply a custom class for additional styling
    stopOnFocus: true,       // Stops the toast from disappearing if focused (useful for longer messages)
    escapeMarkup: true,      // Escape any HTML markup to avoid XSS vulnerabilities
    onClick: function() {    // Optional: Define what happens when the toast is clicked
        console.log("Toast clicked!");
        // You can add any custom logic here, for example, navigating to a specific URL
    },
    newWindow: true,         // Open the link in a new window when clicked (if you want to use links within the toast)
    position: "right",       // You can change the position to top-right, bottom-left, etc.
    transition: "fade",      // You can use different animations like "fade", "bounce", "slide", etc.
}).showToast();

// Function to determine background color based on message type (success, error, info, warning)
function getToastBackgroundColor(messageType) {
    switch (messageType) {
        case "success":
            return "linear-gradient(to right, #28a745, #8bc34a)"; // Green gradient for success
        case "error":
            return "linear-gradient(to right, #dc3545, #ff4d4d)";  // Red gradient for error
        case "info":
            return "linear-gradient(to right, #17a2b8, #61c0d1)";  // Blue gradient for info
        case "warning":
            return "linear-gradient(to right, #ffc107, #ffca2c)";  // Yellow gradient for warnings
        default:
            return "linear-gradient(to right, #00b09b, #96c93d)";  // Default gradient (greenish)
    }
}
