$(document).ready(function() {

    const search = document.getElementById('search');
    const search_error = document.getElementById('search_error');
    const another_site_flag = document.getElementById('another_site_flag');
    const another_site = document.getElementById('another_site');
    const select_url = document.getElementById('select_url');
    const url_error = document.getElementById('url_error');
    const results = document.getElementById('results');
    const hints = document.getElementById('hints');


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

            $(url_error).empty();
            $(search_error).empty();

            $(hints).empty();
            $(hints).append( "Идет поиск, ждите результатов!" );

            // TODO если прошла валидацию то очистить ошибки
            $.ajax({
                type: "POST",
                url: url,
                data: $('form').serialize(),
                success: function (data) {
                    $(hints).empty();

                        $(hints).append(data.data.message);


                         // if (data.data.synonyms.length !== 0){
                         //    $(hints).append(
                         //        "Слишком мало совпадений! Попробуйте: " + data.data.synonyms.join(', '));
                         // } else {
                         //     $(hints).append( "Поиск успешно состоялся :)" );
                         // }


                        $(results).empty();
                        console.log(data.data);
                    data.data.results.forEach(function (el, index) {
                        result_element= "<p> "+(index + 1) +". Адрес: <a href='"+el.url+"'>"+el.url+"</a></p>" +
                            "<p> Найденные варианты: " + el.found_arr.join(", ") + "</p>";
                        $(result_element).clone().appendTo( results );
                    })


            },
                error: function () {
                    $(hints).empty();
                    $(hints).append( "Что то пошло не так :(" );

                }
        });
        }
        // Не прошли валидацию
        else{
            // Если нет слов в запросе
            validate_empty_word_input();
            // Если в строке и & и |
            validate_and_or_words();
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
        console.log("Валидация");
        return search.value !== "" && !(~search.value.indexOf("&") && ~search.value.indexOf("|")) &&
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

    function validate_and_or_words() {
        if (~search.value.indexOf("&") && ~search.value.indexOf("|")){
            if (!~search_error.innerText.indexOf("используйте") ){
                search_error.innerText += " [используйте либо '&' либо '|'] ";
            }
        }
        else{
            search_error.innerText =
            search_error.innerText.replace('[используйте либо \'&\' либо \'|\']','');
        }
    }
    // TODO Почему то не работает вроде
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
// TODO стирать предыдущие результаты
// TODO проверять на пустоту между | или &