import os
import re

from enum import IntFlag, auto


# 需要递交的代码片段的开始和结束标记
# /*SUBMIT BEGIN*/ 和 /*SUBMIT END*/ 之间的代码将被递交
COMMENT_SUBMIT_BEGIN = r"\/\*\s*SUBMIT\s*BEGIN\s*\*\/"
COMMENT_SUBMIT_END = r"\/\*\s*SUBMIT\s*END\s*\*\/"


# 不要递交的代码片段的开始和结束标记
# /*NOT SUBMIT BEGIN*/ 和 /*NOT SUBMIT END*/ 之间的代码将不会被递交
# /*NOT SUBMIT BEGIN*/ 和 /*NOT SUBMIT END*/ 的优先级高于 /*SUBMIT BEGIN*/ 和 /*SUBMIT END*/
COMMENT_NOT_SUBMIT_NEGIN: str = r"\/\*\s*NOT\s*SUBMIT\s*BEGIN\s*\*\/"
COMMENT_NOT_SUBMIT_END: str = r"\/\*\s*NOT\s*SUBMIT\s*END\s*\*\/"


class ConvertMode(IntFlag):
    """转换模式。"""

    # 仅考虑需要递交的代码片段
    POSITIVE = auto()

    # 仅考虑不需要递交的代码片段
    NEGATIVE = auto()

    # 同时考虑需要递交的代码片段和不需要递交的代码片段
    BOTH = POSITIVE | NEGATIVE


def copy_sas_to_txt(
    src: str, dest: str, convert_mode: ConvertMode = ConvertMode.BOTH, encoding: str | None = None
) -> None:
    """将 SAS 代码复制到 txt 文件中，并移除指定标记之间的内容。

    Args:
        src (str): SAS 文件路径。
        dest (str): TXT 文件路径。
        convert_mode (ConvertMode, optional): 转换模式，默认值为 ConvertMode.BOTH。
        encoding (str | None, optional): 字符编码，默认值为 None，将自动检测编码。
    """

    if encoding is None:
        try:
            from chardet import detect
        except ImportError:
            print("没有找到 chardet 库，请先执行 pip install chardet 进行安装。")
            return

        with open(src, "rb") as f:
            encoding = detect(f.read())["encoding"]

    with open(src, "r", encoding=encoding) as f:
        sas_string = f.read()

    if convert_mode in (ConvertMode.NEGATIVE, ConvertMode.BOTH):
        # 移除不需要递交的代码片段
        sas_string = re.sub(
            rf"{COMMENT_NOT_SUBMIT_NEGIN}.*?{COMMENT_NOT_SUBMIT_END}", "", sas_string, flags=re.I | re.S
        )

    if convert_mode in (ConvertMode.POSITIVE, ConvertMode.BOTH):
        # 提取需要递交的代码片段
        sas_string = re.findall(rf"{COMMENT_SUBMIT_BEGIN}(.*?){COMMENT_SUBMIT_END}", sas_string, re.I | re.S)
        sas_string = "".join(sas_string)

    txt_string = sas_string
    with open(dest, "w", encoding=encoding) as f:
        f.write(txt_string)


def copy_sas_to_txt_dir(
    src_dir: str,
    dest_dir: str,
    convert_mode: ConvertMode = ConvertMode.BOTH,
    exclude: list[str] = None,
    encoding: str | None = None,
) -> None:
    """将 SAS 代码复制到 txt 文件中，并移除指定标记之间的内容。

    Args:
        src_dir (str): SAS 文件夹路径。
        dest_dir (str): TXT 文件夹路径。
        convert_mode (ConvertMode, optional): 转换模式，默认值为 ConvertMode.BOTH。
        exclude (list[str], optional): 排除文件名列表，默认值为 None。
        encoding (str | None, optional): 字符编码，默认值为 None，将自动检测编码。
    """

    if not os.path.exists(src_dir):
        print(f"源文件夹 {src_dir} 不存在。")
        return
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for root, _, files in os.walk(src_dir):
        for file in files:
            if exclude is not None and file in exclude:
                continue
            if file.endswith(".sas"):
                src = os.path.join(root, file)
                dest = os.path.join(dest_dir, file.replace(".sas", ".txt"))
                copy_sas_to_txt(src, dest, convert_mode=convert_mode, encoding=encoding)


copy_sas_to_txt_dir(
    r"C:\Users\wtwang\Desktop\tmp\01 主程序",
    r"C:\Users\wtwang\Desktop\tmp\01 主程序\txt",
    convert_mode=ConvertMode.BOTH,
    exclude=["BAplot_daft0.2.sas"],
)

copy_sas_to_txt(
    r"C:\Users\wtwang\Desktop\tmp\01 主程序\BAplot_daft0.2.sas",
    r"C:\Users\wtwang\Desktop\tmp\01 主程序\txt\BAplot_daft0.2.txt",
    convert_mode=ConvertMode.NEGATIVE,
)
