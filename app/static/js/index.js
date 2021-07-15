// ------------------------------------------------------
// Focus input
// ------------------------------------------------------
$('.form_input>input,.form_input>textarea').each(function () {
    $(this).on('blur', function () {
        if ($(this).val().trim() != "") {
            $(this).addClass('has-val');
            $(this).prev().fadeIn()
        } else {
            $(this).prev().fadeOut()
            $(this).removeClass('has-val');
        }
    })
})


// ------------------------------------------------------
// Show Password
// ------------------------------------------------------
$('.form_input>.pass_show').on('click', function () {
    if (!$(this).hasClass('toggle')) {
        $(this).addClass('toggle')
        $(this).children().children().attr('xlink:href', '/static/svg/sprite.svg#icon-hide')
        $(this).next().attr('type', 'text');
        $(this).next().focus();

    } else {
        $(this).removeClass('toggle')
        $(this).children().children().attr('xlink:href', '/static/svg/sprite.svg#icon-show')
        $(this).next().attr('type', 'password')
        $(this).next().focus();
    }
});
$('.form_input>input[type="password"]').each(function () {
    $(this).on('keypress', function (e) {
        if (e.keyCode === 32) {
            if ($(this).val().trim() == "") {
                $(this).prev().fadeOut()
            }
            return false;
        }
        $(this).prev().fadeIn()
    })
})