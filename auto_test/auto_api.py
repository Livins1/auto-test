import os
import unittest
from unittest import TextTestRunner

import toml
from request_adapter import RequestAdapter


def handler_length(value):
    return len(value)


HandlerMap = {"length": handler_length}


class AutoTestManager:
    def __init__(self, case_path="./toml_case"):
        self.case_path = case_path
        self.files = []
        self.cases = []
        self.base_config = ""
        self.runner = TextTestRunner()

    def find_cases(self):
        if not self.case_path:
            raise Exception("Case path unset.")
        for file in os.listdir(self.case_path):

            if not os.path.isabs(file):
                file = os.path.abspath(f"{self.case_path}/{file}")

            filename = os.path.basename(file)

            if filename.startswith("_test") and filename.endswith(".toml"):
                if filename == "_test_config.toml":
                    self.base_config = toml.load(file)
                else:
                    self.files.append(file)
                    self.cases.append(toml.load(file))

    def stdout_cases(self):
        print("====" * 20)
        print("All toml test case:", "" if self.cases else "no cases detective")
        for x in self.files:
            print(x)
        print("====" * 20)

    def build_case(self):
        if self.verbose:
            self.stdout_cases()

        base_config = self.base_config.get("base")
        if not base_config:
            raise Exception("base config unset")
        for case in self.cases:
            if (case_name := case.get("name")) is None:
                case_name = "test_noname"
            api_config = case.get("api")
            if not api_config:
                raise Exception("api config unset")

            for index, subcase in enumerate(case.get("subcase")):
                function_name = f"test_{case_name}_{index}"
                TestCase = TestCaseConstructor(
                    api_config,
                    subcase,
                    RequestAdapter(),
                    base_config=base_config,
                    method_name=function_name,
                )
                self.runner.run(TestCase)

    def verbose(
        self,
    ):
        return self.base_config.get("verbose")

    def show_action(self, output):
        if self.verbose:
            print(output)


def split_keys(field_str, _dict):
    keys = field_str.split(".")
    for key in keys:
        if isinstance(_dict, list):
            _dict[int(key)]
            continue
        _dict = _dict.get(key)
        if not _dict:
            return None
    return _dict


class TestCaseConstructor(unittest.TestCase):
    def __init__(
        self,
        api_config,
        case_config,
        req_adapter,
        method_name,
        base_config=None,
    ):
        self.function_constructor(method_name)
        super(TestCaseConstructor, self).__init__(method_name)
        self.method_name = method_name
        self.req_adapter = req_adapter or RequestAdapter()
        self.case_config = case_config
        self.base_config = base_config
        self.assert_list = case_config.get("assert")
        self.api_config = api_config

        host_url = self.base_config.get("host")
        if not host_url:
            raise Exception("host unset in base configruation")
        self.req_adapter.set_host(host_url)

        api = self.api_config.get("url")
        if not api:
            raise Exception("no api set", case_config)
        self.req_adapter.set_api(api)

        self.req_adapter.set_method(self.api_config.get("method"))

    def assert_builder(self, method, response_value, expcet_value, assert_conf):
        fn = None
        params = None
        if method == "equal":
            fn = self.assertEqual
            params = {"first": response_value, "second": expcet_value}
        elif method == "False":
            fn = self.assertFalse
            params = {"expr": response_value}
        elif method == "IsNotNone":
            fn = self.assertIsNotNone
            params = {"obj": response_value}
        elif method == "CountEqual":
            fn = self.assertCountEqual
            params = {"first": response_value, "second": expcet_value}
        elif method == "":
            fn = self.assertDictEqual
            params = {"d1": response_value, "d2": expcet_value}

        if "msg" in assert_conf.keys():
            params["msg"] = assert_conf["msg"]
        return fn, params

    @classmethod
    def function_constructor(cls, method_name):
        def function(cls):
            cls.req_adapter.set_req_body(cls.case_config.get("body"))
            res = cls.req_adapter.send()

            for assert_conf in cls.assert_list:
                fn = None
                method = assert_conf.get("method")
                if not method:
                    raise Exception("No assert method set")

                field = assert_conf.get("field")
                spfiled = assert_conf.get("splitField")

                if field is None and spfiled is None:
                    raise Exception("field unset")

                fieldHandle = assert_conf.get("fieldHandle")

                res_value = None
                if field:
                    res_value = res.get(field)
                elif spfiled:
                    res_value = split_keys(spfiled, res)

                if fieldHandle:
                    res_value = HandlerMap[fieldHandle](res_value)

                value = assert_conf.get("value")
                function, args = cls.assert_builder(
                    method, res_value, value, assert_conf
                )

                function(**args)

        setattr(cls, method_name, function)


if __name__ == "__main__":
    t = AutoTestManager()
    t.find_cases()
    t.build_case()
