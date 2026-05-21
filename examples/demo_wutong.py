"""
追风者 · WindCatcher — 演示脚本
场景：梧桐咖啡 × 愚园路落叶季
用途：现场演示（10分钟版本）

运行方式：
  python demo_wutong.py              # 完整演示
  python demo_wutong.py --fast       # 快速版（跳过等待）
  python demo_wutong.py --stage 3    # 从阶段3开始
"""

import json
import time
import yaml
from pathlib import Path
from typing import Optional

# ============================================================
# 配置
# ============================================================

STORE_FILE = Path(__file__).parent / "test_store.yaml"
STORE_NAME = "wutong-coffee"

# 演示用预设数据（避免演示时等待 API）
PRESET_TRENDS = {
    "douyin": [
        ("#上海秋天 citywalk", "1,250万"),
        ("#愚园路 拍照打卡", "680万"),
        ("#咖啡探店 上海", "920万"),
        ("#最美落叶季", "450万"),
        ("#周末去哪儿", "2,100万"),
    ],
    "local": [
        ("愚园路落叶不扫政策", "11月15日-12月5日", "每年保留节目，市政府主办"),
        ("愚园路城市漫步节", "11月20日-11月26日", "文创市集+街区导览"),
        ("上海咖啡文化周", "11月全月", "全市咖啡联动"),
    ],
    "calendar": [
        ("11月", "落叶季 · 秋季限定"),
        ("11月23日", "感恩节前 · 暖心营销"),
        ("11月24日", "黑色星期五 · 消费氛围"),
    ],
}

PRESET_DIRECTIONS = [
    {
        "id": 1,
        "name": "愚园路落叶季 × 限定特调",
        "why": "梧桐咖啡临街梧桐树景是天然场景，落叶不扫政策每年吸引大量人流",
        "effect": "曝光3-5万 / 到店200+人 / ROI 1:8",
        "difficulty": "⭐⭐",
        "budget_level": "中(500-2000元)",
        "reference": "杭州「满觉陇桂花季」咖啡馆借势案例——限定款+窗景打卡，小红书自发传播500+笔记",
    },
    {
        "id": 2,
        "name": "上海咖啡文化周 × 愚园路咖啡地图",
        "why": "全市咖啡联动自带流量，愚园路已有3家精品咖啡馆可做联合",
        "effect": "曝光5-8万 / 到店300+人 / ROI 1:6",
        "difficulty": "⭐⭐⭐",
        "budget_level": "中(500-2000元)",
        "reference": "北京「胡同咖啡地图」联合营销，8家店互推，单店到店提升40%",
    },
    {
        "id": 3,
        "name": "双十一后报复性消费 × 咖啡月卡",
        "why": "双十一后消费者从线上回归线下，愿意为体验买单",
        "effect": "月卡售出50-80张 / 锁定11月复购 / ROI 1:4",
        "difficulty": "⭐",
        "budget_level": "低(0-500元)",
        "reference": "M Stand「半月卡」模式，锁定2周复购，售出率超预期30%",
    },
    {
        "id": 4,
        "name": "感恩节 × 愚园路邻里温情",
        "why": "梧桐咖啡有200+熟客社群，适合打情感牌做老客裂变",
        "effect": "老客裂变率15% / 新增社群100人 / ROI 纯口碑",
        "difficulty": "⭐",
        "budget_level": "低(0-500元)",
        "reference": "社区咖啡馆「请陌生人喝咖啡」活动，单次裂变200+新客",
    },
    {
        "id": 5,
        "name": "初冬暖心季 × 热饮升级",
        "why": "11月气温下降，热饮需求上升，是产品升级的好时机",
        "effect": "客单价提升5-8元 / 热饮占比从30%→60%",
        "difficulty": "⭐⭐",
        "budget_level": "中(500-2000元)",
        "reference": "Seesaw冬季「暖饮计划」，热饮限定杯套引发收集",
    },
]

