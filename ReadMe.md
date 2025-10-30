# LINGUAECHO - 产品需求文档 (PRD)

## 1. 项目概述

### 1.1 项目目标
开发一个AI驱动的语言学习对话练习平台,帮助用户通过实际对话场景练习目标语言,并获得详细的反馈报告。

### 1.2 核心价值
- **实战练习**: 提供真实场景对话练习
- **智能反馈**: AI分析语言使用问题并给出建议
- **零门槛**: 无需注册,打开即用

### 1.3 目标用户
语言学习者(初级到中级),希望提升口语/书面表达能力

---

## 2. 功能需求

### 2.1 Phase 1: MVP核心功能 (当前阶段)

#### 2.1.1 语言选择
- 支持语言: 日语、英语
- 用户界面: 首页展示两个语言卡片供选择

#### 2.1.2 场景选择
**10个预设场景** (涵盖日常+专业场景):

**日常生活类:**
1. 🍜 **餐厅点餐** - 在餐厅与服务员交流,点餐、询问菜单
2. 🏨 **酒店入住** - 办理入住手续,询问房间设施
3. 🛒 **超市购物** - 寻找商品,询问价格和促销
4. 🚇 **问路交通** - 询问方向,购买车票

**社交场景类:**
5. 👋 **自我介绍** - 第一次见面,介绍自己的背景和兴趣
6. ☕ **日常闲聊** - 与朋友聊天气、周末计划等轻松话题
7. 📞 **电话预约** - 电话预约医生、理发等服务

**职场/学术类:**
8. 💼 **工作面试** - 回答面试官问题,展示自己的能力
9. 📧 **商务邮件** - 讨论如何撰写正式商务邮件
10. 🎓 **课堂讨论** - 在学术环境中表达观点和提问

#### 2.1.3 对话功能
**交互流程:**
1. 用户输入消息(文本框)
2. AI回复(模拟场景中的对话伙伴)
3. 支持多轮连续对话(建议10-15轮)
4. 用户可随时点击"结束对话"按钮

**对话界面要素:**
- 消息气泡(区分用户/AI)
- 时间戳
- 发送按钮
- "结束对话"按钮(显眼位置)
- 轮次计数器(可选,显示当前第几轮)

**AI角色定位:**
- AI扮演场景中的对应角色(服务员、朋友、面试官等)
- 根据用户回复自然推进对话
- 不在对话中纠错(保持流畅性)

#### 2.1.4 对话报告生成
**触发时机:** 用户点击"结束对话"后

**报告内容模块:**

1. **对话概览**
   - 语言: [日语/英语]
   - 场景: [具体场景]
   - 对话轮数: X轮
   - 总字数: X字

2. **语法错误分析**
   - 列出具体错误句子
   - 指出错误类型(时态、助词、语序等)
   - 提供正确版本

3. **词汇问题**
   - 不当用词
   - 建议使用的更自然/准确的词汇

4. **表达自然度**
   - 指出不自然的表达方式
   - 提供母语者常用的说法

5. **正面反馈与建议**
   - 表扬做得好的地方(用词准确、语法正确的句子)
   - 鼓励性评语
   - 下次练习的改进方向

**报告格式:** 网页展示,支持打印/复制

#### 2.1.5 本地存储
- 使用浏览器 `localStorage`
- 存储内容:
  - 对话历史(最近10次)
  - 每次对话的完整报告
- 历史记录入口: 首页"查看历史"按钮
- 记录列表显示: 日期、语言、场景

---

### 2.2 Phase 2: 数据库版本 (后续扩展)

#### 2.2.1 后端数据持久化
- 数据库: **PostgreSQL** (推荐,支持免费托管)
- 存储内容同Phase 1,但迁移到服务器
- 生成分享链接功能(方便展示给面试官)

#### 2.2.2 简单统计
- 总练习次数
- 各语言练习次数
- 进步趋势可视化(可选)

---

## 3. 技术架构

### 3.1 技术栈

#### 前端
- **框架**: Vue 3 (Composition API)
- **UI库**: Element Plus / Naive UI (推荐Naive UI,更现代)
- **状态管理**: Pinia (轻量,适合中小项目)
- **路由**: Vue Router
- **HTTP客户端**: Axios
- **样式**: Tailwind CSS (可选,快速美化)

#### 后端
- **语言**: Python 3.10+
- **框架**: FastAPI (异步,性能好,自动生成API文档)
- **AI框架**: LangChain
- **LLM API**: **推荐方案:**
  1. **主力**: OpenRouter (聚合多个免费模型,有API rate limit保护)
     - 免费模型: Google Gemini 2.0 Flash (免费且强大)
     - Meta Llama 3.1 8B (开源免费)
  2. **备选**: Groq (超快推理速度,有免费额度)
     - Llama 3.1 系列免费

- **数据库** (Phase 2): PostgreSQL + SQLAlchemy ORM
- **环境管理**: Poetry / pip + venv

#### 部署
**Phase 1 (MVP):**
- **前端**: Vercel / Netlify (免费,自动HTTPS)
- **后端**: Railway / Render 免费层 (每月免费额度)
  - Railway: 500小时/月免费
  - Render: 750小时/月免费
- **成本控制**:
  - 设置API调用频率限制(FastAPI中间件)
  - 设置每IP每日请求上限
  - LLM API选择有免费额度的服务

**Phase 2:**
- 数据库: Railway内置PostgreSQL / Supabase免费层

---

### 3.2 系统架构图

```
[用户浏览器]
    ↓
[Vue前端 - Vercel]
    ↓ HTTPS API调用
[FastAPI后端 - Railway]
    ↓
    ├─→ [LangChain] → [OpenRouter API] → [Gemini/Llama]
    └─→ [localStorage] (Phase 1)
         [PostgreSQL] (Phase 2)
```

