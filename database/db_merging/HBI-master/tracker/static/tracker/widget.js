$("#sidebar li").click({
	$(this).addClass("selected");
	$(this).siblings().removeClass("selected");
}) 