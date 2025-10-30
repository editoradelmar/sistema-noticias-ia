<#
.SYNOPSIS
  Sincroniza archivos Markdown desde ./docs/ a la raíz del repositorio.

.DESCRIPTION
  Copia todos los archivos `*.md` encontrados en la carpeta `docs` al directorio raíz.
  Opciones:
    -DryRun : muestra las acciones que se ejecutarían sin realizar cambios
    -Force  : sobrescribe archivos existentes en la raíz (hace backup en --BackupDir)
    -BackupDir <path> : directorio donde se guardan backups antes de sobrescribir (por defecto: ./docs/root_copies_backup)

.EXAMPLE
  .\scripts\sync_docs.ps1 -DryRun
  .\scripts\sync_docs.ps1 -Force

#>

param(
    [switch]$DryRun,
    [switch]$Force,
    [string]$BackupDir = ".\docs\root_copies_backup"
)

function Write-Info($msg){ Write-Host "[info] $msg" -ForegroundColor Cyan }
function Write-Warn($msg){ Write-Host "[warn] $msg" -ForegroundColor Yellow }
function Write-Err($msg){ Write-Host "[error] $msg" -ForegroundColor Red }

try{
    $RepoRoot = (Resolve-Path -Path "./").ProviderPath
    $DocsDir = Join-Path $RepoRoot 'docs'

    if (-not (Test-Path $DocsDir)){
        Write-Err "No existe la carpeta 'docs' en: $RepoRoot"
        exit 2
    }

    $mdFiles = Get-ChildItem -Path $DocsDir -Filter *.md -File -ErrorAction Stop
    if ($mdFiles.Count -eq 0){
        Write-Info "No se encontraron archivos .md en '$DocsDir'. Nada que sincronizar."
        exit 0
    }

    if ($DryRun){ Write-Info "Modo DRY RUN activado — no se realizarán cambios" }

    $actions = @()

    foreach ($f in $mdFiles){
        $src = $f.FullName
        $dest = Join-Path $RepoRoot $f.Name

        if (Test-Path $dest){
            if ($Force){
                $backupPath = Join-Path $RepoRoot $BackupDir
                if (-not (Test-Path $backupPath)){
                    if ($DryRun){ Write-Info "[dry] Crear backup dir: $backupPath" }
                    else { New-Item -ItemType Directory -Path $backupPath -Force | Out-Null }
                }

                $timestamp = (Get-Date).ToString('yyyyMMdd_HHmmss')
                $backupFile = Join-Path $backupPath "$($f.BaseName)_backup_$timestamp$($f.Extension)"

                if ($DryRun){
                    Write-Info "[dry] Mover '$dest' -> '$backupFile' (backup)"
                    Write-Info "[dry] Copiar '$src' -> '$dest' (sobrescribir)"
                } else {
                    Write-Info "Backup: moviendo '$dest' -> '$backupFile'"
                    Move-Item -Path $dest -Destination $backupFile -Force
                    Write-Info "Copiando: '$src' -> '$dest'"
                    Copy-Item -Path $src -Destination $dest -Force
                }
                $actions += @{ Source=$src; Dest=$dest; Action='overwrite'; Backup=$backupFile }
            } else {
                Write-Warn "Omitiendo '$dest' (ya existe). Use -Force para sobrescribir."
                $actions += @{ Source=$src; Dest=$dest; Action='skip' }
            }
        } else {
            if ($DryRun){ Write-Info "[dry] Copiar '$src' -> '$dest'" }
            else { Write-Info "Copiando '$src' -> '$dest'"; Copy-Item -Path $src -Destination $dest }
            $actions += @{ Source=$src; Dest=$dest; Action='copy' }
        }
    }

    Write-Host "`nResumen:`n" -ForegroundColor Green
    $actions | ForEach-Object { Write-Host ("{0} -> {1} : {2}" -f $_.Source, $_.Dest, $_.Action) }

    if ($DryRun){ Write-Info "DryRun finalizado. Ningún archivo fue modificado." }
    else { Write-Info "Sincronización completada." }

    exit 0

} catch{
    Write-Err $_.Exception.Message
    exit 1
}
