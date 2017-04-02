$("#sidebar li").click(function() {
	$(this).addClass("selected");
	$(this).siblings().removeClass("selected");
});