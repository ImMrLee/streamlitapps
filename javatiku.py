import streamlit as st
import json
import os
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="Java题库系统",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS防止文本选中和复制
st.markdown("""
<style>
    /* 防止文本被选中 */
    * {
        user-select: none !important;
        -webkit-user-select: none !important;
        -moz-user-select: none !important;
        -ms-user-select: none !important;
    }
    
    /* 允许输入框内选中，但禁止粘贴 */
    textarea, input {
        user-select: text !important;
        -webkit-user-select: text !important;
        -moz-user-select: text !important;
        -ms-user-select: text !important;
    }
    
    /* 禁止粘贴 */
    textarea, input {
        -webkit-user-modify: read-write-plaintext-only;
    }
    
    /* 自定义按钮样式 */
    .stButton > button {
        background-color: #FF6B00;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #E55A00;
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(255, 107, 0, 0.3);
    }
    
    /* 折叠面板样式 */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 8px;
        font-weight: bold;
    }
    
    /* 标签页样式优化 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF6B00 !important;
        color: white !important;
    }
    
    /* 答案区域高亮 */
    .answer-box {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        margin: 10px 0;
    }
    
    /* 解析区域样式 */
    .ai-analysis {
        background-color: #f3e5f5;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #9C27B0;
        margin: 10px 0;
    }
</style>

<script>
    // 阻止粘贴事件
    document.addEventListener('paste', function(e) {
        if (e.target.tagName === 'TEXTAREA' || e.target.tagName === 'INPUT') {
            e.preventDefault();
            alert('禁止粘贴内容，请手动输入！');
        }
    });
    
    // 阻止右键菜单
    document.addEventListener('contextmenu', function(e) {
        e.preventDefault();
    });
</script>
""", unsafe_allow_html=True)

