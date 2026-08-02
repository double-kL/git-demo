const express = require('express');
const cors = require('cors');
const multer = require('multer');
const bodyParser = require('body-parser');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 8000;

// 中间件
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use('/static', express.static('uploads'));

// 文件上传配置
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        const dir = './uploads';
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir);
        }
        cb(null, dir);
    },
    filename: (req, file, cb) => {
        const uniqueName = Date.now() + '-' + Math.round(Math.random() * 1E9) + path.extname(file.originalname);
        cb(null, uniqueName);
    }
});
const upload = multer({ storage });

// 模拟数据库
let users = [];
let posts = [];
let userSettings = {};
let tokenStore = {}; // 存储token和userId的映射
let currentUserId = 1;
let currentPostId = 1;

// 辅助函数：生成Token
function generateToken(userId) {
    const token = `mock_token_${userId}_${Date.now()}`;
    tokenStore[token] = userId; // 存储token映射
    return token;
}

// 辅助函数：验证Token
function verifyToken(token) {
    if (!token || !token.startsWith('Bearer ')) return null;
    const tokenValue = token.split(' ')[1];
    const userId = tokenStore[tokenValue]; // 从映射中获取userId
    if (!userId) return null;
    return users.find(u => u.id === userId);
}

// 辅助函数：隐藏手机号
function maskPhone(phone) {
    return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2');
}

// ========== 公开接口 ==========

// 健康检查
app.get('/api/health', (req, res) => {
    res.json({
        status: "ok",
        version: "0.5.0",
        device: "cuda",
        gpu: {
            devices: [{ name: "Mock GPU", total_gb: 32.0, free_gb: 18.5 }]
        },
        models_loaded: ["diffae", "fr_models", "bisenet"]
    });
});

// 人脸验证演示
app.post('/api/verify', upload.fields([
    { name: 'image_a', maxCount: 1 },
    { name: 'image_b', maxCount: 1 }
]), (req, res) => {
    const models = req.query.models ? req.query.models.split(',') : ['ir152', 'irse50', 'facenet', 'mobile_face'];

    // 模拟验证结果
    const allResults = {
        ir152: {
            similarity: 0.87,
            threshold: 0.55,
            verdict: "same_person",
            label: "IR-152"
        },
        irse50: {
            similarity: 0.82,
            threshold: 0.55,
            verdict: "same_person",
            label: "IR-SE-50"
        },
        facenet: {
            similarity: 0.43,
            threshold: 0.50,
            verdict: "different_person",
            label: "FaceNet"
        },
        mobile_face: {
            similarity: 0.91,
            threshold: 0.55,
            verdict: "same_person",
            label: "MobileFace"
        }
    };

    const results = {};
    models.forEach(model => {
        if (allResults[model]) {
            results[model] = allResults[model];
        }
    });

    const sameVotes = Object.values(results).filter(r => r.verdict === 'same_person').length;
    const differentVotes = Object.values(results).filter(r => r.verdict === 'different_person').length;

    res.json({
        status: "ok",
        face_detected_a: true,
        face_detected_b: true,
        results,
        summary: {
            total_models: models.length,
            same_votes: sameVotes,
            different_votes: differentVotes,
            consensus: sameVotes >= Math.ceil(models.length * 0.75) ? "same_person" : "different_person",
            consensus_rule: `至少 ${Math.ceil(models.length * 0.75)}/${models.length} 模型认为同人才判定为同人`
        },
        processing_time: (Math.random() * 0.5 + 0.1).toFixed(2)
    });
});

// ========== 认证接口 ==========

// 注册
app.post('/api/auth/register', (req, res) => {
    const { phone, nickname, password } = req.body;

    // 校验
    if (!phone || phone.length !== 11) {
        return res.status(400).json({ detail: "手机号格式错误" });
    }
    if (!nickname || nickname.length < 2 || nickname.length > 20) {
        return res.status(400).json({ detail: "昵称长度应为2-20字符" });
    }
    if (!password || password.length < 6) {
        return res.status(400).json({ detail: "密码至少6个字符" });
    }

    // 检查重复
    if (users.find(u => u.phone === phone)) {
        return res.status(400).json({ detail: "手机号已注册" });
    }
    if (users.find(u => u.nickname === nickname)) {
        return res.status(400).json({ detail: "昵称已被使用" });
    }

    // 创建用户
    const userId = `u_${currentUserId++}`;
    const user = {
        id: userId,
        phone,
        nickname,
        password,
        created_at: new Date().toISOString()
    };
    users.push(user);

    // 初始化设置
    userSettings[userId] = {
        protect_level: 2,
        selective_protection: false,
        selected_faces: []
    };

    const token = generateToken(userId);

    res.json({
        status: "ok",
        message: "注册成功",
        user: {
            id: userId,
            nickname,
            phone: maskPhone(phone)
        },
        token
    });
});

// 登录
app.post('/api/auth/login', (req, res) => {
    const { phone, password } = req.body;

    const user = users.find(u => u.phone === phone && u.password === password);
    if (!user) {
        return res.status(400).json({ detail: "手机号或密码错误" });
    }

    const token = generateToken(user.id);

    res.json({
        status: "ok",
        message: "登录成功",
        user: {
            id: user.id,
            nickname: user.nickname,
            phone: maskPhone(user.phone)
        },
        token
    });
});

