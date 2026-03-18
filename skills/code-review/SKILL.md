---
name: code-review
description: 进行深入代码评审，覆盖安全、性能和可维护性分析。适用于用户要求评审代码、排查 bug 或审计代码库时。
---

# Code Review Skill

你现在具备系统化代码评审能力。按下面结构执行。

## 评审清单

### 1. 安全性（最高优先级）

检查：
- [ ] **注入漏洞**：SQL、命令、XSS、模板注入
- [ ] **认证问题**：硬编码凭证、弱认证
- [ ] **授权缺陷**：缺少访问控制、IDOR
- [ ] **数据泄露**：日志或错误信息中暴露敏感数据
- [ ] **密码学问题**：弱算法、密钥管理不当
- [ ] **依赖风险**：已知漏洞（用 `npm audit`、`pip-audit` 检查）

```bash
# 快速安全扫描
npm audit                    # Node.js
pip-audit                    # Python
cargo audit                  # Rust
grep -r "password\|secret\|api_key" --include="*.py" --include="*.js"
```

### 2. 正确性

检查：
- [ ] **逻辑错误**：off-by-one、空值处理、边界情况
- [ ] **竞争条件**：并发访问缺乏同步
- [ ] **资源泄露**：文件、连接、内存未释放
- [ ] **错误处理**：异常被吞掉、缺少失败路径
- [ ] **类型安全**：隐式转换、`any` 滥用

### 3. 性能

检查：
- [ ] **N+1 查询**：循环内数据库访问
- [ ] **内存问题**：大对象分配、引用残留
- [ ] **阻塞操作**：异步代码里做同步 I/O
- [ ] **低效算法**：能做 O(n) 却写成 O(n^2)
- [ ] **缺少缓存**：昂贵计算重复执行

### 4. 可维护性

检查：
- [ ] **命名**：是否清晰、一致、可描述
- [ ] **复杂度**：函数超过 50 行、嵌套超过 3 层
- [ ] **重复代码**：复制粘贴的逻辑块
- [ ] **死代码**：未使用导入、不可达分支
- [ ] **注释**：是否过时、冗余，或该写没写

### 5. 测试

检查：
- [ ] **覆盖率**：关键路径是否有测试
- [ ] **边界情况**：空值、空集合、边界值
- [ ] **Mock 策略**：外部依赖是否隔离
- [ ] **断言质量**：是否具体、有意义

## 评审输出格式

```markdown
## 代码评审：[文件/组件名]

### 概要
[1-2 句总体判断]

### 严重问题
1. **[问题]**（第 X 行）：[描述]
   - 影响：[可能造成什么后果]
   - 修复建议：[建议方案]

### 改进项
1. **[建议]**（第 X 行）：[描述]

### 正向评价
- [做得好的地方]

### 结论
[ ] 可以合并
[ ] 需要小改
[ ] 需要大改
```

## 常见需要标记的模式

### Python
```python
# Bad: SQL 注入
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
# Good:
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# Bad: 命令注入
os.system(f"ls {user_input}")
# Good:
subprocess.run(["ls", user_input], check=True)

# Bad: 可变默认参数
def append(item, lst=[]):  # Bug: 共享可变默认值
# Good:
def append(item, lst=None):
    lst = lst or []
```

### JavaScript/TypeScript
```javascript
// Bad: 原型污染
Object.assign(target, userInput)
// Good:
Object.assign(target, sanitize(userInput))

// Bad: 使用 eval
eval(userCode)
// Good: 永远不要对用户输入使用 eval

// Bad: 回调地狱
getData(x => process(x, y => save(y, z => done(z))))
// Good:
const data = await getData();
const processed = await process(data);
await save(processed);
```

## 常用评审命令

```bash
# 查看最近变更
git diff HEAD~5 --stat
git log --oneline -10

# 查找潜在问题
grep -rn "TODO\|FIXME\|HACK\|XXX" .
grep -rn "password\|secret\|token" . --include="*.py"

# 检查复杂度（Python）
pip install radon && radon cc . -a

# 检查依赖
npm outdated  # Node
pip list --outdated  # Python
```

## 评审工作流

1. **理解上下文**：阅读 PR 描述、关联 issue
2. **运行代码**：尽量构建、测试、在本地运行
3. **自顶向下阅读**：先看入口点和主路径
4. **检查测试**：改动是否被覆盖，测试是否通过
5. **安全扫描**：跑自动化检查
6. **手工评审**：按上述清单核查
7. **写反馈**：具体、可执行，并给出修复方向