# 题库数据
def get_chapter_data():
    return {
        "第一章 Java概述": {
            "single_choice": [
                {"id": 1, "question": "Java语言最初是由哪家公司开发的？", "options": ["A. Microsoft", "B. IBM", "C. Sun Microsystems", "D. Oracle"], "answer": "C. Sun Microsystems"},
                {"id": 2, "question": "Java之父是哪位计算机科学家？", "options": ["A. Dennis Ritchie", "B. Bjarne Stroustrup", "C. James Gosling", "D. Linus Torvalds"], "answer": "C. James Gosling"},
                {"id": 3, "question": "Java语言的出世年份是", "options": ["A. 1991", "B. 1993", "C. 1995", "D. 1999"], "answer": "C. 1995"},
                {"id": 4, "question": "下列哪项不是Java语言的主要特点？", "options": ["A. 跨平台性", "B. 面向过程", "C. 自动垃圾回收", "D. 多线程支持"], "answer": "B. 面向过程"},
                {"id": 5, "question": "JDK的全称是什么？", "options": ["A. Java Development Kit", "B. Java Deployment Kit", "C. Java Debug Kit", "D. Java Design Kit"], "answer": "A. Java Development Kit"},
                {"id": 6, "question": "在Windows系统中安装JDK后，需要配置哪个环境变量来指定JDK的安装路径？", "options": ["A. PATH", "B. CLASSPATH", "C. JAVA_HOME", "D. JDK_ROOT"], "answer": "C. JAVA_HOME"},
                {"id": 7, "question": "编译Java源程序使用的命令是？", "options": ["A. java", "B. javac", "C. javadoc", "D. jar"], "answer": "B. javac"},
                {"id": 8, "question": "经过javac编译后生成的字节码文件扩展名是？", "options": ["A. .java", "B. .exe", "C. .class", "D. .jar"], "answer": "C. .class"},
                {"id": 9, "question": "Java反编译是指将什么文件转换回源代码？", "options": ["A. .java文件", "B. .class文件", "C. .exe文件", "D. .txt文件"], "answer": "B. .class文件"},
                {"id": 10, "question": "下列哪个命令用于运行Java程序？", "options": ["A. javac", "B. java", "C. javap", "D. jar"], "answer": "B. java"}
            ],
            "multiple_choice": [
                {"id": 1, "question": "以下哪些属于Java语言的特点？（多选）", "options": ["A. 平台无关性", "B. 支持指针操作", "C. 面向对象", "D. 健壮性"], "answer": "ACD"},
                {"id": 2, "question": "关于JDK、JRE和JVM，下列说法正确的有？（多选）", "options": ["A. JDK包含JRE", "B. JRE包含JVM", "C. JVM负责执行字节码", "D. JDK只包含编译器"], "answer": "ABC"},
                {"id": 3, "question": "下列关于Java程序开发流程的说法，正确的有？（多选）", "options": ["A. 先用文本编辑器编写源代码", "B. 使用javac命令编译源代码", "C. 编译后生成.exe可执行文件", "D. 使用java命令运行程序"], "answer": "ABD"},
                {"id": 4, "question": "关于Java的跨平台特性，以下说法正确的有？（多选）", "options": ["A. 一次编译，到处运行", "B. 跨平台依赖于JVM", "C. Java程序可以直接在操作系统上运行", "D. 不同操作系统需要安装对应版本的JVM"], "answer": "ABD"},
                {"id": 5, "question": "下列哪些是合法的Java源文件命名？（多选）", "options": ["A. HelloWorld.java", "B. MyApp.java", "C. 123Test.java", "D. Test_1.java"], "answer": "ABD"},
                {"id": 6, "question": "关于Java程序的编写规范，以下说法正确的有？（多选）", "options": ["A. Java源文件扩展名为.java", "B. 类名可以与文件名不一致", "C. 一个源文件可以包含多个类", "D. public类的类名必须与文件名一致"], "answer": "ACD"},
                {"id": 7, "question": "以下哪些工具属于JDK？（多选）", "options": ["A. javac", "B. java", "C. jar", "D. javap"], "answer": "ABCD"},
                {"id": 8, "question": "关于Java反编译，以下说法正确的有？（多选）", "options": ["A. 可以将.class文件还原为Java源代码", "B. 反编译工具如JD-GUI", "C. 反编译后的代码与原代码完全一样", "D. 反编译可以用于学习研究"], "answer": "ABD"},
                {"id": 9, "question": "下列哪些不是Java语言的设计目标？（多选）", "options": ["A. 简单性", "B. 依赖于特定平台", "C. 安全性", "D. 使用复杂的语法"], "answer": "BD"},
                {"id": 10, "question": "关于Java语言的发展历史，以下说法正确的有？（多选）", "options": ["A. Java最初名为Oak", "B. Java在1995年正式发布", "C. Java从诞生起就属于Oracle公司", "D. Java的命名与咖啡有关"], "answer": "ABD"}
            ],
            "short_answer": [
                {"id": 1, "question": "简述Java语言\"一次编译，到处运行\"的跨平台原理。", "answer": "Java源代码经编译器编译后生成字节码文件，字节码不是直接运行在操作系统上的，而是由各平台上的Java虚拟机解释执行。不同操作系统有对应的JVM实现，只要安装了JVM，同一份字节码就可以在任何平台上运行，从而实现跨平台"},
                {"id": 2, "question": "请说明JDK、JRE和JVM三者之间的关系。", "answer": "JVM是Java虚拟机，负责执行字节码；JRE是Java运行时环境，包含JVM和核心类库，用于运行Java程序；JDK是Java开发工具包，包含JRE以及编译器、调试器等开发工具。三者为包含关系"}
            ],
            "programming": [
                {"id": 1, "question": "编写一个简单的Java程序，在控制台输出\"Hello, Java!\"。要求类名为HelloJava。", "answer": "public class HelloJava {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, Java!\");\n    }\n}"},
                {"id": 2, "question": "编写一个Java程序，定义两个整数变量并赋初值，计算它们的和并输出结果。要求类名为SumDemo。", "answer": "public class SumDemo {\n    public static void main(String[] args) {\n        int a = 10;\n        int b = 20;\n        int sum = a + b;\n        System.out.println(\"和为：\" + sum);\n    }\n}"}
            ],
            "advanced": [
                {"id": 1, "question": "编写一个Java程序，定义三个整数变量，使用if语句找出其中的最大值并输出。要求类名为FindMax", "answer": "public class FindMax {\n    public static void main(String[] args) {\n        int a = 15;\n        int b = 28;\n        int c = 9;\n        int max = a;\n        if (b > max) {\n            max = b;\n        }\n        if (c > max) {\n            max = c;\n        }\n        System.out.println(\"最大值是：\" + max);\n    }\n}"}
            ]
        },
        "第二章 Java基础语法": {
            "single_choice": [
                {"id": 1, "question": "下列哪项是Java中的合法标识符？", "options": ["A. 2user", "B. class", "C. _name", "D. user-name"], "answer": "C. _name"},
                {"id": 2, "question": "以下哪个不是Java的关键字？", "options": ["A. int", "B. float", "C. main", "D. boolean"], "answer": "C. main"},
                {"id": 3, "question": "在Java中，int类型数据占用的字节数是？", "options": ["A. 1", "B. 2", "C. 4", "D. 8"], "answer": "C. 4"},
                {"id": 4, "question": "下列哪种类型转换需要强制类型转换？", "options": ["A. int转long", "B. float转double", "C. double转int", "D. char转int"], "answer": "C. double转int"},
                {"id": 5, "question": "下列代码的输出结果是？\n\nint a = 5;\ndouble b = 2.0;\nSystem.out.println(a / b);", "options": ["A. 2", "B. 2.5", "C. 2.0", "D. 编译错误"], "answer": "B. 2.5"},
                {"id": 6, "question": "使用Scanner类读取用户输入的整数，应使用哪个方法？", "options": ["A. next()", "B. nextLine()", "C. nextInt()", "D. nextDouble()"], "answer": "C. nextInt()"},
                {"id": 7, "question": "声明一个整型数组的正确语法是？", "options": ["A. int arr = new int[5];", "B. int[] arr = new int[5];", "C. int arr[] = new int(5);", "D. int[] arr = new int(5);"], "answer": "B. int[] arr = new int[5];"},
                {"id": 8, "question": "获取数组arr长度的正确方式是？", "options": ["A. arr.size()", "B. arr.length()", "C. arr.length", "D. arr.getLength()"], "answer": "C. arr.length"},
                {"id": 9, "question": "下列哪种数组初始化方式是合法的？", "options": ["A. int[] arr = {1, 2, 3};", "B. int[] arr = new int[3]{1, 2, 3};", "C. int arr[3] = {1, 2, 3};", "D. int[] arr = [1, 2, 3];"], "answer": "A. int[] arr = {1, 2, 3};"},
                {"id": 10, "question": "数组在Java中属于什么类型？", "options": ["A. 基本数据类型", "B. 引用数据类型", "C. 抽象数据类型", "D. 原始数据类型"], "answer": "B. 引用数据类型"}
            ],
            "multiple_choice": [
                {"id": 1, "question": "以下哪些是Java中的合法标识符？（多选）", "options": ["A. userName", "B. $price", "C. 123abc", "D. 价格"], "answer": "ABD"},
                {"id": 2, "question": "下列哪些属于Java的基本数据类型？（多选）", "options": ["A. int", "B. String", "C. boolean", "D. double"], "answer": "ACD"},
                {"id": 3, "question": "关于char类型，下列说法正确的有？（多选）", "options": ["A. 占用2个字节", "B. 可以存储一个英文字母", "C. 可以存储一个汉字", "D. 采用ASCII编码"], "answer": "ABC"},
                {"id": 4, "question": "以下哪些属于自动类型转换？（多选）", "options": ["A. int转long", "B. float转double", "C. int转byte", "D. char转int"], "answer": "ABD"},
                {"id": 5, "question": "下列代码中，哪些会导致编译错误？（多选）", "options": ["A. float f = 3.14;", "B. int i = 100;", "C. byte b = 200;", "D. boolean b = 1;"], "answer": "ACD"},
                {"id": 6, "question": "关于Scanner类的使用，下列说法正确的有？（多选）", "options": ["A. 使用前需要导入java.util.Scanner", "B. nextLine()可以读取一整行字符串", "C. nextInt()读取整数后不会留下换行符", "D. 使用完可以调用close()方法关闭"], "answer": "ABD"},
                {"id": 7, "question": "关于数组的声明，以下哪些是正确的？（多选）", "options": ["A. int[] a;", "B. int a[];", "C. int a[5];", "D. int[] a = new int[5];"], "answer": "ABD"},
                {"id": 8, "question": "以下关于数组默认值的说法，正确的有？（多选）", "options": ["A. int类型数组元素的默认值是0", "B. boolean类型数组元素的默认值是false", "C. 引用类型数组元素的默认值是null", "D. char类型数组元素的默认值是'\\u0000'"], "answer": "ABCD"},
                {"id": 9, "question": "关于数组的length属性，以下说法正确的有？（多选）", "options": ["A. length是一个属性，不是方法", "B. length的值是数组能容纳的元素个数", "C. 数组创建后length的值不可改变", "D. length的值等于最大下标值"], "answer": "ABC"},
                {"id": 10, "question": "以下关于数组引用的说法，正确的有？（多选）", "options": ["A. 数组变量存储的是数组对象的引用", "B. 将数组赋值给另一个数组变量，两个变量指向同一个数组", "C. 可以通过下标访问数组元素", "D. 数组下标从1开始"], "answer": "ABC"}
            ],
            "short_answer": [
                {"id": 1, "question": "请列出Java中的8种基本数据类型", "answer": "byte、short、int、long、float、double、char、boolean"},
                {"id": 2, "question": "数组的length属性有什么作用？请简要说明。", "answer": "length属性用于获取数组的长度，即数组中元素的个数。它是一个属性而非方法，数组创建后length的值不可改变"}
            ],
            "programming": [
                {"id": 1, "question": "编写一个Java程序，声明一个包含5个整数的数组，使用循环从控制台读取用户输入的5个整数存入数组，然后计算并输出这5个整数的平均值", "answer": "import java.util.Scanner;\n\npublic class ArrayAverage {\n    public static void main(String[] args) {\n        Scanner scanner = new Scanner(System.in);\n        int[] arr = new int[5];\n        int sum = 0;\n        for (int i = 0; i < arr.length; i++) {\n            arr[i] = scanner.nextInt();\n            sum += arr[i];\n        }\n        System.out.println(\"平均值为：\" + (sum / 5.0));\n        scanner.close();\n    }\n}"},
                {"id": 2, "question": "编写一个Java程序，声明一个整型数组并初始化为{12, 45, 7, 23, 56, 89, 34}，使用循环找出数组中的最大值并输出", "answer": "public class FindMax {\n    public static void main(String[] args) {\n        int[] arr = {12, 45, 7, 23, 56, 89, 34};\n        int max = arr[0];\n        for (int i = 1; i < arr.length; i++) {\n            if (arr[i] > max) {\n                max = arr[i];\n            }\n        }\n        System.out.println(\"最大值为：\" + max);\n    }\n}"}
            ],
            "advanced": [
                {"id": 1, "question": "编写一个Java程序，声明一个整型数组并初始化为{23, 14, 56, 78, 32, 45}，将数组中的元素按照从大到小的顺序排序后输出", "answer": "public class SortArray {\n    public static void main(String[] args) {\n        int[] arr = {23, 14, 56, 78, 32, 45};\n        for (int i = 0; i < arr.length - 1; i++) {\n            for (int j = 0; j < arr.length - 1 - i; j++) {\n                if (arr[j] < arr[j + 1]) {\n                    int temp = arr[j];\n                    arr[j] = arr[j + 1];\n                    arr[j + 1] = temp;\n                }\n            }\n        }\n        System.out.print(\"排序后的数组：\");\n        for (int i = 0; i < arr.length; i++) {\n            System.out.print(arr[i] + \" \");\n        }\n    }\n}"}
            ]
        },
        "第三章 流程控制": {
            "single_choice": [
                {"id": 1, "question": "在Java中，表达式 10 % 3 的结果是？", "options": ["A. 3", "B. 1", "C. 0", "D. 3.33"], "answer": "B. 1"},
                {"id": 2, "question": "下列运算符中，哪个是逻辑与运算符？", "options": ["A. &", "B. &&", "C. |", "D. !"], "answer": "B. &&"},
                {"id": 3, "question": "执行 int a = 5; a += 3; 后，a的值是？", "options": ["A. 5", "B. 3", "C. 8", "D. 15"], "answer": "C. 8"},
                {"id": 4, "question": "下列代码的输出结果是？\n\nint x = 10;\nif (x > 5)\n    System.out.print(\"A\");\n    System.out.print(\"B\");", "options": ["A. A", "B. B", "C. AB", "D. 编译错误"], "answer": "C. AB"},
                {"id": 5, "question": "switch语句中，表达式的类型不能是？", "options": ["A. int", "B. char", "C. String", "D. double"], "answer": "D. double"},
                {"id": 6, "question": "在switch语句中，用于结束每个case分支的关键字是？", "options": ["A. stop", "B. end", "C. break", "D. exit"], "answer": "C. break"},
                {"id": 7, "question": "下列哪个循环语句至少执行一次循环体？", "options": ["A. for循环", "B. while循环", "C. do-while循环", "D. 以上都不是"], "answer": "C. do-while循环"},
                {"id": 8, "question": "break语句在循环中的作用是？", "options": ["A. 跳过本次循环，继续下一次循环", "B. 结束当前循环，执行循环后的语句", "C. 结束整个程序", "D. 返回到循环开头"], "answer": "B. 结束当前循环，执行循环后的语句"},
                {"id": 9, "question": "下列代码的输出结果是？\n\nfor (int i = 0; i < 3; i++) {\n    if (i == 1) continue;\n    System.out.print(i);\n}", "options": ["A. 012", "B. 01", "C. 02", "D. 12"], "answer": "C. 02"},
                {"id": 10, "question": "下列for循环的语法，正确的是？", "options": ["A. for (int i = 0; i < 5; i++) { }", "B. for (int i = 0, i < 5, i++) { }", "C. for (i = 0; i < 5; i++) { } （未声明i）", "D. A和C都对"], "answer": "A. for (int i = 0; i < 5; i++) { }"}
            ],
            "multiple_choice": [
                {"id": 1, "question": "下列哪些是Java中的算术运算符？（多选）", "options": ["A. +", "B. -", "C. *", "D. %"], "answer": "ABCD"},
                {"id": 2, "question": "关于if语句，下列说法正确的有？（多选）", "options": ["A. if语句可以单独使用", "B. else语句必须与if语句配对使用", "C. if语句的条件表达式结果必须是boolean类型", "D. if语句后面只能跟一条语句"], "answer": "ABC"},
                {"id": 3, "question": "关于switch语句，下列说法正确的有？（多选）", "options": ["A. switch的表达式中可以使用int类型", "B. switch的表达式中可以使用String类型", "C. 每个case后面必须跟break", "D. default分支是可选的"], "answer": "ABD"},
                {"id": 4, "question": "以下哪些循环结构是Java支持的？（多选）", "options": ["A. for循环", "B. while循环", "C. do-while循环", "D. repeat-until循环"], "answer": "ABC"},
                {"id": 5, "question": "关于while和do-while循环的区别，下列说法正确的有？（多选）", "options": ["A. while循环先判断条件再执行", "B. do-while循环先执行一次再判断条件", "C. do-while循环至少执行一次", "D. 两者没有区别"], "answer": "ABC"},
                {"id": 6, "question": "关于break语句，下列说法正确的有？（多选）", "options": ["A. break可以用于switch语句中", "B. break可以用于循环语句中", "C. break用于结束当前循环", "D. break用于跳过本次循环"], "answer": "ABC"},
                {"id": 7, "question": "关于continue语句，下列说法正确的有？（多选）", "options": ["A. continue用于结束当前循环", "B. continue用于跳过本次循环，继续下一次", "C. continue只能用于循环语句中", "D. continue也可以用于switch语句中"], "answer": "BC"},
                {"id": 8, "question": "下列代码中，哪些会导致无限循环？（多选）", "options": ["A. for (int i = 0; i < 5; i++)", "B. while (true) { }", "C. for (;;) { }", "D. while (false) { }"], "answer": "BC"},
                {"id": 9, "question": "关于for语句遍历数组，下列说法正确的有？（多选）", "options": ["A. 可以使用普通for循环遍历数组", "B. 可以使用增强for循环（for-each）遍历数组", "C. 增强for循环中可以直接修改数组元素的值", "D. 普通for循环可以通过下标修改数组元素"], "answer": "ABD"},
                {"id": 10, "question": "下列表达式中，结果为true的有？（多选）", "options": ["A. 5 > 3 && 2 < 4", "B. 10 == 10 || 3 > 5", "C. !(5 < 3)", "D. 4 >= 4"], "answer": "ABCD"}
            ],
            "short_answer": [
                {"id": 1, "question": "请说明break语句和continue语句在循环中的作用有什么区别。", "answer": "break语句用于完全结束当前循环，程序继续执行循环后面的语句；continue语句用于跳过本次循环中剩余的代码，直接进入下一次循环的判断条件"},
                {"id": 2, "question": "请说明switch语句中break的作用，并说明如果省略break会可能发生什么现象。", "answer": "break用于结束当前case分支，跳出整个switch语句。如果省略break，程序会继续执行下一个case分支的代码（不管是否匹配）"}
            ],
            "programming": [
                {"id": 1, "question": "编写一个Java程序，使用for循环计算1到100之间所有偶数的和并输出", "answer": "public class EvenSum {\n    public static void main(String[] args) {\n        int sum = 0;\n        for (int i = 1; i <= 100; i++) {\n            if (i % 2 == 0) {\n                sum += i;\n            }\n        }\n        System.out.println(\"1到100之间所有偶数的和为：\" + sum);\n    }\n}"},
                {"id": 2, "question": "编写一个Java程序，声明一个字符串数组，包含\"苹果\"、\"香蕉\"、\"橙子\"、\"葡萄\"四个元素，使用增强for循环遍历数组并打印每个元素", "answer": "public class FruitList {\n    public static void main(String[] args) {\n        String[] fruits = {\"苹果\", \"香蕉\", \"橙子\", \"葡萄\"};\n        for (String fruit : fruits) {\n            System.out.println(fruit);\n        }\n    }\n}"}
            ],
            "advanced": [
                {"id": 1, "question": "编写一个Java程序，输出九九乘法表。要求使用嵌套for循环", "answer": "public class MultiplicationTable {\n    public static void main(String[] args) {\n        for (int i = 1; i <= 9; i++) {\n            for (int j = 1; j <= i; j++) {\n                System.out.print(j + \"x\" + i + \"=\" + (i * j) + \"\\t\");\n            }\n            System.out.println();\n        }\n    }\n}"}
            ]
        },
        "第四章 面向对象基础": {
            "single_choice": [
                {"id": 1, "question": "下列哪种编程范式是Java语言主要采用的？", "options": ["A. 面向机器编程", "B. 面向过程编程", "C. 面向对象编程", "D. 函数式编程"], "answer": "C. 面向对象编程"},
                {"id": 2, "question": "类的声明使用哪个关键字？", "options": ["A. object", "B. class", "C. struct", "D. type"], "answer": "B. class"},
                {"id": 3, "question": "构造方法的名称必须满足什么条件？", "options": ["A. 与类名相同", "B. 以大写字母开头", "C. 以init开头", "D. 任意命名即可"], "answer": "A. 与类名相同"},
                {"id": 4, "question": "使用哪个关键字创建对象实例？", "options": ["A. create", "B. malloc", "C. new", "D. alloc"], "answer": "C. new"},
                {"id": 5, "question": "在Java中，方法参数传递的方式是？", "options": ["A. 值传递", "B. 引用传递", "C. 指针传递", "D. 地址传递"], "answer": "A. 值传递"},
                {"id": 6, "question": "下列哪个是方法重载的正确描述？", "options": ["A. 方法名相同，参数列表不同", "B. 方法名不同，参数列表相同", "C. 方法名相同，返回值类型不同", "D. 方法名相同，参数列表相同"], "answer": "A. 方法名相同，参数列表不同"},
                {"id": 7, "question": "this关键字的作用是？", "options": ["A. 调用父类构造方法", "B. 引用当前对象", "C. 创建新对象", "D. 释放当前对象"], "answer": "B. 引用当前对象"},
                {"id": 8, "question": "使用import语句的目的是？", "options": ["A. 定义包", "B. 导入其他包中的类", "C. 声明类", "D. 创建对象"], "answer": "B. 导入其他包中的类"},
                {"id": 9, "question": "下列哪个访问权限修饰符表示仅在本类中可见？", "options": ["A. public", "B. protected", "C. private", "D. 默认（无修饰符）"], "answer": "C. private"},
                {"id": 10, "question": "类成员（静态成员）使用哪个关键字修饰？", "options": ["A. final", "B. static", "C. abstract", "D. const"], "answer": "B. static"}
            ],
            "multiple_choice": [
                {"id": 1, "question": "以下关于面向对象编程特点的说法，正确的有？（多选）", "options": ["A. 封装", "B. 继承", "C. 多态", "D. 面向过程"], "answer": "ABC"},
                {"id": 2, "question": "类的成员包括哪些？（多选）", "options": ["A. 成员变量", "B. 方法", "C. 包", "D. 构造方法"], "answer": "ABD"},
                {"id": 3, "question": "关于构造方法，下列说法正确的有？（多选）", "options": ["A. 构造方法名称与类名相同", "B. 构造方法没有返回值类型", "C. 一个类只能有一个构造方法", "D. 构造方法在创建对象时自动调用"], "answer": "ABD"},
                {"id": 4, "question": "关于对象的组合，下列说法正确的有？（多选）", "options": ["A. 一个类的成员变量可以是另一个类的对象", "B. 对象组合体现了\"has-a\"关系", "C. 对象组合是一种代码复用方式", "D. 组合对象在创建时也会调用其构造方法"], "answer": "ABCD"},
                {"id": 5, "question": "关于实例成员和类成员，下列说法正确的有？（多选）", "options": ["A. 实例成员属于每个对象", "B. 类成员使用static修饰", "C. 类成员可以通过类名直接访问", "D. 实例方法中不能访问类成员"], "answer": "ABC"},
                {"id": 6, "question": "关于方法重载，下列说法正确的有？（多选）", "options": ["A. 方法名必须相同", "B. 参数列表必须不同（个数或类型）", "C. 返回值类型必须相同", "D. 可以发生在同一类中"], "answer": "ABD"},
                {"id": 7, "question": "关于this关键字，下列说法正确的有？（多选）", "options": ["A. this可以调用本类的构造方法", "B. this可以区分成员变量和局部变量", "C. this代表当前对象的引用", "D. this可以用于静态方法中"], "answer": "ABC"},
                {"id": 8, "question": "关于包语句，下列说法正确的有？（多选）", "options": ["A. package语句必须在源文件的第一行", "B. 包用于组织和管理类", "C. 同一个包中的类可以互相访问默认权限成员", "D. 一个源文件可以有多个package语句"], "answer": "ABC"},
                {"id": 9, "question": "关于import语句，下列说法正确的有？（多选）", "options": ["A. import语句位于package语句之后", "B. 可以使用import导入整个包中的所有类", "C. java.lang包中的类无需手动导入", "D. import语句可以导入不同包中的同名类"], "answer": "ABCD"},
                {"id": 10, "question": "关于访问权限修饰符，下列说法正确的有？（多选）", "options": ["A. private成员只能在本类中访问", "B. 默认权限成员可以在同包中访问", "C. protected成员可以在不同包的子类中访问", "D. public成员可以在任何地方访问"], "answer": "ABCD"}
            ],
            "short_answer": [
                {"id": 1, "question": "请说明实例变量和类变量（静态变量）的区别。", "answer": "实例变量属于对象，每个对象都有自己的一份实例变量，通过对象名访问；类变量使用static修饰，属于类本身，所有对象共享同一份类变量，可以通过类名直接访问"},
                {"id": 2, "question": "请说明什么是方法重载，并举例说明。", "answer": "方法重载是指在同一个类中定义多个同名的方法，但参数列表不同（参数个数不同或参数类型不同）。例如：public int add(int a, int b) 和 public double add(double a, double b) 构成了方法重载"}
            ],
            "programming": [
                {"id": 1, "question": "编写一个Student类，包含name和age两个成员变量，一个带参构造方法用于初始化这两个变量，以及一个display方法用于输出学生信息。再编写一个测试类TestStudent，在main方法中创建一个Student对象并调用display方法。要求两个类写在同一个文件中。", "answer": "class Student {\n    String name;\n    int age;\n    \n    public Student(String name, int age) {\n        this.name = name;\n        this.age = age;\n    }\n    \n    public void display() {\n        System.out.println(\"姓名：\" + name + \"，年龄：\" + age);\n    }\n}\n\npublic class TestStudent {\n    public static void main(String[] args) {\n        Student s = new Student(\"张三\", 18);\n        s.display();\n    }\n}"},
                {"id": 2, "question": "编写一个Counter类，包含一个静态变量count用于记录创建对象的次数，构造方法中使count自增，以及一个静态方法getCount用于返回count的值。再编写一个测试类TestCounter，在main方法中创建两个Counter对象，然后输出count的值。", "answer": "class Counter {\n    static int count = 0;\n    \n    public Counter() {\n        count++;\n    }\n    \n    public static int getCount() {\n        return count;\n    }\n}\n\npublic class TestCounter {\n    public static void main(String[] args) {\n        Counter c1 = new Counter();\n        Counter c2 = new Counter();\n        System.out.println(\"创建的对象数量：\" + Counter.getCount());\n    }\n}"}
            ],
            "advanced": [
                {"id": 1, "question": "编写一个Point类表示坐标点，包含x和y两个成员变量，一个无参构造方法（默认值为0,0）和一个带参构造方法。使用this关键字调用带参构造方法。再编写一个测试类TestPoint，创建两个Point对象（一个使用无参构造，一个使用带参构造），分别输出它们的坐标。要求两个类写在同一个文件中。", "answer": "class Point {\n    int x;\n    int y;\n    \n    public Point() {\n        this(0, 0);\n    }\n    \n    public Point(int x, int y) {\n        this.x = x;\n        this.y = y;\n    }\n    \n    public void display() {\n        System.out.println(\"坐标：(\" + x + \", \" + y + \")\");\n    }\n}\n\npublic class TestPoint {\n    public static void main(String[] args) {\n        Point p1 = new Point();\n        Point p2 = new Point(3, 5);\n        p1.display();\n        p2.display();\n    }\n}"}
            ]
        },
        "第五章 继承与多态": {
            "single_choice": [
                {"id": 1, "question": "在Java中，子类继承父类使用哪个关键字？", "options": ["A. extends", "B. implements", "C. super", "D. this"], "answer": "A. extends"},
                {"id": 2, "question": "Java中，一个子类最多可以有几个直接父类？", "options": ["A. 0个", "B. 1个", "C. 2个", "D. 多个"], "answer": "B. 1个"},
                {"id": 3, "question": "子类中可以定义与父类同名的成员变量，这种现象称为？", "options": ["A. 方法重写", "B. 方法重载", "C. 成员变量的隐藏", "D. 多态"], "answer": "C. 成员变量的隐藏"},
                {"id": 4, "question": "子类重写父类方法时，访问权限可以怎样变化？", "options": ["A. 只能保持不变", "B. 只能扩大不能缩小", "C. 只能缩小不能扩大", "D. 可以任意改变"], "answer": "B. 只能扩大不能缩小"},
                {"id": 5, "question": "super关键字的作用是？", "options": ["A. 引用当前对象", "B. 引用父类对象", "C. 创建子类对象", "D. 调用子类方法"], "answer": "B. 引用父类对象"},
                {"id": 6, "question": "使用final关键字修饰的类，其特点是？", "options": ["A. 可以被继承", "B. 不能被继承", "C. 只能有一个子类", "D. 必须有抽象方法"], "answer": "B. 不能被继承"},
                {"id": 7, "question": "对象的上转型对象是指？", "options": ["A. 子类对象赋值给父类变量", "B. 父类对象赋值给子类变量", "C. 将对象转换为基本类型", "D. 将对象序列化"], "answer": "A. 子类对象赋值给父类变量"},
                {"id": 8, "question": "多态的核心机制是？", "options": ["A. 编译时确定调用哪个方法", "B. 运行时根据实际对象类型确定调用哪个方法", "C. 总是调用父类方法", "D. 总是调用子类方法"], "answer": "B. 运行时根据实际对象类型确定调用哪个方法"},
                {"id": 9, "question": "abstract类的主要特点是？", "options": ["A. 不能被实例化", "B. 不能被继承", "C. 不能有构造方法", "D. 所有方法必须是抽象方法"], "answer": "A. 不能被实例化"},
                {"id": 10, "question": "下列关于abstract方法的描述，正确的是？", "options": ["A. 抽象方法必须有方法体", "B. 抽象方法必须在抽象类中", "C. 抽象方法不能被子类重写", "D. 抽象方法使用final修饰"], "answer": "B. 抽象方法必须在抽象类中"}
            ],
            "multiple_choice": [
                {"id": 1, "question": "关于子类与父类的关系，下列说法正确的有？（多选）", "options": ["A. 子类继承父类的所有成员", "B. 子类可以添加新的成员", "C. 子类可以重写父类的方法", "D. 一个子类可以有多个直接父类"], "answer": "ABC"},
                {"id": 2, "question": "子类能继承父类的哪些成员？（多选）", "options": ["A. public成员", "B. protected成员", "C. private成员", "D. 默认权限成员（同包时）"], "answer": "ABD"},
                {"id": 3, "question": "关于成员变量的隐藏，下列说法正确的有？（多选）", "options": ["A. 子类可以定义与父类同名的成员变量", "B. 隐藏后子类默认访问自己的变量", "C. 隐藏后父类的变量被删除", "D. 可以使用super访问被隐藏的父类变量"], "answer": "ABD"},
                {"id": 4, "question": "关于方法重写，下列说法正确的有？（多选）", "options": ["A. 子类方法名必须与父类相同", "B. 子类参数列表必须与父类相同", "C. 子类返回值类型必须与父类相同或是其子类型", "D. 重写是方法重载的一种"], "answer": "ABC"},
                {"id": 5, "question": "关于super关键字，下列说法正确的有？（多选）", "options": ["A. super可以调用父类的构造方法", "B. super可以调用父类的普通方法", "C. super可以访问父类的成员变量", "D. super可以在静态方法中使用"], "answer": "ABC"},
                {"id": 6, "question": "关于final关键字，下列说法正确的有？（多选）", "options": ["A. final修饰的类不能被继承", "B. final修饰的方法不能被重写", "C. final修饰的变量值不可改变", "D. final修饰的类中所有方法自动成为final"], "answer": "ABC"},
                {"id": 7, "question": "关于上转型对象，下列说法正确的有？（多选）", "options": ["A. 上转型对象可以调用父类的方法", "B. 上转型对象可以调用子类新增的方法", "C. 上转型对象调用重写方法时调用子类版本", "D. 上转型对象不能访问子类新增的成员变量"], "answer": "ACD"},
                {"id": 8, "question": "关于多态，下列说法正确的有？（多选）", "options": ["A. 多态依赖于方法重写", "B. 多态通过上转型对象实现", "C. 多态在运行时确定调用哪个方法", "D. 多态提高了代码的可扩展性"], "answer": "ABCD"},
                {"id": 9, "question": "关于abstract类，下列说法正确的有？（多选）", "options": ["A. 抽象类不能被实例化", "B. 抽象类中可以包含非抽象方法", "C. 抽象类必须包含抽象方法", "D. 抽象类可以有构造方法"], "answer": "ABD"},
                {"id": 10, "question": "关于抽象方法和抽象类，下列说法正确的有？（多选）", "options": ["A. 抽象方法使用abstract修饰", "B. 抽象方法没有方法体", "C. 包含抽象方法的类必须是抽象类", "D. 子类必须实现父类的所有抽象方法，否则子类也必须是抽象类"], "answer": "ABCD"}
            ],
            "short_answer": [
                {"id": 1, "question": "请说明方法重写（Override）和方法重载（Overload）的区别。", "answer": "方法重写发生在父子类之间，子类定义与父类同名、同参数列表、同返回值类型的方法，运行时根据对象实际类型调用；方法重载发生在同一类中，多个方法同名但参数列表不同，编译时确定调用哪个方法"},
                {"id": 2, "question": "请说明什么是对象的上转型对象，以及上转型对象的特点。", "answer": "上转型对象是指将子类对象赋值给父类类型的变量。其特点是：可以调用父类的方法和被子类重写的方法（调用子类版本），但不能调用子类新增的方法和成员变量"}
            ],
            "programming": [
                {"id": 1, "question": "编写一个父类Animal，包含一个makeSound方法输出\"动物发出声音\"。编写一个子类Dog继承Animal，重写makeSound方法输出\"小狗汪汪叫\"。编写测试类TestAnimal，创建Animal类型变量引用Dog对象，调用makeSound方法，体验多态。要求所有类写在同一个文件中。", "answer": "class Animal {\n    public void makeSound() {\n        System.out.println(\"动物发出声音\");\n    }\n}\n\nclass Dog extends Animal {\n    @Override\n    public void makeSound() {\n        System.out.println(\"小狗汪汪叫\");\n    }\n}\n\npublic class TestAnimal {\n    public static void main(String[] args) {\n        Animal animal = new Dog();\n        animal.makeSound();\n    }\n}"},
                {"id": 2, "question": "编写一个抽象类Shape，包含一个抽象方法area用于计算面积。编写两个子类Circle和Rectangle，分别实现area方法（Circle通过半径计算面积，Rectangle通过长和宽计算面积）。编写测试类TestShape，使用上转型对象分别创建Circle和Rectangle对象并输出面积。要求所有类写在同一个文件中。", "answer": "abstract class Shape {\n    public abstract double area();\n}\n\nclass Circle extends Shape {\n    double radius;\n    \n    public Circle(double radius) {\n        this.radius = radius;\n    }\n    \n    @Override\n    public double area() {\n        return 3.14 * radius * radius;\n    }\n}\n\nclass Rectangle extends Shape {\n    double length;\n    double width;\n    \n    public Rectangle(double length, double width) {\n        this.length = length;\n        this.width = width;\n    }\n    \n    @Override\n    public double area() {\n        return length * width;\n    }\n}\n\npublic class TestShape {\n    public static void main(String[] args) {\n        Shape s1 = new Circle(5);\n        Shape s2 = new Rectangle(4, 6);\n        System.out.println(\"圆的面积：\" + s1.area());\n        System.out.println(\"矩形的面积：\" + s2.area());\n    }\n}"}
            ],
            "advanced": [
                {"id": 1, "question": "编写一个父类Person，包含name和age两个成员变量，一个带参构造方法初始化这两个变量，以及一个display方法输出个人信息。编写一个子类Student继承Person，新增score成员变量，使用super调用父类构造方法，重写display方法输出包含成绩的个人信息。编写测试类TestPerson，创建一个Student对象并调用display方法。要求所有类写在同一个文件中。", "answer": "class Person {\n    String name;\n    int age;\n    \n    public Person(String name, int age) {\n        this.name = name;\n        this.age = age;\n    }\n    \n    public void display() {\n        System.out.println(\"姓名：\" + name + \"，年龄：\" + age);\n    }\n}\n\nclass Student extends Person {\n    double score;\n    \n    public Student(String name, int age, double score) {\n        super(name, age);\n        this.score = score;\n    }\n    \n    @Override\n    public void display() {\n        super.display();\n        System.out.println(\"成绩：\" + score);\n    }\n}\n\npublic class TestPerson {\n    public static void main(String[] args) {\n        Student student = new Student(\"李四\", 20, 92.5);\n        student.display();\n    }\n}"}
            ]
        }
    }

