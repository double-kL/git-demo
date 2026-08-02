// Mock数据 - 用于前端开发和演示
// 当后端未启动时，可以使用此文件的数据进行界面测试

const MOCK_DATA = {
    // 健康检查
    health: {
        status: "ok",
        version: "0.5.0",
        device: "cuda",
        gpu: {
            devices: [{ name: "Tesla V100", total_gb: 32.0, free_gb: 18.5 }]
        },
        models_loaded: ["diffae", "fr_models", "bisenet"]
    },

    // 登录响应
    loginSuccess: {
        status: "ok",
        message: "登录成功",
        user: {
            id: "u_demo001",
            nickname: "演示用户",
            phone: "138****8000"
        },
        token: "mock_token_eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    },

    // 注册响应
    registerSuccess: {
        status: "ok",
        message: "注册成功",
        user: {
            id: "u_demo002",
            nickname: "新用户",
            phone: "139****9000"
        },
        token: "mock_token_new_user_xyz123"
    },

    // 人脸验证结果
    verifyResult: {
        status: "ok",
        face_detected_a: true,
        face_detected_b: true,
        results: {
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
        },
        summary: {
            total_models: 4,
            same_votes: 3,
            different_votes: 1,
            consensus: "same_person",
            consensus_rule: "至少 3/4 模型认为同人才判定为同人"
        },
        processing_time: 0.23
    },

    // 动态列表
    posts: {
        status: "ok",
        page: 1,
        page_size: 10,
        total: 5,
        has_next: false,
        posts: [
            {
                id: "p_001",
                author: {
                    id: "u_demo001",
                    nickname: "演示用户",
                    avatar: null
                },
                content: "测试保护效果的第一张照片 🎭",
                images: [
                    "https://via.placeholder.com/400x400/4f46e5/ffffff?text=Protected+Image+1"
                ],
                video: null,
                is_protected: true,
                protect_level: 2,
                likes_count: 15,
                liked_by_me: false,
                comments_count: 3,
                created_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString()
            },
            {
                id: "p_002",
                author: {
                    id: "u_demo002",
                    nickname: "张三",
                    avatar: null
                },
                content: "未保护的普通照片",
                images: [
                    "https://via.placeholder.com/400x400/10b981/ffffff?text=Normal+Image+1",
                    "https://via.placeholder.com/400x400/f59e0b/ffffff?text=Normal+Image+2"
                ],
                video: null,
                is_protected: false,
                protect_level: 0,
                likes_count: 8,
                liked_by_me: true,
                comments_count: 1,
                created_at: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString()
            },
            {
                id: "p_003",
                author: {
                    id: "u_demo003",
                    nickname: "李四",
                    avatar: null
                },
                content: "重度保护测试 Level 3 🛡️",
                images: [
                    "https://via.placeholder.com/400x400/ef4444/ffffff?text=Heavy+Protected",
                    "https://via.placeholder.com/400x400/8b5cf6/ffffff?text=Image+2",
                    "https://via.placeholder.com/400x400/06b6d4/ffffff?text=Image+3"
                ],
                video: null,
                is_protected: true,
                protect_level: 3,
                likes_count: 22,
                liked_by_me: false,
                comments_count: 5,
                created_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString()
            },
            {
                id: "p_004",
                author: {
                    id: "u_demo001",
                    nickname: "演示用户",
                    avatar: null
                },
                content: "动态照片测试 - 视频保护 🎬",
                images: [],
                video: "https://via.placeholder.com/800x450/6366f1/ffffff?text=Protected+Video",
                is_protected: true,
                protect_level: 2,
                likes_count: 30,
                liked_by_me: true,
                comments_count: 7,
                created_at: new Date(Date.now() - 48 * 60 * 60 * 1000).toISOString()
            },
            {
                id: "p_005",
                author: {
                    id: "u_demo004",
                    nickname: "王五",
                    avatar: null
                },
                content: "多图测试 - 选择性保护部分人脸",
                images: [
                    "https://via.placeholder.com/400x400/ec4899/ffffff?text=1",
                    "https://via.placeholder.com/400x400/14b8a6/ffffff?text=2",
                    "https://via.placeholder.com/400x400/f97316/ffffff?text=3",
                    "https://via.placeholder.com/400x400/84cc16/ffffff?text=4"
                ],
                video: null,
                is_protected: true,
                protect_level: 2,
                likes_count: 18,
                liked_by_me: false,
                comments_count: 4,
                created_at: new Date(Date.now() - 72 * 60 * 60 * 1000).toISOString()
            }
        ]
    },

    // 用户设置
    settings: {
        status: "ok",
        settings: {
            protect_level: 2,
            selective_protection: false,
            selected_faces: []
        }
    },

    // 点赞响应
    likeResponse: {
        status: "ok",
        liked: true,
        likes_count: 16
    },

    // 发帖成功响应
    postSuccess: {
        status: "ok",
        post: {
            id: "p_new_001",
            content: "新发布的动态",
            images: ["http://localhost:8000/static/uploads/p_new_001_img_0.png"],
            is_protected: true,
            protect_level: 2,
            created_at: new Date().toISOString()
        }
    },

    // 错误响应示例
    errors: {
        unauthorized: {
            detail: "未登录或 token 过期"
        },
        phoneExists: {
            detail: "手机号已注册"
        },
        wrongPassword: {
            detail: "手机号或密码错误"
        },
        noFace: {
            detail: "未检测到人脸"
        },
        networkError: {
            detail: "网络连接失败"
        }
    }
};

// Mock模式开关
const MOCK_MODE = {
    enabled: false, // 设置为 true 启用 Mock 模式
    delay: 500 // 模拟网络延迟（毫秒）
};

// Mock API 函数
const MockAPI = {
    // 模拟延迟
    async delay() {
        return new Promise(resolve => setTimeout(resolve, MOCK_MODE.delay));
    },

    // 登录
    async login(phone, password) {
        await this.delay();
        if (phone === '13800138000' && password === '123456') {
            return { ok: true, json: async () => MOCK_DATA.loginSuccess };
        }
        return { ok: false, json: async () => MOCK_DATA.errors.wrongPassword };
    },

    // 注册
    async register(data) {
        await this.delay();
        return { ok: true, json: async () => MOCK_DATA.registerSuccess };
    },

    // 人脸验证
    async verify(formData) {
        await this.delay();
        return { ok: true, json: async () => MOCK_DATA.verifyResult };
    },

    // 获取动态
    async getPosts(page = 1) {
        await this.delay();
        return { ok: true, json: async () => MOCK_DATA.posts };
    },

    // 点赞
    async toggleLike(postId) {
        await this.delay();
        return { ok: true, json: async () => MOCK_DATA.likeResponse };
    },

    // 发帖
    async createPost(formData) {
        await this.delay();
        return { ok: true, json: async () => MOCK_DATA.postSuccess };
    },

    // 获取设置
    async getSettings() {
        await this.delay();
        return { ok: true, json: async () => MOCK_DATA.settings };
    },

    // 保存设置
    async saveSettings(data) {
        await this.delay();
        return { ok: true, json: async () => ({ status: "ok" }) };
    }
};

// 使用方法：
// 1. 在 app.js 中，如果检测到后端无法连接，自动切换到 Mock 模式
// 2. 或者手动设置 MOCK_MODE.enabled = true
//
// 示例：
// if (MOCK_MODE.enabled) {
//     response = await MockAPI.login(phone, password);
// } else {
//     response = await fetch(`${apiBaseUrl}/api/auth/login`, ...);
// }

console.log('📦 Mock 数据已加载');
console.log('💡 设置 MOCK_MODE.enabled = true 启用 Mock 模式');
