$(document).ready(function() {

    const search = document.getElementById('search');
    const search_error = document.getElementById('search_error');
    const another_site_flag = document.getElementById('another_site_flag');
    const another_site = document.getElementById('another_site');
    const select_url = document.getElementById('select_url');
    const url_error = document.getElementById('url_error');
    const results = document.getElementById('results');

    another_site.disabled = true;

    another_site_flag.onchange = function() {
        if (this.checked){
            another_site.disabled = false;
            select_url.disabled = true;
            select_url.value = "не выбрано";
        }
        else{
            another_site.disabled = true;
            select_url.disabled = false;
            another_site.value = "";
            check_domain()

        }
    };

    $('form').submit(function (e) {
        e.preventDefault();
        const url = "/process_form/"; // {{ url for }}
        if (validate_form()){
            console.log("ok");
            // TODO если прошла валидацию то очистить ошибки
            $.ajax({
                type: "POST",
                url: url,
                data: $('form').serialize(),
                success: function (data) {
                    data.data.forEach(function (el, index) {
                        $(results).empty();
                        result_element= "<p> "+(index + 1) +". Адрес: <a href='"+el.url+"'>"+el.url+"</a></p>" +
                            "<p> Найденные варианты: " + el.found_arr + "</p>";
                        $(result_element).clone().appendTo( results );
                    })
            }
        });
        }
        // Не прошли валидацию
        else{
            // Если нет слов в запросе
            validate_empty_word_input();
            // Если невалидна сязка полей список-галочка-инпут
            validate_select_checkbox_input();
            // Если в урле нету домена
            check_domain()
        }

    });

    // Вставляем CSRF токен в AJAX запрос.
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", "{{ form.csrf_token._value() }}")
            }
        }
    });

    function validate_form() {
        console.log("dv");
        return search.value !== "" &&
            (/\.\w{2,3}\/?/.test(another_site.value) && another_site.value !== "" && another_site_flag.checked ||
                select_url.value !== "не выбрано" && !another_site_flag.checked )

    }

    function validate_empty_word_input() {
        if (search.value === ""){
            if (!~search_error.innerText.indexOf("заполните") ){
                search_error.innerText += " [заполните это поле] ";
            }
        }
        else{
            search_error.innerText =
            search_error.innerText.replace('[заполните это поле]','');
        }
    }

    function validate_select_checkbox_input() {
        if ((select_url.value === "не выбрано" && !another_site_flag.checked)||
            (another_site.value === "" && another_site_flag.checked)){
            if (!~url_error.innerText.indexOf("выберите") ){
                url_error.innerText += " [выберите сайт из списка или введите адрес сайта самостоятельно] ";
            }
        }
        else {
            url_error.innerText =
            url_error.innerText.replace('[выберите сайт из списка или введите адрес сайта самостоятельно]','');
        }
    }

    function check_domain() {
        if (another_site_flag.checked && another_site.value !== "" && !/\.\w{2,3}\/?/.test(another_site.value)){
            if (!~url_error.innerText.indexOf("неправильный") ){
                url_error.innerText += " [неправильный адрес сайта] ";
            }
        }
        else {
            url_error.innerText =
             url_error.innerText.replace('[неправильный адрес сайта]','');
        }

    }
});

//TODO раскидать чтоб не было повторов (хотяб в предикатах)