<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>芭乐桌游管理页面</title>
		<link rel="stylesheet" href="bulma.css">
		<script type="text/javascript" src="choose_item.js"></script>
	</head>
	<body>
		<div class="columns">
			<div class="column">
				<h1 class="title">全部桌游</h1>
				<div class="buttons" id="bglist">
<?php
	$dbhost = "localhost";
	$dbuser = "mysql";
	$dbpasswd = "mysql";
	$dbname = "boardgameRecommendation";
	$db = mysqli_connect($dbhost, $dbuser, $dbpasswd, $dbname);
	$userid = mysqli_real_escape_string($db, $_GET["userid"]);

	$mylist = "";
	$bglist = "";
	$str = "";
	for($i = 0; $i < 10; $i++) {
		// Do I have it?
		$query = "SELECT id FROM barmanager WHERE userid='$userid' AND id='$i'";
		$query_result = mysqli_query($db, $query);
		// Boardgame name
		$query_name = mysqli_query($db, "SELECT name FROM boardgame WHERE id='$i'");
		$name_row = mysqli_fetch_array($query_name, MYSQLI_BOTH);
		// Dispatch
		if(mysqli_num_rows($query_result) != 0){
			$mylist .= "<a class=\"button\" data-bgid=\"$i\" data-chosen=\"yes\">$name_row[0]</a>";
		}
		else {
			$bglist .= "<a class=\"button\" data-bgid=\"$i\" data-chosen=\"no\">$name_row[0]</a>";
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
		<script type="text/javascript" src="event_register.js"></script>
	</body>
</html>