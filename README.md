# AI Workflow System (Phase 1)

拖拽式 AI 工作流系统（Flowise/n8n 类），当前实现 Phase 1：后端节点系统。

## 功能范围（Phase 1）
- 节点基类 + 6 类节点实现
- 节点注册中心
- 可选真实 API 集成（OpenAI/Tavily/Pinecone），未配置时提供可运行的 fallback

## 目录结构
```
ai-workflow-system/
├── frontend/   # Next.js 16 (App Router) 占位项目
└── backend/    # FastAPI + 节点系统
```

## 快速开始

### 后端
```
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### 前端
```
cd frontend
npm install
npm run dev
```

## 环境变量
参考 `.env.example`。

## 面试要点
1. 节点系统扩展性（BaseNode + Registry）
2. 节点间数据流（input_key/output_key 约定）
3. 安全执行（Code 节点 AST 限制）
