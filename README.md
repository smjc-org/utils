# utils

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/smjc-org/utils/main.svg)](https://results.pre-commit.ci/latest/github/smjc-org/utils/main)

本仓库包含一些可能有用的工具包。

| 🎯 语言 | 🧩 程序名称                   | ✨ 描述                                | 📚 文档                                                         |
| ------- | ----------------------------- | -------------------------------------- | --------------------------------------------------------------- |
| Python  | `submit.py`                   | 递交 `.sas` 代码至监管机构前的处理程序 | [↗️](https://github.com/smjc-org/py-submit/blob/main/README.md) |
| Python  | `multi_encoding_converter.py` | 编码格式转换                           | [↗️](python/multi_encoding_converter/README.md)                 |
| Batch   | `create_virtual_driver.bat`   | 创建虚拟磁盘                           | [↗️](batch/create_virtual_driver/README.md)                     |

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

2. 获取所有 tags

   ```bash
   git fetch --tags
   ```

3. 检出指定的 tag

   ```bash
   git checkout <tag-name>
   ```

4. 返回主仓库目录

   ```bash
   cd -
   ```

5. 更新子模块引用

   ```bash
   git add path/to/submodule
   git commit -m "bump: update <submodule> to <tag-name>"
   ```

6. 推送更改到远程仓库

   ```bash
   git push
   ```
