# DingZhen
一眼丁真合集，目前已收集504张

随机查看: https://dj.aya1.top

## Api接口

### 随机丁真（Collected by Aya）
返回一张随机的丁真表情包
#### GET https://api.aya1.top/randomdj

| 参数 | 类型 | 默认值 | 说明                    |
| ---- | ---- | ------ | ----------------------- |
| r    | int  | 1      | 值为0时不进行重定向,    |
| g    | int  | 0      | 值为1时返回github的直链 |

#### 示例：

直接访问 https://api.aya1.top/randomdj 跳转到图片地址

访问 https://api.aya1.top/randomdj?r=0 时，返回json

curl调用：
```bash
$ curl -s "https://api.aya1.top/randomdj?r=0"
输出：
{"status":"ok","url":"https://ayatale.coding.net/p/picbed/d/DingZhen/git/raw/main/src/917021660f75098cba21f16aa3d7a2ae.jpg"}
$ curl -s "https://api.aya1.top/randomdj?r=0&g=1"
输出：
{"status":"ok","url":"https://raw.githubusercontent.com/Brx86/DingZhen/main/src/87754eabec44cc90ba5c198454871990.jpg"}
```

### 隐约丁真（Powered by Wombo.Art）：
根据关键词，调用wombo即时生成
#### POST https://api.aya1.top/wombo

| 参数     | 类型 | 默认值   | 说明                 |
| -------- | ---- | -------- | -------------------- |
| keywords | str  | (必填)   | 待生成图片的关键词   |
| style    | int  | 1~26随机 | 图片风格(1~26的序号) |
| file     | int  | 0        | 值为1时返回图片文件  |

#### 示例：

curl调用，关键词`cloud`，返回json
```bash
curl -X POST "https://api.aya1.top/wombo" \
-d '{"keywords":"cloud"}' \
-H "Content-type: application/json" | jq
```
输出：
```json
{
    "style": "Ghibli",
    "keywords": "cloud",
    "status": "ok",
    "url": "https://prod-wombo-paint.s3.amazonaws.com/exports/8d0ea5be-b4f8-4de5-b510-9aba6d9cfac4/blank_tradingcard.jpg?AWSAccessKeyId=AKIAWGXQXQ6WCOB7PP5J&Signature=9b9%2B8eVegCrkf8T060cQxCOd9Ek%3D&Expires=1663739352"
}
```

python调用，关键词`desert`，风格`18`RoseGold，返回json
```python
r = requests.post(
    "https://api.aya1.top/wombo",
    json={"keywords": "desert", "style": 18},
    timeout=60,
)
print(r.json())
```
输出：
```json
{
    "style": "RoseGold",
    "keywords": "desert",
    "status": "ok",
    "url": "https://prod-wombo-paint.s3.amazonaws.com/exports/67c29cda-b4f3-46ab-982e-a312ae3bbb53/blank_tradingcard.jpg?AWSAccessKeyId=AKIAWGXQXQ6WCOB7PP5J&Signature=6qm%2BS162%2F3bzlg0kEcfCJnOnFIg%3D&Expires=1663741052"
}
```

curl调用，关键词`ocean of flowers`，风格`5`FantasyArt，保存到图片
```bash
curl -X POST "https://api.aya1.top/wombo" \
-d '{"keywords":"ocean of flowers","style":5,"file":1}' \
-H "Content-type: application/json" \
-o example.jpg
```
输出图片示例：
![output1](https://github.com/Brx86/DingZhen/raw/api/output/1.jpg)

![output2](https://github.com/Brx86/DingZhen/raw/api/output/2.jpg)

![output3](https://github.com/Brx86/DingZhen/raw/api/output/3.jpg)

![output4](https://github.com/Brx86/DingZhen/raw/api/output/4.jpg)

![output5](https://github.com/Brx86/DingZhen/raw/api/output/5.jpg)