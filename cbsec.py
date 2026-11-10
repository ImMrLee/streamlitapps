import random

import streamlit as st

# ============================================================
# 页面配置
# ============================================================
st.set_page_config(page_title="社团纳新 · 欢迎来到网安社团", layout="centered")

# ============================================================
# 题库数据（中等难度卷，20 题）
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
]

CATEGORIES = ["网络安全", "数据警务", "电子取证", "系统维护"]
BY_ID = {q["id"]: q for q in QUESTIONS}
LETTERS = "ABCD"


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
    """按方向与难度筛选出题池。"""
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


def render_result(q: dict, picked: str) -> None:
    """判分并显示解析。"""
    is_right = picked and picked[0] == q["answer"]
    if is_right:
        st.success("回答正确")
    else:
        st.error(f"回答错误　正确答案是 {q['answer']}")

    st.markdown(f"**解析**　{q['explain']}")


def render_draw_mode(pool: list, avoid_repeat: bool) -> None:
    """随机抽题模式。"""
    left, mid, right = st.columns([1, 2, 1])
    with mid:
        if st.button("随机抽一题", type="primary", width="stretch"):
            if draw_question(pool, avoid_repeat):
                st.rerun()

    st.write("")

    if st.session_state.cur_id is None:
        st.info("点击上方按钮，随机抽一道题。")
        return

    q = BY_ID[st.session_state.cur_id]

    with st.container(border=True):
        render_meta(q)
        st.markdown(f"#### {q['stem']}")

        labels = [f"{LETTERS[i]}. {opt}" for i, opt in enumerate(q["options"])]
        picked = st.radio(
            "选择一个答案",
            labels,
            index=None,
            key=f'pick_{q["id"]}_{st.session_state.nonce}',
            disabled=st.session_state.submitted,
            label_visibility="collapsed",
        )

        if not st.session_state.submitted:
            if st.button("提交答案", width="stretch"):
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
        else:
            render_result(q, picked)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("再来一题", type="primary", width="stretch"):
            if draw_question(pool, avoid_repeat):
                st.rerun()
    with c2:
        if st.button("重做本题", width="stretch"):
            st.session_state.submitted = False
            st.session_state.nonce += 1
            st.rerun()


def render_browse_mode() -> None:
    """浏览模式：按方向分组，展开看答案。"""
    tabs = st.tabs(CATEGORIES)
    for tab, cat in zip(tabs, CATEGORIES):
        with tab:
            items = [q for q in QUESTIONS if q["cat"] == cat]
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
st.caption("网络安全 / 数据警务 / 电子取证 / 系统维护　·　中等难度　·　共 20 题")

# ---------- 侧边栏：筛选与统计 ----------
with st.sidebar:
    st.subheader("模式")
    mode = st.radio("模式", ["随机抽题", "浏览题库"], label_visibility="collapsed")

    st.subheader("筛选")
    cats = st.multiselect("方向", CATEGORIES, default=list(CATEGORIES))
    level_labels = {1: "基础 ★", 2: "进阶 ★★"}
    picked_levels = st.multiselect(
        "难度", list(level_labels.keys()),
        default=list(level_labels.keys()),
        format_func=lambda x: level_labels[x],
    )
    levels = picked_levels or [1, 2]
    avoid_repeat = st.toggle("抽过的题不重复", value=True)

    st.divider()
    st.subheader("本次统计")
    if st.session_state.attempts:
        rate = st.session_state.correct / st.session_state.attempts * 100
    else:
        rate = 0.0
    c1, c2 = st.columns(2)
    c1.metric("已答", st.session_state.attempts)
    c2.metric("正确率", f"{rate:.0f}%")

    if st.button("重置统计", width="stretch"):
        st.session_state.answered = set()
        st.session_state.attempts = 0
        st.session_state.correct = 0
        st.session_state.seen = []
        st.session_state.cur_id = None
        st.session_state.submitted = False
        st.rerun()

# ---------- 筛选条件变化时重置抽题状态 ----------
signature = (tuple(cats or CATEGORIES), tuple(levels))
if st.session_state._sig is None:
    # 首次进入只记录签名，不能清空状态
    st.session_state._sig = signature
elif st.session_state._sig != signature:
    st.session_state._sig = signature
    st.session_state.seen = []
    st.session_state.cur_id = None
    st.session_state.submitted = False

pool = build_pool(cats or CATEGORIES, levels)

# ---------- 主区域 ----------
if mode == "随机抽题":
    if not pool:
        st.warning("当前筛选条件下没有题目，请调整方向或难度。")
    else:
        st.caption(f"当前题池：{len(pool)} 道　·　已抽 {len(st.session_state.seen)} 道")
        render_draw_mode(pool, avoid_repeat)
else:
    render_browse_mode()
