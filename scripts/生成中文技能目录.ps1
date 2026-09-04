param(
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot)
)

$chineseOverrides = @{
    'find-skills' = '发现、筛选并安装适合任务的智能体技能。'
    'imagegen' = '生成或编辑栅格图像。'
    'openai-docs' = '查询 OpenAI 产品、模型、价格与官方文档。'
    'plugin-creator' = '创建并搭建 Codex 插件目录与配置。'
    'review-agent' = '以只读方式审查改动并优先发现缺陷。'
    'skill-creator' = '创建或更新结构合理、可复用的 Codex skill。'
    'skill-installer' = '将 skill 安装到 Codex 的本地技能目录。'
    'ai-video-project-coordination' = '运行异地 AI 视频项目的协作、任务与交付流程。'
    'authority-transfer' = '通过权威背书增强产品或品牌的信任感。'
    'browser-use' = '通过 CDP 直接控制浏览器完成网页交互。'
    'cognitive-contrast' = '通过认知对比突出产品相对竞品的优势。'
    'copywriting-four-step-system' = '用四步法从零创作或诊断销售型文案。'
    'cost-accounting' = '把产品价格拆解为日常小额成本，降低价格阻力。'
    'customer-testimonial' = '选择和编排客户评价，用于提升文案可信度。'
    'dbs' = 'dontbesilent 商业工具箱的任务路由入口。'
    'dbs-action' = '诊断执行力障碍，并给出行动调整建议。'
    'dbs-agent-migration' = '将项目迁移整理为 Codex 或其他智能体工作台。'
    'dbs-ai-check' = '识别文案中的 AI 生成痕迹并提出修订建议。'
    'dbs-benchmark' = '用多重过滤法寻找可借鉴的对标案例。'
    'dbs-bridge' = '把 skill 或 skill 集合桥接到智能体工作流。'
    'dbs-chatroom-austrian' = '以奥地利经济学派视角进行多角色讨论。'
    'dbs-content' = '诊断内容选题与表达，提升内容成型质量。'
    'dbs-content-system' = '把大量内容材料整理为可检索、可复用的系统。'
    'dbs-decision' = '建立并维护个人长期决策系统。'
    'dbs-deconstruct' = '拆解模糊概念，澄清可讨论的问题边界。'
    'dbs-diagnosis' = '诊断商业模式问题并提供问诊或体检框架。'
    'dbs-goal' = '把模糊目标审计为清晰、可执行的目标。'
    'dbs-good-question' = '把模糊提问改写为智能体可推理的好问题。'
    'dbs-hook' = '诊断短视频开头，并优化停留与传播钩子。'
    'dbs-learning' = '将课题拆为连续、可互动的学习内容。'
    'dbs-report' = '合并多次诊断结果，生成可交付的 Markdown 报告。'
    'dbs-resonate' = '诊断文稿共鸣与传播风险。'
    'dbs-restore' = '恢复已保存的诊断状态并继续工作。'
    'dbs-save' = '保存当前诊断的关键状态，方便下次续作。'
    'dbs-script-flow' = '检查短视频逐字稿的逻辑延续与流失风险。'
    'dbs-slowisfast' = '寻找看似更慢、长期更快的行动路径。'
    'dbs-spread' = '用传播心理理论解码内容的传播机制。'
    'dbs-wechat-html' = '把 Markdown 转为可粘贴到微信公众号后台的 HTML。'
    'dbs-xhs-title' = '为小红书内容选择和生成合适标题。'
    'factual-evidence' = '用客观数据或实验增强产品卖点的可信度。'
    'fear-appeal' = '通过痛点与风险唤起，推动读者采取行动。'
    'friend-chat-title' = '生成亲切、像朋友聊天的文案标题。'
    'h3-prompt-writing' = '编写 MiniMax H3 多模式视频生成提示词。'
    'h3context-script-to-video' = '把中英文剧本、角色和场景转为 H3 视频提示词。'
    'justified-consumption' = '消除购买负罪感，让消费决定更容易成立。'
    'libtv-cli' = '使用 LibTV 官方命令行工具操作和运行 LibTV。'
    'local-life-shooting' = '策划并编写本地生活类短视频。'
    'music-caption-rewriter' = '将简短音乐描述改写为更适合发布的音乐文案。'
    'news-editorial-title' = '生成具有新闻感与吸引力的文案标题。'
    'practical-tip-title' = '生成指出痛点并给出解决方案的实用型标题。'
    'price-anchor' = '建立价格锚点，降低消费者对价格的抵触。'
    'sensory-occupation' = '用文字还原使用体验，让读者形成感官代入。'
    'usage-scenario' = '帮助读者看到产品的具体使用场景。'
    'white-amazon-image-set' = '创建或优化亚马逊白底商品图片组。'
}

$roots = @('codex-skills', 'agents-skills')
$records = foreach ($rootName in $roots) {
    $root = Join-Path $RepoRoot $rootName
    if (-not (Test-Path -LiteralPath $root)) { continue }
    Get-ChildItem -LiteralPath $root -Recurse -File -Filter 'SKILL.md' -Force | ForEach-Object {
        $raw = Get-Content -Raw -LiteralPath $_.FullName
        if ($raw -notmatch '(?s)^---\s*\r?\n(.*?)\r?\n---') { throw "缺少 frontmatter：$($_.FullName)" }
        $frontmatter = $Matches[1]
        $name = if ($frontmatter -match '(?m)^name:\s*(.+)$') { $Matches[1].Trim().Trim('"') } else { throw "缺少 name：$($_.FullName)" }
        $description = if ($frontmatter -match '(?m)^description:\s*(.+)$') { $Matches[1].Trim().Trim('"') } else { '' }
        $chineseDescription = if ($description -match '[\u4e00-\u9fff]') { $description } elseif ($chineseOverrides.ContainsKey($name)) { $chineseOverrides[$name] } else { '' }
        if (-not $chineseDescription) { throw "缺少中文说明映射：$name ($($_.FullName))" }
        [pscustomobject]@{
            Source = $rootName
            Name = $name
            Description = $chineseDescription.Replace('|', '／')
            Path = $_.FullName.Substring($RepoRoot.Length + 1).Replace('\', '/')
        }
    }
}

$lines = @(
    '# 技能中文说明目录',
    '',
    "本目录由 `scripts/生成中文技能目录.ps1` 生成，覆盖当前仓库全部 $($records.Count) 个可发现 skill。新增或修改 skill 后运行该脚本，再提交目录文件。",
    '',
    '| 技能名称 | 中文说明 | 来源目录 |',
    '| --- | --- | --- |'
)
foreach ($record in $records | Sort-Object Source, Name, Path) {
    $lines += '| `' + $record.Name + '` | ' + $record.Description + ' | `' + $record.Path + '` |'
}
$output = Join-Path $RepoRoot '技能中文说明目录.md'
[System.IO.File]::WriteAllLines($output, $lines, [System.Text.UTF8Encoding]::new($false))
"已生成：$output（$($records.Count) 个 skill）"
