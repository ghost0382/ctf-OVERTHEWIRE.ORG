<?php
$hex = '6b4253776b4253776b425377';
$binario = hex2bin($hex);

if ($binario === false) {
    die("Stringa esadecimale non valida\n");
}

echo bin2hex($binario) . PHP_EOL;
?>
