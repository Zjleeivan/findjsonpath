

---


## 项目名称

基于正则表达式的JSON/Map文本解析器

---

## 项目简介

本项目实现了一个基于正则表达式的JSON解析工具，能够逆向解析出嵌套或不完整JSON或类似的map-like文本中的路径信息。其主要应用场景是对格式混乱、不完整的JSON数据进行分析和处理，特别是当需要查找特定的key或value时。

---

## 功能概述

- **JSON或Map-like文本的解析**：能够解析带有嵌套结构的JSON或类似JSON格式的字符串。
- **逆向路径查找**：通过给定的key或value，逆向追溯出其所在的完整路径。
- **处理不完整的JSON**：该工具具备一定的容错性，能够应对尾部残缺、嵌套变异等情况。
- **支持自定义查找对象**：用户可指定查找key或value，并获取对应的路径。

---

## 技术栈

- **语言**：Python 3.x
- **依赖库**：`re` (正则表达式库)

---

## 项目目录结构

```bash
├── json_parser.py        # 主程序文件，包含findjsonpath函数
└── README.md             # 项目说明文档
```



## 代码模块

### `findjsonpath` 函数

这是项目的核心函数，对**不规则的JSON**或**map-like**文本进行逆向解析，找到指定的`key`或`value`在JSON结构中的路径，并返回一个路径列表。

#### 参数说明

```python
def findjsonpath(dictStr, deStr='\r\n', mode='value') -> list:
```

- **`dictStr`**: 需要解析的JSON或map-like字符串。
- **`deStr`**: 要查找的key或value，默认为回车符。
- **`mode`**: 指定查找的对象是key还是value，默认为`value`。

#### 返回值

- 返回包含目标的路径列表，每个路径以字符串形式表示。

### 工作原理

#### 1. 文本预处理
首先，使用 `re.sub` 去除文本中的空格、换行、回车和制表符，保证数据的连续性，避免这些字符对查找的影响。

```python
dictStr = re.sub('[\s|\n|\r|\t]*', '', dictStr, 0, re.MULTILINE)
```

#### 2. 查找目标字符
根据 `mode` 的不同，确定查找的目标对象是 `key` 还是 `value`，然后遍历整个字符串，寻找目标的出现位置。

#### 3. 逆向解析路径
每次找到目标之后，从当前位置**向前逐字符解析**，追溯出目标所在的完整路径。解析过程中涉及以下几个步骤：

- **处理不同层级的嵌套**：包括花括号`{}`和方括号`[]`，以识别key和数组下标。
- **识别JSON对象的结构**：根据逗号、冒号、括号等符号判断当前字符的上下文。

#### 4. 返回结果
将解析出来的路径以列表形式返回，使用 `\n` 分隔各路径，方便展示。

## 运行与测试

### 运行

1. 直接运行 `json_parser.py` 即可：

   ```bash
   python json_parser.py
   ```

2. 函数执行结果将输出至控制台。

### 测试

项目内置了一些测试数据，位于 `test_data.py` 文件中。你可以修改测试数据以验证不同情况的解析效果。以下是运行测试的示例：

```bash
python test_data.py
```

#### 示例输入：

```python
data = '''{
    "configs": [
        {"type": "field", "config": {"fields": [
            {"guid": "04d1d5aa", "fid": "7ce5017bba"},
            {"guid": "7c6e8436", "fid": "2e917274f1"}
        ]}},
        {"type": "paging", "config": {"limit": 50, "offset": 0}}
    ],
    "reportId": "9d827f27"
}'''
```

#### 示例输出：

```
1: ["configs"][0]["type"]
2: ["configs"][1]["type"]
```

---

## 使用说明

### 基本用法

在Python脚本中导入`findjsonpath`函数，并传入需要解析的字符串、查找的key或value。

#### 示例

```python
from json_parser import findjsonpath

data = '''{
    "olapQueryParam": {"configs": [
        {"type": "field", "config": {"fields": [
            {"guid": "04d1d5aa", "fid": "7ce5017bba"},
            {"guid": "7c6e8436", "fid": "2e917274f1"}
        ]}},
        {"type": "paging", "config": {"limit": 50, "offset": 0}}
    ]},
    "reportId": "9d827f27"
}'''

# 查找 "type" 出现的位置
result = findjsonpath(data, '"type"', 'key')
print(result)
```

### 输出

```
1: ["olapQueryParam"]["configs"][0]["type"]
2: ["olapQueryParam"]["configs"][1]["type"]
```
这个输出表示 `"type"` 出现在第n个 `configs` 数组元素的`key`位置。

---


### 代码优势

1. **处理不完整的JSON**：该方法可以处理尾部缺失、嵌套变异、格式不标准的JSON或map-like结构。
2. **灵活性**：支持 `key` 和 `value` 的查找，解析路径十分精准。

---

### 注意事项

- **输入格式**：此方法假设输入的文本接近JSON格式。如果输入与JSON差异较大，可能会解析错误。
- **性能问题**：对于大规模或深度嵌套的JSON，解析效率可能较低。

---

## 版本更新

### v1.0.0
- 实现核心JSON解析功能。
- 支持key和value的逆向路径查找。
- 处理不完整的JSON或map-like字符串。

---

