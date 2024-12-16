from submit import copy_file, copy_directory


class TestSubmit:
    def test_copy_file(tmp_path):
        test_file = "tests/test_file/adam/adae.sas"
        validate_file = "tests/validate_file/adam/adae.txt"
        tmp_file = tmp_path / "adam/adae.txt"

        copy_file(test_file, tmp_file)

        with open(tmp_file, "r", encoding="utf-8") as f:
            tmp_code = f.read()
        with open(validate_file, "r", encoding="utf-8") as f:
            validate_code = f.read()

        assert tmp_code == validate_code

    def test_copy_directory():
        copy_directory("tests/test_file", "tests/tmp")


def main():
    test_list = [func for name, func in globals().items() if callable(func) and name.startswith("test_")]
    for test in test_list:
        test()


if __name__ == "__main__":
    main()
