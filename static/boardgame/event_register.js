var bglist = document.getElementById("bglist").childNodes;
for(var i = 0; i < bglist.length; i++) {
	bglist[i].onclick = choose_item;
}
var mylist = document.getElementById("mylist").childNodes;
for(i = 0; i < mylist.length; i++) {
	mylist[i].onclick = choose_item;
}