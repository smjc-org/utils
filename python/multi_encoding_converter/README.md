# multi_encoding_converter.py

- SAS 不同编码环境下，需使用对应编码格式的代码，否则执行过程中可能会报错，或者出现乱码。
- SAS 代码文件需存放在项目的 `src` 目录下，`src` 目录包含多个子文件夹，例如：`src/gbk`, `src/gb2312`, `src/utf8`，分别存放对应编码格式的 SAS 代码文件，初始情况下，只有 `src/gbk` 目录中存在代码文件。
- 基准编码为 `gbk`，可转换编码为 `utf8`, `utf16`, `gb2312`, `gb18030`，部分中文字符可能超出 `gb2312` 可编码的范围，手动修改 `convert_encode_list` 的值即可。

## 使用

```bash
python multi_encoding_converter.py
```
