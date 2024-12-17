import os
import shutil

from submit import ConvertMode, copy_file, copy_directory


class TestSubmit:
    def test_copy_file(self):
        test_file = "tests/test_file/adam/adae.sas"
        validate_file = "tests/validate_file/adam/adae.txt"
        tmp_file = "tests/tmp/adam/adae.txt"

        copy_file(test_file, tmp_file)

        with open(tmp_file, "r", encoding="utf-8") as f:
            tmp_code = f.read()
        with open(validate_file, "r", encoding="utf-8") as f:
            validate_code = f.read()

        assert tmp_code == validate_code

    def test_copy_directory(self):
        test_dir = "tests/test_file"
        validate_dir = "tests/validate_file"
        tmp_dir = "tests/tmp"
        copy_directory(test_dir, tmp_dir, exclude_dirs=["macro"])
        copy_directory(
            os.path.join(test_dir, "macro"), os.path.join(tmp_dir, "macro"), convert_mode=ConvertMode.NEGATIVE
        )

        for dirpath, _, filenames in os.walk(validate_dir):
            rel_path = os.path.relpath(dirpath, validate_dir)
            for filename in filenames:
                validate_file = os.path.join(validate_dir, rel_path, filename).replace(".sas", ".txt")
                tmp_file = os.path.join(tmp_dir, rel_path, filename).replace(".sas", ".txt")

                if os.path.exists(validate_file) and os.path.exists(tmp_file):
                    with open(tmp_file, "r", encoding="utf-8") as f:
                        tmp_code = f.read()
                    with open(validate_file, "r", encoding="utf-8") as f:
                        validate_code = f.read()

                    assert tmp_code == validate_code
                else:
                    assert False

    def teardown_class(self):
        shutil.rmtree("tests/tmp")


def main():
    test_list = [func for name, func in globals().items() if callable(func) and name.startswith("test_")]
    for test in test_list:
        test()


if __name__ == "__main__":
    main()
    main()
