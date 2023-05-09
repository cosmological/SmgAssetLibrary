$arcExtractsFolderPath = "SMG2-Extracts\ObjectData"
$wiiExplorerPath = "WiiExplorer\WiiExplorer.exe"
$superBmdPath = "SuperBMD\SuperBMD.exe"

#Extract .bdl from .arc with WiiExplorer
$arcFiles = Get-ChildItem -Path $arcExtractsFolderPath -Filter *.arc
foreach ($file in $arcFiles) 
{
    Write-Output "Current .arc file:" $file.FullName

    & $wiiExplorerPath --unpack $file.FullName
    Start-Sleep -Milliseconds 50
}

#I added this sleep to make sure all the subdirectories are found
Start-Sleep -Seconds 3

#Go through each newly created folder and use SuperBMD to convert to .dae
$exportSubdirs = Get-ChildItem -Path $arcExtractsFolderPath -Directory
if ($exportSubdirs)
{
    foreach ($subdir in $exportSubdirs)
    {
        Write-Output 'subDir Name: ' $subdir.Name
        #Find the right .bdl file
        $bdl_file = Get-ChildItem -Path $subdir.FullName -Filter "$($subdir.Name).bdl"

        if ($bdl_file)
        {
            Write-Output ".bdl filepath:" $bdl_file.FullName
            
            & $superBmdPath $bdl_file.FullName
        }
        else {
            Write-Output "Could not find .bdl file"
        }

        Start-Sleep -Milliseconds 100
    }
}
else {
    Write-Output 'Export subDirs is empty'
}
