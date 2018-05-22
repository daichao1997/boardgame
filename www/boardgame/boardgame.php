<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>芭乐桌游管理页面</title>
		<link rel="stylesheet" href="../../static/boardgame/bulma.css">
		<script type="text/javascript" src="../../static/boardgame/jquery-3.3.1.js"></script>
		<script type="text/javascript" src="../../static/boardgame/choose_item.js"></script>
	</head>
	<body>
		<div class="columns">
			<div class="column">
				<div class="box has-text-centered has-background-grey-dark">
					<h1 class="title has-text-light">全部桌游</h1>
				</div>
				<div class="box has-background-grey">
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

	$secret = "HELLO_I_AM_A_KEY"; // same secret as python
	$iv="HELLO_I_AM_A_KEY";  // same iv as python
	$padding = "{";  //same padding as python
	function decrypt_data($data, $iv, $key) {
		$cypher = mcrypt_module_open(MCRYPT_RIJNDAEL_128, '', MCRYPT_MODE_CBC, '');

		if(is_null($iv)) {
			$ivlen = mcrypt_enc_get_iv_size($cypher);
			$iv = substr($data, 0, $ivlen);
			$data = substr($data, $ivlen);
		}

		// initialize encryption handle
		if (mcrypt_generic_init($cypher, $key, $iv) != -1) {
				// decrypt
				$decrypted = mdecrypt_generic($cypher, $data);

				// clean up
				mcrypt_generic_deinit($cypher);
				mcrypt_module_close($cypher);

				return $decrypted;
		}
		return false;
	}
	$userid = rtrim(decrypt_data(base64_decode($userid), $iv, $secret), $padding);
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
	$rslt = mysqli_query($db, $sql);
	while($row = mysqli_fetch_assoc($rslt)){
		array_push($barids,$row["id"]);
	}
	$len = count($names);
	for($i = 0; $i < $len; $i++) {
		if(array_search($ids[$i], $barids) === FALSE){
			$bglist .= "<a class=\"button is-danger is-inverted is-outlined\" data-bgid=\"$ids[$i]\" data-chosen=\"no\">$names[$i]</a>";
		}
		else {
			$mylist .= "<a class=\"button is-success is-inverted is-outlined\" data-bgid=\"$ids[$i]\" data-chosen=\"yes\">$names[$i]</a>";
		}
	}
	$str .= $bglist;
	$str .= "</div></div></div>";
	$str .= "<div class=\"column\"><div class=\"box has-text-centered has-background-grey-dark\">
					<h1 class=\"title has-text-light\">您的桌游</h1>
				</div><div class=\"box has-background-grey\"><div class=\"buttons\" id=\"mylist\">";
	$str .= $mylist;

	echo $str;
?>
					</div>
				</div>
			</div>
		</div>
		<div class="buttons has-addons" id="action-add">
			<a class="button is-success" id="add">添加</a>
<!--			<a class="button">查看</a>-->
			<a class="button is-info" id="buy-add">购买</a>
		</div>
		<div class="buttons has-addons" id="action-del">
			<a class="button is-danger" id="del">删除</a>
<!--			<a class="button">查看</a>-->
			<a class="button is-info" id="buy-del">购买</a>
		</div>
		<div id="hint">Please choose your boardgame.</div>
		<script type="text/javascript" src="../../static/boardgame/event_register.js"></script>
	</body>
</html>
