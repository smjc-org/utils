# create_virtual_driver.bat

此 `.bat` 脚本主要用于解决 SAS 无法正确处理长路径的问题，特别是在 UTF-8 编码环境下的 SAS 会话中读取和写入文件。

## 使用方法

假设你的项目文件夹的绝对路径是：`D:\OneDrive\统计部\项目\MD\2022\16 xxxxxxxxxxxxxxxxxxxx`，将此 `.bat` 脚本放在该路径下，双击运行即可。

此电脑将会出现一个虚拟磁盘，后续所有文件的读取和写入操作都可以通过这个虚拟磁盘进行。

## 原理

`subst` 命令用于创建虚拟磁盘，利用这一点可将长路径的公共路径替换为虚拟磁盘的盘符，例如：

长路径：

`D:\OneDrive\统计部\项目\MD\2022\16 xxxxxxxxxxxxxxxxxxxx\04 统计分析\06 TFL\01 table\表 6.3.10 按系统器官分类、首选术语和严重程度汇总与试验医疗器械相关的TEAE 安全性分析集.rtf`

替换之后的短路径：

`V:\04 统计分析\06 TFL\01 table\表 6.3.10 按系统器官分类、首选术语和严重程度汇总与试验医疗器械相关的TEAE 安全性分析集.rtf`。
