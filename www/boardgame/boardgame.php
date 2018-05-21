<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>芭乐桌游管理页面</title>
		<link rel="stylesheet" href="../../static/boardgame/bulma.css">
		<script type="text/javascript" src="../../static/boardgame/choose_item.js"></script>
	</head>
	<body>
		<div class="columns">
			<div class="column">
				<h1 class="title">全部桌游</h1>
				<div class="buttons" id="bglist">
<?php
	header("content-Type: text/html; charset=utf-8");
	$dbhost = "localhost";
	$dbuser = "mysql";
	$dbpasswd = "mysql";
	$dbname = "boardgameRecommendation";
	$db = mysqli_connect($dbhost, $dbuser, $dbpasswd, $dbname);
	$userid = mysqli_real_escape_string($db, $_GET["userid"]);
	$userid = urldecode($userid);
	$userid = base64_decode($userid);
	//$userid = openssl_decrypt($userid, "AES-128-CBC", "YEK_A_MA_I_OLLEH", OPENSSL_RAW_DATA, "THIS_IS_A_VECTOR");
	$mylist = "";
	$bglist = "";
	$str = "";
	$ids = array();
	$names = array();
	$sql = "SELECT id, name FROM boardgame";
	mysqli_query($db, "set character set 'utf8'");
	$rslt = mysqli_query($db, $sql);
	while($row = mysqli_fetch_assoc($rslt)){
		array_push($ids,$row["id"]);
		array_push($names,$row["name"]);
	}

	// bar
	$barids = array();
	$sql = "SELECT id FROM barmanager WHERE userid='$userid'";
	mysqli_query($db, "set character set 'utf8'");
	$rslt = mysqli_query($db, $sql);
	while($row = mysqli_fetch_assoc($rslt)){
		array_push($barids,$row["id"]);
	}
	$len = count($names);
	for($i = 0; $i < $len; $i++) {
		if(array_search(strval($i), $barids) === FALSE){
			$bglist .= "<a class=\"button\" data-bgid=\"$i\" data-chosen=\"no\">$names[$i]</a>";
		}
		else {
			$mylist .= "<a class=\"button\" data-bgid=\"$i\" data-chosen=\"yes\">$names[$i]</a>";
		}
	}
	$str .= $bglist;
	$str .= "</div></div>";
	$str .= "<div class=\"column\"><h1 class=\"title\">您的桌游</h1><div class=\"buttons\" id=\"mylist\">";
	$str .= $mylist;

	echo $str;
?>
				</div>
			</div>
		</div>
		<div id="hint">Please choose your boardgame.</div>
		<script type="text/javascript" src="../../static/boardgame/event_register.js"></script>
	</body>
</html>