$(document).ready(function(){
	// var bglist = document.getElementById("bglist").childNodes;
	// for(var i = 0; i < bglist.length; i++) {
	// 	//bglist[i].onclick = choose_item;
	// 	bglist[i].onclick = show_action_add;
	// }
	
	// var mylist = document.getElementById("mylist").childNodes;
	// for(i = 0; i < mylist.length; i++) {
	// 	//mylist[i].onclick = choose_item;
	// 	mylist[i].onclick = show_action_del;
	// }
	$("#bglist").children().click(show_action_add)
	$("#mylist").children().click(show_action_del)
	// var action_add = document.getElementById("action-add");
	// var action_del = document.getElementById("action-del");
	// action_add.style.display = "none";
	// action_del.style.display = "none";
	$('#action-add').hide();
	$('#action-del').hide();
	// function wtf(event) {
	// 	if(action_add.style.display == "block") {
	// 		action_add.style.display = "none";
	// 	}
	// 	if(action_del.style.display == "block") {
	// 		action_del.style.display = "none";
	// 	}
	// }
	function wtf(event) {
		if($('#action-add').is(":visible")) {
			$('#action-add').hide();
		}
		if($('#action-del').is(":visible")) {
			$('#action-del').hide();
		}
	}
	document.addEventListener("click", wtf, true);
	// $(document).click(function(event) { 
	// 	if(!$(event.target).closest('#action-add').length) {
	// 		if($('#action-add').is(":visible")) {
	// 			$('#action-add').hide();
	// 		}
	// 	}
	// });

	var add = document.getElementById("add");
	var del = document.getElementById("del");
	var buy_add = document.getElementById("buy-add");
	var buy_del = document.getElementById("buy-del");

	add.onclick = add_item;
	del.onclick = del_item;
	buy_add.onclick = buy_del.onclick = buy_item;
});