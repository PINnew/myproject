$(document).ready(function () {
    $("#newsletterForm").submit(function (e) {
        e.preventDefault();  // Предотвращаем стандартную отправку формы

        let subject = $("#subject").val();
        let html_content = $("#html_content").val();
        let scheduled_time = $("#scheduled_time").val();

        $.ajax({
            url: "/mailing/create_newsletter/",
            type: "POST",
            data: {
                subject: subject,
                html_content: html_content,
                scheduled_time: scheduled_time,
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function (response) {
                alert("Рассылка успешно создана!");
                $("#newsletterModal").modal("hide");
            },
            error: function (xhr) {
                alert("Ошибка: " + xhr.responseText);
            }
        });
    });
});