# 保存答案功能
def save_answer(chapter, question_type, question_id, answer):
    save_dir = "saved_answers"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    filename = os.path.join(save_dir, f"{chapter.replace(' ', '_')}.json")
    
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {}
    
    key = f"{question_type}_{question_id}"
    data[key] = answer
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return True

def load_saved_answers(chapter):
    filename = f"saved_answers/{chapter.replace(' ', '_')}.json"
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# AI解析功能（小米Mimo模型）
def call_ai_api(api_key, question, answer, model="mimo-v2-flash"):
    """调用AI模型解析题目"""
    api_key = "sk-crwl9fq9mkfdob19dznss9c8zdoyv4fz0a8gqftbvhg23j8c"
    
    try:
        import requests
        
        url = "https://api.xiaomimimo.com/v1/chat/completions"  # 假设的API端点，请根据实际调整
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"请简单解析这道Java题目，并解释正确答案的原因：\n\n题目：{question}\n"
        
        # 2. 如果有选项，则添加选项部分（仅选择题）
        if options:
            options_text = "\n".join(options)  # 将选项列表转换为多行文本
            prompt += f"选项：\n{options_text}\n"
        
        # 3. 添加正确答案
        prompt += f"正确答案：{answer}\n\n"
        
        # 4. 添加解析要求
        prompt += """请从以下几个方面进行解析：
1. 题目考察的知识点
2. 每个选项的分析（如果有选项的话）
3. 为什么正确答案是正确的
4. 要求内容简洁，不冗长

请用中文回答，保持专业且易懂。"""

        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": "你是一位专业的Java编程教育专家，擅长用清晰简洁的方式解释编程概念。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2048
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
        
    except ImportError:
        return "请安装requests库: pip install requests"
    except requests.exceptions.Timeout:
        return "请求超时，请检查网络连接"
    except requests.exceptions.RequestException as e:
        return f"API调用失败: {str(e)}"
    except Exception as e:
        return f"发生错误: {str(e)}"

