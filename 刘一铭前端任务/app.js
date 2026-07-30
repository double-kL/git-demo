const { createApp } = Vue;

createApp({
    data() {
        return {
            // 基础配置
            apiBaseUrl: 'http://localhost:8000',

            // 用户状态
            isLoggedIn: false,
            user: null,
            token: null,

            // 页面状态
            currentPage: 'home',

            // 登录表单
            loginForm: {
                phone: '',
                password: ''
            },
            loggingIn: false,

            // 注册表单
            registerForm: {
                phone: '',
                nickname: '',
                password: ''
            },
            registering: false,

            // 人脸验证
            verifyImages: {
                imageA: null,
                imageB: null
            },
            verifyFiles: {
                imageA: null,
                imageB: null
            },
            selectedModels: {
                ir152: true,
                irse50: true,
                facenet: true,
                mobile_face: true
            },
            verifying: false,
            verifyResult: null,

            // 动态流
            posts: [],
            loadingPosts: false,
            pagination: {
                page: 1,
                page_size: 10,
                total: 0,
                has_next: false
            },

            // 发帖
            newPost: {
                content: '',
                images: [],
                previewImages: [],
                video: null,
                videoPreview: null,
                is_protected: false,
                protect_level: 2,
                selective_protection: false,
                protect_faces_input: ''
            },
            publishing: false,

            // 设置
            settings: {
                protect_level: 2,
                selective_protection: false,
                selected_faces: [],
                selected_faces_input: ''
            },
            loadingSettings: false,
            savingSettings: false,

            // Toast 提示
            toast: {
                show: false,
                message: '',
                type: 'info'
            }
        };
    },

    computed: {
        canVerify() {
            return this.verifyFiles.imageA && this.verifyFiles.imageB &&
                   Object.values(this.selectedModels).some(v => v);
        },

        canPublish() {
            return this.newPost.content || this.newPost.images.length > 0 || this.newPost.video;
        },

        authHeaders() {
            return this.token ? { 'Authorization': `Bearer ${this.token}` } : {};
        }
    },

    mounted() {
        // 从本地存储恢复登录状态
        const savedToken = localStorage.getItem('token');
        const savedUser = localStorage.getItem('user');

        if (savedToken && savedUser) {
            this.token = savedToken;
            this.user = JSON.parse(savedUser);
            this.isLoggedIn = true;
            this.verifyToken();
        }
    },

    methods: {
        // ========== 工具方法 ==========
        showToast(message, type = 'info') {
            this.toast = { show: true, message, type };
            setTimeout(() => {
                this.toast.show = false;
            }, 3000);
        },

        formatTime(timestamp) {
            const date = new Date(timestamp);
            const now = new Date();
            const diff = now - date;
            const seconds = Math.floor(diff / 1000);
            const minutes = Math.floor(seconds / 60);
            const hours = Math.floor(minutes / 60);
            const days = Math.floor(hours / 24);

            if (days > 0) return `${days}天前`;
            if (hours > 0) return `${hours}小时前`;
            if (minutes > 0) return `${minutes}分钟前`;
            return '刚刚';
        },

        getLevelDesc(level) {
            const descs = {
                1: '轻度保护',
                2: '中度保护',
                3: '重度保护'
            };
            return descs[level] || '';
        },

        // ========== 认证相关 ==========
        async login() {
            if (!this.loginForm.phone || !this.loginForm.password) {
                this.showToast('请填写完整信息', 'error');
                return;
            }

            this.loggingIn = true;

            try {
                const response = await fetch(`${this.apiBaseUrl}/api/auth/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(this.loginForm)
                });

                const data = await response.json();

                if (response.ok && data.status === 'ok') {
                    this.token = data.token;
                    this.user = data.user;
                    this.isLoggedIn = true;

                    // 保存到本地存储
                    localStorage.setItem('token', data.token);
                    localStorage.setItem('user', JSON.stringify(data.user));

                    this.showToast('登录成功', 'success');
                    this.currentPage = 'feed';
                    this.loginForm = { phone: '', password: '' };
                } else {
                    this.showToast(data.detail || '登录失败', 'error');
                }
            } catch (error) {
                console.error('Login error:', error);
                this.showToast('网络错误，请检查后端是否运行', 'error');
            } finally {
                this.loggingIn = false;
            }
        },

        async register() {
            if (!this.registerForm.phone || !this.registerForm.nickname || !this.registerForm.password) {
                this.showToast('请填写完整信息', 'error');
                return;
            }

            if (this.registerForm.password.length < 6) {
                this.showToast('密码至少6个字符', 'error');
                return;
            }

            this.registering = true;

            try {
                const response = await fetch(`${this.apiBaseUrl}/api/auth/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(this.registerForm)
                });

                const data = await response.json();

                if (response.ok && data.status === 'ok') {
                    this.token = data.token;
                    this.user = data.user;
                    this.isLoggedIn = true;

                    localStorage.setItem('token', data.token);
                    localStorage.setItem('user', JSON.stringify(data.user));

                    this.showToast('注册成功', 'success');
                    this.currentPage = 'feed';
                    this.registerForm = { phone: '', nickname: '', password: '' };
                } else {
                    this.showToast(data.detail || '注册失败', 'error');
                }
            } catch (error) {
                console.error('Register error:', error);
                this.showToast('网络错误，请检查后端是否运行', 'error');
            } finally {
                this.registering = false;
            }
        },

        async verifyToken() {
            try {
                const response = await fetch(`${this.apiBaseUrl}/api/auth/me`, {
                    headers: this.authHeaders
                });

                if (!response.ok) {
                    this.logout();
                }
            } catch (error) {
                console.error('Token verification error:', error);
            }
        },

        logout() {
            this.isLoggedIn = false;
            this.user = null;
            this.token = null;
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            this.currentPage = 'home';
            this.showToast('已退出登录', 'info');
        },

        // ========== 人脸验证 ==========
        handleImageUpload(event, target) {
            const file = event.target.files[0];
            if (!file) return;

            this.verifyFiles[target] = file;

            const reader = new FileReader();
            reader.onload = (e) => {
                this.verifyImages[target] = e.target.result;
            };
            reader.readAsDataURL(file);
        },

        async verifyFaces() {
            if (!this.canVerify) return;

            this.verifying = true;
            this.verifyResult = null;

            try {
                const formData = new FormData();
                formData.append('image_a', this.verifyFiles.imageA);
                formData.append('image_b', this.verifyFiles.imageB);

                // 获取选中的模型
                const selectedModelsList = Object.entries(this.selectedModels)
                    .filter(([key, value]) => value)
                    .map(([key]) => key)
                    .join(',');

                const url = `${this.apiBaseUrl}/api/verify?models=${selectedModelsList}`;

                const response = await fetch(url, {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (response.ok && data.status === 'ok') {
                    this.verifyResult = data;
                    this.showToast('验证完成', 'success');
                } else {
                    this.showToast(data.detail || '验证失败', 'error');
                }
            } catch (error) {
                console.error('Verify error:', error);
                this.showToast('网络错误，请检查后端是否运行', 'error');
            } finally {
                this.verifying = false;
            }
        },

        // ========== 动态流 ==========
        async loadPosts(page = 1) {
            if (!this.isLoggedIn) {
                this.showToast('请先登录', 'error');
                this.currentPage = 'login';
                return;
            }

            this.loadingPosts = true;

            try {
                const response = await fetch(
                    `${this.apiBaseUrl}/api/posts?page=${page}&page_size=${this.pagination.page_size}`,
                    { headers: this.authHeaders }
                );

                const data = await response.json();

                if (response.ok && data.status === 'ok') {
                    this.posts = data.posts;
                    this.pagination = {
                        page: data.page,
                        page_size: data.page_size,
                        total: data.total,
                        has_next: data.has_next
                    };
                } else {
                    this.showToast(data.detail || '加载失败', 'error');
                }
            } catch (error) {
                console.error('Load posts error:', error);
                this.showToast('网络错误', 'error');
            } finally {
                this.loadingPosts = false;
            }
        },

        async toggleLike(post) {
            try {
                const response = await fetch(
                    `${this.apiBaseUrl}/api/posts/${post.id}/like`,
                    {
                        method: 'POST',
                        headers: this.authHeaders
                    }
                );

                const data = await response.json();

                if (response.ok && data.status === 'ok') {
                    post.liked_by_me = data.liked;
                    post.likes_count = data.likes_count;
                } else {
                    this.showToast(data.detail || '操作失败', 'error');
                }
            } catch (error) {
                console.error('Toggle like error:', error);
                this.showToast('网络错误', 'error');
            }
        },

        showCommentToast() {
            this.showToast('Demo 版暂不支持评论功能', 'info');
        },

        // ========== 发帖 ==========
        addImages(event) {
            const files = Array.from(event.target.files);
            const remaining = 9 - this.newPost.images.length;

            if (files.length > remaining) {
                this.showToast(`最多上传9张图片，已选择前${remaining}张`, 'warning');
                files.splice(remaining);
            }

            files.forEach(file => {
                this.newPost.images.push(file);

                const reader = new FileReader();
                reader.onload = (e) => {
                    this.newPost.previewImages.push(e.target.result);
                };
                reader.readAsDataURL(file);
            });
        },

        removeImage(index) {
            this.newPost.images.splice(index, 1);
            this.newPost.previewImages.splice(index, 1);
        },

        addVideo(event) {
            const file = event.target.files[0];
            if (!file) return;

            this.newPost.video = file;

            const reader = new FileReader();
            reader.onload = (e) => {
                this.newPost.videoPreview = e.target.result;
            };
            reader.readAsDataURL(file);
        },

        async publishPost() {
            if (!this.canPublish) return;

            this.publishing = true;

            try {
                const formData = new FormData();

                if (this.newPost.content) {
                    formData.append('content', this.newPost.content);
                }

                this.newPost.images.forEach((file) => {
                    formData.append('images', file);
                });

                if (this.newPost.video) {
                    formData.append('video', this.newPost.video);
                }

                formData.append('is_protected', this.newPost.is_protected);

                if (this.newPost.is_protected) {
                    formData.append('protect_level', this.newPost.protect_level);

                    if (this.newPost.selective_protection && this.newPost.protect_faces_input) {
                        const faces = this.newPost.protect_faces_input.split(',')
                            .map(f => parseInt(f.trim()))
                            .filter(f => !isNaN(f));
                        formData.append('protect_faces', JSON.stringify(faces));
                    }
                }

                const response = await fetch(`${this.apiBaseUrl}/api/posts`, {
                    method: 'POST',
                    headers: this.authHeaders,
                    body: formData
                });

                const data = await response.json();

                if (response.ok && data.status === 'ok') {
                    this.showToast('发布成功', 'success');
                    this.resetNewPost();
                    this.currentPage = 'feed';
                    this.loadPosts();
                } else {
                    this.showToast(data.detail || '发布失败', 'error');
                }
            } catch (error) {
                console.error('Publish post error:', error);
                this.showToast('网络错误', 'error');
            } finally {
                this.publishing = false;
            }
        },

        resetNewPost() {
            this.newPost = {
                content: '',
                images: [],
                previewImages: [],
                video: null,
                videoPreview: null,
                is_protected: false,
                protect_level: 2,
                selective_protection: false,
                protect_faces_input: ''
            };
        },

        // ========== 设置 ==========
        async loadSettings() {
            if (!this.isLoggedIn) return;

            this.loadingSettings = true;

            try {
                const response = await fetch(`${this.apiBaseUrl}/api/settings`, {
                    headers: this.authHeaders
                });

                const data = await response.json();

                if (response.ok && data.status === 'ok') {
                    this.settings = {
                        ...data.settings,
                        selected_faces_input: data.settings.selected_faces.join(',')
                    };
                } else {
                    this.showToast(data.detail || '加载设置失败', 'error');
                }
            } catch (error) {
                console.error('Load settings error:', error);
                this.showToast('网络错误', 'error');
            } finally {
                this.loadingSettings = false;
            }
        },

        async saveSettings() {
            this.savingSettings = true;

            try {
                const payload = {
                    protect_level: this.settings.protect_level,
                    selective_protection: this.settings.selective_protection,
                    selected_faces: []
                };

                if (this.settings.selective_protection && this.settings.selected_faces_input) {
                    payload.selected_faces = this.settings.selected_faces_input.split(',')
                        .map(f => parseInt(f.trim()))
                        .filter(f => !isNaN(f) && f >= 0 && f <= 4);
                }

                const response = await fetch(`${this.apiBaseUrl}/api/settings`, {
                    method: 'PUT',
                    headers: {
                        ...this.authHeaders,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });

                const data = await response.json();

                if (response.ok && data.status === 'ok') {
                    this.showToast('保存成功', 'success');
                } else {
                    this.showToast(data.detail || '保存失败', 'error');
                }
            } catch (error) {
                console.error('Save settings error:', error);
                this.showToast('网络错误', 'error');
            } finally {
                this.savingSettings = false;
            }
        }
    },

    watch: {
        currentPage(newPage) {
            // 页面切换时的逻辑
            if (newPage === 'feed') {
                this.loadPosts();
            } else if (newPage === 'settings') {
                this.loadSettings();
            } else if (newPage === 'newpost') {
                // 需要登录
                if (!this.isLoggedIn) {
                    this.showToast('请先登录', 'error');
                    this.currentPage = 'login';
                }
            }

            // 需要登录的页面检查
            const protectedPages = ['feed', 'settings', 'newpost'];
            if (protectedPages.includes(newPage) && !this.isLoggedIn) {
                this.showToast('请先登录', 'error');
                this.currentPage = 'login';
            }
        }
    }
}).mount('#app');