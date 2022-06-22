import time, random, httpx, asyncio

# 26种生成风格的名称
style_dict = {
    1: "Synthwave",
    2: "Ukiyoe",
    3: "NoStyle",
    4: "Steampunk",
    5: "FantasyArt",
    6: "Vibrant",
    7: "HD",
    8: "Pastel",
    9: "Psychic",
    10: "DarkFantasy",
    11: "Mystical",
    12: "Festive",
    13: "Baroque",
    14: "Etching",
    15: "S.Dali",
    16: "Wuhtercuhler",
    17: "Provenance",
    18: "RoseGold",
    19: "Moonwalker",
    20: "Blacklight",
    21: "Psychedelic",
    22: "Ghibli",
    23: "Surreal",
    24: "Love",
    25: "Death",
    26: "Robots",
}


class Wombo:
    # wombo的api，以及丁真裁剪后的背景图base64
    API = "https://app.wombo.art/api"
    DJ64 = """/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDABALDA4MChAODQ4SERATGCgaGBYWGDEjJR0oOjM9PDkzODdASFxOQERXRTc4UG1RV19iZ2hnPk1xeXBkeFxlZ2P/2wBDARESEhgVGC8aGi9jQjhCY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2P/wAARCAEsAakDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwDdTezAct+NTCMY+YAD2OaijSVvlUNg9hmnNFIDhhj9RUsodlR90Bfxpw8s8nn8cUkQVgRtYqvenNJGFwI1+hpAOXb/AAqVHqWpd6gYU8+wzUTShzgsVH0ppAJ++D9QaAHmQgdMZ9RSbz+FHlvnaOfxpyw4I3flQAocEYVTn2FAyx5qQ7V4Kj8KaCcYGBzQABQQRg0oUZ4HPvRkDqRTtwxwDQABf72CaMAcf0pN2WPPNDPzxQAhxu9ab0zxRSqdx9PegCL7RHnAbn3FKZM1Hc2QkbzVIV8ckfxfWkTKLyaBlhDmn549qjRSRuFPUkHtQA7n0p4UkYOfzpodgTnNIZH6ZBH0piHjjil6jrTN5UDcQPxpGnUfxZpASYoqPz8rkKTSmXOMDmgB/wClJvUdxSBs9QaAQTjigB2QT1pQRjtTGUf3RSbV9SBQA8mkfLKVU4yMZFM2jJIz+JqZF+Tpg0gKyxCKUEBjxwcf4VOAABgce1OOAM1GZADgEZ9KBkgOfpSbip6DFOXkfd5FIU9emO1MQxpdpAO7J6L600zEgfIwJ9qlUBeFGKQjn1pDGJudSHAXPoacsewfLyfU9aUDDDg04kKKYhp3YxkD6CmMoP8AEfrin7lPbNG70wKLAReUQSQQfrSENjgD8DUpYngHmm7ivpSsO4seSoJP5UNuz98/kKYZT9aPOOeRRYB3z+o6+lAdsfNtpvmg9T+lBkX1xQBJuJ7/AJUu4juajDcUbu5BxTEPznrScZ6Um4UE8cUALtPek/CgEYzzTcf9ND+VAFeQmOPCyfe6gVDsZsEqee56Gpjh5ACQDj5iQCKHkCfcfzG7nb0/GgBEtt3Vv++R0pJFVTgE/wDAqY15ISU8xfpSGY5+chs09QHhAOrCnBgG+VcHsQc0m+JxxHtP1pViJXcAxH0pAKrEMdzkH3zQJCegIpdjbQBGfrg0oVl4aNjn/ZP+FADSzHj+lHI5qdYcjOAP50u1Vyc8+1F0BAo7kE/Sng542in7crkscfSpFAQYGST6nFK4EWGUcFV/OmhSx559yakaQE8AfgKFYt2PNMBnlsO3H1p20j1pWcE9elIeTk8ikAgP0NMCIzHv9D0pZWYRlkUEjt61TtZppZmzEUHbPemBoIF98elLgL0+X6j+tJGpC/MDk9sUpbAxyT6UgHD5sbiT601oQWyMg+madyelKFbOe3qaYEXlhTyBRsFPpSOBg8fSgBmxfWgIO+aUoQ2Awz3pWwvGefegBrKMccn3pscYUlj1PXFMa5hD/NPGABzzTTqVlG+0TKW9c5ouFi2qnG7OKdtB7fpVAavY5O6UfXBNB1qyGB5xOem1TQBfB4xjA+lIKqLqlk5wJ8f7yEf0p/260ZgBcx5PT5utIY+Y/IQGwTSW8TM+9u3QnvUgmhP3WUnvzSecW4HSgCRpApwOT61GWJ5yTRn8KT6UxBk+tLuI70hODR+IoAXJPU5pOvH86DRjt60ALg+v5UYzTdje/wCBoMRPPP50AP28c4owB0/nTPK9f1NKEA7LQAhbnn9KaXXslSYPrikEfoM0AN8zH/LMGgHjOwVLjA44PpQceooAiGPTP0anbRjq1OyvqKAPQ0ANAPtQQSMenoadg5oxSAj2vnrn2pdreg/OnYHpS/gKYzOlkZyRvdlPOOlRhR6H86d52Ac5yaejgJucHaT09aBETRp1Ix9abHHC2HQKcHqOeanFwuTttYyD/fJanrdMBtKKU/ugAAUXASLaHGatq0hHynAHdqgaSFQGEJyeeTgU2SR5+GKgdlHFG4E5cj78y/QVG0nPDg+3NRbMYAwT7U4xke9AAzlh1x9Kbk545+tKFO7GMH3qQJjOcZ7YIpgN3MTkHFLgsfUmj5gemPwpAWA6nPqKAJCgUctz7ULIygjAOe5NRjI6sTTs4FIB24nrSgH2qGSVIxukZVA/vHFULjWIYiQmZT/3yv496ANbcuOhzUL3sEH8ZLf3FGT+Vc5Jqs02SOQOQO3+frVGa8l2bQxOegH+elFrgdS+sRI2Dkg9PmAP5VUk8RKrhfJ3A8gqST+uK5rLKCZCS393PamqGY8nC46L0/8A107Bc6P/AISQ4z5A+pcj9KB4mbcoEZGOpz1/SufCBSAeR2x/jTNzByoG3txTsI62LX1kDZjIIH8PQ0xvEA+cJGvy9zmuaWXGEZ2B7H0qZIi27qSf4cd6VkO5cuNXuJJHw7RrwAF6dKrS6m7keYxbHGWOearrG2DK7FRgn6+1VbqN1VXK8MNw7f5607CuXjMxI+baexz1/Gk2sT98gnsw6iobaYYRZAGDNxkfnTzPkAAZAPOelFgJCr7Rjbgn3z+WKTAyQrkN7n/GjzD5at12nAz0BpBIrdeexBAOB7d6ADccfK3zDt607z3UYJKg9xzTHAADEjA96jklYHn5SelAFuK4UlSjYzjBLHd+fap11O6Q797le3Ib/P5Vkl8thWIHUH/GlR3ALFmAxyVHWiwXN6HxDLzuVHUdduRVqLxFCSPMicD0HJxXMLOpHzqDzncuT/8AXqMuobLZ2k9cf1pWHc7iDV7KXGJGUnswx+tXY5IphmJ9/uvNediZ1xu5A4HerEVw3LRO8b+1Fgud/g9gfxpHjyOCMiuRh12/g+9J5qDnnnP9a1LLxHFKVEybTjqOlFgNvDegzTtuB8wxUMFzFNnY3vyMH8qn3Y/pSAMDHQU0/QUpPPrTMn0FAD8j/wDVQX4703I7g4+lJgE8UAOJJ7mm5IPpSnGOtNB460AH4YpcfQ/jQAB9aQAbuc0AOwe3H40mfYn6U15Nv3R+JFMJZjkk49qQEpYDqQD7mk3r/eX86ZtxS8e1AzMjkKyAnoPaphKZSQyktUMpQnK4z9abFOouF3gAAEEjnPFMRZSNidrFFA7kA5qZUjUgqxJ9aoSSs74XcV7ZOMUgZj6GgC+cnrLuJ7Mf/rVGzpCmSQcflVYEk+gpHRm+Ung0AWY5mmztyijqc4AqQFVYYwx7HNV4xsBCk89eMUqgqeCRn1oAtLgdwSfWnb1weVH4f4VCFUpuLY9BTCxJxQBPtz0yfemOVUEuwCgckmql3feQuwMSxH3Risu5uHU/v33HsM4x/hx+NAzTl1GKM4jy5PQ9qpT6lOwOCEzkdKpGTncwG7PHpmmndnDYUjjkd6AFuLhzJnJLHuTmqpJLsMnjuOQKkncbxAo+ZlJLHp9P8+1MYKSuOgOQTxk+/wBPSmIfKRBbL6kHB9aYkXIOcsoCnt1PahXjlhZS+5s/Lnk0kkmAy42hevv0/wAKYirIChDtwD0Hr9KmZDjccBW5JU5A4z9aYGMyO7OCAQQB6cipjJGAVUdCeM8Y/wA4oAQRfdCgqcAj3/wpXULnIJ68gYxjrTWugxzIRgkcBc5x+NAnDqAvRck8c0wHTRAZZGOQMgpz7f59s1L55jgVR17/AP1qppMc7RgscjmoppSsxXlhng+ooAt+ftgCtzjnGev/AOumyzLKV3YCgBQMelQysoXg4NRlggUZzQIsRgBQhxnGQcY55GM/56UsigQswIyMMBjqfwqPqq44Ixg9hSksen8C9BQBAspVgpOBjpTTIS67hjPfHWnbFdSed3UcU9UVt4YEheBk4oAWKQ4IJ/E9/Y08ZHyc7DyOOlQuQPvL8hIB4574P6Uu4ocHlOtADniZc9iOhHemIzAcH9eKsiQOuCBkgdKjdMc8MCMfQ+9ADUEbY3ZjbscUrxN/EMjsRyKX5mQhAvHDKR1qASPEwCk4xnaen60ASheO5A6kDp9RQI3Uq6nI9RxSiRWG5ABjqPSnK4kLDgEnOB0NIYkxKDejEK2GKkcA0qESLnkH1pwdipST2A7EVC6NH0Ofx/lQBctb25szwzLkcHqPyPFbtn4jYHbcJkYyCv8An+tcxFMsq7CD7g+v1o2shxGxZR1VqLBc9AtdQt7s/upAX/u96s85/wA5rz1JCrCROCvUg1tadrlzEMXJ82Mcbj16cDP4GlYo6gAZ5J/GlBUdKgt7uK4TdH6Z5qRicdAakBSR0qM57EU4snQnFM2g5wfzNACM79P0psbs7HIPAx1xULvKJ1UZx7dKspnbg4z9OtACYGMYPHvSBcdM/jT92P4R+NGOu4Ee1MQg4/izS4H96jaPSjbQBh9etLinCGb/AJ5Of+Amm/oaQx4pwpgqUK5QuFO0cE4pgA5NO6DPNNBIOfSlDsQd2foaAHbh0U8D3pc8c4pnXk0oz6mgCT+ADpiqt/d+THtQAyHgVYwQpIGcdqyNUnEGTu+ft7fT+VAFeSfyARvzI2dzg96pebukG4Zx0GKjds4z1PYdhUSvg57KadgLYbILE5+bofYUhmHn4yTkbh7gAj+dQrOfmyPlIOPQ+v65pGlGVZeWxwT1Ht+dNIQkjh4zlhknqenv/Kg/JbpzgnioBncQec9OevtTUc7VBHfp6UxEludrbsgEHP5USyFtwJJyc0xV+Xk889TScFDQIdE7KCAQVHt1pUOFJHINQxruYd+ak3AOF/hNADt4ZsHI47U2IkHg8+1LIuGBHK9qagCuCemeaAF8z5jxlgeTintiSIf7Peo3BLlsnHajJABBxn9KAFJytNPzKOnWnrhmI79TxUbYBxTAlDMVb2HY1JCxkV2bOcYzUBb5QOuOakQlUOTznpSAlXasbMB0GeaAdxO7kbc9KjxiMg9/WgAhOTj3oAdcRll3Lzt+bAxxUYIwF9c1LnejAccY69qiAG5hnDZ49qAEjJWU88HirBwy5HbrUGMOXI6dqeMshccEelAD04lDY7YJpk8WZRyAMgfQU4NlVz1p+/cgU9OnNAFKJmSTaT0JHNWJFbPmIef4hUMqDcT69amiJAG4dBgjFADs5UMePQj1ocZh+bHtjtSR9HUjGTTZuijkcgUDG4IOeQe7dhUivux1BHT60mzcmD/e70gyOcY70ASK5VhjJHoKkEzRSEdR1APSoPM2uCDznvRJndlRSA39JmPmoiOSvTaW5z6j866aIttADAZ6k1wVpIySrIDtKnNdlZytOisXHTsOtSyi8SOhDZ9gTUUke4HblfqQKMehJHvSjg9qkCO3gKks/wB49ic8VMchQMfkKPwpCQTyp/A0AKwHf+eKZlhwSfoaeP8AdP50Ebv4B+IpgRmZEwHbZn1NH2qH/notKywyHawQ+2M0zyYf+eQ/75/+vQBltPM/WRvzpuXzlnBqZraVFDNGceoIP8qjAFIB0Ujx8rtJ9wDUz3k0i7WCke4qECnAc5pgSiYgYSKMe7Lk0mWJycZ9him0ooAd9cUoHtUkUPmDO4D61YjiWI5ba2ehFAiq8cnlMxGFAySSK5e6kWactxtBzg10OvzhLAohALnbwMVzBbapYA5PU00NFS4k5KjOccmmRYMe3HQU6ZCxbYSSx5554qNcrcGPHWqESRYKohHJJz+dPCHOMHcvUZqDzfLkGcbc4zVsgSPvyN/3TjoeKAK7AByUGV71FL6jir8kbbDleAM5A9DVdUHc/gaYrEWWYA9R/Om/dyQc89O9SmMpyBhCfl9KYckkcAj1oEJ9wkjk560uNwyDyDikByOnOeRTkXbJgjvQA5shSDjnpTMcYqVkwxGcimurAdCB/OmAwngDnrgD1pxXAAzz3PpSHs2AMdjQp3nJoAAwU5AOKawLdTmp44Wbk/l6VKbRivSgdmVUGR2+lSiM4JPSlaLawAp0fB29BSCwxgVU9zijG5MDrjj61Ky59c03bhfpQAyHHmY9RzSTIQSeuOnrSov7xecDvUxA+UnGSKBEHVeO45NKMLCp9T0pG+V2GcjtT1Tfx6UARnJbAA46+9TJnaQMHjHI700x5YIDzmrLQGNBleaVxpGfLuAKKeG+9781LEMR5OcjrSSqQw2/U06MYjKjjjr6UwsMX7x5HWiVufXOKeF657VEVLMPT/P+FABHuIIx1Pap2A3Eg9M4qIAKD9aQMeTwRQA1gQ+4kn/CpUYs2e1R87snuKUOOi80gJg/oRwRXW6JMZLQbj8yfLn1FcihPbqeTnpXX6EjJaszDa2cHPcfSkykaW78aXjv/KnHjsP0pOh6ZqQDg+gFG70AoG3BySD6U0Anp+lIA2k9WI/HFLsB7Z+tIFPc4o25H3j+BoAXHIpc+5poQj+M/lS7T/eH5UwMlbuRQFU4A796tQTpOdskO5sdcimeSCMeXwOm4kAfrUiW4AxHye7K1LQCX7PbtwFKnsQSaa1kCMq5H+8Ki8mZW+VWI/3hijzZEBBXb74pW7AK1pMo4Xd9DQsDjBk+Qd8jJ/Knx3EjDCHn/dyKnSSYg7ghH+ySDRqhjI4FVQeWz3K4pkgxyrHHpVkYfqrD04BpWQFT8gzjqRzRcRzeq7pRjjagJPHQ4wP61h3IMbsq54PGfT6128lkkkmdoJxjpwMf/rrB102tu5tyrPKvfONvp9aq5STeiMAkq2cZHpUbfLKrEAEdMVe8rdHlOQPzFVzF2IOc8VSYOLW4x4g3PGCMnH50kb4LKMgAcAjOalZcx7dobFT2to0zKXzx/KhuwlG7JbT5k+Y8ds0+SGM5+TqOK0EtlRQBS+Wo7Cs+bU25DFNuwGACfrUbW5Lfd/IVuZj55Bx1xzUUssCH53XJ/wBof41XOS6a7mFJCwbO08dSRS7HZQVBNaslzZbSGlGaat7YdpOnoDVcz7Eci7mcscuMMpz3NRmNwfmHTtW0k9vIMq/HrxUhSFxk4P1pc4/Z32Zgqm48g1KkWSODj+dbH2eE4G0YqVLePPHFHtB+yZThh+UZQrVjYOwq0sCDkmnbEqHI0UDOmt0fJ4A/rVGS3KH1Xpmt8RqRyBSNEuKamJ07nOPE6HoSOoNMZ26fqa33gQc1A1tEzZbnjFUpoh0mY6KTESBjHTildJG2kDkDGK1dsKnaoZj6LzUXnxA4FtK5zjKpnmnzNk+zS3ZQSFmcgD5lOMGpDBMFPHsatR3qeYwjtZSyglhs6Y6nrVuK5Ehwbdzj0TP8jQ210BQj3M21tpTJkL8w9auPDOF+bn/ZxmrC3Vuj4YCMgfxZU/qKnE8br3AP4j8xWbm+xrGmu5gm3l8zJUnt0pTCyjkfnW+FjK9BTJLZGHpS9qDpGNbwNNnjio7+3aBdw5reSFIxhRiqOqrmIcdKFO7FKmlEwuTjP4U9VyO9WIrQzSADjir0elomN5ya0ckjOMHIyBuOcAnJq1Z2E10+yNQWx3OK1TaxomEXjGMVXiTy7hAMqc8EVPP2NVQ7svaf4fkVle4IxkZUdxXRxoYxj9cdakIA44pCcHgY+tF7mAh98mkOAPuHHrSgkg4APqOtICOeBn0FADc8nGfyozk0/OejD6dKbtY4xn+dACZbNLkjtS7Tg5J/Kkx6HH40AJux1b8KN/0/OlwPbPuaOf7o/KmAxImA4Tj6YFOKy8ZaNV9M1S818nJ/HIoBy3LhcdcnB/wqbAXDwQWkzn04FN85WBB3nnB7/wA6rEqfmaaRvTPSniR+Qozj1H+RRYCwWLMBuyO4Kk8U/hcDYR7kYFUmmlDcnaPTcKartknJLfmKLAaAck/whfXpTTNEnBkAx6Kf51RDc/PvOf8AaoLAgBST9adgLkkqlVVHJJPVT2rkNdjMeoFs5BI5rpFfbyBjt61n63b/AGi0EoHzx9fp/wDr/nTsaUpcsjOsozsLkcdqV4Ek4II9CBUM0xCIyfcxx7VCZy3GT+dQdLjfcntIAbnaR061qKiovyjFU9OAAc9+KuP0pNmajYaXOajkXzBgnH4ZpSKdikXYrSWXmL88zMPQ9KfFG9uMRLF9QME1IQaTrTuxciKcttO0pkR9vsx3flnt7VAmnypMZPPOWzkY7EYNagUetLsSq52T7KPYrWyNbg4KsWxkuM0jQs7BkZYznnYvBq0EQdAKXcAKOcagkR9AM9aeCewpQV6nrT1PHAqLlpDQCBzThSsKEAyKlspE6oCvNNdPSpgMDpTGNS2CKxGeDUEsRZSuCB7VcOD2pQoIqlIHEzo1aEYR2X8BUbWkckjSMx3nuOP5VplB7UnlAnoKvmI5EZkOl2yPvBJPuKuwokIISXGfapvLH90UojGelJyYKmuxXkht5Dl8uffmkFrADlYsH1xirWB27e1JtP8A+qpuyuVESxqvTj8admnEUwjvUlWHA5qC8jEkJ9ualU0OQI2J6YprciSKMbCCDcoyx5pkd1IPvkN9RU8bqIwMA1BLCWYnawz7VbsEVZE4ulNJKB5iMOnUVXS3OcngVcgge6nWKMZ9+w96S30Kbsjp1BVFGScAAml3H6/U0hbacZIHqaMd/XuK1OFgTkc9PTrSFh3GD+VGCehpAeoyfyoEKSp4JBz680gXH3W/CjBPUn8aTGTjCj60AL6fdoYELlU3H34/WmkEcH5ffNM3HHJGfXFAET3qRttlidT3xzS/2haf35PyNTEh1/eKGHvTPIt/7g/OgDOWQ4LAHae3WnBs5GQc85Cg4/DFVwwOSSAR/s0K3mcdcetMCysgGQrnH0xn9aN4ZmwMHPbBqLocDH8qXORyQaAJVZfmPQ+/JoyrEfMfxqPoAPXmjNAEzKQORgUgNMBqTe+c5yffmgBRTxgnnkHgj1FMXJp4BPoKYjLvdLKM723zIeTGf6ViyRANjJjOejCuy2nb0qpeWnnfMijeOvuKlrsbwq9GYUIliIkQhh3ArRVxIgYfiPSq7IImwymM+mMU6FwZMJuc9wB2rNmvmT9aUCk6GnDmkO4hFNKZpxNNLAUyhNlGAKa0qqMk0zfv4HGaYrjzKucUbdx+WkSECpVUKciiwXGpE2eTUyrTWkbHSoGkmzwygfQ0WC5bKjHak24IxVdZ2/iKn6ClMxJ4FLlHcvZyOaaT7iqnnN2FMdpDyJCPpily3C5bK56Gk2H1qqrzg43g/UVYVnOAetLksNSBhgc1EZmXpk1MUGeTzTHj70KwNiLcA8VKJFNU3XB4FNEpXqSKdhXNAEEUHrVMSn61Is2aQ7kxxTSOKTfSFuKkLigVFMC/yfw9TUoyTUUiN5yF3MMT8eaVyuf8g0IlvuMCxocbfpmlYlhjOKmngiAURagjy9U8pctn25q6bTzPLkaMbto3DsT6miz5rCdRFO208XL+YQY4s9Sck/T/ABrbt4EgiCwphfUDk/U1FmRVwDx6AU1Vx8wGPwrdKxzSk5FrcOjn/GmlwMjqPcf1qMBsfKB+FKCwPoaZArSMDwMU0uWOOAfpTiWYkEH+dN2rj+IH6UDDvyxP40u3d/GD/MUg9+tBXk45+lAAPlyO1L9Bn8aQE56kGg57E5oAQ8ZBAFGF9F/OlIJGSPzNM2r6/qaBGNuBzwfoBQPl6ALS+9OHXJ5NUAgc47Y9cU4LIad6YpwBNADUU7irZPHapRyvQUgA9Sfwp6igBFFPC457U04HHSnrzigByoWPAz9anBVRgkfQD+tQDP8AjSOEJyQPbFIRaVgO+eOgNLlCeRxVYdB/WpQx2DAAx1pgScYzkfnRjIHH401HYMMAfT/9VB80vjYfoaAKN7aGP94g+Q9cdqotkdOtb/lSucODz2NZ97YNDlkII7qOorOUeptCfRlANu+tR4JPNPK5NKAD9ag3K7IWII6A81KHReCQKkKg9RUbxKwwRmqTETKQeh/Klx71TFqgbIBQ+q8VHJa3CnclzN/32T+hp28w1NBhxUbcDkgfU1WhubiJkE0UM6Dg5TDEfXpVlry2eRStskag8h06/l0p8orvsMwOuQfxpeO2Pzqzb3GnhmMyxA9uMipTJphX/liAfoKLC512KPfkj86UGPPLCrcUmmheTDz/AHmBp7TWDKBGYgc9sCnyj512KoaPOd6/nUiyJ2dfwNSyXdoIiEVGPTkiqzajm1KQWaiYjA3fcHvnr+lJxDnfYm356EGjcPas10vZ9u+VIgByIV6/nmiLTIQSzjJPJzyalwS6lJvsWpJ4ckFlJHYHJqIMrZAHFSrCijai4FNdFSkAxE2ng8U51yQR1pUHtT6ljEQYFL1NFBKJgvIiAnGXYAfrSC9iaNTI6xr1NbiKIowo4VB3qvZQRwxB1ZXZxncDwfpVbxFHcyaVJHbxl3OCyjklepx61rGNjmqTvsVdOuLifXLuS4l/c8iMLICrDgDoT2APrn8q2SOfl/GuM0tpp7k2kSMkmSG8wbdgHX8a7QKVAHUAY5rSSS2MISk/iQ0D0xR0p2P0ox3qSyPj2NGSfuipDuUfdxTTk9aAGbSDggj8KceetIV6c5/GkGRnvQAoAz2HvmkwR3pwJx3xSx4d9rMFoAbyBzzSY55HWrDCJOTz+NM85P4Y6AItrAcZ/Kk2Sf3FqY3Kj+AD/P0pPtA/vD/P4UAYXc05Voxv5pyIdwGDk9qoBcYpR1qyluuzJYHHvT1t41QFlGD33ilcCrmnL7datLChxhPxHNS7UXG0cgZ9BRcCg6lcFh19aegZuFGfwq3PD5kRVWBOMgD1pkCKIlbaASO+RzRcAWNxjdtA9xjNPEYOSVz74PNPEZyTkDPfFOAXtk0riEAUn5ox+dKWPACRrk/3egpwGeq8ewpeB0U/zoAbhjnDcetBVVPByfrThwf4lHXmk3DoOR7GmAdeSeAOgpAvcDGPcU4HPtXN+Lb6aGJLeBigcEuRxkDsDTQEuq6hpUBP79RN/dj+bP17ColIIBVgQRkH1riJA3Oa2tG1NfJW2nbBXhST1FKcOxpTn0Zv9aCMVAs3fqKlWVWrE6ExetA46U7GelGKBjSQeCtMMaY4H6VIV9KTBp3YyFo19s0nlr/dWp8D0oK+1VzMdyDYDjgflS7FH8IqXb7U5UPp+tHMO7GKq/3F/KpMfXFPCU4JUuQXY1QB0GKCM0/bil21FxERzjio/L5yeanJCjk1A8w5A5oQmLwKaWAqIyE96bnHNOwrku/d0/Wue1+cvfJGMkIn6n/IrWmukhUkmubuZftF3JKecnjNaU1rcxqy0sW9O1O4spMwzeWf7uTg/UdK7bRdW/tOM+YgWVOuDkEetcAjN0+U/gK6nwhbM873OCiKNvGfmNayRkmmjqwCx45pNjDIBz9Kf1H3s0mGxnJAPrWYhu0556ikz+R9afhh3zSED2zQMYV7dvSkIzwSafjnkf8A1qTAzz0oEROxjbAA5703cT1xipmETLtcAj8yKYsKknZISD27imMZnA6D8KA6sMYAPrSmB157/WhEcnGM0XFYjwARk/SnZGeM/hT2ideq5/Cm9DyCPegBO/H60v4Gg5xkHIo596YGZsuG4FtcAepiIpypMuVKEn0ckVpF5VQtHOTkZweg/PP86LS4KKxdWYg84xmlqBAgQnMjvn0x0qZmww2o7E9xxUMsf2wAGDahbIYMAR75xVpSIo1igYhF4yc5ouAzaSDhG+p4/kacEIHLqPr1oByQSd+G9P8ACpGXJx074BNIAwD/ABbh7VWXMcrR7Rtb5gScc96sBGxyD/Oo5BgBxgNnOelADlA9h7jmnZPUggduxpCwO3AHI4JOaPNC8BgSfWhAKBnt+dOIO0YI/Cm+ZjuOfSl3HGAxA9himIXpxt/Xil446fnSDkZ6n65NAyRuJJ/GgBWOcZxj61Q1fTI9StChba68ow5wau8dBnJ60rsFUsSTj1NAHmd7Zy2c7wzqA4PbpVR0GMj+VbeuXgu753X7oG1ec8ZrJYqw6VqiRsN7cQcByR6Gr8Ws9pF/EGs1kpCvXH60OKZSm0dFDqsR/ix9auxX0T9x+BrjhkDinK7joeneodNGirNHbLIjfdYGlNccl7PH0dvzqxHrE6jBNS6bLVZHU4pOfWufTXXHXB+oqVddHcL+Cmp5JFqrE3ASD7U4NWGNcTrtHNIddB6FR9QaORj9rE3wwzS+Z6Vzra1kH5wPopqNtWDD5nlb6cUezYnWidG86Jklh9Kge9HRawP7Ui7Rvn3ph1RiOI/1o9mS6qNp7gsfmNRmZR1NYjX0zA8gfhUbTSP96Rv5VXsyHVRsy38cfU81Sl1QnOwZ/Ss4496PeqVNEOq2OkkeZsux+nakC56UhNAPpV2M73JEAHX17V0nh/WhZMYZuYCOMdVrmangOUKqfnByDQ1cqOrPTUuIpYw6FSp5BHelLknIXNcNYazeWke23kQrzmJ+Rn271pJ4rkXb59pwOrI3/wBb+tZuJbTWp04YsMcZ9KXLAgFHzjtWNB4l064OGkeI5xiROv5VpwTxTqWhkWQDuhzUtWJHF3zhQuPfNJ5jgfeUe4Gf50rj+Ig++TT1j4ycD2FIZEryc5kGO3yinqATy+T6KcU8BQeCM/QUBE3bjtDdARjincQfdGB09zRu54HNISo7gUhdccc/iKQyQOQOtIxD8YGfeo9+e7Ag0oOe2aQCGLYeTn6Cm4X0k/SpCflPzD3AqP5/71F2BXNqEH7yVfyJqX5RtXMe3PTOD+VDxpg+aQCP1qpKqAcOAfTFWmIme7jT5kjBPTmmDUJOQVU+noKrlVPfP0oCADj9aAJEuJWYhmHXIyOKmWbamCAW9hiqwBz1FL9TTAs/aXb0A9qTLzfLuwPQCoDMAOOTR5kpj2gbQTzkc0WAnwfukOwHUYpYzEXOWCHrye1Rx3cdsmZiq+7sAD+dU5NX06MsXkZ2zwI+aLCNMOrHiUkduBUwB49T3Of6VzEviKFSfKt3cepOP8aqv4hvyCImWMd9q5/nTswudfI8cSl5ZUVB3ZsD+dZlz4isIDhCZjjnaOAfqa5Ca6muH3zStIfVjn/9VQsSOhHuBT5RXN+68VzvlbaJIl9SdxH+fpWbLql1OW825kZWHI3ED8ulZpzjtRnHaqsK5K7ZNV3Bp5J603dng8UxDDSZ9TTiDjim4NMBN2eCKBijFHPTrTAMD1pMCiikAYPajbg0dqO+KAE+lHbpS454opDDNBOfajGKMUAH1pc54pMClHFAB75oyaMZNKFzQIDn0waOeKXGPwoxQAgFKKOKM5oGLTlbBzjNNI5oGRQFyzvjf767T6ipAJAAY5Nw9DVQN607PpU2NVV7olllbGHQB+uRTFndWDKxDDuDg5ph56mkA5zmmRKXM7mpBr2pQDCXchz/AHyH/nmra+Kr3jfHC5/vEEE/kcVg4/SjNKyJudOniuM7fMsyPUrL/TH9asf8JJYsRhZlz1LIMD8jmuQ/Wl+n86LIdzvbbV9OlB23KKR/fyo/XFaUZ3oHRlKtyCDkGvMVYg8d6kinkhk3oxRh3QkGk4hc9O8sEcsAfyo2qMDOSOnFefw67qMQAW4c+7gMT+J5rQg8V3C8T28cg/2cqf61PIx3OvPTgfnSbD6N/wB81zsfii2KZkhlVv8AYww/XFS/8JPbf9N/++R/jS5WO6LJLSHlix9zUotZWbBQqT/eGKwjrsqnMUSr25Of8KpXGr3szHMzJ7IcU+Viudf9gcdZI/z/APrVVnEMDESXEJ7/AOsHH4GuOedmYszMzE8lj1ppztJwTT5QudU+o2MZIM4JHpzVeTXLZMiOORj+AFc2COykfjS4JPY/U1XKK5rS67Ic+XHGg7ZOSKqvql7IMeewB67QF/lVLIGO30FDMDzgc+tOyFcc0ruSS5Ynrk5poB7LikLDOMZ+lNLAdzQAuTnrn8KMnrmmlgT8q0v1PFMA46HkUZ9eaTNJmgQpUZyBTTnHWlzzwaN2fT6GgBpHNNKdc1JnnNN78D8aAISpHTpSZPSpsZx60jJxTAi4PbFKQPejaRxR1oAbxS4FOxntSY9e1ADeAOtL19KUr7Um3npQAY9MUUbeKNtAABSUoU0oSkMbS5pwjOOTS7AOKBDCaUA08KBS7aAG0mMmnYGPejbQA2jFOABzS7RQA2gfSlC0uMdqAAD1oIHaloJpAHFHOKM0CgAJ6ZpO9BpMUAKKCP1oA9qMUAAP5UcepooGaAAU4Djr+tJ+ApMUAOU8c5/Sl3f7ZpoFFAyzk85wMcctSM2TjGPpTBjv3oPemAufzpQ3bjim9P8A69H9aBBzzkg+tH16UfSjNAB9KO/SjvxRQAc0cZpcYHNGKADIB5FNJFL2NA9BigYmOM0hPsadjI6U3HPOKAGnvQQeMU7A70mPr9aAGj1PFKCfalxSY5oAXNGeMUmO1GKBCEZPQU0p9afyO9HfnFMCJgQemaQcnAqXvxSH6UANAzQB+eafj2pBzQAmOeaMe1O9iKXj0pAM96UEUvHWl7DpQAhPI60mORTvqKD7UANyfwo5xS4PrR9aADvzR26Ug6+9LnvQAUvWjtzRxSAMYoxxQB2NFACYx1zS/rSkcUZ7mgBuM/Sl9sUv0oxx1oAb3pelKBRQAmPTigY+tFAoGFLRzRjtQAlBHPSlPFB6UAJS5NHTrRn3oAk6D/61ICc+1OIH/wBekxTEN7//AF6XPpTgD07mm4J4oAM5HtRS9OPWjGfagAH1NIM0uMUYoAOfakINKBS/hQA3BznilHPORS0n4E0DA570nbGR70p5HtSc+1ACY9qQDsfzpxo60AJgE0mKdx3o43Y/lQA3FJxTjQOO9ACfrSYpxH40UANxx6UYzTqKBDCOKbTzz9KQ59KYDR14paOg9KOKQC4PekxzS5weaBQAgpaXrxSY5oAO9GKX60UAJjmjj0pcd6McUgD8aSlpMUAL046UlLRTADR9aKBSAKD1ooAzQAd6O1FHvQApHFFFLz6UAJj1pCOKdjP1oxQAnejBpc0A++aBid6PxpevFJj3FAiQ445petL/ADpMelMYlHXtTu+KMd6BDemaDjPWj196PzoAGoHvmjvmjNAxMc0tHH40nB9aADNIfal/CgDmgBMUDpzSkE0YxQAn5UUp+tA5B/xoATBo5pQeOtHcc5oATHFB/lRk59qCSaAFB460nJHWk+gpenpQAfWkx70uD14o7UAN/CgilooAYR70Up9aTFAB3oozRQIX6UAe3FFHXrSAXgCkzRRxQMXdnrzScCl6YoxznFACCjt60uaOPWmAmKO/Wj8KMfrSEGKPzpaMegzQAnelJ6dKSlAzQAg5o+tL+FANABjml5I55o/Clzj8aAE/Kl/CjvxR1oAMZoIoB/Kl/nQMQCjFHejNAiT8P1oHB7U0tSd/WmMdmjOTjBpvWlPtmgA688ijgjikz19aKAHZ4pp46fpQSOxP1pM9aAHfSjOAc5/Cm0ooAcBxnNJ345oBz2pD+dAB70ucZ9fagcUh+tABxjk/WjPH0o475/Kkz165oAXqeSKTOOP1petN/KgB2eelIfpRR14xj3oAOvbpQev86BnNGTyDQAbjSfjRRQAdKM0Uc9+9ABgc009elOLE9zjvSdsc0CEIpOOuaU0fzoAD0yBRxn/69J0o60AH8qUY7CkBoHT2oGLR2oH1oGAfagBelIMkUdqBQAuM5oA4pOTR9RSAX60CkpetAgx3oOB3oA5ooAXHGeKMd/zpM5PPQUoNAwxgmlPPak6UDp60AB4o/WjNLQAdD/SjqKOooz6UALmjj1po6880uf8AOKADJx9aAecnpTASRyaUDJI96YDj04pPxpM4NKeGoAX6UGkpfSgAB4waDmmqc5p3YUAO6AZI+mKTOSKaR3pM0CH598UDr0pucnkdaXoKBi5x2pueKe1MPTNAC/nQPpzR/EKapyPrQAueaOn1pASM4OMUZyaAF9utGKVRnuaQ8MPrQAUd6QCjqaAFz2xyKOevFN64pcdPrQIXr/hSdeKTopNB4P4UDF/pSD6UbjilznmgQnX2pCMdqU9KD9e1ACHmjvTgPmx7U2gYvakpDRkg0ALx+NKelIvNKBxSAAcZo49aQnBooAd06cUCk6fnQeM0AL3opDwfwoAzj60AKelFIO1GeSKAFJo6UnYmgc4oAXk/hR9aQcijNADhWpaaQrrC95eJapMrPGNhkcqP4sDoOvJI6GsteakWaUReSJHEWd2zccZ9cetAGvf6FFaeSx1KPyZlysjRsQx9tu4frVe/0tdNjaG93pd43pggo43YwMc9OcnHpiqEdzPFN5sU8qSYxvVyGx9aZI7SyF5GLO/LMTkk5oAs2di90dqE5KeZ8o3YXdtyQOevoDVz+wLj/np/5Lzf/EVkLI6qwViobqAcZpdzf3m/OgD/2Q=="""

    # 初始化类（因为有异步函数所以不能用__init__）
    @classmethod
    async def init(cls, client, auth):
        self = Wombo()
        self.client = client
        self.auth = await self.identify()
        return self, self.auth

    # 多次尝试调用api
    async def call_api(self, method, api_url, params=None, data=None, headers=None):
        for _ in range(5):
            r = await self.client.request(
                method,
                api_url,
                json=data,
                params=params,
                headers=headers,
            )
            if r.status_code == 200:
                return r
            print(
                f"{r.status_code}: Failed to {method} api {api_url} , try {_+1} times..."
            )
            await asyncio.sleep(1)
        return None

    # 获取最新的token
    async def identify(self):
        r = await self.call_api(
            "POST",
            "https://identitytoolkit.googleapis.com/v1/accounts:signUp",
            params={"key": "AIzaSyDCvp5MTJLUdtBYEKYWXJrlLzu1zuKM6Xw"},
        )
        token = r.json().get("idToken")
        if token:
            print(f"Identified: {token[:30]}...")
            self.client.headers.update({"Authorization": f"bearer {token}"})
            return time.time(), await self.upload_img()
        return None

    # 上传背景图片
    async def upload_img(self):
        r = await self.call_api(
            "POST",
            "https://app.wombo.art/api/mediastore",
            data={"media_suffix": "jpeg", "num_uploads": 1, "image": Wombo.DJ64},
            headers={"Content-Type": "text/plain;charset=UTF-8"},
        )
        print(f"Uploaded image: {r.text}")
        return r.json().get("mediastore_uid")

    # 创建一个空任务
    async def get_task(self):
        r = await self.call_api(
            "POST",
            f"{Wombo.API}/tasks",
            data={"premium": "false"},
        )
        task_id = r.json().get("id")
        print(f"Created task: {task_id}")
        return task_id

    # 填写参数，初始化任务
    async def start_task(self, task_id, keywords, style=None):
        if style == None:
            style = random.randint(1, 26)
        r = await self.call_api(
            "PUT",
            f"{Wombo.API}/tasks/{task_id}",
            data={
                "input_spec": {
                    "prompt": keywords,
                    "style": style,
                    "display_freq": 10,
                    "input_image": {"weight": "MEDIUM", "mediastore_id": self.auth[1]},
                }
            },
        )
        return style_dict[style]

    # 轮询请求，检查任务是否完成
    async def query_task(self, task_id):
        await asyncio.sleep(5)
        for _ in range(50):
            r = await self.call_api("GET", f"{Wombo.API}/tasks/{task_id}")
            status = r.json().get("state")
            print(f"Querying task for {_+1} times...{status}")
            if status == "completed":
                break
            else:
                await asyncio.sleep(1)
        else:
            return None
        r = await self.call_api("POST", f"{Wombo.API}/tradingcard/{task_id}")
        return r.text

    # 用于运行全部步骤
    async def run(self, keywords, style=None):
        self.keywords = keywords
        task_id = await self.get_task()
        style_name = await self.start_task(task_id, keywords, style)
        url = await self.query_task(task_id)
        print("Task finished!")
        if url == None:
            return style_name, None
        return style_name, url.strip('"')


# 调用示例
async def main():
    async with httpx.AsyncClient(timeout=10) as client:
        w = await Wombo.init(client)
        url = await w.run("sun")
    print(url)


if __name__ == "__main__":
    asyncio.run(main())
