$(document).ready(function() {

    const search = document.getElementById('search');
    const search_error = document.getElementById('search_error');
    const select_url = document.getElementById('select_url');
    const select_error = document.getElementById('select_error');
    const results = document.getElementById('results');
    const hints = document.getElementById('hints');
    const info_btn = document.getElementById('info-btn');
    const info = document.getElementById('info');

    const mySelectr = new Selectr(document.getElementById('select_url'));


    $('form').submit(function (e) {
        e.preventDefault();

        const url = "/process_form/";
        if (validate_form()){
            console.log("Validation ok");

            $(select_error).empty();
            $(search_error).empty();

            $(search).removeClass("red_border");
            $(select_url).removeClass("red_border");

            $(hints).empty();
            $(hints).append( "Идет поиск, ждите результатов!" );

            $(results).empty();
            $(results).append( "Тут будет поисковая выдача" );

            $.ajax({
                type: "POST",
                url: url,
                data: $('form').serialize(),
                success: function (data) {
                    $(hints).empty();

                        $(hints).append(data.data.message);
                        $(results).empty();

                        data.data.results.forEach(function (el, index) {
                            result_element= "<span> "+(index + 1) +". Адрес: <a href='"+el.url+"'>"+el.url+"</a> - найдено " +
                                + el.count + " вариантов(а) </span>" +
                                "<br><span> Найденные варианты: " + el.found_arr.join(", ") + "</span> <br> <br>";
                            $(result_element).clone().appendTo( results );
                        });

                    if (!data.data.results.length){
                        $(results).empty();
                        $(results).append( "Поиск не дал результатов" );
                    }

            },
                error: function () {
                    $(hints).empty();
                    $(hints).append( "Что то пошло не так :(" );
                    $(results).empty();
                    $(results).append( "Поиск не дал результатов" );
                }
        });
        }
        // Не прошли валидацию
        else{
            console.log("Validation fail");
            // Если нет слов в запросе
            validate_empty_word_input();
            //русские символы в запросе
            validate_cyrillic_symbols();
            // Если в строке и & и |
            validate_and_or_words();
            // Если невалиднен селект
            validate_select();
            // Остальные неправильные случаи ввода слов
            validate_words_other();
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
        return search.value !== "" &&
            !/[а-яА-ЯЁё]/.test(search.value)&&
            !predicate_validate_and_or_words() &&
            !predicate_validate_words_other()&&
                $(select_url).val()

    }

    function validate_empty_word_input() {
        if (search.value === ""){
            if (!~search_error.innerText.indexOf("заполните") ){
                search_error.innerText += " [заполните это поле] ";
                $(search).addClass("red_border");
            }

        }
        else{
            search_error.innerText =
            search_error.innerText.replace('[заполните это поле]','');
            if (search_error.innerText === ""){
                $(search).removeClass("red_border");
            }
        }
    }

    function validate_cyrillic_symbols() {
        if (/[а-яА-ЯЁё]/.test(search.value)){
            if (!~search_error.innerText.indexOf("латиница") ){
                search_error.innerText += " [должна присутствовать только латиница] ";
                $(search).addClass("red_border");
            }

        }
        else{
            search_error.innerText =
            search_error.innerText.replace('[должна присутствовать только латиница]','');
            if (search_error.innerText === ""){
                $(search).removeClass("red_border");
            }
        }
    }

    function validate_and_or_words() {
        if (predicate_validate_and_or_words()){
            if (!~search_error.innerText.indexOf("используйте") ){
                search_error.innerText += " [используйте либо '&' либо '|'] ";
                $(search).addClass("red_border");
            }
        }
        else{
            search_error.innerText =
            search_error.innerText.replace('[используйте либо \'&\' либо \'|\']','');
            if (search_error.innerText === ""){
                $(search).removeClass("red_border");
            }

        }
    }

    function predicate_validate_and_or_words() {
        return (~search.value.indexOf("&") && ~search.value.indexOf("|"))
    }

    function predicate_validate_words_other() {
        return(~search.value.indexOf("&&")) ||(~search.value.indexOf("||")) ||(~search.value.indexOf("& "))||
                (~search.value.indexOf(" &")) ||(~search.value.indexOf("| "))|| (~search.value.indexOf(" |"))||
                search.value.indexOf("&") === 0 || search.value.indexOf("|") === 0||
            (search.value.lastIndexOf("&") === (search.value.length -1) && search.value.length)||
             (search.value.lastIndexOf("|") === (search.value.length -1) && search.value.length)
    }

    function validate_words_other() {
        if (predicate_validate_words_other()){
            if (!~search_error.innerText.indexOf("неверно") ){
                search_error.innerText += " [неверно заполнено поле] ";
                $(search).addClass("red_border");
            }
        }
        else{
            search_error.innerText =
            search_error.innerText.replace('[неверно заполнено поле]','');
            if (search_error.innerText === ""){
                $(search).removeClass("red_border");
            }

        }
    }

    function validate_select() {
        if (!$(select_url).val()){
            if (!~select_error.innerText.indexOf("выберите") ){
                select_error.innerText += " [выберите сайт(ы) из списка] ";
                $(select_url).addClass("red_border");
            }
        }
        else {
            select_error.innerText =
            select_error.innerText.replace('[выберите сайт(ы) из списка]','');
            $(select_url).removeClass("red_border");
        }
    }


    $(info_btn).click(function (e) {
        e.preventDefault();
        if ($(info).is(":visible")){
          $(info).hide("fast");
          $(info_btn).val("справка "+$("<div>").html("&#9660;").text())

        }
        else {
         $(info).show("fast");
         $(info_btn).val("справка "+$("<div>").html("&#9650;").text())
        }


    })
});