PRESET_CONCEPTS = [
    {
        "id": "A",
        "name": "「落叶配方」限定特调",
        "theme": "愚园路的梧桐叶落了，我们把它煮进了咖啡里",
        "mechanism": "推出1款「落叶配方」秋季特调（梧桐叶焦糖冷萃），杯套印愚园路手绘地图",
        "hook": "杯套打卡 + 愚园路落叶地图社交传播",
        "platform": "小红书 + 朋友圈",
        "budget": 800,
        "diff": "产品创新驱动，轻活动重内容——适合产品力强的门店",
    },
    {
        "id": "B",
        "name": "「梧桐树下的故事」征集",
        "theme": "在愚园路上，你和谁一起走过了梧桐树下？",
        "mechanism": "征集愚园路故事，入选者免费喝一个月咖啡，故事印在店内故事墙上",
        "hook": "UGC故事在小红书二次传播 + 故事墙打卡",
        "platform": "小红书 + 线下",
        "budget": 1200,
        "diff": "情感连接驱动，UGC裂变——适合社群活跃、有情感资产的门店",
    },
    {
        "id": "C",
        "name": "「落叶不扫」咖啡摄影赛",
        "theme": "愚园路落叶不扫，你的照片我们来买单",
        "mechanism": "拍愚园路落叶+梧桐咖啡出镜，发小红书带话题，每周最佳送月卡",
        "hook": "摄影赛天然UGC + 本地摄影爱好者圈层传播",
        "platform": "小红书",
        "budget": 500,
        "diff": "摄影圈层裂变，成本最低——适合预算紧张但想扩大传播半径的门店",
    },
]


# ============================================================
# 模拟技能调用（演示用占位函数）
# ============================================================

def call_douyin_hot_trend(limit: int = 30) -> list:
    """模拟：调用 douyin-hot-trend CLI"""
    print(f"  🔥 调用 douyin-hot-trend → 获取 TOP {limit}")
    time.sleep(0.5)  # 模拟 API 延迟
    return PRESET_TRENDS["douyin"]


def call_web_search(query: str) -> str:
    """模拟：WebSearch"""
    print(f"  🔍 WebSearch: {query[:60]}...")
    time.sleep(0.3)
    return f"[搜索结果] {query}"


def call_skill(name: str, args: str = "") -> None:
    """模拟：调用技能"""
    print(f"  🎯 Skill: {name} {args}")
    time.sleep(0.3)


