# ZTplusAutoAnswer（Fork 自 Moeary/ZTplusAutoAnswer）

本项目基于 [Moeary/ZTplusAutoAnswer](https://github.com/Moeary/ZTplusAutoAnswer) fork 修改，已获得原作者许可进行修改与发布。

本项目使用 [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html) 进行许可。详情见 LICENSE 文件。

更新内容：
 - 修复了点击“开始测试”按钮跳转到考试页面后，自动答题助手控制面板未自动弹出的问题。现在点击“开始测试”按钮后，控制面板会自动弹出。
 - 本项目默认已内置服务端，仅进行客户端配置即可使用，无需额外配置服务端。

#### 开源代码仅供学习交流使用，默认的服务端题量有限，且不会长期支持。若有进一步使用需求，请自行使用CollectQuestion.js脚本收集题目，并自行搭建服务端。
#### 默认服务端走海外的流量，如果确认应有的题库却搜不出来，那就是没连上服务器，请自己想办法。服务器性能较弱且带宽较小，如果无论如何都无法连接，可以等一会再使用，或者联系我。

这是一个用于 ZTplus 在线教育平台的自动答题助手项目，包含练习题收集、题库服务器和自动答题功能。

## 📋 项目组成

### 核心文件
- **`AutoAnswer.js`** 测试题专用脚本（查询题库 + 智能答题） 
- **`CollectQuestion.js`** - - 练习题专用脚本（收集题库 + 自动选A）
- **`question_server.py`** - 题库查询服务器
- **`题库*.json`** - 题库数据文件

### 数据库文件
- **`question_bank.db`** - SQLite 题库数据库（自动生成）

# 🚀 快速开始

## 客户端配置

1. 打开 Tampermonkey 管理页面
2. 点击"添加新脚本"
3. 将对应的 `.js` 文件内容复制粘贴进去
4. 修改`SERVER_URL`
5. 保存脚本

### 或者

[Greasyfork](https://greasyfork.org/zh-CN/scripts/539590-ztplus%E8%87%AA%E5%8A%A8%E7%AD%94%E9%A2%98%E5%8A%A9%E6%89%8B-%E6%B5%8B%E8%AF%95%E9%A2%98%E4%B8%93%E7%94%A8)


## 服务端配置

### 1. 部署环境


在全新 Ubuntu 24.04.2 LTS 系统下，推荐如下命令安装依赖：
```bash
sudo -i
apt update && apt dist-upgrade -y && apt install python3 pip -y && apt install python3-flask python3-flask-cors sqlite3 -y

```

或者使用Dockerfile全新构建环境（自行安装docker），在项目目录下运行：
```bash
 docker buildx build -t ztplus . --load
 ```

或者直接拉取docker镜像：
```bash
docker pull cooldruid256/ztplus:latest
```

### 2. 启动题库服务器

在项目目录下运行：
```bash
python3 question_server.py
```

或者使用docker运行：
```bash
docker run -d -p 8880:8880 cooldruid256/ztplus:latest
```

服务器将在 `http://localhost:8880` 启动，并自动扫描当前目录下的所有 JSON 题库文件。


## 📚 脚本功能详解

### 练习题脚本 (`CollectQuestion.js`)

**适用场景：** 练习模式，用于收集题库和简单答题

**主要功能：**
- ✅ 自动选择第一个选项（通常是A或"正确"）
- ✅ 自动收集题目和正确答案到本地存储
- ✅ 支持判断题、单选题、多选题
- ✅ 导出题库为 JSON 格式
- ✅ 自动确认和跳转下一题

**使用方法：**
1. 访问练习题页面
2. 脚本会自动显示控制面板
3. 默认开启题库收集功能
4. 点击"导出题库"可下载收集的题目

**控制面板功能：**
- 暂停/继续答题
- 查看收集进度
- 导出题库数据
- 清除缓存数据

### 测试题脚本 (`AutoAnswer.js`)

**适用场景：** 正式考试，利用题库智能答题

**主要功能：**
- 🎯 自动识别页面中所有题目
- 🔍 向题库服务器查询正确答案
- 🤖 智能选择答案（支持单选和多选）
- ⚡ 控制答题速度，避免检测
- 📊 实时显示答题进度

**支持题型：**
- **判断题：** A(正确) / B(错误)
- **单选题：** A / B / C / D
- **多选题：** ABC / ABCD / BD 等组合

**使用方法：**
1. 确保题库服务器正在运行
2. 访问测试页面（如：`http://www.ztplus.cn/pc/index.html#/paper/testing/...`）
3. 等待页面加载完成
4. 点击控制面板中的"开始答题"
5. 脚本会自动处理所有题目

**答题逻辑：**
- 优先查询题库获取正确答案
- 如果题库中没有答案，默认选择A
- 多选题支持 "ABCD" 格式的答案

### 题库服务器 (`question_server.py`)

**功能：**
- 🗄️ 自动扫描并导入所有 JSON 题库文件
- 🔍 提供题目查询 API
- 📈 显示题库统计信息
- 🚫 避免重复导入相同题目

**API 接口：**

1. **查询题目**
   ```
   GET /query?term=题目关键词
   ```
   返回匹配的题目和答案

2. **服务器状态**
   ```
   GET /status
   ```
   返回服务器状态和题库统计

**启动信息示例：**
```
Initializing database...
Loading data from JSON to database...
Found 2 JSON files: ['题库1.json', '题库2.json']

Processing file: 题库1.json
File '题库1.json': Imported 99, Skipped 0

Processing file: 题库2.json
File '题库2.json': Imported 401, Skipped 0

=== Loading Summary ===
Total files processed: 2
Total questions imported: 500
Total questions skipped: 0
Data loading complete.

Starting Flask server on http://localhost:8880
```

## 🎮 使用流程

### 题库收集流程
1. 使用 `1.js` 脚本在练习模式下收集题目
2. 导出题库为 JSON 文件（如 `题库3.json`）
3. 重启题库服务器，自动导入新题库

### 考试答题流程
1. 启动题库服务器 `python question_server.py`
2. 安装并启用 `2.js` 脚本
3. 访问考试页面
4. 点击"开始答题"，脚本自动处理

## ⚙️ 配置说明

### 答题速度配置 (`2.js`)
```javascript
const CONFIG = {
    ANSWER_DELAY_MIN: 200,  // 最小答题间隔(毫秒)
    ANSWER_DELAY_MAX: 400,  // 最大答题间隔(毫秒)
    RETRY_DELAY: 100,       // 重试间隔
    MAX_RETRIES: 3          // 最大重试次数
};
```

### 服务器配置 (`question_server.py`)
- 端口：8880
- 数据库：SQLite (`question_bank.db`)
- 支持 CORS 跨域请求

## 📊 题库格式

JSON 题库文件格式：
```json
[
  {
    "question": "职业道德是从业者在职业活动中应该遵循的符合自身职业特点的职业行为规范。（  ）",
    "answer": "A"
  },
  {
    "question": "在软件工程中，概要设计阶段的任务主要包括详细编写各个模块的源代码。（  ）",
    "answer": "B"
  }
]
```

**答案格式说明：**
- 判断题：`"A"` (正确) 或 `"B"` (错误)
- 单选题：`"A"`, `"B"`, `"C"`, `"D"`
- 多选题：`"ABC"`, `"ABCD"`, `"BD"` 等

## 🛠️ 故障排除

### 常见问题

**1. 脚本不工作**
- 检查页面 URL 是否匹配脚本的 `@match` 规则
- 确认 Tampermonkey 已启用脚本
- 查看浏览器控制台错误信息

**2. 题库服务器连接失败**
- 确认服务器正在运行（`http://localhost:8880/status`）
- 检查防火墙设置
- 确认没有其他程序占用 8880 端口

**3. 答题速度过快被检测**
- 增加 `CONFIG.ANSWER_DELAY_MIN` 和 `CONFIG.ANSWER_DELAY_MAX` 的值
- 避免在短时间内重复使用

**4. 多选题选择错误**
- 检查题库中答案格式是否正确（如 "ABCD"）
- 确认页面中的多选框元素结构

### 调试技巧

1. **查看控制台日志**
   - 打开浏览器开发者工具 (F12)
   - 查看 Console 标签页的日志信息

2. **测试题库服务器**
   ```bash
   curl "http://localhost:8880/status"
   curl "http://localhost:8880/query?term=职业道德"
   ```

3. **检查脚本状态**
   - 控制面板会显示当前状态和进度
   - 注意状态信息和错误提示

## 📝 更新日志

### v1.2 (2025-09-15)
- ✨ 题库11已更新上线

### v1.1 (2025-06-16)
- ✨ 新增多选题支持
- 🔧 优化题目类型识别
- 📊 改进答题统计显示

### v0.9.0 (2025-06-15)
- 🔄 移除练习题脚本的服务器依赖
- 🎯 优化选择逻辑，支持多种题型
- 📈 保留题库收集功能

### v1.0 (2025-06-15)
- 🎉 初始版本发布
- 🤖 支持自动答题和题库收集
- 🗄️ 集成题库服务器

## ⚠️ 注意事项

1. **使用目的**：本脚本仅供学习和研究使用，请遵守相关平台的使用条款
2. **答题速度**：建议设置合理的答题间隔，避免被系统检测
3. **数据备份**：定期备份题库数据，避免数据丢失
4. **版本兼容**：如果平台更新页面结构，可能需要更新脚本

## 📞 技术支持

如果遇到问题或需要技术支持，请：
1. 检查本文档的故障排除部分
2. 查看浏览器控制台的错误信息
3. 确认所有依赖都已正确安装

---

**免责声明：** 本项目仅供学习和研究使用，使用者需要自行承担使用风险。请遵守相关平台的使用条款和法律法规。
