<?php
/*
* Login Library 
* 
* Karthik
*/

require 'facebook/src/facebook.php';
require 'constants.php';

function base64url_encode($data) {
  return rtrim(strtr(base64_encode($data), '+/', '-_'), '=');
}

function base64url_decode($data) {
  return base64_decode(str_pad(strtr($data, '-_', '+/'), strlen($data) % 4, '=', STR_PAD_RIGHT));
} 


function encryptData($sensitiveData, &$hash) {
    $publicKeys = openssl_pkey_get_public(file_get_contents('public.key'));
    openssl_public_encrypt($sensitiveData, $encryptedData, $publicKeys);
    $transfer = base64url_encode($encryptedData);
    $hash['param'] = $transfer;
    return;
}


function encryptDataWithPvtKey(&$sensitiveData, &$hash) {
    $publicKeys[] = openssl_get_publickey(file_get_contents('public.key'));
    $res = openssl_seal($sensitiveData, $encryptedText, $encryptedKeys, $publicKeys);
    $transfer = base64url_encode($encryptedText);
    $enc = base64url_encode($encryptedKeys[0]);
    $hash['param'] = $transfer;
    $hash['unl'] = $enc;
    return;
}

function decryptData($encryptedData) {
    $passPhrase = 'greenocracy';
    $fp=fopen("private.key","r");
    $priv_key=fread($fp,8192);
    fclose($fp);
    $finalEncData = base64url_decode($encryptedData);
    // $passphrase is required if your key is encoded (suggested)
    $res = openssl_get_privatekey($priv_key);
    //,$passPhrase);
    /*
     * NOTE:  Here you use the returned resource value
    */
    openssl_private_decrypt($finalEncData, $decryptedData,$res);    
    return $decryptedData;
}

function decryptDataWithPvtKey($encryptedData, $encryptedKey) {
    $privateKey = openssl_get_privatekey(file_get_contents('private.key'));

    $result = openssl_open(base64url_decode($encryptedData),
                           $decryptedData,
                           base64url_decode($encryptedKey),
                           $privateKey);
    if (!$result) {
        echo "Error in redir";
    }
        
    return $decryptedData;
}
    /*
    $passPhrase = 'greenocracy';
    $fp=fopen("private.key","r");
    $priv_key=fread($fp,8192);
    fclose($fp);
    #echo $priv_key;
    #echo $encryptedData;
    $finalEncData = base64_decode($encryptedData);
    // $passphrase is required if your key is encoded (suggested)
    $res = openssl_get_privatekey($priv_key,$passPhrase);
     * NOTE:  Here you use the returned resource value
    openssl_private_decrypt($finalEncData, $decryptedData,$res);    
    #echo $decryptedData;
    return $decryptedData;
}
    */

function SetSessionAndRedir(&$fbusr) {
    $uid = $fbusr['id'];
    $ref = 'facebook';
    $expTime = time() + (1*30);
    $urlString = "id=".$uid."&ref=".$ref."&exp=".$expTime;
    //valid=".$expTime."&";
    encryptData($urlString,$urlParams);
    //encryptDataWithPvtKey($urlString,$urlParams);
    #$finalData = decryptData($urlParams['param'], 
    #                $urlParams['unl']);
    //$url = 'decrypt.php?param='.$urlParams['param'].'&unl='.$urlParams['unl'];
    $url = 'decrypt.php?param='.$urlParams['param'];
    #echo strlen($transferData);
    #echo $finalData;
    header ("Location: ".$url);
    #echo $finalData;
    #print_r($fbusr['id']);
    #return $transferData;
}


?>
