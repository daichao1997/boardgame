var item;

function getQueryString(name) {
	var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
	var r = window.location.search.substr(1).match(reg);
	if (r != null) return unescape(r[2]); return null;
}
function show_action_add(event) {
	item = event.target;
	var action_add = document.getElementById("action-add");
	action_add.style.display = "block";
	action_add.style.position="absolute";
	action_add.style.left = event.clientX+'px';
	action_add.style.top = event.clientY+'px';
}
function show_action_del(event) {
	item = event.target;
	var action_del = document.getElementById("action-del");
	action_del.style.display = "block";
	action_del.style.position="absolute";
	action_del.style.left = event.clientX+'px';
	action_del.style.top = event.clientY+'px';
}
function add_item(event) {
	var userid = getQueryString("userid");
	
	var bglist = document.getElementById("bglist");
	var mylist = document.getElementById("mylist");
	
	//var item = event.currentTarget;
	var bgid = item.getAttribute("data-bgid");
	var chosen = item.getAttribute("data-chosen");
	
	item.setAttribute("data-chosen", "yes");
	mylist.appendChild(item);
	item.onclick = show_action_del;
	
	var xmlhttp;
	if(window.XMLHttpRequest)
		xmlhttp = new XMLHttpRequest();
	else
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	
	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200)
		{
			document.getElementById("hint").innerHTML = xmlhttp.responseText;
		}
		else
		{
			document.getElementById("hint").innerHTML = "FAIL!";
		}
	}
	xmlhttp.open("GET","handle.php?userid="+userid+"&bgid="+bgid+"&op="+chosen,true);
	xmlhttp.send();
}

function del_item(event) {
	var userid = getQueryString("userid");
	
	var bglist = document.getElementById("bglist");
	var mylist = document.getElementById("mylist");
	
	//var item = event.currentTarget;
	var bgid = item.getAttribute("data-bgid");
	var chosen = item.getAttribute("data-chosen");
	
	item.setAttribute("data-chosen", "no");
	bglist.appendChild(item);
	item.onclick = show_action_add;
	
	var xmlhttp;
	if(window.XMLHttpRequest)
		xmlhttp = new XMLHttpRequest();
	else
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	
	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200)
		{
			document.getElementById("hint").innerHTML = xmlhttp.responseText;
		}
		else
		{
			document.getElementById("hint").innerHTML = "FAIL!";
		}
	}
	xmlhttp.open("GET","handle.php?userid="+userid+"&bgid="+bgid+"&op="+chosen,true);
	xmlhttp.send();
}

function buy_item(event) {
	window.location.replace("https://www.baidu.com");
}