# 渲染题目
def render_question(question, q_type, q_index, chapter, saved_answers, api_key):
    col1, col2 = st.columns([9, 1])
    with col1:
        st.markdown(f"**{q_type} {q_index+1}.** {question['question']}")
    
    if "options" in question:
        for opt in question["options"]:
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;{opt}")
    
    # 答案折叠区域
    with st.expander("📝 查看答案", expanded=False):
        st.markdown(f"<div class='answer-box'><strong>✅ 答案：</strong>{question['answer']}</div>", unsafe_allow_html=True)
        
        # AI解析按钮
        if st.button(f"🤖 AI解析", key=f"ai_{chapter}_{q_type}_{q_index}"):
            with st.spinner("正在调用AI模型解析..."):
                # 根据题目类型决定是否传递 options
                if q_type in ["单选题", "多选题"] and "options" in question:
                    # 选择题：传递选项列表
                    analysis = call_ai_api(
                        question=question['question'],
                        answer=question['answer'],
                        options=question['options']  # 传递选项列表
                    )
                else:
                    # 简答题、编程题：不传递 options
                    analysis = call_ai_api(
                        question=question['question'],
                        answer=question['answer']
                    )
                st.markdown(f"<div class='ai-analysis'><strong>🧠 AI解析：</strong><br>{analysis}</div>", unsafe_allow_html=True)
    
    # 简答题和编程题显示解答框
    if q_type in ["简答题", "编程题", "进阶编程题"]:
        key = f"answer_{chapter}_{q_type}_{question['id']}"
        saved_value = saved_answers.get(f"{q_type}_{question['id']}", "")
        
        # 使用HTML禁止粘贴
        st.text_area(
            "✏️ 输入你的答案",
            value=saved_value,
            key=key,
            height=150 if q_type == "简答题" else 250,
            help="请在此输入你的答案（禁止粘贴）"
        )
        
        # 保存按钮
        if st.button(f"💾 保存答案", key=f"save_{chapter}_{q_type}_{question['id']}"):
            answer_text = st.session_state.get(key, "")
            if save_answer(chapter, q_type, question['id'], answer_text):
                st.success("✅ 答案已保存！")
            else:
                st.error("❌ 保存失败")
    
    st.divider()

