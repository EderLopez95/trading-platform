$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

if (-not (Get-Command openssl -ErrorAction SilentlyContinue)) {
    throw "openssl not found in PATH"
}

if (-not (Test-Path "root-ca.key") -or -not (Test-Path "root-ca.pem")) {
    & openssl genrsa -out root-ca.key 4096
    & openssl req -x509 -new -nodes -key root-ca.key -sha256 -days 3650 -out root-ca.pem -subj "/CN=Trading-Platform-Root-CA"
}

function New-ServiceCertificate {
    param(
        [Parameter(Mandatory = $true)][string]$ServiceName,
        [Parameter(Mandatory = $true)][string]$CommonName,
        [Parameter(Mandatory = $true)][string]$ExtFile
    )

    & openssl genrsa -out "$ServiceName.key" 2048
    & openssl req -new -key "$ServiceName.key" -out "$ServiceName.csr" -subj "/CN=$CommonName"
    & openssl x509 -req -in "$ServiceName.csr" -CA root-ca.pem -CAkey root-ca.key -CAcreateserial -out "$ServiceName.pem" -days 825 -sha256 -extfile $ExtFile

    if (Test-Path "$ServiceName.csr") {
        Remove-Item "$ServiceName.csr" -Force
    }
}

New-ServiceCertificate -ServiceName "auth-service" -CommonName "auth_service" -ExtFile "auth-service.ext"
New-ServiceCertificate -ServiceName "signal-service" -CommonName "signal_service" -ExtFile "signal-service.ext"
New-ServiceCertificate -ServiceName "market-data-service" -CommonName "market_data_service" -ExtFile "market-data-service.ext"

Write-Host "Certificates generated in $scriptDir"
