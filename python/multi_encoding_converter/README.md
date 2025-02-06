# multi_encoding_converter.py

> [!IMPORTANT]
>
> - SAS 不同编码环境下，需使用对应编码格式的代码，否则执行过程中可能会报错，或者出现乱码。
> - SAS 代码文件需存放在项目的 `src` 目录下，`src` 目录包含多个子文件夹，例如：`src/gbk`, `src/gb2312`, `src/utf8`，分别存放对应编码格式的 SAS 代码文件，初始情况下，只有 `src/gbk` 目录中存在代码文件。
> - 基准编码为 `gbk`，可转换编码为 `utf8`, `utf16`, `gb2312`, `gb18030`，部分中文字符可能超出 `gb2312` 可编码的范围，手动修改 `convert_encode_list` 的值即可。

## 使用

```bash
python multi_encoding_converter.py
```

## Github workflow 示例

```yml
name: multi_encoding_converter

on:
  pull_request:
    types: [opened, synchronize, reopened]
    paths:
      - "src/**.sas"
      - "multi_encoding_converter.py"

defaults:
  run:
    shell: bash -e {0}

jobs:
  convert:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: 3.13

      - name: Run converter
        run: python multi_encoding_converter.py

      - name: Configure Git
        run: |
          git config --global user.name  "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"

      - name: Check for changes
        id: check_changes
        run: |
          if [ -n "$(git status --porcelain)" ]; then
            echo "has_changed=true" >> $GITHUB_OUTPUT
          fi

      - name: Commit changes
        if: ${{ steps.check_changes.outputs.has_changed == 'true' }}
        run: |
          git add .
          git commit -m "chore: multi encoding version"
          git pull --rebase origin ${{ github.head_ref }}
          git push origin HEAD:${{ github.head_ref }}

      - name: Push changes
        if: ${{ steps.check_changes.outputs.has_changed == 'true' }}
        uses: ad-m/github-push-action@master
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          branch: ${{ github.head_ref }}
```
