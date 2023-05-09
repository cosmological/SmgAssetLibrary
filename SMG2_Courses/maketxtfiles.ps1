$filePath = "SMG2Courses.txt"
$lines = Get-Content $filePath

foreach ($line in $lines) {
    $fileName = $line + ".txt"
    New-Item -ItemType File -Path "$fileName" -Value ""
}