// 获取当前用户
app.get('/api/auth/me', (req, res) => {
    const user = verifyToken(req.headers.authorization);
    if (!user) {
        return res.status(401).json({ detail: "未登录或 token 过期" });
    }

    res.json({
        status: "ok",
        user: {
            id: user.id,
            nickname: user.nickname,
            phone: maskPhone(user.phone),
            created_at: user.created_at
        }
    });
});

// ========== 社交平台接口（需登录）==========

// 获取帖子列表
app.get('/api/posts', (req, res) => {
    const user = verifyToken(req.headers.authorization);
    if (!user) {
        return res.status(401).json({ detail: "未登录或 token 过期" });
    }

    const page = parseInt(req.query.page) || 1;
    const page_size = Math.min(parseInt(req.query.page_size) || 10, 20);

    const start = (page - 1) * page_size;
    const end = start + page_size;
    const paginatedPosts = posts.slice(start, end);

    res.json({
        status: "ok",
        page,
        page_size,
        total: posts.length,
        has_next: end < posts.length,
        posts: paginatedPosts.map(post => ({
            ...post,
            liked_by_me: post.likes.includes(user.id)
        }))
    });
});

// 点赞
app.post('/api/posts/:postId/like', (req, res) => {
    const user = verifyToken(req.headers.authorization);
    if (!user) {
        return res.status(401).json({ detail: "未登录或 token 过期" });
    }

    const post = posts.find(p => p.id === req.params.postId);
    if (!post) {
        return res.status(404).json({ detail: "帖子不存在" });
    }

    const likeIndex = post.likes.indexOf(user.id);
    let liked;

    if (likeIndex > -1) {
        // 取消点赞
        post.likes.splice(likeIndex, 1);
        liked = false;
    } else {
        // 点赞
        post.likes.push(user.id);
        liked = true;
    }

    post.likes_count = post.likes.length;

    res.json({
        status: "ok",
        liked,
        likes_count: post.likes_count
    });
});

// 发帖
app.post('/api/posts', upload.fields([
    { name: 'images', maxCount: 9 },
    { name: 'live_videos', maxCount: 9 },
    { name: 'video', maxCount: 1 }
]), (req, res) => {
    const user = verifyToken(req.headers.authorization);
    if (!user) {
        return res.status(401).json({ detail: "未登录或 token 过期" });
    }

    const postId = `p_${currentPostId++}`;
    const images = req.files.images ? req.files.images.map(f =>
        `http://localhost:${PORT}/static/${f.filename}`
    ) : [];
    const video = req.files.video ? `http://localhost:${PORT}/static/${req.files.video[0].filename}` : null;

    // 处理动态照片的视频
    const liveVideos = {};
    if (req.files.live_videos && req.body.live_photo_indices) {
        const indices = JSON.parse(req.body.live_photo_indices);
        req.files.live_videos.forEach((videoFile, idx) => {
            const imageIndex = indices[idx];
            liveVideos[imageIndex] = `http://localhost:${PORT}/static/${videoFile.filename}`;
        });
    }

    const post = {
        id: postId,
        author: {
            id: user.id,
            nickname: user.nickname,
            avatar: null
        },
        content: req.body.content || '',
        images,
        live_videos: liveVideos, // 动态照片的视频映射
        video,
        is_protected: req.body.is_protected === 'true',
        protect_level: parseInt(req.body.protect_level) || 0,
        likes: [],
        likes_count: 0,
        comments_count: 0,
        created_at: new Date().toISOString()
    };

    posts.unshift(post); // 最新的在前面

    res.json({
        status: "ok",
        post: {
            id: postId,
            content: post.content,
            images: post.images,
            live_videos: post.live_videos,
            video: post.video,
            is_protected: post.is_protected,
            protect_level: post.protect_level,
            created_at: post.created_at
        }
    });
});

// 发表评论
app.post('/api/posts/:postId/comments', (req, res) => {
    const user = verifyToken(req.headers.authorization);
    if (!user) {
        return res.status(401).json({ detail: "未登录或 token 过期" });
    }

    const post = posts.find(p => p.id === req.params.postId);
    if (!post) {
        return res.status(404).json({ detail: "帖子不存在" });
    }

    const { content } = req.body;
    if (!content || !content.trim()) {
        return res.status(400).json({ detail: "评论内容不能为空" });
    }

    // 初始化评论数组
    if (!post.comments) {
        post.comments = [];
    }

    const commentId = `c_${Date.now()}`;
    const comment = {
        id: commentId,
        author: {
            id: user.id,
            nickname: user.nickname,
            avatar: null
        },
        content: content.trim(),
        created_at: new Date().toISOString()
    };

    post.comments.push(comment);
    post.comments_count = post.comments.length;

    res.json({
        status: "ok",
        comment
    });
});

