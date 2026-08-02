# DiffProtect Pro — 前端接口文档 v1.0

> **Base URL**: `http://<host>:8000`
> **Content-Type**: `application/json` (除文件上传用 `multipart/form-data`)

---

## 目录

- [一、公开接口（无需登录）](#一公开接口无需登录)
- [二、认证接口](#二认证接口)
- [三、社交平台接口（需登录）](#三社交平台接口需登录)
- [四、用户设置接口（需登录）](#四用户设置接口需登录)
- [五、人脸处理接口](#五人脸处理接口)
- [六、通用说明](#六通用说明)

---

## 一、公开接口（无需登录）

### 1.1 健康检查

```
GET /api/health
```

**响应:**
```json
{
  "status": "ok",
  "version": "0.5.0",
  "device": "cuda",
  "gpu": {
    "devices": [{ "name": "Tesla V100", "total_gb": 32.0, "free_gb": 18.5 }]
  },
  "models_loaded": ["diffae", "fr_models", "bisenet"]
}
```

### 1.2 人脸验证演示（答辩核心功能）

> 两张照片 → 多个 FR 模型分别判断 → 返回各模型相似度 + 综合结论。
> 用于答辩时现场演示：评委上传两张照片，系统展示保护前后 FR 模型的识别结果差异。

```
POST /api/verify
```

**请求:** `multipart/form-data`

| 参数 | 类型 | 说明 |
|------|------|------|
| `image_a` | file | 第一张人脸图片 |
| `image_b` | file | 第二张人脸图片 |
| `models` | string | 可选，逗号分隔的模型列表。默认全部。可选值见下方 |

**可用模型 (4个):**

| 模型ID | 模型名 | 简介 |
|--------|--------|------|
| `ir152` | IR-152 | ResNet-152 骨干，ArcFace 训练 |
| `irse50` | IR-SE-50 | ResNet-50 + SE 注意力 |
| `facenet` | FaceNet | Google 出品，Triplet Loss |
| `mobile_face` | MobileFace | 轻量移动端模型 |

**响应:**
```json
{
  "status": "ok",
  "face_detected_a": true,
  "face_detected_b": true,
  "results": {
    "ir152": {
      "similarity": 0.87,
      "threshold": 0.55,
      "verdict": "same_person",
      "label": "IR-152"
    },
    "irse50": {
      "similarity": 0.82,
      "threshold": 0.55,
      "verdict": "same_person",
      "label": "IR-SE-50"
    },
    "facenet": {
      "similarity": 0.43,
      "threshold": 0.50,
      "verdict": "different_person",
      "label": "FaceNet"
    },
    "mobile_face": {
      "similarity": 0.91,
      "threshold": 0.55,
      "verdict": "same_person",
      "label": "MobileFace"
    }
  },
  "summary": {
    "total_models": 4,
    "same_votes": 3,
    "different_votes": 1,
    "consensus": "same_person",
    "consensus_rule": "至少 3/4 模型认为同人才判定为同人"
  },
  "processing_time": 0.23
}
```

**verdict 取值:**
| 值 | 含义 |
|----|------|
| `same_person` | 该模型认为两张照片是同一个人 |
| `different_person` | 该模型认为是不同人 |
| `no_face` | 未检测到人脸 |
| `error` | 处理出错 |

**前端切换模型:** 传 `?models=ir152,facenet` 只启用指定模型。前端可做 4 个 toggle 开关。

---

## 二、认证接口

### 2.1 注册

```
POST /api/auth/register
```

**请求:** `application/json`
```json
{
  "phone": "13800138000",
  "nickname": "张三",
  "password": "123456"
}
```

**校验规则:**
| 字段 | 规则 |
|------|------|
| phone | 11 位中国大陆手机号 |
| nickname | 2-20 字符，不可重复 |
| password | 6-50 字符 |

**响应 (成功):**
```json
{
  "status": "ok",
  "message": "注册成功",
  "user": {
    "id": "u_abc123",
    "nickname": "张三",
    "phone": "138****8000"
  },
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**响应 (失败):**
```json
{
  "status": "error",
  "detail": "手机号已注册"
}
```

### 2.2 登录

```
POST /api/auth/login
```

**请求:** `application/json`
```json
{
  "phone": "13800138000",
  "password": "123456"
}
```

**响应 (成功):**
```json
{
  "status": "ok",
  "message": "登录成功",
  "user": {
    "id": "u_abc123",
    "nickname": "张三",
    "phone": "138****8000"
  },
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

### 2.3 获取当前用户

```
GET /api/auth/me
Authorization: Bearer <token>
```

**响应:**
```json
{
  "status": "ok",
  "user": {
    "id": "u_abc123",
    "nickname": "张三",
    "phone": "138****8000",
    "created_at": "2026-07-30T10:00:00"
  }
}
```

---

## 三、社交平台接口（需登录）

> 所有社交接口需携带 Header: `Authorization: Bearer <token>`

### 3.1 获取帖子列表

```
GET /api/posts?page=1&page_size=10
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| page | 1 | 页码 |
| page_size | 10 | 每页数量（最大 20） |

**响应:**
```json
{
  "status": "ok",
  "page": 1,
  "page_size": 10,
  "total": 42,
  "has_next": true,
  "posts": [
    {
      "id": "p_001",
      "author": {
        "id": "u_abc123",
        "nickname": "张三",
        "avatar": null
      },
      "content": "今天的照片",
      "images": [
        "http://<host>:8000/static/uploads/p_001_img_0.png",
        "http://<host>:8000/static/uploads/p_001_img_1.png"
      ],
      "video": null,
      "is_protected": true,
      "protect_level": 2,
      "likes_count": 15,
      "liked_by_me": false,
      "comments_count": 3,
      "created_at": "2026-07-30T12:00:00"
    }
  ]
}
```

**帖子字段说明:**
| 字段 | 类型 | 说明 |
|------|------|------|
| images | array/null | 帖子图片 URL 列表 |
| video | string/null | 帖子视频 URL（动态照片） |
| is_protected | bool | 是否经过 DiffProtect 保护 |
| liked_by_me | bool | 当前用户是否已点赞 |
| likes_count | int | 点赞总数 |

### 3.2 点赞

```
POST /api/posts/{post_id}/like
Authorization: Bearer <token>
```

**请求体:** 无

**响应:**
```json
{
  "status": "ok",
  "liked": true,
  "likes_count": 16
}
```

> 重复请求会取消点赞（toggle 行为）。前端首次点图标高亮 + count++，再点取消高亮 + count--。

### 3.3 评论（Demo 占位）

```
POST /api/posts/{post_id}/comment
Authorization: Bearer <token>
```

**请求:**
```json
{
  "content": "好看！"
}
```

**响应:**
```json
{
  "status": "ok",
  "message": "Demo 版暂不支持评论功能",
  "demo_mode": true
}
```

> 前端点击评论图标直接弹 toast "Demo 版暂不支持评论"，无需真正调接口。这里提供接口仅为后续扩展预留。

### 3.4 发帖

```
POST /api/posts
Authorization: Bearer <token>
```

**请求:** `multipart/form-data`

| 参数 | 类型 | 说明 |
|------|------|------|
| content | string | 文字内容（可选） |
| images | file[] | 图片列表（可选，最多 9 张） |
| video | file | 视频（可选，动态照片） |
| is_protected | bool | 是否启用保护（默认 false） |
| protect_level | int | 保护强度 1-3（is_protected=true 时生效） |
| protect_faces | int[] | 选择性保护的人脸索引（JSON 数组字符串） |

**响应:**
```json
{
  "status": "ok",
  "post": {
    "id": "p_002",
    "content": "今天的照片",
    "images": ["http://<host>:8000/static/uploads/p_002_img_0.png"],
    "is_protected": true,
    "protect_level": 2,
    "created_at": "2026-07-30T12:30:00"
  }
}
```

> **注意:** is_protected=true 时，服务端会对上传的图片/视频执行 DiffProtect + DreamID-V 处理后才返回。处理中的帖子状态为 `processing`，前端可轮询或 WebSocket 等待。

---

## 四、用户设置接口（需登录）

### 4.1 获取设置

```
GET /api/settings
Authorization: Bearer <token>
```

**响应:**
```json
{
  "status": "ok",
  "settings": {
    "protect_level": 2,
    "selective_protection": false,
    "selected_faces": []
  }
}
```

### 4.2 更新设置

```
PUT /api/settings
Authorization: Bearer <token>
```

**请求:**
```json
{
  "protect_level": 3,
  "selective_protection": true,
  "selected_faces": [0, 2]
}
```

| 字段 | 类型 | 范围 | 说明 |
|------|------|------|------|
| protect_level | int | 1-3 | 保护强度：1=轻度 2=中度 3=重度 |
| selective_protection | bool | — | 是否开启选择性保护 |
| selected_faces | int[] | 0-4 | 选择要保护的人脸索引（仅 selective_protection=true 时生效） |

---

## 五、人脸处理接口

> 社交平台内部调用，也支持直接调用。

### 5.1 单图 DiffProtect 保护

```
POST /api/protect
```

**请求:** `multipart/form-data`

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| image | file | 必填 | 人脸图片 |
| level | int | 2 | 保护强度 1-3 |
| lam | float | 0.0 | 语义保持度 0-10 |

**响应:** `image/png`（256×256 保护后图片）

### 5.2 批量源脸保护

```
POST /api/protect-source
```

**请求:** `multipart/form-data`

| 参数 | 类型 | 说明 |
|------|------|------|
| images | file[] | 源脸图片（最多 5 张） |
| level | int | 保护强度 1-3 |
| lam | float | 语义保持度 |

**响应:** `image/png`（第一张，Headers 含 `X-Face-Count`）

### 5.3 视频保护（DiffProtect + DreamID-V）

```
POST /api/protect-video
```

**请求:** `multipart/form-data`

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| source_images | file[] | 必填 | 源脸图片（每人一张，最多5张） |
| video | file | 必填 | 目标视频 MP4 |
| level | int | 2 | 保护强度 1-3 |
| lam | float | 0.0 | 语义保持度 |
| dreamidv_size | string | "832*480" | DreamID 输出分辨率 |
| dreamidv_steps | int | 12 | 采样步数 4-50 |

**响应:** `video/mp4`

---

## 六、通用说明

### 6.1 认证方式

登录/注册成功后返回 `token`。后续请求携带：
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### 6.2 错误响应格式

```json
{
  "detail": "错误描述信息"
}
```

### 6.3 HTTP 状态码

| 状态码 | 含义 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未登录或 token 过期 |
| 404 | 资源不存在 |
| 422 | 业务规则拒绝（如人脸数超限） |
| 500 | 服务端错误 |

### 6.4 保护强度参数速查

| level | eps | 迭代次数 | 效果 |
|-------|-----|---------|------|
| 1 | 0.01 | 30 | 轻度保护，视觉变化最小 |
| 2 | 0.02 | 50 | 中度保护（默认） |
| 3 | 0.04 | 80 | 重度保护，FR 最难识别 |

### 6.5 页面路由建议

```
/                         首页 (公开)
/verify                   人脸验证演示页 (公开) ★ 答辩用
/login                    登录页 (公开)
/register                 注册页 (公开)
/feed                     动态流 (需登录)
/post/new                 发帖 (需登录)
/settings                 设置 (需登录)
```

### 6.6 前端开发 Mock 数据

未部署后端的阶段，认证接口可 mock：

```javascript
// POST /api/auth/login mock
{
  "status": "ok",
  "user": { "id": "u_demo", "nickname": "Demo用户" },
  "token": "mock_token_for_dev"
}

// GET /api/posts mock (初始空)
{ "status": "ok", "page": 1, "total": 0, "posts": [] }
```
