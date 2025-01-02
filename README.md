# utils

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/smjc-org/utils/main.svg)](https://results.pre-commit.ci/latest/github/smjc-org/utils/main)

本仓库包含一些可能有用的工具包。

- [submit.py](https://github.com/smjc-org/py-submit) 递交 `.sas` 代码至监管机构前的处理程序

## pre-commit 安装

```bash
pre-commit install
pre-commit install --hook-type commit-msg
```

## 更新子模块

1. 进入子模块目录

   ```bash
   cd path/to/submodule
   ```

2. 检出指定的 tag

   ```bash
   git checkout <tag-name>
   ```

3. 返回主仓库目录

   ```bash
   cd -
   ```

4. 更新子模块引用

   ```bash
   git add path/to/submodule
   git commit -m "bump: update <submodule> to <tag-name>"
   ```

5. 推送更改到远程仓库

   ```bash
   git push
   ```
