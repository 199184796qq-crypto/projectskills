# projectskills

本仓库备份本机可复用的 Codex skills 与 `.agents` skills，供新项目或新成员安装、复制和维护。

```text
codex-skills/   # 来自 ~/.codex/skills，含 .system 基础能力
agents-skills/  # 来自 ~/.agents/skills
```

本仓库不保存访问令牌、API 密钥、`.env`、本地连接文件或运行缓存。涉及第三方平台的 skill 应从环境变量或成员本机连接文件读取凭据。

所有可发现 skill 的中文名称与说明见 [技能中文说明目录.md](技能中文说明目录.md)。新增或修改 skill 后，运行 `scripts/生成中文技能目录.ps1` 更新目录。
