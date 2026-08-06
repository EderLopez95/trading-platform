#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Sync and regenerate gRPC/protobuf stubs across the trading-platform services.

.DESCRIPTION
    Each .proto is owned by one service and copied into its consumers. This script
    copies the owner proto to every consumer, regenerates the *_pb2 / *_pb2_grpc
    stubs in each service, and fixes the generated grpc import to the package path
    this project requires (from app.infrastructure.protos.generated import ...).

    Run from the repository root with a Python environment that has grpc_tools
    installed (pip install grpcio-tools).

.PARAMETER Proto
    One of: auth | signal | market_data. Omit to sync all three.

.EXAMPLE
    ./.github/skills/regenerate-grpc-stubs/scripts/sync_protos.ps1 -Proto auth

.EXAMPLE
    ./.github/skills/regenerate-grpc-stubs/scripts/sync_protos.ps1
#>

param(
    [ValidateSet('auth', 'signal', 'market_data')]
    [string]$Proto
)

$ErrorActionPreference = 'Stop'

# Resolve repo root (script lives at .github/skills/regenerate-grpc-stubs/scripts/)
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot '../../../..')
$ProtoSubPath = 'app/infrastructure/protos'

# Owner -> consumers fan-out map (see SKILL.md).
$Map = @{
    'auth'        = @{ Owner = 'auth-service';        Consumers = @('gateway-api', 'signal-service') }
    'signal'      = @{ Owner = 'signal-service';      Consumers = @('gateway-api') }
    'market_data' = @{ Owner = 'market-data-service'; Consumers = @('signal-service') }
}

function Get-ProtoDir([string]$service) {
    Join-Path $RepoRoot "services/$service/$ProtoSubPath"
}

function Sync-One([string]$name) {
    $entry = $Map[$name]
    $owner = $entry.Owner
    $ownerProtoDir = Get-ProtoDir $owner
    $ownerProto = Join-Path $ownerProtoDir "$name.proto"

    if (-not (Test-Path $ownerProto)) {
        throw "Owner proto not found: $ownerProto"
    }

    Write-Host "==> $name.proto (owner: $owner)" -ForegroundColor Cyan

    # 1. Copy owner proto to every consumer.
    foreach ($consumer in $entry.Consumers) {
        $dest = Join-Path (Get-ProtoDir $consumer) "$name.proto"
        Copy-Item -Path $ownerProto -Destination $dest -Force
        Write-Host "    copied -> services/$consumer/$ProtoSubPath/$name.proto"
    }

    # 2. Regenerate stubs + 3. fix imports for owner and every consumer.
    $services = @($owner) + $entry.Consumers
    foreach ($service in $services) {
        $protoDir = Get-ProtoDir $service
        $genDir = Join-Path $protoDir 'generated'
        if (-not (Test-Path $genDir)) { New-Item -ItemType Directory -Path $genDir | Out-Null }

        Push-Location $protoDir
        try {
            python -m grpc_tools.protoc -I . --python_out=generated --grpc_python_out=generated "$name.proto"
            if ($LASTEXITCODE -ne 0) { throw "protoc failed for $service/$name.proto" }
        }
        finally {
            Pop-Location
        }

        # Fix the grpc import to the package-absolute path this project uses.
        $grpcFile = Join-Path $genDir "${name}_pb2_grpc.py"
        if (Test-Path $grpcFile) {
            $content = Get-Content -Raw $grpcFile
            $pattern = "(?m)^import ${name}_pb2 as "
            $replacement = "from app.infrastructure.protos.generated import ${name}_pb2 as "
            $fixed = [regex]::Replace($content, $pattern, $replacement)
            if ($fixed -ne $content) {
                Set-Content -Path $grpcFile -Value $fixed -NoNewline
                Write-Host "    regenerated + import fixed -> services/$service (generated/${name}_pb2_grpc.py)" -ForegroundColor Green
            }
            else {
                Write-Host "    regenerated -> services/$service (import already correct)" -ForegroundColor Green
            }
        }
    }
}

$targets = if ($Proto) { @($Proto) } else { $Map.Keys }
foreach ($t in $targets) { Sync-One $t }

Write-Host "`nDone. Smoke-test the affected services and check gRPC logs." -ForegroundColor Yellow