---

### 3.3 API设计

#### 3.3.1 对话相关

**POST /api/chat**
```json
// Request
{
  "session_id": "uuid",
  "language": "japanese",
  "scenario": "restaurant",
  "message": "すみません、メニューをください",
  "history": [
    {"role": "assistant", "content": "..."},
    {"role": "user", "content": "..."}
  ]
}

// Response
{
  "reply": "かしこまりました。こちらがメニューでございます。お決まりになりましたらお呼びください。",
  "session_id": "uuid"
}
```

**POST /api/report/generate**
```json
// Request
{
  "session_id": "uuid",
  "language": "japanese",
  "scenario": "restaurant",
  "conversation": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}

// Response
{
  "report": {
    "overview": {...},
    "grammar_errors": [...],
    "vocabulary_issues": [...],
    "naturalness": [...],
    "positive_feedback": [...]
  }
}
```

#### 3.3.2 历史记录 (Phase 2)

**GET /api/history**
```json
// Response
{
  "conversations": [
    {
      "id": "uuid",
      "date": "2025-10-30T10:30:00Z",
      "language": "japanese",
      "scenario": "restaurant",
      "turn_count": 12
    }
  ]
}
```

**GET /api/history/{id}**
```json
// Response
{
  "conversation": [...],
  "report": {...}
}
```

---

## 4. LangChain实现方案

### 4.1 对话Agent设计

```python
# 伪代码示例
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage

# 对话Prompt模板
conversation_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a {role} in a {scenario} scenario.
    The user is practicing {language}.
    Have a natural conversation in {language}.
    Do NOT correct their mistakes during conversation.
    Keep responses concise (2-3 sentences).
    Guide the conversation naturally within the scenario.
    """),
    ("placeholder", "{history}"),
    ("human", "{input}")
])

# 报告生成Prompt
report_prompt = """
Analyze the following conversation where a user practiced {language}.
Provide detailed feedback in the following format:

1. Grammar Errors: [list specific mistakes with corrections]
2. Vocabulary Issues: [unnatural word choices with better alternatives]
3. Naturalness: [awkward expressions with native alternatives]
4. Positive Feedback: [praise 2-3 things they did well, give encouragement]

Conversation:
{conversation}
"""
```

### 4.2 Prompt策略
- **对话阶段**: System prompt定义AI角色和场景规则
- **报告阶段**: 单独的分析prompt,明确输出结构
- **语言特定**: 为日语和英语准备不同的分析维度(如日语关注助词、敬语)

---

## 5. 开发计划

### Sprint 1: 项目搭建 
1. 初始化前端Vue项目
2. 初始化后端FastAPI项目
3. 配置CORS,连接前后端
4. 测试基础API调用

### Sprint 2: 对话功能 
1. 实现场景选择页面
2. 实现对话界面UI
3. 后端集成LangChain + OpenRouter
4. 实现对话API端点
5. 前后端对话流程联调

### Sprint 3: 报告生成 
1. 设计报告页面UI
2. 实现报告生成API
3. 前端展示报告
4. 优化报告prompt

### Sprint 4: 本地存储 
1. 前端实现localStorage逻辑
2. 历史记录列表页面
3. 查看历史对话和报告

### Sprint 5: 部署与优化 
1. 部署前端到Vercel
2. 部署后端到Railway
3. 配置环境变量和API密钥
4. 添加rate limiting
5. 性能优化和测试

**总预估时间: 7-9天**

---

## 6. 成本控制与安全

### 6.1 防止API滥用
```python
# FastAPI中间件示例
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/chat")
@limiter.limit("20/hour")  # 每IP每小时20次
async def chat_endpoint():
    ...
```

### 6.2 API密钥保护
- 后端环境变量存储API key
- 前端不暴露任何密钥
- Railway/Render支持环境变量配置

### 6.3 免费额度监控
- OpenRouter提供使用仪表板
- 设置每日预算上限($0)
- 使用完全免费的模型(Gemini 2.0 Flash)

---

## 7. 面试展示要点

### 7.1 技术亮点
- ✅ **全栈能力**: Vue前端 + Python后端独立开发
- ✅ **AI集成**: LangChain + LLM API实际应用
- ✅ **现代技术栈**: FastAPI异步框架,Vue 3 Composition API
- ✅ **工程化**: 合理的架构设计,API RESTful规范
- ✅ **部署经验**: 云端部署,环境配置

### 7.2 可演示功能
1. 实时对话流畅性
2. 报告质量(展示真实的错误分析)
3. 历史记录功能
4. 响应式设计(手机端适配)

---

## 8. 未来扩展方向 (Phase 3+)

### 8.1 功能扩展
- [ ] 用户账户系统
- [ ] 自定义场景
- [ ] 难度级别选择(初级/中级/高级)
- [ ] 语音识别输入(Web Speech API)
- [ ] 语音合成输出(TTS)
- [ ] 每日一练推送
- [ ] 学习进度可视化

### 8.2 AI能力增强
- [ ] 根据用户水平动态调整AI对话难度
- [ ] 多模态支持(图片场景描述)
- [ ] 实时语法建议(对话中subtle提示)

---

## 9. 参考资源

### 9.1 文档
- FastAPI: https://fastapi.tiangolo.com
- LangChain: https://python.langchain.com
- Vue 3: https://vuejs.org
- OpenRouter: https://openrouter.ai/docs

### 9.2 部署平台
- Vercel: https://vercel.com
- Railway: https://railway.app
- Render: https://render.com

---