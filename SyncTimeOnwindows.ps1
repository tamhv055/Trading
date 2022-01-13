#Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -A
while($true)
{
    w32tm /resync
    Start-Sleep -s 120
}


#Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser