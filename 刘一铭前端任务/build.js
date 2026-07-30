const fs = require('fs');
const path = require('path');

console.log('🚀 开始打包...\n');

// 读取文件
const htmlContent = fs.readFileSync('index.html', 'utf-8');
const cssContent = fs.readFileSync('styles.css', 'utf-8');
const jsContent = fs.readFileSync('app.js', 'utf-8');

// 替换外部引用为内联内容
let result = htmlContent;

// 内联CSS
result = result.replace(
    '<link rel="stylesheet" href="styles.css">',
    `<style>\n${cssContent}\n    </style>`
);

// 内联JS
result = result.replace(
    '<script src="app.js"></script>',
    `<script>\n${jsContent}\n    </script>`
);

// 写入打包后的文件
fs.writeFileSync('dist.html', result, 'utf-8');

console.log('✅ 打包完成！');
console.log('📦 输出文件: dist.html');
console.log('📏 文件大小:', (fs.statSync('dist.html').size / 1024).toFixed(2), 'KB');
console.log('\n💡 提示: 直接用浏览器打开 dist.html 即可使用');
