# author: @Snoopy1866

from __future__ import annotations
import argparse
import os
import re
from enum import IntFlag, auto

from chardet import detect


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

    def __str__(self) -> str:
        return self.name.lower()

    @classmethod
    def get_from_str(cls, value: str) -> ConvertMode:
        return cls[value.upper()]

    @classmethod
    def get_available_values(cls) -> list[str]:
        modes = [mode.name.lower() for mode in cls]
        modes.append("both")
        return modes


def copy_file(
    sas_file: str, txt_file: str, convert_mode: ConvertMode = ConvertMode.BOTH, encoding: str | None = None
) -> None:
    """将 SAS 代码复制到 txt 文件中，并移除指定标记之间的内容。

    Args:
        sas_file (str): SAS 文件路径。
        txt_file (str): TXT 文件路径。
        convert_mode (ConvertMode, optional): 转换模式，默认值为 ConvertMode.BOTH。
        encoding (str | None, optional): 字符编码，默认值为 None，将自动检测编码。
    """

    if encoding is None:
        with open(sas_file, "rb") as f:
            encoding = detect(f.read())["encoding"]

    with open(sas_file, "r", encoding=encoding) as f:
        sas_code = f.read()

    if convert_mode & ConvertMode.NEGATIVE:
        # 移除不需要递交的代码片段
        sas_code = re.sub(
            rf"{COMMENT_NOT_SUBMIT_NEGIN}.*?{COMMENT_NOT_SUBMIT_END}",
            "",
            sas_code,
            flags=re.I | re.S,
        )

    if convert_mode & ConvertMode.POSITIVE:
        # 提取需要递交的代码片段
        sas_code = re.findall(rf"{COMMENT_SUBMIT_BEGIN}(.*?){COMMENT_SUBMIT_END}", sas_code, re.I | re.S)
        sas_code = "".join(sas_code)

    txt_code = sas_code

    txt_code_dir = os.path.dirname(txt_file)
    if not os.path.exists(txt_code_dir):
        os.makedirs(txt_code_dir)
    with open(txt_file, "w", encoding=encoding) as f:
        f.write(txt_code)


def copy_directory(
    sas_dir: str,
    txt_dir: str,
    convert_mode: ConvertMode = ConvertMode.BOTH,
    exclude_files: list[str] = None,
    exclude_dirs: list[str] = None,
    encoding: str | None = None,
) -> None:
    """将 SAS 代码复制到 txt 文件中，并移除指定标记之间的内容。

    Args:
        sas_dir (str): SAS 文件夹路径。
        txt_dir (str): TXT 文件夹路径。
        convert_mode (ConvertMode, optional): 转换模式，默认值为 ConvertMode.BOTH。
        exclude_files (list[str], optional): 排除文件列表，默认值为 None。
        exclude_dirs (list[str], optional): 排除目录列表，默认值为 None。
        encoding (str | None, optional): 字符编码，默认值为 None，将自动检测编码。
    """

    if not os.path.exists(sas_dir):
        print(f"源文件夹 {sas_dir} 不存在。")
        return
    if not os.path.exists(txt_dir):
        os.makedirs(txt_dir)

    for dirpath, _, filenames in os.walk(sas_dir):
        if exclude_dirs is not None and os.path.split(dirpath)[-1] in exclude_dirs:
            continue
        ref_path = os.path.relpath(dirpath, sas_dir)
        for file in filenames:
            if exclude_files is not None and file in exclude_files:
                continue
            if file.endswith(".sas"):
                sas_file = os.path.join(dirpath, file)
                txt_file = os.path.join(txt_dir, ref_path, file.replace(".sas", ".txt"))
                copy_file(sas_file, txt_file, convert_mode=convert_mode, encoding=encoding)


def main():
    parser = argparse.ArgumentParser(
        prog="submit",
        usage="%(prog)s [options]",
        description="本工具用于在代码递交之前进行简单的转换。",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("sas_dir", help="SAS 文件目录")
    parser.add_argument("txt_dir", help="TXT 文件目录")
    parser.add_argument(
        "-c",
        "--convert_mode",
        type=ConvertMode.get_from_str,
        choices=ConvertMode.get_available_values(),
        default="both",
        help="转换模式",
    )
    parser.add_argument("-exf", "--exclude_files", nargs="*", default=None, help="排除文件列表（默认无）")
    parser.add_argument("-exd", "--exclude_dirs", nargs="*", default=None, help="排除目录列表（默认无）")
    parser.add_argument("-ec", "--encoding", default=None, help="编码格式（默认自动检测）")
    args = parser.parse_args()

    copy_directory(
        sas_dir=args.sas_dir,
        txt_dir=args.txt_dir,
        convert_mode=args.convert_mode,
        exclude_files=args.exclude_files,
        exclude_dirs=args.exclude_dirs,
        encoding=args.encoding,
    )


if __name__ == "__main__":
    main()
