
# 微信小程序 WXML JSON Schema 转换工具

## 项目介绍

当前工具用于抓取微信小程序官方组件定义，并通过 AI 自动分析转换为标准化的 JSON Schema 数据。

转换后的 JSON Schema 可用于后续的组件解析、代码生成、智能提示、低代码平台等场景。

整体流程如下：

```
微信小程序官方文档
        |
        v
   download.py
        |
        v
本地 HTML 组件定义数据
        |
        v
   generate.py
        |
        v
单个组件 JSON Schema 文件
        |
        v
    build.py
        |
        v
合并后的完整 JSON Schema
```

---

## 文件说明

### download.py

负责从微信小程序官方文档中抓取组件定义数据。

主要功能：

- 获取微信小程序官方 WXML 组件列表
- 下载组件属性、事件、使用说明等定义
- 保存原始数据到本地

输出：

```
output/
 ├── button.html
 ├── view.html
 ├── input.html
 └── ...
```

---

### generate.py

负责将本地抓取的组件定义转换为 JSON Schema。

主要功能：

- 读取 `download.py` 下载的原始数据
- 调用 AI 对组件定义进行分析
- 将 WXML 组件转换为标准 JSON Schema
- 生成单个组件 Schema 文件

例如：

输入：

```
output/button.html
```

输出：

```
output/button.json
```

转换内容包括：

- 组件名称
- 属性定义
- 属性类型
- 默认值
- 可选值
- 事件定义
- 插槽信息
- 使用描述等

---

### build.py

负责合并所有组件 Schema。

主要功能：

- 扫描转换后的 JSON Schema 文件
- 合并所有组件定义
- 生成完整组件 Schema 文件

输入：

```
output/
 ├── button.json
 ├── input.json
 ├── view.json
 └── ...
```

输出：

```
elementDescriptions.json
```

最终文件包含全部微信小程序组件定义。

---

## 使用流程

### 1. 下载官方组件定义

执行：

```bash
python download.py
```

完成后会生成本地组件原始数据。

---

### 2. AI 转换组件 Schema

执行：

```bash
python generate.py
```

该步骤会逐个处理组件，并生成对应 JSON Schema。

---

### 3. 合并 Schema

执行：

```bash
python build.py
```

生成最终完整 Schema 文件。

---

## 目录结构

示例：

```
element-tool/
|
├── download.py        # 下载微信官方组件定义
├── generate.py        # AI 转换 JSON Schema
├── build.py           # 合并 Schema
|
├── output/              # 原始组件定义
|
├── output/            # 单个组件 Schema
|
└── elementDescriptions.json
                       # 最终完整 Schema
```

---

## 说明

由于微信小程序官方组件数量较多，并且组件定义存在一定复杂度，转换过程采用 AI 辅助解析。

生成后的 Schema 可以作为：

- AI 编程助手组件知识库
- 小程序代码生成基础数据
- WXML 编辑器智能提示
- 可视化搭建工具组件模型

等用途。
