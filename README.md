# DingZhen
一眼丁真合集，目前已收集203张

随机查看: https://dj.aya1.top

## Api接口: 
https://api.aya1.top/randomdj


| 参数名 | 类型   | 是否必须 | 说明                |
| ------ | ------ | -------- | ------------------- |
| r      | string | 否       | 值为0时不进行重定向 |

示例: 

    直接访问 https://api.aya1.top/randomdj 跳转到图片地址
    访问 https://api.aya1.top/randomdj?r=0 时，返回json

```bash
$ curl -s "https://api.aya1.top/randomdj?r=0"
输出: 
{"status":"ok","url":"https://ayatale.coding.net/p/picbed/d/DingZhen/git/raw/main/src/917021660f75098cba21f16aa3d7a2ae.jpg"}
```