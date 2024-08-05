# Import the Active Directory module
Import-Module ActiveDirectory

# Prompt for AD credentials
$cred = Get-Credential

# Query Active Directory for all Windows servers
$servers = Get-ADComputer -Filter {OperatingSystem -like "*Windows*Server*"} -SearchBase "DC=corp,DC=company,DC=com" -Credential $cred

# Initialize an array to hold the results
$results = @()

# Function to check if a server is online
function Test-ServerOnline {
    param (
        [string]$server
    )
    Test-Connection -ComputerName $server -Count 2 -Quiet
}

# Loop through each server and check if it's online
foreach ($server in $servers) {
    $serverName = $server.Name
    if (Test-ServerOnline -server $serverName) {
        # Query local user accounts
        $localUsers = Invoke-Command -ComputerName $serverName -Credential $cred -ScriptBlock {
            Get-WmiObject -Class Win32_UserAccount -Filter "LocalAccount=True AND Disabled=False AND Name<>'Administrator'"
        }

        foreach ($user in $localUsers) {
            $userName = $user.Name
            # Query the local groups the user is a member of
            $localGroups = Invoke-Command -ComputerName $serverName -Credential $cred -ScriptBlock {
                param ($userName)
                Get-LocalUser -Name $userName | Get-LocalGroupMember
            } -ArgumentList $userName

            $userGroups = $localGroups | Select-Object -ExpandProperty Name

            # Append the result to the array
            $results += [PSCustomObject]@{
                ServerName = $serverName
                UserName = $userName
                Groups = $userGroups
            }
        }
    }
}

# Convert the results to JSON and save to a file
$results | ConvertTo-Json | Out-File -FilePath "C:\Temp\EnabledLocalAccounts.json"

Write-Output "The script has completed. Results are saved in C:\Temp\EnabledLocalAccounts.json"
