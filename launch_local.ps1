$projectRoot = "D:\Ai explore projects\ML-algo-practice\ml-algorithm-visualizer"
$pythonExe = "C:\Users\cmeht\AppData\Local\Programs\Python\Python310\python.exe"
$appUrl = "http://localhost:8501"

Set-Location $projectRoot

$existingPids = netstat -ano |
    Select-String ":8501" |
    ForEach-Object { (($_.ToString().Trim()) -split "\s+")[-1] } |
    Sort-Object -Unique

foreach ($pidValue in $existingPids) {
    if ($pidValue -match "^[0-9]+$") {
        Stop-Process -Id ([int]$pidValue) -Force -ErrorAction SilentlyContinue
    }
}

$env:STREAMLIT_BROWSER_GATHER_USAGE_STATS = "false"
Start-Process -FilePath $pythonExe -ArgumentList "-m", "streamlit", "run", "app.py", "--server.headless", "true", "--server.port", "8501" -WorkingDirectory $projectRoot | Out-Null

$isReady = $false
for ($i = 0; $i -lt 60; $i++) {
    Start-Sleep -Milliseconds 800
    try {
        $response = Invoke-WebRequest -UseBasicParsing $appUrl -TimeoutSec 2
        if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 500) {
            $isReady = $true
            break
        }
    } catch {
    }
}

if ($isReady) {
    Start-Process $appUrl
} else {
    Write-Output "Server did not become ready in time. Open $appUrl manually."
}
