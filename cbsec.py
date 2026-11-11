"""网安社团纳新 · 刷题 / 答题工具（Streamlit 单文件应用）。

优化依据：Streamlit 官方开发文档 https://docs.streamlit.io/develop/api-reference
  1. st.button 的 width="stretch" 是新版 API，旧版只有 use_container_width；
     运行时自动探测，避免部署到旧版本时抛 TypeError。
  2. 筛选与模式切换改用文档推荐的 st.pills / st.segmented_control，
     并按版本自动回退到 st.multiselect / st.radio。
  3. 空选语义显式化、筛选联动到浏览模式、状态签名改用 frozenset。
  4. 依据官方 "Widget behavior"：脚本某次运行未渲染的 widget，Streamlit 会自动
     删除其 session_state 键值对，因此抽题时递增 nonce 产生的旧选项 key
     无需手动清理（也不要在 widget 实例化后写它的 session_state）。
"""

from __future__ import annotations

import inspect
import random

import streamlit as st

# ============================================================
# 页面配置
# ============================================================
st.set_page_config(page_title="社团纳新 · 欢迎来到网安社团", layout="centered")

# ============================================================
# 题库数据（40 题：原卷 20 题中等难度 + 扩展 20 道简单题，每个方向 5 道）
#   cat    方向
#   level  1 = 基础(★)  2 = 进阶(★★)
#   answer 正确选项的字母
# ============================================================
QUESTIONS = [
    # ---------------- 网络安全 ----------------
    {
        "id": 1,
        "cat": "网络安全",
        "level": 1,
        "stem": "访问某网站时，浏览器警告「此连接不是私密连接」。这最可能意味着？",
        "options": [
            "网站没有安装杀毒软件",
            "网站一定已被黑客完全控制",
            "连接可能被他人截获，或网站证书本身存在问题",
            "本机网卡出现故障",
        ],
        "answer": "C",
        "explain": "证书告警意味着身份无法验证，可能是劫持，也可能只是配置问题——两者都不能忽略。",
    },
    {
        "id": 2,
        "cat": "网络安全",
        "level": 1,
        "stem": "登录网站后，服务器发给你一个 cookie 用于识别身份。如果这个 cookie 被别人偷走，他能做什么？",
        "options": [
            "可以直接以你的身份使用该网站，不需要知道你的密码",
            "什么也做不了，cookie 只是本地缓存",
            "只能看到你的浏览历史记录",
            "只能修改你的昵称和头像",
        ],
        "answer": "A",
        "explain": "cookie 就是已登录的凭证，拿到它等于拿到会话，不需要密码。这正是「会话劫持」的本质。",
    },
    {
        "id": 3,
        "cat": "网络安全",
        "level": 1,
        "stem": "很多系统强制要求「每 90 天必须更换密码」。这种做法的主要问题是？",
        "options": [
            "会让密码变得太长，难以记住",
            "会大幅增加服务器的存储压力",
            "会导致加密算法失效",
            "用户往往会改成 Password1→Password2 这类可预测的变体，安全性反而下降",
        ],
        "answer": "D",
        "explain": "强制轮换会催生可预测的变体。这题反直觉，答对说明真想过。",
    },
    {
        "id": 4,
        "cat": "网络安全",
        "level": 1,
        "stem": "某登录页面在密码错误时，会分别提示「用户名不存在」和「密码错误」。这有什么问题？",
        "options": [
            "没有影响，只是提示更友好",
            "攻击者可借此批量判断哪些用户名真实存在，为后续爆破缩小范围",
            "会让登录速度变慢",
            "会把用户的密码直接泄露出去",
        ],
        "answer": "B",
        "explain": "分开提示等同于告诉攻击者「这个用户名存在」，可用于批量枚举。",
    },
    {
        "id": 5,
        "cat": "网络安全",
        "level": 1,
        "stem": "使用 HTTPS 访问网站时，别人还能知道你访问了哪个网站吗？",
        "options": [
            "不能，所有信息都被加密，什么也看不到",
            "不能，连对方 IP 地址也被隐藏了",
            "通常能，域名和 IP 往往仍可被观察到，被加密的主要是传输内容",
            "取决于浏览器有没有开启无痕模式",
        ],
        "answer": "C",
        "explain": "HTTPS 加密内容，但域名、IP 通常在握手阶段仍然暴露。",
    },
    # ---------------- 数据警务 ----------------
    {
        "id": 6,
        "cat": "数据警务",
        "level": 1,
        "stem": "一个人用三个不同手机号注册了三个账号，要判断是否为同一人，最可行的思路是？",
        "options": [
            "看三个账号的昵称是否相似",
            "结合设备信息、登录 IP、行为特征等多维数据做关联分析",
            "手机号不同就直接认定为三个人",
            "只能等当事人自己承认",
        ],
        "answer": "B",
        "explain": "单字段不足以定人，多维关联才靠得住。",
    },
    {
        "id": 7,
        "cat": "数据警务",
        "level": 2,
        "stem": "名单里出现「张某」和「张某某」两条记录，能否认定是同一人？",
        "options": [
            "一定是同一个人",
            "一定不是同一个人",
            "名字更长的那个更准确",
            "不能仅凭姓名判断，需结合身份证号、联系方式等辅助信息比对",
        ],
        "answer": "D",
        "explain": "姓名可重名、可简称、可错录，不能作为身份唯一标识。",
    },
    {
        "id": 8,
        "cat": "数据警务",
        "level": 1,
        "stem": "数据收集中的「最小必要原则」，指的是？",
        "options": [
            "只收集与目的直接相关、不可缺少的数据，不多收",
            "数据越多越好，方便以后可能用到",
            "只收集不需要花钱就能拿到的数据",
            "只收集存放在本地的数据",
        ],
        "answer": "A",
        "explain": "关键词：目的相关、不可缺少。",
    },
    {
        "id": 9,
        "cat": "数据警务",
        "level": 1,
        "stem": "一份 10 万条的数据表里，有 300 条缺失身份证号。直接删掉这 300 条有什么问题？",
        "options": [
            "没有问题，删除能让数据更干净",
            "随便补一个号码填上就行",
            "应先分析缺失的原因，直接删除可能引入偏差、丢掉有价值的个案",
            "300 条数量太少，可以不管",
        ],
        "answer": "C",
        "explain": "缺失本身可能是信息（某些人群更易缺失），删了就看不出来了。",
    },
    {
        "id": 10,
        "cat": "数据警务",
        "level": 2,
        "stem": "同一批原始数据，两位民警统计出的案件总数不一致。最可能的原因是？",
        "options": [
            "一定有一个人算错了",
            "数据一定被篡改过",
            "系统存在 bug",
            "两人的统计口径、筛选条件或时间范围不一致",
        ],
        "answer": "D",
        "explain": "口径不一致是数据统计分歧的第一大来源，比「算错」常见得多。",
    },
    # ---------------- 电子取证 ----------------
    {
        "id": 11,
        "cat": "电子取证",
        "level": 1,
        "stem": "分析磁盘镜像之前，先计算它的哈希值，主要目的是？",
        "options": [
            "压缩镜像体积，节省存储",
            "证明镜像与原盘一致，且分析过程中未被改动",
            "加快镜像的读取速度",
            "给镜像文件加密",
        ],
        "answer": "B",
        "explain": "哈希是完整性校验的锚点，前后一致才能证明没被动过。",
    },
    {
        "id": 12,
        "cat": "电子取证",
        "level": 1,
        "stem": "把一个大文件删除后，磁盘空间并没有释放。最可能的原因是？",
        "options": [
            "硬盘出现物理故障",
            "需要重启系统才能生效，属正常现象",
            "仍有进程打开着这个文件，引用没有释放",
            "删除操作执行失败了",
        ],
        "answer": "C",
        "explain": "文件被进程持有句柄时，目录项删了但数据块不释放。",
    },
    {
        "id": 13,
        "cat": "电子取证",
        "level": 1,
        "stem": "现场遇到一台处于开机状态的电脑，希望保全内存中的数据，应当？",
        "options": [
            "先提取内存数据，再考虑关机",
            "先正常关机，避免数据损坏",
            "直接拔掉电源，最快最安全",
            "内存数据无法提取，不必考虑",
        ],
        "answer": "A",
        "explain": "内存易失，断电即清空，必须抢在关机前提取。这是顺序题。",
    },
    {
        "id": 14,
        "cat": "电子取证",
        "level": 1,
        "stem": "涉案手机已经开启飞行模式，还需要放进屏蔽袋吗？",
        "options": [
            "不需要，飞行模式已经切断了网络",
            "不需要，屏蔽袋只是用来防摔",
            "需要，但只是为了防尘",
            "需要，飞行模式可以被改变，不等于物理隔离",
        ],
        "answer": "D",
        "explain": "飞行模式是软件状态，可被更改；屏蔽袋是物理隔离，不可绕过。",
    },
    {
        "id": 15,
        "cat": "电子取证",
        "level": 2,
        "stem": "取证时发现嫌疑电脑的系统时间比标准时间慢 3 小时。这会带来什么问题？",
        "options": [
            "没有影响，把时间改回来即可",
            "时间线分析会错位，与其他来源的日志对不上，需记录偏移量并校正",
            "只会影响开机速度",
            "说明系统一定被入侵过",
        ],
        "answer": "B",
        "explain": "时间偏移会让跨源时间线对不上，必须记录并校正，不能直接改。",
    },
    # ---------------- 系统维护 ----------------
    {
        "id": 16,
        "cat": "系统维护",
        "level": 1,
        "stem": "服务器 CPU 使用率只有 20%，但访问响应极慢。最可能的原因是？",
        "options": [
            "CPU 已经损坏",
            "一定是网络带宽不足",
            "瓶颈可能在磁盘 I/O、锁等待或内存换页上，CPU 并不是限制点",
            "需要更换更高主频的 CPU",
        ],
        "answer": "C",
        "explain": "CPU 空闲而系统慢，说明在等别的资源。答对这题的人有真正的排查直觉。",
    },
    {
        "id": 17,
        "cat": "系统维护",
        "level": 2,
        "stem": "修改了服务的配置文件并重启，但改动没有生效。最可能的原因是？",
        "options": [
            "改的可能不是服务实际读取的那个文件，或配置里存在语法错误",
            "重启命令本身一定是无效的",
            "配置文件不允许手动修改",
            "必须重装系统才能生效",
        ],
        "answer": "A",
        "explain": "改错文件、语法错误导致回退，是两个最常见的原因。",
    },
    {
        "id": 18,
        "cat": "系统维护",
        "level": 1,
        "stem": "一台机器能 ping 通网关 IP，却打不开任何网页。最可能的原因是？",
        "options": [
            "网线没有插好",
            "路由器断电了",
            "网卡驱动没有安装",
            "可能是 DNS 解析异常、端口被拦截或代理配置有误",
        ],
        "answer": "D",
        "explain": "ping 走 ICMP 不走 DNS，能通说明网络层正常，问题在更上层。",
    },
    {
        "id": 19,
        "cat": "系统维护",
        "level": 1,
        "stem": "某服务的日志每天增长约 5 GB，磁盘即将写满。最合理的处理方式是？",
        "options": [
            "每天手动登录删一次日志",
            "配置日志轮转，按大小或时间自动切割并清理旧文件",
            "直接关闭日志功能",
            "换一块更大的硬盘就行",
        ],
        "answer": "B",
        "explain": "自动化轮转才是可持续的做法，手动删和关日志都不可取。",
    },
    {
        "id": 20,
        "cat": "系统维护",
        "level": 2,
        "stem": "备份任务每天显示「成功」，但从未验证过能否恢复。风险是？",
        "options": [
            "没有风险，备份成功就意味着可用",
            "只是浪费了一些存储空间",
            "备份文件本身可能已损坏或无法还原，直到真正出事才发现",
            "会影响系统运行的性能",
        ],
        "answer": "C",
        "explain": "「备份没验证过就等于没有备份」，这是运维里最贵的一课。",
    },
    # ============================================================
    # 扩展题（每个方向 5 道简单题，全部 level=1 基础 ★）
    # ============================================================
    # ---------------- 网络安全（扩展） ----------------
    {
        "id": 21,
        "cat": "网络安全",
        "level": 1,
        "stem": "下面四个密码里，最不容易被猜到或破解的是？",
        "options": [
            "123456",
            "T7#mQ2!vL9p",
            "19980101",
            "admin",
        ],
        "answer": "B",
        "explain": "长度长、字符类型混杂、无规律可循，这三点决定抗猜解能力；生日、连续数字、常见单词都在破解字典里。",
    },
    {
        "id": 22,
        "cat": "网络安全",
        "level": 1,
        "stem": "收到一条短信：「你的快递无法派送，点此链接重新填写地址」。最稳妥的做法是？",
        "options": [
            "立刻点开链接把地址填好，免得耽误收件",
            "把链接转发给同学，大家一起看看",
            "不点链接，自己打开快递官方 App 或官网查询物流",
            "回复短信，让对方把地址发过来",
        ],
        "answer": "C",
        "explain": "陌生链接 + 催促你尽快操作，是钓鱼短信的标准套路；任何通知都应走官方渠道二次核实。",
    },
    {
        "id": 23,
        "cat": "网络安全",
        "level": 1,
        "stem": "在没有密码的公共 Wi-Fi 上直接登录账号，主要风险是什么？",
        "options": [
            "同一网络里的其他人可能截获你传输的数据",
            "手机电池会明显耗得更快",
            "运营商会自动给你限速",
            "浏览器会被强制改成英文版",
        ],
        "answer": "A",
        "explain": "开放 Wi-Fi 缺少加密，同网段的人更容易嗅探到流量；收发敏感信息尽量用蜂窝网络或可信赖的 VPN。",
    },
    {
        "id": 24,
        "cat": "网络安全",
        "level": 1,
        "stem": "开启「两步验证 / 双因素认证」后，登录时除了密码通常还需要什么？",
        "options": [
            "把密码再输一遍",
            "换一个浏览器登录",
            "重启一次电脑",
            "手机短信验证码或认证器 App 生成的动态码",
        ],
        "answer": "D",
        "explain": "第二因子是「你拥有的东西」，即使密码泄露，别人也拿不到这串动态码，账号仍多一层保护。",
    },
    {
        "id": 25,
        "cat": "网络安全",
        "level": 1,
        "stem": "同一个密码在所有网站上重复使用，最大的隐患是什么？",
        "options": [
            "记起来太麻烦",
            "只要其中一个网站泄露密码，其他网站的账号也会跟着失守",
            "浏览器会运行得更慢",
            "网站会拒绝你登录",
        ],
        "answer": "B",
        "explain": "这正是「撞库」：攻击者拿一处泄露的账号密码去其他站点批量尝试。重要站点务必使用不同密码。",
    },
    # ---------------- 数据警务（扩展） ----------------
    {
        "id": 26,
        "cat": "数据警务",
        "level": 1,
        "stem": "一张案件登记表里，表格中的「一行」通常表示什么？",
        "options": [
            "一个字段名，比如「案发时间」",
            "整个数据库文件",
            "一条完整记录，即一起案件的全部信息",
            "一种数据类型",
        ],
        "answer": "C",
        "explain": "行 = 记录、列 = 字段，先把这个分清楚，后面做筛选和统计才不会乱套。",
    },
    {
        "id": 27,
        "cat": "数据警务",
        "level": 1,
        "stem": "能唯一区分每一条记录、绝不重复的字段（例如案件编号），通常称为什么？",
        "options": [
            "主键 / 唯一标识",
            "备注",
            "表头",
            "单位",
        ],
        "answer": "A",
        "explain": "姓名会重名、时间会撞车，只有唯一标识才能可靠地定位和关联记录。",
    },
    {
        "id": 28,
        "cat": "数据警务",
        "level": 1,
        "stem": "把身份证号中间几位打上 * 再拿去展示或共享，这种做法叫什么？",
        "options": [
            "备份",
            "压缩",
            "加密，之后可以用密钥还原",
            "脱敏 / 去标识化",
        ],
        "answer": "D",
        "explain": "脱敏在去掉可识别个人信息的同时保留数据可用性；它和「加密」不同，一般不以还原为目的。",
    },
    {
        "id": 29,
        "cat": "数据警务",
        "level": 1,
        "stem": "要从 10 万条记录里挑出「2024 年以后的案件」，最合适的做法是什么？",
        "options": [
            "把整张表打印出来，逐行圈",
            "按日期字段做筛选或条件查询",
            "把其他列全部删掉",
            "随机抽 100 条看看",
        ],
        "answer": "B",
        "explain": "先按条件把范围缩到最小，再动手分析，这是数据处理最基本也最省力的一步。",
    },
    {
        "id": 30,
        "cat": "数据警务",
        "level": 1,
        "stem": "数据里出现「年龄 = 200 岁」，最合理的处理方式是什么？",
        "options": [
            "照单全收，数据都是真的",
            "直接改成平均年龄填上去",
            "当作异常值回查原始记录，确认是录入错误后再修正",
            "说明系统一定被入侵了",
        ],
        "answer": "C",
        "explain": "明显超出合理范围的值必须先核实来源，既不能默默改掉，更不能直接拿来当结论。",
    },
    # ---------------- 电子取证（扩展） ----------------
    {
        "id": 31,
        "cat": "电子取证",
        "level": 1,
        "stem": "拿到一块涉案硬盘，分析之前最正确的做法是什么？",
        "options": [
            "先制作只读镜像，后续所有分析都在镜像上做，不改动原盘",
            "直接把硬盘插上电脑翻找文件，最方便",
            "先格式化一遍，再用恢复软件找回来",
            "随便拷到一个 U 盘里带回去看",
        ],
        "answer": "A",
        "explain": "原始证据必须保持原样；在镜像上分析，才能证明结论不是分析过程本身造成的改动。",
    },
    {
        "id": 32,
        "cat": "电子取证",
        "level": 1,
        "stem": "取证过程中要记下「谁、在什么时间、做了哪些操作」，主要目的是什么？",
        "options": [
            "让报告看起来更漂亮",
            "法律强制规定必须手写，打字不算",
            "方便以后把这些记录删掉",
            "形成完整的证据保管链，证明证据始终没被替换或篡改",
        ],
        "answer": "D",
        "explain": "这份留痕就是「监管链 / 保管链」，它保证证据从扣押到出庭的每一步都可追溯、经得起质证。",
    },
    {
        "id": 33,
        "cat": "电子取证",
        "level": 1,
        "stem": "手机里已经被「删除」的照片和聊天记录，通常是什么情况？",
        "options": [
            "立刻从存储芯片上彻底消失",
            "内容往往还残留在存储介质上，可能被恢复，直到被新数据覆盖",
            "系统会自动备份一份到云端",
            "会变成病毒文件",
        ],
        "answer": "B",
        "explain": "普通「删除」只是把空间标记为可复用；所以取证时要尽快固定数据、避免继续写入。",
    },
    {
        "id": 34,
        "cat": "电子取证",
        "level": 1,
        "stem": "现场对一台开机中的电脑取证，先拍照记录屏幕、连接线和插着的设备，主要为了什么？",
        "options": [
            "留作个人纪念",
            "证明这台电脑外观好看",
            "固定现场原始状态，避免事后说不清当时是什么样子",
            "没有实际用途，走个流程",
        ],
        "answer": "C",
        "explain": "拍照、录像和文字记录能在事后还原现场，也能说明证据是在什么状态下被提取的。",
    },
    {
        "id": 35,
        "cat": "电子取证",
        "level": 1,
        "stem": "电脑或服务器的「系统日志」里，最常见的一类内容是什么？",
        "options": [
            "带时间戳的登录、开关机、程序运行等事件记录",
            "只有桌面壁纸的设置",
            "只有相机拍的照片",
            "只有通讯录和短信",
        ],
        "answer": "A",
        "explain": "日志是按时间串起来的行为流水，做时间线分析时，它往往是最先要看的东西。",
    },
    # ---------------- 系统维护（扩展） ----------------
    {
        "id": 36,
        "cat": "系统维护",
        "level": 1,
        "stem": "某个网站服务突然打不开了，最先可以尝试的操作是什么？",
        "options": [
            "直接重装操作系统",
            "立刻把硬盘全部格式化",
            "换一颗更高主频的 CPU",
            "重启该服务进程，并查看它的日志",
        ],
        "answer": "D",
        "explain": "先重启服务把影响止住，再从日志找原因——由快到慢、由简到繁，这是排查的基本顺序。",
    },
    {
        "id": 37,
        "cat": "系统维护",
        "level": 1,
        "stem": "查日志时，最应该优先关注的内容是什么？",
        "options": [
            "整个日志文件的最后一行",
            "故障发生时间点附近的记录",
            "日志文件最早的那一行",
            "随便挑一行看看",
        ],
        "answer": "B",
        "explain": "日志是按时间流水记的，先锁定故障时刻，再向前看上下文，比漫无目的地翻要高效得多。",
    },
    {
        "id": 38,
        "cat": "系统维护",
        "level": 1,
        "stem": "磁盘快满了，下面哪种处理方式最不可取？",
        "options": [
            "清理临时文件和过期日志",
            "把旧数据归档到别的存储设备",
            "直接删除自己看不懂的系统文件和目录",
            "给磁盘扩容或加装新硬盘",
        ],
        "answer": "C",
        "explain": "看不懂的文件不等于没用；乱删系统文件往往直接导致服务异常，恢复起来比清理前更麻烦。",
    },
    {
        "id": 39,
        "cat": "系统维护",
        "level": 1,
        "stem": "要修改线上服务的配置文件，动手之前最该先做什么？",
        "options": [
            "备份原文件，并记录自己改了哪几处",
            "直接改，出问题再说",
            "先把配置文件删掉，重新写一遍",
            "挑个半夜时间悄悄改，谁也不说",
        ],
        "answer": "A",
        "explain": "有备份、有改动记录，出问题才能一键回滚；否则只能靠记忆硬猜刚才改了什么。",
    },
    {
        "id": 40,
        "cat": "系统维护",
        "level": 1,
        "stem": "一台机器突然连不上网络，最合理的排查起点是什么？",
        "options": [
            "立刻重装操作系统",
            "直接更换一块新网卡",
            "把所有软件全部卸载重装",
            "先确认电源、网线、IP 等最基础的连通条件",
        ],
        "answer": "D",
        "explain": "从最基础、最容易验证的环节查起，再逐层往上排查，能省掉大量无效动作。",
    },
]

