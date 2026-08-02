// 配置文件示例
// 复制此文件为 config.js 并根据实际情况修改

const CONFIG = {
    // 后端API地址
    // 开发环境
    API_BASE_URL_DEV: 'http://localhost:8000',

    // 生产环境（部署时修改）
    API_BASE_URL_PROD: 'https://your-domain.com',

    // 当前环境（'dev' 或 'prod'）
    ENV: 'dev',

    // 分页配置
    DEFAULT_PAGE_SIZE: 10,
    MAX_PAGE_SIZE: 20,

    // 上传限制
    MAX_IMAGES: 9,
    MAX_FACES: 5,

    // FR模型配置
    FR_MODELS: {
        ir152: {
            id: 'ir152',
            name: 'IR-152',
            description: 'ResNet-152 骨干，ArcFace 训练',
            threshold: 0.55
        },
        irse50: {
            id: 'irse50',
            name: 'IR-SE-50',
            description: 'ResNet-50 + SE 注意力',
            threshold: 0.55
        },
        facenet: {
            id: 'facenet',
            name: 'FaceNet',
            description: 'Google 出品，Triplet Loss',
            threshold: 0.50
        },
        mobile_face: {
            id: 'mobile_face',
            name: 'MobileFace',
            description: '轻量移动端模型',
            threshold: 0.55
        }
    },

    // 保护强度配置
    PROTECT_LEVELS: {
        1: {
            level: 1,
            name: '轻度保护',
            description: '视觉变化最小，适合日常分享',
            eps: 0.01,
            iterations: 30
        },
        2: {
            level: 2,
            name: '中度保护',
            description: '平衡效果与视觉，推荐使用',
            eps: 0.02,
            iterations: 50
        },
        3: {
            level: 3,
            name: '重度保护',
            description: 'FR最难识别，高度敏感场景',
            eps: 0.04,
            iterations: 80
        }
    },

    // Toast提示持续时间（毫秒）
    TOAST_DURATION: 3000,

    // Token过期提示
    TOKEN_EXPIRED_MESSAGE: '登录已过期，请重新登录',

    // 文件类型限制
    ALLOWED_IMAGE_TYPES: ['image/jpeg', 'image/png', 'image/jpg', 'image/webp'],
    ALLOWED_VIDEO_TYPES: ['video/mp4', 'video/webm', 'video/mov'],

    // 文件大小限制（字节）
    MAX_IMAGE_SIZE: 10 * 1024 * 1024, // 10MB
    MAX_VIDEO_SIZE: 100 * 1024 * 1024, // 100MB
};

// 获取当前API地址
CONFIG.getApiBaseUrl = function() {
    return this.ENV === 'prod' ? this.API_BASE_URL_PROD : this.API_BASE_URL_DEV;
};

// 导出配置（如果使用模块化）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}

// 使用方法：
// 1. 在 index.html 的 <head> 中引入：
//    <script src="config.js"></script>
//
// 2. 在 app.js 中使用：
//    apiBaseUrl: CONFIG.getApiBaseUrl(),
//    maxImages: CONFIG.MAX_IMAGES,
//    等等...
