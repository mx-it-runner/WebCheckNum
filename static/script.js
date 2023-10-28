function processPhoneNumber() {
    var phoneNumber = $("#phoneNumberInput").val();
    $.ajax({
        url: "/process",
        method: "POST",
        data: { phoneNumber: phoneNumber },
        success: function(response) {
            $("#result").text("Результат: " + response);
        },
        error: function() {
            $("#result").text("Ошибка при обработке номера");
        }
    });
}