CATEGORIES = ["网络安全", "数据警务", "电子取证", "系统维护"]
# 用「显示文本 -> 难度值」而不是裸整数做选项，避免不同版本控件返回值类型不一致
LEVEL_OPTIONS = {"基础 ★": 1, "进阶 ★★": 2}
MODES = ["随机抽题", "浏览题库"]
BY_ID = {q["id"]: q for q in QUESTIONS}
LETTERS = "ABCD"

# ============================================================
# 版本兼容层
#   文档：st.button 的 width 参数取 "content" / "stretch" / int；
#   use_container_width 已弃用，旧版仅支持后者。
# ============================================================
try:
    _BUTTON_HAS_WIDTH = "width" in inspect.signature(st.button).parameters
except (TypeError, ValueError):
    _BUTTON_HAS_WIDTH = False

# 所有按钮统一展开这组参数，一处适配、新旧版本都能运行
BTN_KW = {"width": "stretch"} if _BUTTON_HAS_WIDTH else {"use_container_width": True}
HAS_PILLS = hasattr(st, "pills")
HAS_SEGMENTED = hasattr(st, "segmented_control")


def pick_multi(label: str, options: list, default: list) -> list:
    """多选筛选：新版用 st.pills，旧版回退 st.multiselect。"""
    if HAS_PILLS:
        return st.pills(label, options, selection_mode="multi", default=default) or []
    return st.multiselect(label, options, default=default) or []


