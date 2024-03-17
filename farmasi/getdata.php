<?php

/* 
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Scripting/EmptyPHP.php to edit this template
 */

header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");

$host = "localhost";
$user = "sik";
$pass = "00";
$database = "yatofa27022024";

$conn = new mysqli($host, $user, $pass, $database);
$sql1 = "SELECT no_rawat FROM antriapotek3";
$result1 = $conn->query($sql1);
$result2 = $result1->fetch_assoc();
$result3 = $result2["no_rawat"];
$sql = "select antriapotek3.no_rawat, pasien.nm_pasien, pasien.alamat, poliklinik.nm_poli, dokter.nm_dokter "
        . "FROM antriapotek3 "
        . "inner join pasien "
        . "inner join reg_periksa "
        . "inner join poliklinik "
        . "inner join dokter "
        . "on antriapotek3.no_rawat=reg_periksa.no_rawat "
        . "and reg_periksa.no_rkm_medis=pasien.no_rkm_medis "
        . "and reg_periksa.kd_dokter=dokter.kd_dokter "
        . "and reg_periksa.kd_poli=poliklinik.kd_poli "
        . "where reg_periksa.no_rawat='$result3'";
$result = $conn->query($sql);

$outp = "";
while($rs = $result->fetch_array(MYSQLI_ASSOC)) {
  if ($outp != "") {$outp .= ",";}
  $outp .= '{"nama":"'  . $rs["nm_pasien"] . '",';
  $outp .= '"poli":"'   . $rs["nm_poli"]        . '",';
  $outp .= '"dokter":"'. $rs["nm_dokter"]     . '"}';
}
$outp ='{"records":['.$outp.']}';
$conn->close();

echo($outp);