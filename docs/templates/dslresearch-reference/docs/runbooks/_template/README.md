# <Runbook 标题 / Runbook Title>

**状态**：draft
**创建日期**：YYYY-MM-DD
**最后更新**：YYYY-MM-DD
**适用范围**：<一句话写清该 runbook 服务哪个正式入口或哪条现行操作链>

---

## 目的 / Purpose

1. 这份 runbook 解决什么操作问题。
2. 哪类读者或 AI 会使用它。

## 权威状态源 / Formal Truth

1. 当前应该以什么命令、文档、状态文件或入口作为 formal truth。
2. 明确哪些 sidecar、截图、debug 输出、历史记录不属于 formal truth。

## 前置条件 / Preconditions

1. 需要的环境、凭据、配置、数据或外部依赖。
2. 明确哪些条件缺失时应停止，而不是继续猜测。
3. 不要把 fallback、compat 或实现细节写成推荐路径。

## Canonical Entry / 单命令入口

```bash
<当前唯一推荐的正式入口命令>
```

## 执行步骤 / Procedure

1. 第一步做什么。
2. 第二步看什么信号。
3. 第三步如何确认进入下一阶段。

## 常见失败 / Failure Signals

| 信号 | 可能原因 | 下一步 |
| --- | --- | --- |
| | | |

## 恢复或回滚 / Recovery Or Rollback

1. 出现哪种信号时应该回滚。
2. 当前推荐的恢复顺序是什么。
3. 哪些动作需要人工确认，不要让 AI 自作主张。

## 证据与产物 / Evidence

1. 本次执行应留下哪些日志、JSON、HTML 或截图。
2. 哪些产物只属于 debug sidecar，不应当成 runtime truth。

## 完成定义 / Done

1. 哪些条件满足后才算当前 runbook 目标完成。
2. 哪些信号出现时应停止、升级或回填 acceptance，而不是继续扩 scope。

## 相关长期文档 / Related Stable Docs

1. `docs/adr/...`
2. `docs/architecture/...`
3. `docs/changes/<change-id>/acceptance.md`
