while($true)
{
    w32tm /resync
    Start-Sleep -s 120
}