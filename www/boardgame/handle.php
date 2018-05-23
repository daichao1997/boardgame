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

$secret = "HELLO_I_AM_A_KEY";
$iv = mysqli_real_escape_string($db, $_GET["iv"]);

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

$userid = (string)(decrypt_data(base64_decode($userid), $iv, $secret));
preg_match_all('/\d+/', $userid, $nums);
$pos = strrpos($userid, substr(end($nums[0]), -1), 0);
$userid = substr($userid, 0, $pos+1);
$userid = substr($userid, 0, strlen($userid)-10);
//if(base64_encode(base64_decode($userid)) !== $userid) {
//	echo "Invalid User ID: $userid";
//	exit;
//}

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
 	echo "Your User ID: $userid. You have just choosed $bgid.";
}
else{
	echo "Update Failed!";
}
?>