// 获取帖子评论
app.get('/api/posts/:postId/comments', (req, res) => {
    const user = verifyToken(req.headers.authorization);
    if (!user) {
        return res.status(401).json({ detail: "未登录或 token 过期" });
    }

    const post = posts.find(p => p.id === req.params.postId);
    if (!post) {
        return res.status(404).json({ detail: "帖子不存在" });
    }

    res.json({
        status: "ok",
        comments: post.comments || []
    });
});

// ========== 用户设置接口（需登录）==========

// 获取设置
app.get('/api/settings', (req, res) => {
    const user = verifyToken(req.headers.authorization);
    if (!user) {
        return res.status(401).json({ detail: "未登录或 token 过期" });
    }

    const settings = userSettings[user.id] || {
        protect_level: 2,
        selective_protection: false,
        selected_faces: []
    };

    res.json({
        status: "ok",
        settings
    });
});

// 更新设置
app.put('/api/settings', (req, res) => {
    const user = verifyToken(req.headers.authorization);
    if (!user) {
        return res.status(401).json({ detail: "未登录或 token 过期" });
    }

    const { protect_level, selective_protection, selected_faces } = req.body;

    userSettings[user.id] = {
        protect_level: protect_level || 2,
        selective_protection: selective_protection || false,
        selected_faces: selected_faces || []
    };

    res.json({
        status: "ok",
        message: "设置已保存"
    });
});

// ========== 启动服务器 ==========

// 初始化一些测试数据
function initTestData() {
    // 创建测试用户
    users.push({
        id: 'u_test1',
        phone: '13800138000',
        nickname: '测试用户',
        password: '123456',
        created_at: new Date().toISOString()
    });

    // 创建测试帖子
    posts.push({
        id: 'p_test1',
        author: {
            id: 'u_test1',
            nickname: '测试用户',
            avatar: null
        },
        content: '这是一条测试动态 - 已启用DiffProtect保护 🛡️',
        images: ['https://via.placeholder.com/400x400/6b7280/ffffff?text=Protected+Image'],
        video: null,
        is_protected: true,
        protect_level: 2,
        likes: [],
        likes_count: 0,
        comments_count: 0,
        created_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString()
    });

    posts.push({
        id: 'p_test2',
        author: {
            id: 'u_test1',
            nickname: '测试用户',
            avatar: null
        },
        content: '这是一条普通动态 - 未启用保护',
        images: [
            'https://via.placeholder.com/400x400/9ca3af/ffffff?text=Normal+Image+1',
            'https://via.placeholder.com/400x400/a8a29e/ffffff?text=Normal+Image+2'
        ],
        video: null,
        is_protected: false,
        protect_level: 0,
        likes: [],
        likes_count: 0,
        comments_count: 0,
        created_at: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString()
    });

    posts.push({
        id: 'p_test3',
        author: {
            id: 'u_test1',
            nickname: '测试用户',
            avatar: null
        },
        content: '这是一条带动态照片的测试动态 📸✨ 点击图片上的"动态"按钮可以播放视频！',
        images: [
            'https://via.placeholder.com/400x400/8b7e74/ffffff?text=Live+Photo+1',
            'https://via.placeholder.com/400x400/7d8471/ffffff?text=Normal+Image'
        ],
        live_videos: {
            0: 'https://www.w3schools.com/html/mov_bbb.mp4' // 第0张图片有对应的视频
        },
        video: null,
        is_protected: false,
        protect_level: 0,
        likes: [],
        likes_count: 0,
        comments: [
            {
                id: 'c_test1',
                author: {
                    id: 'u_test1',
                    nickname: '测试用户',
                    avatar: null
                },
                content: '这个动态照片功能很棒！👍',
                created_at: new Date(Date.now() - 30 * 60 * 1000).toISOString()
            },
            {
                id: 'c_test2',
                author: {
                    id: 'u_test1',
                    nickname: '测试用户',
                    avatar: null
                },
                content: '和微信朋友圈的体验一样流畅',
                created_at: new Date(Date.now() - 15 * 60 * 1000).toISOString()
            }
        ],
        comments_count: 2,
        created_at: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString()
    });

    userSettings['u_test1'] = {
        protect_level: 2,
        selective_protection: false,
        selected_faces: []
    };

    console.log('✅ 测试数据初始化完成');
    console.log('📝 测试账号: 13800138000 / 123456');
}

app.listen(PORT, () => {
    console.log('🚀 DiffProtect Pro Mock 后端服务器启动成功！');
    console.log('📡 服务地址: http://localhost:' + PORT);
    console.log('');
    console.log('📌 可用接口:');
    console.log('   GET  /api/health           - 健康检查');
    console.log('   POST /api/verify           - 人脸验证');
    console.log('   POST /api/auth/register    - 注册');
    console.log('   POST /api/auth/login       - 登录');
    console.log('   GET  /api/auth/me          - 获取当前用户');
    console.log('   GET  /api/posts            - 获取动态列表');
    console.log('   POST /api/posts            - 发布动态');
    console.log('   POST /api/posts/:id/like   - 点赞');
    console.log('   GET  /api/settings         - 获取设置');
    console.log('   PUT  /api/settings         - 更新设置');
    console.log('');

    initTestData();

    console.log('');
    console.log('💡 提示: 按 Ctrl+C 停止服务器');
});
