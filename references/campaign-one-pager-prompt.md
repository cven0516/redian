# Campaign One-Pager 生图 Prompt

> 将本文件全文 + 阶段4策划案MD全文，一起喂给 AI 生图模型，生成方案全景图。

## 使用方式

**!!! 关键是「一字不删地全文传入」!!!**

在阶段6调用时：
1. 读取本文件，不做任何删减
2. 读取阶段4生成的策划案 MD 全文
3. 将两段内容拼接，作为生图 prompt 直接传入
4. 生成结果即为一张一目了然的方案全景图

---

## 固定 Prompt 部分（以下为不可修改的固定部分）

Create a premium desktop widescreen campaign dashboard UI mockup that looks like a high-end creative agency strategy board.

The interface should feel like a visually stunning one-screen operational overview for a brand campaign, event launch, marketing activation, or creative strategy proposal.

STYLE DIRECTION:

- modern editorial UI
- creative studio aesthetic
- awwwards-level composition
- floating glassmorphism panels
- asymmetric modular layout
- sophisticated visual hierarchy
- clean but emotionally engaging
- artistic yet highly professional
- minimal but information-dense
- premium brand presentation
- strategic overview feeling
- soft layered shadows
- floating interface over background image
- elegant typography
- cinematic but not cyberpunk
- NOT a corporate dashboard
- NOT a SaaS admin panel
- NOT a rigid grid system
- NOT dark hacker aesthetics
- NOT gaming UI

LAYOUT:

The entire interface must fit inside ONE desktop screen.

The composition should feel dynamic and flowing instead of boxed and rigid.

Modules should vary in size and placement:

- some large hero panels
- some compact floating widgets
- overlapping visual rhythm
- intentional spacing and breathing room
- magazine-like composition without becoming chaotic

The user should immediately understand the entire campaign structure at a glance.

BACKGROUND:

Use a soft neutral light-toned background by default:

- warm white
- cream
- soft beige
- subtle textured atmosphere

The background should be replaceable with other artistic images later.

All UI elements must appear floating above the background instead of attached to it.

VISUAL LANGUAGE:

Use:

- translucent cards
- soft borders
- subtle shadows
- layered depth
- elegant spacing
- premium typography
- refined color accents

Optional:

- small artistic photos
- abstract textures
- collage-style image fragments
- editorial visual snippets

But avoid heavy illustration overload.

INFORMATION ARCHITECTURE:

Organize the content into visually distinct modules such as:

- campaign overview
- SMART goals
- product system
- content matrix
- budget overview
- execution timeline
- launch strategy
- checklist
- contingency/risk plan
- KPI blocks
- tactical highlights

Do NOT present information as boring tables.

Transform information into:

- strategic cards
- visual data clusters
- timeline flows
- operational widgets
- editorial sections

MOOD:

The final result should make viewers feel:

- "this campaign is extremely well-prepared"
- "this team is highly creative and organized"
- "this is exciting and professionally executed"
- "everything is under control"
- "I want my own project to look like this"

The design should inspire motivation and creative confidence.

Use Chinese typography and real Chinese content layout when applicable.

---

## 可变内容部分

将阶段4策划案 MD 全文（内容×活动×投放三位一体的完整方案）紧接在上述固定 prompt 之后一并传入。

策划案 MD 中通常包含：
- 活动概览 & SMART 校验
- 内容矩阵（小红书/抖音/朋友圈 3/3/3）
- 活动机制 & 用户参与路径
- 投放策略 & 预算
- 执行 Timeline
- 风险预案

> 用户没有明确任务地召唤此 skill 时，我会简短介绍整个流程可以做什么，用户可灵活选用任意阶段。
