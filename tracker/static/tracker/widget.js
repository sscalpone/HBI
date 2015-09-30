$('.delete').click(function(event) {
    event.preventDefault();
    $('#dialog form').removeClass('no-display');
    $('#dialog').dialog();
});