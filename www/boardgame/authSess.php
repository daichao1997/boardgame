<?php
session_start();
$dbhost = "localhost";
$dbuser = "mysql";
$dbpasswd = "mysql";
$dbname = "boardgameRecommendation";
$db = mysqli_connect($dbhost, $dbuser, $dbpasswd, $dbname);

$code = $_POST["code"];
$rslt = mysqli_query($db, "SELECT * FROM code WHERE code='$code'");

$userid = "0123456789abcdef0123456789abcdef";
while($row = mysqli_fetch_assoc($rslt)) {
	if(time() - $row["time"] < 300) {
		$userid = $row["userid"];
		break;
	}
}

function encrypt_data($data, $iv, $key) {
	$cypher = mcrypt_module_open(MCRYPT_RIJNDAEL_128, '', MCRYPT_MODE_CBC, '');

	// initialize encryption handle
	if (mcrypt_generic_init($cypher, $key, $iv) != -1) {
			// decrypt
			$encrypted = mcrypt_generic($cypher, $data);

			// clean up
			mcrypt_generic_deinit($cypher);
			mcrypt_module_close($cypher);

			return $encrypted;
	}
	return false;
}
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
$iv = bin2hex(openssl_random_pseudo_bytes(8));
$userid = urlencode(base64_encode(encrypt_data($userid.time(), $iv, "HELLO_I_AM_A_KEY")));
// echo $userid;
// echo "<br />";
// $userid = decrypt_data(base64_decode(urldecode("cYfuD%2FhpEGk1ifitF3bh43U34ibsutnXAcO0X7M1eZmbjgf8kA26Yf8oB8EyrqRX")), "HELLO_I_AM_A_KEY", "25649aa5ed9260b7");
// echo $userid;
$_SESSION["userid"] = urldecode("$userid");
$_SESSION["iv"] = urldecode("$iv");

echo "<script type='text/javascript'> window.location.href = 'http://v.internetapi.cn/boardgame/boardgameSess.php?userid={$userid}&iv={$iv}'; </script>";

// echo "<script type='text/javascript'> window.location.href = 'http://v.internetapi.cn/boardgame/boardgameSess.php'; </script>";
// exit;
?>