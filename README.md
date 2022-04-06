# DingZhen
一眼丁真合集，目前已收集374张

随机查看: https://dj.aya1.top

## Api接口: 
https://api.aya1.top/randomdj

| 参数名 | 类型   | 是否必须 | 说明                      |
| ------ | ------ | -------- | ------------------------- |
| r      | string | 否       | 值为0时不进行重定向       |
| g      | string | 否       | 值为1时返回github raw链接 |

示例: 

    直接访问 https://api.aya1.top/randomdj 跳转到图片地址
    访问 https://api.aya1.top/randomdj?r=0 时，返回json

```bash
❯ curl -s "https://api.aya1.top/randomdj?r=0"
{"status":"ok","url":"https://ayatale.coding.net/p/picbed/d/DingZhen/git/raw/main/src/917021660f75098cba21f16aa3d7>

❯ curl -s "https://api.aya1.top/randomdj?r=0&g=1"
{"status":"ok","url":"https://raw.githubusercontent.com/Brx86/DingZhen/main/src/5337fbb353d6f1c68c10bdf4cdcc3b56.jpg"}
```