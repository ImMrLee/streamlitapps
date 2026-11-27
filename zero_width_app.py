"""
零宽字符注入器 · Streamlit 版（精简）
------------------------------------------------
固定策略：每个名字的字与字之间插入 U+2060（WORD JOINER）。
输入：人名，一行一个（回车分隔）。
输出：注入后的名字，一行一个，顺序与输入一致。

依赖：streamlit
运行：streamlit run zero_width_app.py
"""

import html
import json
import re

import streamlit as st
import streamlit.components.v1 as components

ZW = "\u2060"  # WORD JOINER：零宽、不产生换行点

st.set_page_config(page_title="零宽字符注入器", layout="centered")

st.markdown(
    """
    <style>
      .block-container {padding-top: 2.4rem;}
      .zw-badge {
        display: inline-block; background: #ff6a00; color: #fff;
        font-size: 11px; font-weight: 700; line-height: 11px;
        padding: 1px 3px; margin: 0 1px; border-radius: 3px;
        vertical-align: middle;
      }
      .marked-box {
        border: 1px dashed #ffd591; background: #fffaf0;
        border-radius: 8px; padding: 14px 16px;
        font-size: 15px; line-height: 2.1; white-space: pre-wrap;
        word-break: break-word; color: #1a1a1a;
      }
      div[data-testid="stBaseButton-primary"],
      button[kind="primary"] {
        background: #07c160 !important; border-color: #07c160 !important;
      }
      div[data-testid="stBaseButton-primary"]:hover,
      button[kind="primary"]:hover {
        background: #06ad56 !important; border-color: #06ad56 !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)


# ----------------------------------------------------------------------------
# 核心逻辑
# ----------------------------------------------------------------------------
def inject_name(name: str) -> tuple[str, int]:
    """字与字之间插入一个 U+2060，返回 (注入后的名字, 插入个数)。

    单字名无法插入，原样返回。
    """
    chars = list(name.strip())
    if len(chars) < 2:
        return name.strip(), 0
    return ZW.join(chars), len(chars) - 1


def split_names(raw: str) -> list[str]:
    """只按回车分行，逐行去首尾空白，丢掉空行。顺序保持不变。"""
    return [line.strip() for line in (raw or "").splitlines() if line.strip()]


def marked_html(text: str) -> str:
    """把零宽字符渲染成橙色小方块，便于核对插入位置。"""
    return re.sub(
        r"\u2060",
        '<span class="zw-badge" title="U+2060">·</span>',
        html.escape(text),
    )


def copy_widget(text: str, label: str, height: int = 58) -> None:
    """带复制按钮的 iframe 组件；优先 Clipboard API，失败回退 execCommand。"""
    payload = json.dumps(text)
    label_js = json.dumps(label)
    components.html(
        f"""
        <style>
          body {{margin:0; background:transparent; font-family:-apple-system,
                 "PingFang SC","Microsoft YaHei",sans-serif;}}
          #cp {{
            width:100%; padding:9px 16px; font-size:14px; font-weight:500;
            color:#07a352; background:#fff; border:1px solid #07c160;
            border-radius:8px; cursor:pointer; transition:all .15s;
          }}
          #cp:hover {{background:#f0fdf6;}}
          #cp.done {{background:#07c160; color:#fff; border-color:#07c160;}}
        </style>
        <button id="cp">{html.escape(label)}</button>
        <script>
          const TXT = {payload};
          const LBL = {label_js};
          const btn = document.getElementById('cp');
          function flash(msg, ok) {{
            btn.textContent = msg;
            btn.classList.toggle('done', ok);
            setTimeout(() => {{ btn.textContent = LBL; btn.classList.remove('done'); }}, 1600);
          }}
          btn.addEventListener('click', async () => {{
            try {{
              await navigator.clipboard.writeText(TXT);
              flash('已复制', true);
            }} catch (e) {{
              const ta = document.createElement('textarea');
              ta.value = TXT;
              ta.style.position = 'fixed';
              ta.style.opacity = '0';
              document.body.appendChild(ta);
              ta.focus(); ta.select();
              let ok = false;
              try {{ ok = document.execCommand('copy'); }} catch (_) {{}}
              document.body.removeChild(ta);
              flash(ok ? '已复制' : '复制失败，请用代码块的复制图标', ok);
            }}
          }});
        </script>
        """,
        height=height,
    )


# ----------------------------------------------------------------------------
# 状态
# ----------------------------------------------------------------------------
ss = st.session_state
ss.setdefault("result", "")      # 注入后的完整文本（每行一个）
ss.setdefault("count", 0)        # 名字个数
ss.setdefault("zw_count", 0)     # 插入的零宽字符总数
ss.setdefault("odd", [])         # 单字名（无法插入）


def _reset():
    ss["result"] = ""
    ss["count"] = 0
    ss["zw_count"] = 0
    ss["odd"] = []


# ----------------------------------------------------------------------------
# 界面
# ----------------------------------------------------------------------------
st.title("零宽字符注入器")
st.caption(
    f"每个名字的字与字之间插入一个不可见但实际存在的空格，可以避免被审查关键词"
)

names_raw = st.text_area(
    "人名",
    height=280,
    placeholder="一行一个，回车分隔\n\n张三\n李四\n欧阳修远",
    key="names_input",
)

c1, c2, c3 = st.columns([1, 1, 2.6])
gen = c1.button("生成", type="primary", use_container_width=True)
c2.button("清空", use_container_width=True, on_click=_reset)

if gen:
    lines = split_names(ss["names_input"])
    if not lines:
        st.error("还没有内容：先输入人名，一行一个。")
        _reset()
    else:
        out, zw_total, odd = [], 0, []
        for name in lines:
            done, n = inject_name(name)
            out.append(done)
            zw_total += n
            if n == 0:
                odd.append(name)
        ss["result"] = "\n".join(out)
        ss["count"] = len(lines)
        ss["zw_count"] = zw_total
        ss["odd"] = odd

if ss["result"]:
    m1, m2 = st.columns(2)
    m1.metric("名字个数", ss["count"])
    m2.metric("插入字符", ss["zw_count"])

    if ss["odd"]:
        st.warning("以下名字不足 2 字，未做处理：" + "、".join(ss["odd"]))

    st.code(ss["result"], language=None, wrap_lines=True)

    a, b = st.columns([1, 1])
    with a:
        copy_widget(ss["result"], "复制全部")
    with b:
        st.download_button(
            "下载 .txt",
            data=ss["result"].encode("utf-8"),
            file_name="names.txt",
            mime="text/plain",
            use_container_width=True,
        )

    if st.checkbox("显示标记（核对插入位置）"):
        st.markdown(
            f'<div class="marked-box">{marked_html(ss["result"])}</div>',
            unsafe_allow_html=True,
        )
        st.caption("橙色小方块是 U+2060 的位置。复制上面的结果时不带这个标记。")

st.divider()
st.caption(
    "**提醒**：微信识别前可能做文本归一化，注入后仍被点亮是有可能的，"
    "请先在手机预览验证。副作用是读者复制名字会带上隐藏字符，"
    "粘到搜索框或 Excel 里可能出现异常空格。"
)
