
This projcet is a minimal demo about autotest.
There are two parts of it.

Requirements:
```
# if you want run the test application server
pip install sanic

# auto api test base on httpx library
pip install httpx

# toml parse
pip insatll toml

```
## tracer
Trace the codes which has been covered.
The core about tracer:
https://docs.python.org/3/library/sys.html#sys.settrace

```
# refrence 
# https://github.com/nedbat/coveragepy
python main.py
```

## auto api test
Parse the toml to auto generate request and run test.
Dont need to write test code any more.
Here are something else we can do:
Rewrite runner to get more test output.
Build more layer from toml to TestCase, add some features.
Others see  auto_api.py.


```
pyhton ./auto_test/auto_api.py
```
To see the resouce file structure.
```
name = "test_signup"
type = "api_test"
priority=0

[api]
url="signup"
timeout=5
method="POST"

[[subcase]]
    [subcase.body]
        username="guest" 
        password="7777777"
    [[subcase.assert]]
        method="equal"
        value=0
        field="code"
        msg="tset code useful"

    [[subcase.assert]]
        method="equal"
        value="success"
        field="message"

[[subcase]]
    [subcase.body]
        username="aksljda"
    [[subcase.assert]]
        method="equal"
        value=101
        field="code"

    [[subcase.assert]]
        method="equal"
        value="fields should not empty"
        field="message"

[[subcase]]
    [subcase.body]
        username="admin"
        password="aksdjakd"

    [[subcase.assert]]
        method="equal"
        value=101
        field="code"

    [[subcase.assert]]
        method="equal"
        value="username already exists"
        field="message"
```


