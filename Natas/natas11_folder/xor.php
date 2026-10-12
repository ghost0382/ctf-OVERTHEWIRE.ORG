<?php
$cipher = hex2bin('1060201f04352316183124181926714d492c3c5547603110082d3f1819606955482435110d24355516');
$plain = '{"showpassword":"no","bgcolor":"#ffffff"}';

for ($i = 0; $i < strlen($cipher); $i++) {
    echo sprintf('%02x', ord($cipher[$i]) ^ ord($plain[$i]));
}
echo PHP_EOL;
?>
