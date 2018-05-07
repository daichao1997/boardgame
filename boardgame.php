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
					$bglist = "";
					$mylist = "";
					if (($bg = fopen("boardgame.csv", "r")) !== FALSE) {
						while (($line = fgetcsv($bg, 1000, ",")) !== FALSE) {
							if($line[2] == "no")
								$bglist = $bglist . "<a class=\"button\" data-bgid=\"$line[0]\" data-chosen=\"no\">$line[1]</a>";
							else if($line[2] == "yes")
								$mylist = $mylist . "<a class=\"button\" data-bgid=\"$line[0]\" data-chosen=\"yes\">$line[1]</a>";
						}
					}
					echo $bglist;
					echo "</div>
			</div>
			<div class=\"column\">
				<h1 class=\"title\">您的桌游</h1>
				<div class=\"buttons\" id=\"mylist\">";
					echo $mylist;
					?>
				</div>
			</div>
		</div>
		<div id="hint">Please choose your boardgame.</div>
		<script type="text/javascript" src="event_register.js"></script>
	</body>
</html>