def pick_mode() -> str:
    """模式切换：新版用 st.segmented_control，旧版回退 st.radio。"""
    if HAS_SEGMENTED:
        picked = st.segmented_control(
            "模式", MODES, default=MODES[0], label_visibility="collapsed"
        )
        return picked or MODES[0]
    return st.radio("模式", MODES, label_visibility="collapsed")


# ============================================================
# 状态初始化
# ============================================================
def init_state() -> None:
    """Streamlit 每次交互都会重跑脚本，状态必须存在 session_state 里。"""
    defaults = {
        "cur_id": None,      # 当前抽到的题目 id
        "submitted": False,  # 当前题是否已提交
        "seen": [],          # 已抽过的题目 id（不重复模式用）
        "nonce": 0,          # 抽题计数器，用来重置选项控件
        "answered": set(),   # 已计分的题目 id
        "attempts": 0,       # 已答题数
        "correct": 0,        # 答对数
        "_sig": None,        # 筛选条件签名，用于检测变化
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def build_pool(cats: list, levels: list) -> list:
    """按方向与难度筛选出题池。空选返回空列表，不再隐式当作「全选」。"""
    return [
        q for q in QUESTIONS
        if q["cat"] in cats and q["level"] in levels
    ]


def draw_question(pool: list, avoid_repeat: bool) -> bool:
    """从题池里随机抽一道，写入 session_state。"""
    if not pool:
        return False

    candidates = pool
    if avoid_repeat:
        remain = [q for q in pool if q["id"] not in st.session_state.seen]
        if not remain:                       # 抽完了就自动重新开始
            st.session_state.seen = []
            remain = pool
        candidates = remain

    q = random.choice(candidates)
    st.session_state.cur_id = q["id"]
    st.session_state.submitted = False
    st.session_state.nonce += 1
    if q["id"] not in st.session_state.seen:
        st.session_state.seen.append(q["id"])
    return True


# ============================================================
# 渲染组件
# ============================================================
def render_meta(q: dict) -> None:
    """题目上方的方向 / 难度标签。"""
    stars = "★" * q["level"]
    level = "基础" if q["level"] == 1 else "进阶"
    st.caption(f'第 {q["id"]} 题　·　{q["cat"]}　·　{stars} {level}')


def render_result(q: dict, picked: str | None) -> None:
    """判分并显示解析。"""
    is_right = picked is not None and picked[0] == q["answer"]
    if is_right:
        st.success("回答正确")
    else:
        st.error(f"回答错误　正确答案是 {q['answer']}")

    st.markdown(f"**解析**　{q['explain']}")


def render_draw_mode(pool: list, avoid_repeat: bool) -> None:
    """随机抽题模式。"""
    left, mid, right = st.columns([1, 2, 1])
    with mid:
        if st.button("随机抽一题", type="primary", **BTN_KW):
            if draw_question(pool, avoid_repeat):
                st.rerun()

    st.write("")

    if st.session_state.cur_id is None:
        st.info("点击上方按钮，随机抽一道题。")
        return

    q = BY_ID[st.session_state.cur_id]
    scored = q["id"] in st.session_state.answered

    with st.container(border=True):
        render_meta(q)
        st.markdown(f"#### {q['stem']}")

        labels = [f"{LETTERS[i]}. {opt}" for i, opt in enumerate(q["options"])]
        # nonce 变化 -> key 变化 -> 选项控件重置。旧 key 由 Streamlit 自动清理。
        picked = st.radio(
            "选择一个答案",
            labels,
            index=None,
            key=f'pick_{q["id"]}_{st.session_state.nonce}',
            disabled=st.session_state.submitted,
            label_visibility="collapsed",
        )

        if not st.session_state.submitted:
            if st.button("提交答案", **BTN_KW):
                if picked is None:
                    st.warning("请先选择一个选项。")
                else:
                    st.session_state.submitted = True
                    # 同一道题只计分一次，避免反复刷分
                    if q["id"] not in st.session_state.answered:
                        st.session_state.answered.add(q["id"])
                        st.session_state.attempts += 1
                        if picked[0] == q["answer"]:
                            st.session_state.correct += 1
                    st.rerun()
            elif scored:
                st.caption("本题已计分，重做或再次提交不会改变统计。")
        else:
            render_result(q, picked)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("再来一题", type="primary", **BTN_KW):
            if draw_question(pool, avoid_repeat):
                st.rerun()
    with c2:
        if st.button("重做本题", **BTN_KW):
            st.session_state.submitted = False
            st.session_state.nonce += 1
            st.rerun()


def render_browse_mode(cats: list, levels: list) -> None:
    """浏览模式：只展示当前筛选命中的方向与难度，展开看答案。"""
    visible = [
        cat for cat in CATEGORIES
        if cat in cats
        and any(q["cat"] == cat and q["level"] in levels for q in QUESTIONS)
    ]
    if not visible:
        st.warning("当前筛选条件下没有题目，请调整方向或难度。")
        return

    tabs = st.tabs(visible)
    for tab, cat in zip(tabs, visible):
        with tab:
            items = [
                q for q in QUESTIONS
                if q["cat"] == cat and q["level"] in levels
            ]
            for q in items:
                stars = "★" * q["level"]
                with st.expander(f'{q["id"]:02d}　{q["stem"]}　{stars}'):
                    for i, opt in enumerate(q["options"]):
                        mark = "　✓" if LETTERS[i] == q["answer"] else ""
                        st.markdown(f"{LETTERS[i]}. {opt}{mark}")
                    st.caption(f"解析：{q['explain']}")


# ============================================================
# 主体
# ============================================================
st.markdown(
    """
    <style>
    /* 收紧顶部留白 */
    div.block-container { padding-top: 2.5rem; padding-bottom: 3rem; }
    div[data-testid="stMetricValue"] { font-size: 1.4rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

init_state()

st.title("超超简单的题，快来挑战")
st.caption("网络安全 / 数据警务 / 电子取证 / 系统维护　·　共 40 题　·　基础 ★ / 进阶 ★★")

# ---------- 侧边栏：筛选与统计 ----------
with st.sidebar:
    st.subheader("模式")
    mode = pick_mode()

    st.subheader("筛选")
    cats = pick_multi("方向", CATEGORIES, list(CATEGORIES))
    picked_labels = pick_multi(
        "难度", list(LEVEL_OPTIONS.keys()), list(LEVEL_OPTIONS.keys())
    )
    levels = [LEVEL_OPTIONS[x] for x in picked_labels if x in LEVEL_OPTIONS]
    avoid_repeat = st.toggle("抽过的题不重复", value=True)
    st.caption("提示：清空任一筛选即不展示题目，重新勾选即可恢复。")

    st.divider()
    st.subheader("本次统计")
    if st.session_state.attempts:
        rate = st.session_state.correct / st.session_state.attempts * 100
    else:
        rate = 0.0
    c1, c2 = st.columns(2)
    c1.metric("已答", st.session_state.attempts)
    c2.metric("正确率", f"{rate:.0f}%")
    st.progress(rate / 100)
    st.caption(
        f"答对 {st.session_state.correct} 题 / 共 {st.session_state.attempts} 题"
    )

    if st.button("重置统计", **BTN_KW):
        st.session_state.answered = set()
        st.session_state.attempts = 0
        st.session_state.correct = 0
        st.session_state.seen = []
        st.session_state.cur_id = None
        st.session_state.submitted = False
        st.rerun()

# ---------- 筛选条件变化时重置抽题状态 ----------
# frozenset 与顺序无关，避免用户勾选顺序不同被误判为「筛选变了」
signature = (frozenset(cats), frozenset(levels))
if st.session_state._sig is None:
    st.session_state._sig = signature
elif st.session_state._sig != signature:
    st.session_state._sig = signature
    st.session_state.seen = []
    st.session_state.cur_id = None
    st.session_state.submitted = False

pool = build_pool(cats, levels)

# ---------- 主区域 ----------
if mode == "随机抽题":
    if not pool:
        st.info("当前筛选条件下没有题目。请在左侧至少选择一个方向和一个难度。")
    else:
        st.caption(f"当前题池：{len(pool)} 道　·　已抽 {len(st.session_state.seen)} 道")
        render_draw_mode(pool, avoid_repeat)
else:
    st.caption(
        "浏览模式会直接显示正确答案与解析，适合复习；如需自测请切换到「随机抽题」。"
    )
    render_browse_mode(cats, levels)
