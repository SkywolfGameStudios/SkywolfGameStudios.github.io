# ArcadeZone promo-code generator
# Usage:  .\new_code.ps1 -Code SUMMER300 -Coins 300 -Expires 2026-12-31
# Prints the JSON entry to paste into codes.json (then commit + push the site).
#
# The game hashes SALT + UPPERCASE(code) with SHA-256 and matches against
# codes.json, so the site never exposes the actual code text.
param(
    [Parameter(Mandatory = $true)][string]$Code,
    [Parameter(Mandatory = $true)][int]$Coins,
    [string]$Expires = ""
)

$salt = "AZREDEEM:"
$normalized = $Code.ToUpper().Replace(" ", "")
$bytes = [System.Text.Encoding]::UTF8.GetBytes($salt + $normalized)
$sha = [System.Security.Cryptography.SHA256]::Create()
$hash = ([System.BitConverter]::ToString($sha.ComputeHash($bytes))).Replace("-", "").ToLower()

Write-Host ""
Write-Host "Code to post publicly :  $normalized" -ForegroundColor Green
Write-Host "Paste into codes.json :" -ForegroundColor Cyan
Write-Host ""
$entry = [ordered]@{ hash = $hash; coins = $Coins }
if ($Expires -ne "") { $entry.expires = $Expires }
($entry | ConvertTo-Json).Split("`n") | ForEach-Object { "    " + $_ }
Write-Host ""
Write-Host "(Remember: commit + push the site repo for it to go live.)"
