# twain

## twain 文档

windows 自带的 twain_32.dll 需要 32位的程序调用，用 32 位的 python

`twain org` <https://twain.org/>

`twain-dsm` <https://github.com/twain/twain-dsm>

`pytwain` <https://pytwain.readthedocs.io/en/latest/>

`tawin.py` <https://pytwain.readthedocs.io/en/latest/_modules/twain.html>

source manager

```json
{
  "Id": 1,
  "Version": {
    "MajorNum": 2,
    "MinorNum": 1,
    "Language": 41,
    "Country": 86,
    "Info": ""
  },
  "ProtocolMajor": 2,
  "ProtocolMinor": 1,
  "SupportedGroups": 805306371,
  "Manufacturer": "Kevin Gill",
  "ProductFamily": "TWAIN Python Interface",
  "ProductName": "twain scanner",
  "MajorNum": 2,
  "MinorNum": 1,
  "Language": 41,
  "Country": 86,
  "Info": ""
}
```

source list

```
['TWAIN2 FreeImage Software Scanner']
```

source

```
ss = sm.open_source()
ss_id = ss.identity
print(ss.name, ss_id.get('Id'), ss.is_twain2())
```
