param(
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot)
)

$chineseNames = @{
    'arkcli-api-explorer' = 'ARK 原始 API 探索器'
    'arkcli-auth' = 'ARK 认证管理'
    'arkcli-billing' = 'ARK 账单查询'
    'arkcli-chat' = 'ARK 多模态对话'
    'arkcli-code-example' = 'ARK 调用示例生成器'
    'arkcli-config' = 'ARK 本地配置管理'
    'arkcli-connect' = 'ARK 技能连接器'
    'arkcli-custommodel' = 'ARK 自定义模型管理'
    'arkcli-deploy' = 'ARK 推理部署'
    'arkcli-infer-endpoint' = 'ARK 推理接入点管理'
    'arkcli-models' = 'ARK 模型查询'
    'arkcli-plans' = 'ARK 套餐管理'
    'arkcli-pricing' = 'ARK 模型定价查询'
    'arkcli-profile' = 'ARK 配置切面管理'
    'arkcli-resources' = 'ARK 资源查询'
    'arkcli-understand' = 'ARK 多模态理解'
    'arkcli-usage' = 'ARK 用量查询'
    'find-skills' = '技能发现与安装'
    'imagegen' = '图像生成与编辑'
    'openai-docs' = 'OpenAI 官方文档'
    'plugin-creator' = '插件创建器'
    'review-agent' = '代码审查智能体'
    'skill-creator' = '技能创建器'
    'skill-installer' = '技能安装器'
    'browser-use' = '浏览器自动化'
    'h3-action-translator' = 'H3 动作翻译器'
    'h3-prompt-writing' = 'H3 提示词编写器'
    'h3context-script-to-video' = 'H3 剧本转视频'
    'huoshan-video-generation' = '火山视频生成'
    'libtv-cli' = 'LibTV 命令行工具'
    'local-life-shooting' = '本地生活短视频创作'
    'music-caption-rewriter' = '音乐文案改写器'
    'sales-video-copy-cases' = '销售视频文案案例库'
    'white-amazon-image-set' = '亚马逊白底图组'
}

$catalogPath = Join-Path $RepoRoot '技能中文说明目录.md'
if (-not (Test-Path -LiteralPath $catalogPath)) { throw "缺少中文目录：$catalogPath" }
$descriptions = @{}
Get-Content -LiteralPath $catalogPath | ForEach-Object {
    if ($_ -match '^\| `(?<name>[^`]+)` \| (?<description>.+) \| `(?<path>[^`]+)` \|$') {
        $descriptions[$Matches['path']] = $Matches['description']
    }
}

$changed = @()
Get-ChildItem -LiteralPath $RepoRoot -Recurse -File -Filter 'SKILL.md' -Force | ForEach-Object {
    $relativePath = $_.FullName.Substring($RepoRoot.Length + 1).Replace('\', '/')
    $raw = Get-Content -Raw -LiteralPath $_.FullName
    if ($raw -match '(?s)^---\s*\r?\n(.*?)\r?\n---') {
        $frontmatter = $Matches[1]
    }
    else { throw "缺少 frontmatter：$relativePath" }
    if ($frontmatter -notmatch '(?m)^name:\s*(.+)$') { throw "缺少 name：$relativePath" }
    $name = $Matches[1].Trim().Trim('"')
    if (-not $descriptions.ContainsKey($relativePath)) { throw "中文目录缺少说明：$relativePath" }
    $description = $descriptions[$relativePath]
    $body = $raw -replace '(?s)^---\s*\r?\n.*?\r?\n---\s*', ''
    $heading = if ($body -match '(?m)^#\s+(.+)$') { $Matches[1].Trim() } else { '' }
    $chineseName = if ($heading -match '[\u4e00-\u9fff]') { $heading } elseif ($chineseNames.ContainsKey($name)) { $chineseNames[$name] } else { throw "缺少中文名称映射：$name ($relativePath)" }
    $summary = ($description -replace '\s+', ' ').Trim()
    if ($summary.Length -gt 52) { $summary = $summary.Substring(0, 52) + '…' }
    $baseRaw = $raw -replace '(?s)\r?\n## 中文名称与说明\r?\n.*\z', ''
    $addition = [Environment]::NewLine + '## 中文名称与说明' + [Environment]::NewLine + [Environment]::NewLine + '- 中文名称：' + $chineseName + [Environment]::NewLine + '- 用途说明：' + $description + [Environment]::NewLine
    $updatedRaw = $baseRaw.TrimEnd() + [Environment]::NewLine + $addition
    if ($updatedRaw -ne $raw) {
        [System.IO.File]::WriteAllText($_.FullName, $updatedRaw, [System.Text.UTF8Encoding]::new($false))
        $changed += [pscustomobject]@{ Path = $relativePath; ChineseName = $chineseName; Summary = $summary }
    }
}

$changed | ConvertTo-Json -Depth 3
