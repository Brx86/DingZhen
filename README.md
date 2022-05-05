# DingZhen
一眼丁真合集，目前已收集495张

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
{"status":"ok","url":"https://ayatale.coding.net/p/picbed/d/DingZhen/git/raw/main/src/e8ec2812f1ff441d21abba6bb67bd898.jpg"}

❯ curl -s "https://api.aya1.top/randomdj?r=0&g=1"
{"status":"ok","url":"https://raw.githubusercontent.com/Brx86/DingZhen/main/src/5337fbb353d6f1c68c10bdf4cdcc3b56.jpg"}
```

# 义眼丁真收集站
另一个丁真表情包收集站，功能更多，界面更友好。 

网址: https://www.yiyandingzhen.top/

## Api接口:
http://www.yiyandingzhen.top/getpic.php

返回示例: 
```json
[
    {
        "fore": {"0": "圆焰丁真", "fore": "圆焰丁真"},
        "mid": {"0": "鉴定为", "mid": "鉴定为"},
        "suffix": {"0": "女同", "suffix": "女同"},
        "picpath": {"0": "pic/367_yuanyandingzhen.png.jpg", "pic_path": "pic/367_yuanyandingzhen.png.jpg"},
        "rand_status": null,
        "rand": 367,
        "request-id": null,
        "verified": {"0": "1", "verified": "1"}
    }
]
```