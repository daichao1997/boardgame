<?php
// When user clicks a button, an event will be triggered, and we will receive a GET request.
// Handle this request by writing to our database correctly.
$dbhost = "localhost";
$dbuser = "mysql";
$dbpasswd = "mysql";
$dbname = "boardgameRecommendation";
$db = mysqli_connect($dbhost, $dbuser, $dbpasswd, $dbname);
// bgid: boardgame ID of that clicked button
$bgid = mysqli_real_escape_string($db, $_GET["bgid"]);
// userid
$userid = mysqli_real_escape_string($db, $_GET["userid"]);
$userid = urldecode($userid);
$userid = base64_decode($userid);
//$userid = openssl_decrypt($userid, "AES-128-CBC", "YEK_A_MA_I_OLLEH", OPENSSL_RAW_DATA, "THIS_IS_A_VECTOR");
// ="no" if $userid wants to insert $bgid, ="yes" if delete
$op = mysqli_real_escape_string($db, $_GET["op"]);
// Write to our database.
if($op === "yes") {
	$sql = "DELETE FROM barmanager WHERE userid='$userid' AND id='$bgid'";
}
else if($op === "no") {
	$sql = "INSERT INTO barmanager(userid,id) VALUES ('$userid', '$bgid');";
}

if(mysqli_query($db, $sql)){
 	echo "Well done, $userid! You have clicked $bgid.";
}
else{
	echo "Update Failed!";
}
?>
