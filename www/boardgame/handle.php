<?php
header("content-Type: text/html; charset=utf-8");
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

// ="no" if $userid wants to insert $bgid, ="yes" if delete
$op = mysqli_real_escape_string($db, $_GET["op"]);
mysqli_query($db, "set character set 'utf8'");
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
