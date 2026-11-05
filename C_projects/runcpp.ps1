$libRoot = "C:/Users/Adam Nagy/Coding projects/coding_projects/C_projects"
$file = (Resolve-Path -LiteralPath (($args -join ' ').Trim('"'))).Path
$dir  = Split-Path $file
$name = [IO.Path]::GetFileNameWithoutExtension($file)
$out  = Join-Path $dir "$name.exe"

function Has-Main($p) { Select-String -Path $p -Pattern '\bmain\s*\(' -Quiet }

$extra = @(
    Get-ChildItem $dir -Filter *.cpp
    Get-ChildItem "$libRoot/C_homebrew_libs" -Recurse -Filter *.cpp
) | Where-Object { $_.FullName -ne $file -and -not (Has-Main $_.FullName) } |
    ForEach-Object FullName |
    Sort-Object -Unique

g++ -std=c++20 $file $extra -I"$libRoot" -I"$dir" -o $out
if ($LASTEXITCODE -eq 0) {
    Set-Location $dir
    & $out
    Write-Host "exit code: $LASTEXITCODE"
} else {
    Write-Host "Compile failed."
}