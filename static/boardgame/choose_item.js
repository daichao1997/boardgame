function getQueryString(name) {
	var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
	var r = window.location.search.substr(1).match(reg);
	if (r != null) return unescape(r[2]); return null;
}

function choose_item(event) {
	var userid = getQueryString("userid");
	
	var bglist = document.getElementById("bglist");
	var mylist = document.getElementById("mylist");
	
	var item = event.currentTarget;
	var bgid = item.getAttribute("data-bgid");
	var chosen = item.getAttribute("data-chosen");
	
	if(chosen == "no") {
		item.setAttribute("data-chosen", "yes");
		mylist.appendChild(item);
	}
	else if(chosen == "yes"){
		item.setAttribute("data-chosen", "no");
		//item.setAttribute("class", "button");
		bglist.appendChild(item);
	}
	
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