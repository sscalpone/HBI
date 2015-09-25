$('#delete').click(function(event) {
	event.preventDefault();
	$('#dialog form').removeClass('');
	$('#dialog').load('tracker/delete-photograph.html').dialog();
});