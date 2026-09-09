# Creates a NEW PRIVATE GitHub repository and publishes this documentation.
# Prerequisites: Git, GitHub CLI, and `gh auth login` for the target account.
# Refuses existing remotes, dirty worktrees, wrong accounts, and non-main branches.
[CmdletBinding()]
param(
    [ValidatePattern('^[A-Za-z0-9][A-Za-z0-9-]*$')]
    [string]$Owner = 'kstecrypto-hub',
    [ValidatePattern('^[A-Za-z0-9][A-Za-z0-9._-]*$')]
    [string]$RepositoryName = 'council'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Invoke-Checked {
    param(
        [Parameter(Mandatory = $true)][string]$Command,
        [string[]]$ArgumentList = @()
    )
    $result = & $Command @ArgumentList
    if ($LASTEXITCODE -ne 0) {
        throw "$Command failed (exit $LASTEXITCODE). Review the preceding output."
    }
    return $result
}

Push-Location $PSScriptRoot
try {
    foreach ($program in @('git', 'gh')) {
        if (-not (Get-Command $program -ErrorAction SilentlyContinue)) {
            throw "$program is required. Install it and reopen PowerShell before retrying."
        }
    }
    if (-not (Test-Path -LiteralPath '.git' -PathType Container)) {
        throw 'The packaged .git folder is missing. Extract the complete archive before publishing.'
    }

    $root = [string](Invoke-Checked 'git' @('rev-parse', '--show-toplevel'))
    if ((Resolve-Path -LiteralPath $root).Path -ne (Resolve-Path -LiteralPath $PSScriptRoot).Path) {
        throw 'This script must publish only its own repository root.'
    }
    $branch = [string](Invoke-Checked 'git' @('branch', '--show-current'))
    if ($branch.Trim() -ne 'main') {
        throw 'Expected the prepared main branch. No repository was created.'
    }
    $dirty = @(Invoke-Checked 'git' @('status', '--porcelain', '--untracked-files=all'))
    if ($dirty.Count -gt 0) {
        throw 'The working tree has changes. Review and commit intended files before publishing.'
    }
    $remotes = @(Invoke-Checked 'git' @('remote'))
    if ($remotes.Count -gt 0) {
        throw 'An existing remote was found. Refusing to overwrite or republish it automatically. See PUBLISHING.md.'
    }
    $localCommit = ([string](Invoke-Checked 'git' @('rev-parse', 'HEAD'))).Trim()
    $login = ([string](Invoke-Checked 'gh' @('api', '--hostname', 'github.com', 'user', '--jq', '.login'))).Trim()
    if ($login -ine $Owner) {
        throw "Active GitHub account is '$login', not '$Owner'. Run gh auth switch --hostname github.com --user $Owner, then retry."
    }

    $fullName = "$Owner/$RepositoryName"
    Write-Host "Creating NEW PRIVATE repository: $fullName"
    Invoke-Checked 'gh' @('auth', 'setup-git', '--hostname', 'github.com') | Out-Host
    Invoke-Checked 'gh' @(
        'repo', 'create', $fullName, '--private', '--source', $PSScriptRoot,
        '--remote', 'origin', '--description',
        'Council: approved design for an evidence-grounded multi-agent investigation platform.'
    ) | Out-Host

    $metadataText = (Invoke-Checked 'gh' @('repo', 'view', $fullName, '--json', 'nameWithOwner,isPrivate,url')) -join "`n"
    $metadata = $metadataText | ConvertFrom-Json
    if ($metadata.nameWithOwner -ine $fullName -or $metadata.isPrivate -ne $true) {
        throw 'Repository identity or privacy verification failed. No git push was attempted.'
    }

    # The remote was just created above; do not modify any pre-existing remote.
    $remoteUrl = "https://github.com/$fullName.git"
    Invoke-Checked 'git' @('remote', 'set-url', 'origin', $remoteUrl) | Out-Host
    Invoke-Checked 'git' @('push', '--set-upstream', 'origin', 'main') | Out-Host

    $remoteLine = [string](Invoke-Checked 'git' @('ls-remote', '--exit-code', 'origin', 'refs/heads/main'))
    $remoteCommit = ($remoteLine.Trim() -split '\s+')[0]
    if ($remoteCommit -ne $localCommit) {
        throw 'Remote main does not match the local commit. Publication could not be verified.'
    }
    Write-Host ''
    Write-Host "Verified private repository: $($metadata.url)"
    Write-Host "Branch: main | Commit: $localCommit"
    Write-Host 'Documentation only. The application has not been implemented.'
}
catch {
    Write-Host "Publication stopped: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host 'No existing repository is deleted or force-pushed by this script.'
    Write-Host 'Authentication: gh auth login --hostname github.com --git-protocol https --web'
    Write-Host 'A failed creation/push may leave a new repository or origin remote; inspect them before retrying.'
    exit 1
}
finally {
    Pop-Location
}
