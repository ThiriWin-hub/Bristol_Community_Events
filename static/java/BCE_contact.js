document.addEventListener("DOMContentLoaded", function() {
    const contactForm = document.querySelector("form");

    if (contactForm) {
        contactForm.addEventListener("submit", function(event) {
            const firstName = document.querySelector("input[name = 'firstname']");
            const lastName = document.querySelector("input[name = 'lastname']");
            const email = document.querySelector("input[name = 'email']");
            const country = document.querySelector("input[name = 'country']");
            const subject = document.querySelector("textarea[name = 'subject']");

            if (!firstName.value.trim() || !lastName.value.trim() || !email.value.trim() || !country.value.trim() || !subject.value.trim()) {
                alert("Please fill in all the fields before submitting.");
                event.preventDefault();
                return;
            }

            if (!confirm("Are you sure you want to submit this contact form?")) {
                event.preventDefault();
            }
        })
    }
})