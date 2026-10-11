const paymentMethod = document.getElementById("payment_method");

const creditCardFields = document.getElementById("credit_card_fields");
const paypalFields = document.getElementById("paypal_fields");
const bankTransferFields = document.getElementById("bank_transfer_fields");
const expiryDate = document.getElementById("expiry_date");

function hideAllFields() {
    creditCardFields.style.display = "none";
    paypalFields.style.display = "none";
    bankTransferFields.style.display = "none";
}

hideAllFields();

paymentMethod.addEventListener("change", function() {
    hideAllFields();

    if (paymentMethod.value === "credit_card") {
        creditCardFields.style.display = "block";
    } else if (paymentMethod.value === "paypal") {
        paypalFields.style.display = "block";
    } else if (paymentMethod.value === "bank_transfer") {
        bankTransferFields.style.display = "block";
    }
});

expiryDate.addEventListener("input", function() {
    let value = expiryDate.value.replace(/\D/g, "");

    if (value.length >= 3) {
        value = value.slice(0, 2) + "/" + value.slice(2, 4);
    }

    expiryDate.value = value;
});