def load_store(store_name: str) -> dict:
    """加载门店数据"""
    with open(STORE_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["stores"][store_name]


def show_card(title: str, items: list[tuple], header: list[str] = None):
    """展示卡片式数据"""
    print(f"\n  ╔═ {title} ═{'═' * (50 - len(title))}")
    if header:
        print(f"  ║ {' | '.join(header)}")
        print(f"  ║ {'-' * 45}")
    for item in items:
        print(f"  ║ {' | '.join(str(x) for x in item)}")
    print(f"  ╚{'═' * 52}")


# ============================================================
# 演示阶段
# ============================================================

def phase_0_store_interview(store: dict):
    """阶段0：门店快诊（预设数据，跳过问卷）"""
    print("\n" + "=" * 56)
    print("  阶段 0：门店快诊")
    print("=" * 56)
    print(f"\n  📋 门店情报已预设：{store['name']}")
    print(f"  📍 {store['city']} · {store['district']} · {store['street']}")
    print(f"  ☕ {store['category']} | 💰 月营收 {store['monthly_revenue']} | 客单价 ¥{store['avg_ticket']}")
    print(f"  🏪 竞品：{', '.join(c['name'] for c in store['competitors'])}")
    print(f"  💊 困境：{store['pains'][0]}")
    print(f"  🎯 预算：{store['budget']}")


def phase_1_hotspot_radar(store: dict):
    """阶段1：热点雷达"""
    print("\n" + "=" * 56)
    print("  阶段 1：热点雷达 — 多源抓取中...")
    print("=" * 56)

    # 1. 抖音热榜
    print("\n  📡 [1/4] 抖音热榜")
    trends = call_douyin_hot_trend(30)
    relevant = [t for t in trends if any(
        kw in t[0] for kw in ["上海", "咖啡", "秋天", "探店", "打卡", "citywalk"]
    )]
    show_card("抖音相关热点", relevant[:5])

    # 2. 本地热点
    print("\n  📡 [2/4] 本地热点 & 活动")
    call_web_search(f"{store['city']} {store['district']} 11月 活动 市集 文化周")
    show_card("本地可蹭热点", PRESET_TRENDS["local"])

    # 3. 营销日历
    print("\n  📡 [3/4] 营销日历")
    show_card("近30天营销节点", PRESET_TRENDS["calendar"])

    # 4. 成功案例
    print("\n  📡 [4/4] 成功案例")
    call_web_search(f"咖啡馆 借势营销 成功案例 落叶季 2025")
    print("  📚 参考案例：杭州「满觉陇桂花季」咖啡馆借势 → 限定款+窗景打卡，小红书自发传播500+笔记")


def phase_2_direction_matching(store: dict) -> int:
    """阶段2：方向匹配 + 用户选择"""
    print("\n" + "=" * 56)
    print("  阶段 2：方向匹配")
    print("=" * 56)
    print(f"\n  🔄 交叉匹配：梧桐咖啡 × 热点库 → 5 个可追方向")

    for d in PRESET_DIRECTIONS:
        print(f"""
  ┌──────────────────────────────────────────────────┐
  │ 🎯 方向{d['id']}：{d['name']}
  │
  │ 追什么：{d['name']}
  │ 为什么追：{d['why']}
  │ 预期效果：{d['effect']}
  │ 难度：{d['difficulty']}  |  预算：{d['budget_level']}
  │ 📚 参考：{d['reference']}
  └──────────────────────────────────────────────────┘""")

    print("\n  ⚠️ 请选择 1-2 个方向 [演示模式：自动选方向1]")
    return 1


def phase_3_concept_matching(direction_id: int) -> int:
    """阶段3：策划概念匹配 + 用户选择"""
    print("\n" + "=" * 56)
    print(f"  阶段 3：策划概念匹配 — 基于方向{direction_id}")
    print("=" * 56)
    print(f"\n  💡 为「{PRESET_DIRECTIONS[direction_id - 1]['name']}」生成 3 个策划概念：")

    for c in PRESET_CONCEPTS:
        print(f"""
  ┌──────────────────────────────────────────────────┐
  │ 🎪 策划概念{c['id']}：{c['name']}
  │
  │ 一句话主题：{c['theme']}
  │ 核心机制：{c['mechanism']}
  │ 传播抓手：{c['hook']}
  │ 主阵地：{c['platform']}
  │ 预算：¥{c['budget']}
  │
  │ ⚠️ 差异点：{c['diff']}
  └──────────────────────────────────────────────────┘""")

    print("\n  ⚠️ 请选择 1 个策划概念 [演示模式：自动选概念B]")
    return 1  # 0-indexed → concept B


def phase_4_smart_plan(store: dict, concept: dict):
    """阶段4：SMART策划案生成"""
    print("\n" + "=" * 56)
    print(f"  阶段 4：SMART 策划案 — {concept['name']}")
    print("=" * 56)

    # 调用 shortvideo-hook
    call_skill("shortvideo-hook", f"生成 {concept['name']} 类型=悬念型")

    # 调用 营销技能库
    call_skill("营销技能库", "social-content + copywriting + paid-ads")

    print(f"""
  ┌──────────────────────────────────────────────────┐
  │ 📋 {concept['name']} · SMART 策划案
  │
  │ 🎯 活动概览
  │   主题：{concept['theme']}
  │   时间：11月15日-12月5日（愚园路落叶不扫期）
  │   预算：¥{concept['budget']}
  │
  │ ✍️ 内容矩阵（3/3/3）
  │   小红书 ×3：
  │     #1 预热 | 11.10 | 《愚园路梧桐叶快黄了，我偷看了隔壁咖啡馆的配方本》
  │     #2 活动 | 11.15 | 《在梧桐树下喝完这杯，才能算在上海过秋天》
  │     #3 复盘 | 11.22 | 《50个陌生人的愚园路故事里，最打动我的是这个》
  │   抖音 ×3：
  │     #1 预告 | 道具：梧桐叶+咖啡杯 → 关联DOU+同城3km
  │     #2 现场 | 窗边座位实拍 → 关联DOU+同城3km
  │     #3 反应 | 顾客读自己故事 → 自然流量
  │   朋友圈 ×3：
  │     #1 悬念预告 | 11.12 | 不说破，制造好奇
  │     #2 活动实况 | 11.15 | 一杯咖啡+一段故事
  │     #3 感谢收尾 | 11.16 | 收尾 + 下周预告
  │
  │ 🎪 活动机制 [关联内容矩阵]
  │   触发：小红书#1+抖音#1+朋友圈#1 → "梧桐树下的故事"话题
  │   到店：小红书#2+抖音#2+朋友圈#2 → 写故事→故事墙+免费咖啡
  │   传播：小红书#3+自然流量 → UGC二次传播
  │   裂变：入选者邀请朋友来看自己的故事 → 自然裂变
  │
  │ 💰 投放策略 [关联内容矩阵]
  │   小红书#1 预热 | 薯条50元 | 同城·女性·18-35 | CTR>3%
  │   小红书#2 活动 | 薯条100元 | 同城+愚园路商圈 | 到店>20人
  │   抖音#1 预告 | DOU+100元 | 同城3km | 播放>5000
  │   抖音#2 现场 | DOU+100元 | 同城3km | 到店归因
  │   总投放：¥350
  │
  │ 📊 SMART 校验
  │   S: 覆盖5000+人 → 内容曝光+到店
  │   M: 到店转化80+人 → 暗号"梧桐故事"归因
  │   A: 预算¥1200 → 物料600+投放350+免费咖啡250
  │   R: 关联门店 → 梧桐树景·愚园路·社群
  │   T: 11.10-12.05 → 日历追踪
  └──────────────────────────────────────────────────┘
  """)


def phase_5_visual_generation(store: dict, concept: dict):
    """阶段5：视觉物料生成"""
    print("\n" + "=" * 56)
    print(f"  阶段 5：视觉物料生成")
    print("=" * 56)

    print(f"""
  📸 收集门店素材：
  "在生成海报之前，我需要一些参考——

  1. 梧桐咖啡门头照片（愚园路街景最好）
  2. 梧桐冷萃的产品照（招牌款）
  3. 窗边座位的实拍（最出片的角落）
  4. 现有的 logo 或品牌色（如果有）

  有这些参考，AI 生成的海报会更贴合你的店。"
  """)

    # 模拟用户提供了照片后
    print("  [演示模式：假设已收到门店照片]\n")

    call_skill("lovart", f"生成 '{concept['name']}' 活动海报")
    print("  🎨 Lovart 渲染中...")
    time.sleep(1)

    print(f"""
  🖼️ 已生成 3 张视觉物料：

  ┌─────────────────┬─────────────────┬─────────────────┐
  │  活动主海报      │  小红书配图      │  抖音封面        │
  │  [AI 生成]      │  [AI 生成]      │  [AI 生成]      │
  │  愚园路落叶+      │  梧桐冷萃+      │  "在梧桐树下"    │
  │  梧桐咖啡门头    │  故事卡片特写    │  文字+门头      │
  │  1200×800px     │  1080×1080px    │  1080×1920px    │
  └─────────────────┴─────────────────┴─────────────────┘
  """)


def phase_6_ppt_pitch(store: dict, concept: dict):
    """阶段6：PPT生成"""
    print("\n" + "=" * 56)
    print(f"  阶段 6：PPT Pitch")
    print("=" * 56)

    call_skill("ppt-deck-master", f"'{concept['name']} · {store['name']} 营销方案'")
    print("  📊 Ppt Deck Master 渲染中...（约 15 页，成本 ¥5）")
    time.sleep(1)

    print(f"""
  ✅ PPT 已生成：{concept['name']}_{store['name']}_营销方案.pptx

  包含 15 页：
   1. 封面 — {concept['name']}
   2. 痛点 — {store['pains'][0]}
   3. 机会 — 愚园路落叶不扫 · 11月
   4. 方案 — {concept['theme']}
   5. 内容矩阵 — 小红书3+抖音3+朋友圈3
   6. 活动机制 — 故事征集全流程
   7. 投放策略 — ¥350 四轮投放
   8. 视觉物料 — 3张AI海报展示
   9. 执行Timeline — 11.10-12.05
  10. KPI — SMART 指标
  11. 预算总表 — ¥1200
  12. 风险预案
  13. 下一步
  14. 团队
  15. 谢谢
  """)


# ============================================================
# 主演示流程
# ============================================================

def demo(fast: bool = False, start_stage: int = 0):
    """完整演示流程"""
    print("""
  ╔══════════════════════════════════════════════════╗
  ║  追风者 · WindCatcher                            ║
  ║  中小门店热点借势营销助手                          ║
  ║  演示：梧桐咖啡 × 愚园路落叶季                      ║
  ╚══════════════════════════════════════════════════╝
  """)

    # 加载门店数据
    store = load_store(STORE_NAME)

    # 设置全局速度
    global SLEEP
    SLEEP = 0.1 if fast else 0.5

    # 阶段0：门店快诊
    if start_stage <= 0:
        phase_0_store_interview(store)
        if not fast:
            input("\n  [按 Enter 继续 → 阶段1：热点雷达]")

    # 阶段1：热点雷达
    if start_stage <= 1:
        phase_1_hotspot_radar(store)
        if not fast:
            input("\n  [按 Enter 继续 → 阶段2：方向匹配]")

    # 阶段2：方向匹配
    if start_stage <= 2:
        selected_direction = phase_2_direction_matching(store)
        if not fast:
            input("\n  [按 Enter 继续 → 阶段3：策划概念匹配]")

    # 阶段3：策划概念匹配
    if start_stage <= 3:
        selected_concept = phase_3_concept_matching(selected_direction)
        if not fast:
            input("\n  [按 Enter 继续 → 阶段4：SMART策划案]")

    # 阶段4：SMART策划案
    if start_stage <= 4:
        concept = PRESET_CONCEPTS[selected_concept]
        phase_4_smart_plan(store, concept)
        if not fast:
            input("\n  [按 Enter 继续 → 阶段5：视觉生成]")

    # 阶段5：视觉生成
    if start_stage <= 5:
        phase_5_visual_generation(store, concept)
        if not fast:
            input("\n  [按 Enter 继续 → 阶段6：PPT Pitch]")

    # 阶段6：PPT
    if start_stage <= 6:
        phase_6_ppt_pitch(store, concept)

    # 总结
    print("\n" + "=" * 56)
    print("  🏁 追风者演示完成！")
    print("=" * 56)
    print(f"""
  ⏱ 总耗时：约 8 分钟（实际演示含讲解）

  📦 产出物：
     ✅ 门店情报卡片
     ✅ 热点机会报告（5个可追方向）
     ✅ 策划概念匹配（3选1）
     ✅ SMART 策划案（3/3/3内容+活动+投放）
     ✅ AI 视觉物料 ×3
     ✅ 投融资 PPT ×15页

  💰 总成本：
     策划案：¥0（AI生成）
     视觉物料：¥0.15（Lovart API ×3）
     PPT：¥5（Ppt Deck Master）
     ————————————————
     合计：¥5.15

  🎯 核心价值：
     传统营销公司：3-7天 | ¥5000-20000
     追风者：10分钟 | ¥5.15
     ————————————————
     效率提升：400倍 | 成本降低：1000倍
  """)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="追风者 演示脚本")
    parser.add_argument("--fast", action="store_true", help="快速模式（跳过等待）")
    parser.add_argument("--stage", type=int, default=0, help="起始阶段 (0-6)")
    parser.add_argument("--store", type=str, default=STORE_NAME, help="门店名称")
    args = parser.parse_args()

    demo(fast=args.fast, start_stage=args.stage)
