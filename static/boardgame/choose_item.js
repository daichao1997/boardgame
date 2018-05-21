var item;

function getQueryString(name) {
	var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
	var r = window.location.search.substr(1).match(reg);
	if (r != null) return unescape(r[2]); return null;
}
function show_action_add(event) {
	item = event.target;
	//var action_add = document.getElementById("action-add");
	$("#action-add").show();
	// action_add.style.position="absolute";
	// action_add.style.left = event.pageX+'px';
	// action_add.style.top = event.pageY+'px';
	$('#action-add').css({ 
		position: "absolute",
		top: event.pageY+'px', left: event.pageX+'px'
	}).appendTo('body');
}

function show_action_del(event) {
	item = event.target;
	//var action_del = document.getElementById("action-del");
	$("#action-del").show();
	// action_del.style.position="absolute";
	// action_del.style.left = event.pageX+'px';
	// action_del.style.top = event.pageY+'px';
	$('#action-del').css({ 
		position: "absolute",
		top: event.pageY+'px', left: event.pageX+'px'
	}).appendTo('body');
}
function add_item(event) {
	var userid = getQueryString("userid");
	
	// var bglist = document.getElementById("bglist");
	var mylist = document.getElementById("mylist");
	
	//var item = event.currentTarget;
	var bgid = item.getAttribute("data-bgid");
	var chosen = item.getAttribute("data-chosen");
	
	var xmlhttp;
	if(window.XMLHttpRequest)
		xmlhttp = new XMLHttpRequest();
	else
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	
	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200)
		{
			document.getElementById("hint").innerHTML = xmlhttp.responseText;
			item.setAttribute("data-chosen", "yes");
			mylist.appendChild(item);
			item.onclick = show_action_del;
			//$(item).click(show_action_del);
			item.className = "button is-success is-inverted is-outlined";
		}
		else
		{
			document.getElementById("hint").innerHTML = "FAIL!";
		}
	}
	if(!userid || userid.length != 44) {
		document.getElementById("hint").innerHTML = "Invalid userid";
	}
	else {
		xmlhttp.open("GET","handle.php?userid="+userid+"&bgid="+bgid+"&op="+chosen,true);
		xmlhttp.send();
	}
}

function del_item(event) {
	var userid = getQueryString("userid");
	
	var bglist = document.getElementById("bglist");
	// var mylist = document.getElementById("mylist");
	
	//var item = event.currentTarget;
	var bgid = item.getAttribute("data-bgid");
	var chosen = item.getAttribute("data-chosen");
	
	var xmlhttp;
	if(window.XMLHttpRequest)
		xmlhttp = new XMLHttpRequest();
	else
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	
	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200)
		{
			document.getElementById("hint").innerHTML = xmlhttp.responseText;
			item.setAttribute("data-chosen", "no");
			bglist.appendChild(item);
			item.onclick = show_action_add;
			item.className = "button is-danger is-inverted is-outlined";
		}
		else if (xmlhttp.readyState == 4)
		{
			document.getElementById("hint").innerHTML = "FAIL!";
		}
	}
	if(!userid || userid.length != 44) {
		document.getElementById("hint").innerHTML = "Invalid userid";
	}
	else {
		xmlhttp.open("GET","handle.php?userid="+userid+"&bgid="+bgid+"&op="+chosen,true);
		xmlhttp.send();
	}
}

var links = new Array(26);
links[0] = "https://detail.tmall.com/item.htm?id=520039178599"
links[1] = "https://detail.tmall.com/item.htm?id=41414138685"
links[2] = "https://item.taobao.com/item.htm?id=3477905332"
links[3] = "https://item.taobao.com/item.htm?id=10917532149"
links[4] = "https://detail.tmall.com/item.htm?id=15735285950"
links[5] = "https://detail.tmall.com/item.htm?id=44234749492"
links[6] = "https://detail.tmall.com/item.htm?id=10625792948"
links[7] = "https://detail.tmall.com/item.htm?id=4298984588"
links[8] = "https://detail.tmall.com/item.htm?id=522968001275"
links[9] = "https://detail.tmall.com/item.htm?id=14852080978"
links[10] = "https://item.taobao.com/item.htm?id=535636029062"
links[11] = "https://detail.tmall.com/item.htm?id=25495324479"
links[12] = "https://item.taobao.com/item.htm?id=10917532149"
links[13] = "https://item.taobao.com/item.htm?id=6728804097"
links[14] = "https://detail.tmall.com/item.htm?id=17345949847"
links[15] = "https://item.taobao.com/item.htm?id=6023896479"
links[16] = "https://item.taobao.com/item.htm?id=3412059509"
links[17] = "https://item.taobao.com/item.htm?id=10311501840"
links[18] = "https://detail.tmall.com/item.htm?id=41439472591"
links[19] = "https://detail.tmall.com/item.htm?id=549541479299"
links[20] = "https://item.taobao.com/item.htm?id=3782592653"
links[21] = "https://item.taobao.com/item.htm?id=523994323646"
links[22] = "https://item.taobao.com/item.htm?id=8518310263"
links[23] = "https://item.taobao.com/item.htm?id=3959805429"
links[24] = "https://item.taobao.com/item.htm?id=3421467337"
links[25] = "https://item.taobao.com/item.htm?id=3335212729"

function buy_item(event) {
	var bgid = parseInt(item.getAttribute("data-bgid"));
	window.open(links[bgid],"_blank");
}
