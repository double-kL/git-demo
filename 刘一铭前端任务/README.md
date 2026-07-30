# DiffProtect Pro - 前端项目

这是 DiffProtect Pro 人脸隐私保护平台的前端实现，基于 Vue 3 开发。

## 📁 项目结构

```
刘一铭前端任务/
├── index.html          # 主HTML文件（单页应用）
├── styles.css          # 样式文件
├── app.js              # Vue应用逻辑
├── API_DOCS.md         # API接口文档
└── README.md           # 本文件
```

## ✨ 功能特性

### 公开页面（无需登录）
- **首页** - 产品介绍和功能展示
- **人脸验证演示** - 核心功能，支持4个FR模型验证
- **登录/注册** - 用户认证

### 需登录页面
- **社交平台动态流** - 浏览和发布动态帖子
- **发帖页** - 支持图片/视频上传，DiffProtect保护选项
- **设置页** - 配置默认保护参数

## 🚀 快速开始

### 方式一：直接打开（推荐）

1. 确保后端服务已启动在 `http://localhost:8000`
2. 直接用浏览器打开 `index.html` 文件即可使用

**注意：** 如果遇到 CORS 跨域问题，请使用以下方式：

### 方式二：使用本地服务器

```bash
# 使用 Python 启动简单HTTP服务器
python -m http.server 8080

# 或使用 Node.js http-server
npx http-server -p 8080
```

然后访问 `http://localhost:8080`

### 方式三：配置后端CORS

在后端 FastAPI 中添加 CORS 中间件：

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境可用 *，生产环境指定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🔧 配置

### 修改API地址

如果后端地址不是 `http://localhost:8000`，请在 `app.js` 中修改：

```javascript
data() {
    return {
        apiBaseUrl: 'http://your-backend-address:port',
        // ...
    }
}
```

## 📱 页面说明

### 1. 首页 (/)
- 产品介绍
- 功能特性展示
- 快速导航

### 2. 人脸验证演示 (/verify) ⭐答辩核心
- 上传两张照片进行对比
- 支持选择4个FR模型（IR-152, IR-SE-50, FaceNet, MobileFace）
- 显示每个模型的相似度和判定结果
- 综合结论展示

**使用步骤：**
1. 点击"人脸验证"菜单
2. 上传照片A和照片B
3. 选择要使用的验证模型（默认全选）
4. 点击"开始验证"
5. 查看各模型结果和综合结论

### 3. 登录 (/login)
- 手机号 + 密码登录
- 自动保存登录状态（LocalStorage）

**测试账号：**
- 手机号：13800138000
- 密码：123456
（需要先注册）

### 4. 注册 (/register)
- 手机号（11位）
- 昵称（2-20字符）
- 密码（6-50字符）

### 5. 动态流 (/feed) 🔒需登录
- 浏览所有用户发布的动态
- 查看保护状态标识
- 点赞功能
- 评论（Demo版提示）
- 分页加载

### 6. 发布动态 (/newpost) 🔒需登录
- 文字内容（可选）
- 上传图片（最多9张）
- 上传视频（动态照片）
- **DiffProtect 保护选项：**
  - 是否启用保护
  - 保护强度（1-3级）
  - 选择性保护（指定人脸索引）

### 7. 设置 (/settings) 🔒需登录
- 配置默认保护强度
- 设置默认选择性保护
- 保存用户偏好

## 🎨 UI特性

- **响应式设计** - 支持桌面和移动端
- **现代化界面** - 使用渐变色、阴影、圆角
- **动画效果** - 页面切换、Toast提示
- **直观交互** - 清晰的视觉反馈

## 🔑 核心功能实现

### 人脸验证流程
```javascript
1. 用户上传两张图片
2. 前端FormData封装
3. 调用 POST /api/verify
4. 接收多模型验证结果
5. 可视化展示相似度和判定
```

### 认证流程
```javascript
1. 登录/注册成功后获取token
2. 保存到localStorage
3. 后续请求携带 Authorization: Bearer <token>
4. 页面刷新时自动恢复登录状态
```

### 社交功能
```javascript
1. 获取动态列表（分页）
2. 点赞（toggle行为）
3. 发布动态（支持保护选项）
4. 图片/视频预览
```

## 📦 打包部署

### 单文件打包

如需打包成单个HTML文件（内联CSS和JS），可使用以下脚本：

**Windows:**
```bash
# 运行打包脚本（见下方）
node build.js
```

**或手动内联：**
将 `styles.css` 和 `app.js` 的内容分别复制到 `index.html` 的 `<style>` 和 `<script>` 标签中。

### 生产部署

1. **静态托管：** 直接上传 HTML/CSS/JS 到任意静态服务器
2. **CDN：** Vue 3 使用CDN加载，无需打包工具
3. **配置：** 修改 `apiBaseUrl` 为生产环境地址

## 🐛 故障排查

### 1. 网络错误
- 检查后端是否启动
- 检查 `apiBaseUrl` 配置是否正确
- 检查浏览器控制台CORS错误

### 2. 登录失败
- 确认后端数据库已初始化
- 检查手机号格式（11位）
- 查看后端日志

### 3. 图片上传失败
- 检查文件大小限制
- 确认后端 `/static/uploads` 目录权限
- 查看网络请求状态码

### 4. 人脸验证无结果
- 确认上传的图片包含清晰人脸
- 检查后端模型是否加载成功
- 查看 `/api/health` 检查GPU状态

## 🔐 安全注意事项

1. **生产环境：**
   - 使用HTTPS
   - 配置正确的CORS白名单
   - Token设置合理过期时间

2. **敏感信息：**
   - 不要在前端存储敏感数据
   - LocalStorage仅存储token和基本用户信息

## 📝 开发说明

### 技术栈
- **Vue 3** (CDN) - 渐进式框架
- **原生 Fetch API** - HTTP请求
- **LocalStorage** - 本地状态持久化
- **纯CSS** - 无UI框架依赖

### 代码结构
- **index.html** - 所有页面模板（单页应用）
- **styles.css** - 全局样式和组件样式
- **app.js** - Vue应用，包含所有逻辑

### 扩展功能

如需添加新页面：
1. 在 `index.html` 中添加 `<div v-if="currentPage === 'newpage'">` 块
2. 在 `app.js` 的 `data()` 中添加相关状态
3. 在 `methods` 中添加对应方法
4. 在 `styles.css` 中添加样式

## 📄 许可

本项目用于学术答辩演示。

## 👥 联系方式

如有问题，请查看 `API_DOCS.md` 或联系开发团队。