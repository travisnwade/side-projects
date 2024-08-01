# Define variables
$prtgApiUrl = "https://prtg.example.com/api"
$prtgApiToken = "your_prtg_api_token"
$outputFilePath = "C:\path\to\output\prtg_devices.csv"

# Function to query PRTG API and return devices
function Get-PRTGDevices {
    param (
        [string]$ApiUrl,
        [string]$ApiToken
    )

    # Build the API URL for devices query
    $url = "$ApiUrl/table.json?content=devices&columns=device,host,objid&username=api&passhash=$ApiToken"

    # Send API request
    $response = Invoke-RestMethod -Uri $url -Method Get

    # Check if the response contains devices
    if ($response.devices) {
        return $response.devices
    } else {
        Write-Error "No devices found in the PRTG response."
        return @()
    }
}

# Query PRTG API for devices
$devices = Get-PRTGDevices -ApiUrl $prtgApiUrl -ApiToken $prtgApiToken

# Prepare the output data
$outputData = @()
foreach ($device in $devices) {
    $outputData += [PSCustomObject]@{
        DeviceName = $device.device
        IPAddress  = $device.host
        DeviceID   = $device.objid
    }
}

# Export data to CSV
$outputData | Export-Csv -Path $outputFilePath -NoTypeInformation

Write-Output "PRTG devices information exported to $outputFilePath"