# 主程序
def main():
    st.title("☕ Java 题库系统")
    st.markdown("---")
    
    # 侧边栏配置
    with st.sidebar:
        #st.header("⚙️ 设置")
        api_key = "sk-crwl9fq9mkfdob19dznss9c8zdoyv4fz0a8gqftbvhg23j8c"
        
        st.markdown("---")
        st.markdown("### 📊 使用说明")
        st.markdown("""
        1. 点击标签页切换章节
        2. 点击「查看答案」展开答案
        3. 点击「AI解析」获取详细解析
        4. 在简答题/编程题下方输入答案
        5. 点击「保存答案」本地保存
        """)
        
        st.markdown("---")
        st.markdown("### 📁 已保存答案")
        if st.button("📂 查看所有已保存答案"):
            save_dir = "saved_answers"
            if os.path.exists(save_dir):
                files = os.listdir(save_dir)
                if files:
                    for f in files:
                        with open(os.path.join(save_dir, f), 'r', encoding='utf-8') as file:
                            data = json.load(file)
                            st.write(f"📄 {f.replace('.json', '')}: {len(data)} 条")
                else:
                    st.info("暂无已保存的答案")
            else:
                st.info("暂无已保存的答案")
    
    # 获取题库数据
    chapters = get_chapter_data()
    chapter_names = list(chapters.keys())
    
    # 创建标签页
    tabs = st.tabs(chapter_names)
    
    for i, tab in enumerate(tabs):
        with tab:
            chapter_name = chapter_names[i]
            chapter_data = chapters[chapter_name]
            
            st.header(f"📚 {chapter_name}")
            
            # 加载已保存的答案
            saved_answers = load_saved_answers(chapter_name)
            
            # 单选题
            st.subheader("📝 单选题")
            for j, q in enumerate(chapter_data["single_choice"]):
                render_question(q, "单选题", j, chapter_name, saved_answers, api_key)
            
            # 多选题
            st.subheader("📝 多选题")
            for j, q in enumerate(chapter_data["multiple_choice"]):
                render_question(q, "多选题", j, chapter_name, saved_answers, api_key)
            
            # 简答题
            st.subheader("📝 简答题")
            for j, q in enumerate(chapter_data["short_answer"]):
                render_question(q, "简答题", j, chapter_name, saved_answers, api_key)
            
            # 编程题
            st.subheader("📝 编程题")
            for j, q in enumerate(chapter_data["programming"]):
                render_question(q, "编程题", j, chapter_name, saved_answers, api_key)
            
            # 进阶编程题
            if "advanced" in chapter_data and chapter_data["advanced"]:
                st.subheader("📝 进阶编程题")
                for j, q in enumerate(chapter_data["advanced"]):
                    render_question(q, "进阶编程题", j, chapter_name, saved_answers, api_key)

if __name__ == "__main__":
    main()