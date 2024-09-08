# 中国语文教材重编

中国中小学教材的现状和发展趋势有目共睹。为此，有必要在民间自发地重编公益性的教材。我自2021年“毒教材”事件后萌发了自修教材的想法。目前已经有数学的中学教材10册（计划编修12册）。

本项目是关于语文科目的重编计划。中国语文科目，也即以往说的“国文”，是面向中国学龄儿童教授的普通学科。主要人群是母语为汉语的学龄儿童。

## 这个教材长什么样

本项目过于庞大，因此目前阶段的目标是搜集合理的学材。目前能搜集到的学材主要是各个时代的语文教科书的课文。我们将这些课文统编为四个阶段：

- 识字阶段：这个阶段主要面向学龄前儿童（4-7岁），以识字为主要目的。这个阶段的学材应该有两部分。一部分是识字课文素材。每篇课文负责一定的识字目标。另一部分是用于教学的基础字法知识，如偏旁、部首、字体结构等等。目前阶段只有课文集萃部分的内容。
- 词句阶段：这个阶段主要面向小学学力儿童（7-12岁），以掌握现代汉语字词，掌握句子的阅读和写作为主要目的。这个阶段的学材应该有两部分。一部分是用于学习现代汉语语文的阅读和写作能力的教材，一部分是用于欣赏、学习参考的课文集萃。目前阶段只有课文集萃部分的内容。语文能力的教材目前不在计划中。
- 篇章阶段：这个阶段主要面向中学学历的青少年（12-15岁），以掌握现代汉语文章的基础阅读和写作能力为主要目的，兼之以掌握古代文言的字词和句法的基础知识为次要目的。这个阶段的学材应该有四部分。一部分是用于学习现代汉语文章阅读理解能力的教材，一部分是古代文言字词和基本句法的学习材料，一部分是现代汉语应用文章写作能力的培养材料，一部分是用于欣赏、学习参考的课文集萃。目前阶段只有课文集萃部分的内容。前三部分语文能力的教材目前不在计划中。
- 文学阶段：这个阶段主要面向中学学历的青少年（15-19岁），以掌握现代汉语文本的书面理解和书面表达能力，和古代文言文本的阅读理解能力为主要目的。这个阶段的学材应该有四部分。一部分是用于学习现代汉语文章阅读理解能力的教材，一部分是古代文言文法学习和阅读能力培养的教材，一部分是现代汉语实用与文学文本写作能力的培养材料，一部分是用于欣赏、学习参考的课文集萃。目前阶段只有课文集萃部分的内容。前三部分语文能力的教材目前不在计划中。

本项目和主流的语文教材编排最大的不同，就是摆脱以课文为中心、以课文为单位的教学方式。而是以语言能力的学习为单位，课文只是用于参考的“例子”。这是符合目前各国的母语教学实践的。可惜的是由于我们能力不足，语言能力的学习材料和教材目前不在计划中。本项目目前能用的部分只有搜集的各阶段课文。

### 已完成内容：
- [学龄前发蒙识字课本](./语文/发蒙识字.pdf)
- [小学现代文课文集萃](./语文/小学现代文阅读课文.pdf)
- [中学现代文课文集萃](./语文/中学现代文阅读课文.pdf)

### 本项目内容的版权

本项目的内容，除了课文正文内容，都是免费开源、共同创作、释出版权的，欢迎在遵守版权要求的基础上合理使用乃至参与共同创作。具体的权限协议为[CC BY-SA 4.0协议](https://creativecommons.org/licenses/by-sa/4.0/legalcode.zh-hans)，或参见[版权页](./LICENSE)。

课文正文内容的版权，若已经在中国的语文教科书中出现过的，以当时说明的版权（著作权）为准，本项目仅出于教育目的作合理使用。没有在中国的语文教科书中出现过，但在本项目发布以前已经出版或经公众发布的，以发布当时说明的版权（著作权）为准，本项目仅出于教育目的作合理使用。除此之外的课文正文内容，版权（著作权）归本项目上传者所有。

## 如何使用本项目的材料

本项目的材料主要有两类。一类是完成品，以`pdf`格式发布，是已排版可以打印的文本，建议以A5纸张打印。另一类是结构化数据，以`json`格式发布。

完成品主要是前一节提到的课文集萃，包括识字课文、小学与中学的课文集萃。其中搜集了从50年代起至今编入各个版本语文教科书的大量中小学课文。识字课文包括至少40篇课文，识字量为400字左右，学完之后可以衔接小学的语文学习。小学课文包括180篇现代文，中学课文包括120篇现代文。中学课文的文言文部分是下一阶段的整理目标。

结构化数据则是以上内容的结构化储存版本，以`json`格式储存，编码格式为`utf-8`，可以使用`Python`、`Java`、`C`语言等进行调用。适合进行语料分析以及生成`latex`编译代码。

此外，本项目包括了从结构化数据批量生成`latex`编译代码的`Python`脚本。使用`Python`脚本可以自动化地将结构化数据中的课文转为可编译的`latex`代码，使用`Tex`编译器即可编译为可打印的`pdf`或`ps`文件。