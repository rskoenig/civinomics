<?php
require_once('lib/loginlib.php');

$variables = decryptData($_REQUEST['param']);
#$variables = decryptDataWithPvtKey($_REQUEST['param'], $_REQUEST['unl']);
echo $variables;
#echo strlen($_REQUEST['param']);
?>
