document.addEventListener("DOMContentLoaded", function() {
    const bookingForm = document.querySelector("form");

    if (bookingForm) {
        bookingForm.addEventListener("submit", function(event) {

            const quantity = document.querySelector("input[name = 'ticket_quantity']");

            if (quantity.value <= 0) {
                alert("Please enter a valid ticket quantity");
                event.preventDefault();
                return;
            }

            if (!confirm("Are you sure you want to submit this booking?")) {
                event.preventDefault();
            }
        })
    }
})