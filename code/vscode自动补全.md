# VSCode 自动补全方法

在VSCode 中设置自动补全。

首先用`Ctrl+Shift+P`调出指令盘，输入`snippet`，找到`Configure User Snippets`，单击后选择合适的自动补全文件，或直接创建全局/项目用的自动补全文件（不用打后缀名，会自动补上）。在文件中按要求添加新的自动补全命令。

```json
	"<命令名字>": {
        "scope": "<作用域>", 
		"prefix": ["<启动符>", "<可以是字符串，也可以是字符串的列表>"],  
		"body": ["<效果实现代码>", "<可以是字符串，也可以是字符串的列表>"],
		"description": "<命令说明>"
	},
```
如上所示。具体各个变量的解释：
- `scope`：作用域。即希望VSCode在哪些类型的语言环境上实现这个自动补全命令。形式为一个字符串，里面用半角逗号隔开，列出你希望的语言的代码。具体的代码名字可以通过`Ctrl+Shift+P`再单击`Configure User Snippets`得到的下拉菜单里查看、搜索。
- `prefix`：启动符。一串字符，你输入这串字符后按`Tab`键，即可发动自动补全，实现你要的效果。这里可以只写一个字符串，也可以给出一些字符串的列表，每个字符串都是启动符。
- `body`：效果实现代码。具体来说，就是实现你想要的自动补全的效果的代码。这里可以只写一个字符串，也可以给出一些字符串的列表。每个字符串代表一个命令或效果。具体语法见“Snippet语法”。
- `description`：命令说明。说明这个命令的文字，形式为一个字符串。

### 例子

以下是实现自动补全六角括号的例子。

我们要实现自动补全六角括号。

在“命令名字”处，写下`Hexagonal parentheses`。这里的名字与实际执行无关。

首先决定希望在哪里用到。下面给的`scope`是字符串`"tex, json, latex, python"`，它说明我们希望在`latex`、`json`、`python`这些环境里使用。

再决定启动符。这里设置为`hep`和`liu`。键盘输入两者中任何一种，然后按`Tab`键，即可实现自动补全。

接下来是效果实现代码。输入启动符，然后按`Tab`键，命令就会执行。这里的命令是`〔$TM_SELECTED_TEXT〕`。即直接填充六角括号。如果输入启动符之前有选中文字，则选中的文字会出现在六角括号里面。

最后是命令说明。这是一个字符串：`add a pair of hexogonal parentheses`，说明了自动补全命令的意义。

```json
	"Hexagonal parentheses": {
        "scope": "tex, json, latex, python", 
		"prefix": ["hep", "liu"],
		"body": "〔$TM_SELECTED_TEXT〕",
		"description": "add a pair of hexogonal parentheses"
	},
```

### 实际应用

在`latex`文档中，选中文字`abc`，然后输入`liu`，可以看到右方出现相应提示框。单击`Tab`键即得到`〔abc〕`。