import os

def to_rtf(text):
    result = []
    for char in text:
        code = ord(char)
        if code > 127:
            if code > 32767:
                code -= 65536
            result.append(f'\\u{code}?')
        elif char == '\\':
            result.append('\\\\')
        elif char == '{':
            result.append('\\{')
        elif char == '}':
            result.append('\\}')
        else:
            result.append(char)
    return ''.join(result)

def title(text, size=48):
    return f'\\pard\\qc\\sb400\\sa200{{\\b\\fs{size} {to_rtf(text)}}}\\par\n'

def heading1(text):
    return f'\\pard\\sb360\\sa160\\brdrb\\brdrs\\brdrw10\\brsp40{{\\b\\fs36\\cf1 {to_rtf(text)}}}\\par\n'

def heading2(text):
    return f'\\pard\\sb300\\sa120{{\\b\\fs30\\cf1 {to_rtf(text)}}}\\par\n'

def heading3(text):
    return f'\\pard\\sb240\\sa100{{\\b\\fs26\\cf2 {to_rtf(text)}}}\\par\n'

def para(text, indent=0):
    li = f'\\li{indent}' if indent else ''
    return f'\\pard\\sa120{li}\\fs22 {to_rtf(text)}\\par\n'

def bold_para(text, indent=0):
    li = f'\\li{indent}' if indent else ''
    return f'\\pard\\sa120{li}{{\\b\\fs22 {to_rtf(text)}}}\\par\n'

def bullet(text, indent=360):
    return f'\\pard\\li{indent}\\fi-240\\sa80\\fs22 \\bullet  {to_rtf(text)}\\par\n'

def quote_block(text):
    return f'\\pard\\li480\\ri480\\sa100\\fs22\\cf2\\i {to_rtf(text)}\\i0\\cf0\\par\n'

def separator():
    return '\\pard\\sb200\\sa200\\brdrb\\brdrs\\brdrw5\\brsp20\\par\n'

def table_row(cells, bold=False, bg_color=0):
    n = len(cells)
    widths = {
        2: [3800, 5700],
        3: [2800, 3200, 3500],
        6: [1200, 2600, 2600, 1200, 1200, 700],
    }
    w = widths.get(n, [int(9500/n)] * n)
    
    row = '\\trowd\\trqc\\trgaph80\n'
    pos = 0
    for i in range(n):
        pos += w[i]
        border = '\\clbrdrt\\brdrs\\brdrw5\\clbrdrb\\brdrs\\brdrw5\\clbrdrl\\brdrs\\brdrw5\\clbrdrr\\brdrs\\brdrw5'
        bg = f'\\clcbpat{bg_color}' if bg_color else ''
        row += f'{border}{bg}\\cellx{pos}\n'
    
    row += '\\pard\\intbl\\sa40\\sb40\\fs20'
    for cell in cells:
        fmt = '{\\b ' + to_rtf(cell) + '}' if bold else to_rtf(cell)
        row += f' {fmt}\\cell\n'
    row += '\\row\n'
    return row

# ====== Build the RTF document ======

rtf = '{\\rtf1\\ansi\\ansicpg936\\deff0\n'

# Font table
rtf += '{\\fonttbl'
rtf += '{\\f0\\fswiss\\fcharset134 Microsoft YaHei;}'
rtf += '{\\f1\\fmodern\\fcharset134 Consolas;}'
rtf += '}\n'

# Color table
rtf += '{\\colortbl;'
rtf += '\\red0\\green82\\blue155;'    # 1: blue for headings
rtf += '\\red100\\green100\\blue100;'  # 2: gray for subtitles
rtf += '\\red255\\green255\\blue255;'  # 3: white
rtf += '\\red230\\green240\\blue250;'  # 4: light blue bg
rtf += '\\red220\\green53\\blue69;'    # 5: red accent
rtf += '\\red40\\green167\\blue69;'    # 6: green accent
rtf += '\\red0\\green0\\blue0;'        # 7: black
rtf += '}\n'

# Default font & margins
rtf += '\\margl1440\\margr1440\\margt1440\\margb1440\n'
rtf += '\\f0\\fs22\n'

# ===== Title =====
rtf += '\\pard\\qc\\sb600\\sa100{\\b\\fs52\\cf1 WebUACAD AI Agent}\\par\n'
rtf += '\\pard\\qc\\sa80{\\fs28\\cf2 ' + to_rtf('浏览器中的智能 CAD 专家：从绘图到深度解析') + '}\\par\n'
rtf += '\\pard\\qc\\sa300{\\fs24\\cf2 ' + to_rtf('安全 · 智能 · 零安装 — 重新定义 AI CAD 的交互方式') + '}\\par\n'

rtf += separator()

# ===== Section 1 =====
rtf += heading1('AI Agent 正在改变世界，但你的电脑安全吗？')

rtf += para('过去一年，AI Agent（智能体）概念席卷全球。越来越多的产品声称可以"替你操作电脑"——自动点击、自动输入、自动执行命令。听起来很美好，但背后隐藏着巨大的安全隐患：')

rtf += bullet('它们需要操作系统级别的权限，能读取你的文件、访问你的剪贴板、甚至控制你的键盘和鼠标')
rtf += bullet('它们像后台进程一样运行，你无法确知它在做什么、访问了什么数据')
rtf += bullet('一旦被攻击或误用，后果等同于电脑被植入了一个拥有完整权限的"合法病毒"')

rtf += bold_para('我们认为，这不是 AI Agent 应有的样子。')

rtf += separator()

# ===== Section 2 =====
rtf += heading1('WebUACAD：在浏览器沙箱中运行的 AI 智能体')

rtf += para('WebUACAD AI Agent 采用了完全不同的技术路线。我们基于 WebAssembly (WASM) 技术，将专业级 CAD 引擎编译到浏览器中运行。')

# Comparison table
rtf += '\\pard\\sb200\\sa80{\\b\\fs22 ' + to_rtf('安全对比一览：') + '}\\par\n'

headers = ['', '桌面端 AI Agent', 'WebUACAD AI Agent']
rtf += table_row(headers, bold=True, bg_color=4)
rows = [
    ('运行环境', '操作系统进程，拥有完整系统权限', '浏览器沙箱，受严格安全策略保护'),
    ('文件访问', '可读写本地任意文件', '仅限浏览器沙箱内存空间'),
    ('安装要求', '需下载安装包，授予管理员权限', '打开网页即用，零安装'),
    ('数据安全', '数据经本地 Agent 处理，存在泄露风险', '图纸数据在浏览器内存中处理，关闭标签页即释放'),
    ('攻击面', '操作系统级，后果严重', '浏览器级，受同源策略和沙箱机制保护'),
    ('更新维护', '需用户手动更新客户端', '服务端部署，用户始终使用最新版本'),
]
for row in rows:
    rtf += table_row(list(row))

rtf += '\\pard\\sb160\\sa120\n'
rtf += bold_para('浏览器就是我们的安全边界。你的操作系统、你的文件系统、你的隐私数据——我们的 Agent 碰不到，也不需要碰。')

rtf += separator()

# ===== Section 3 =====
rtf += heading1('用自然语言绘制专业 CAD 图纸')

rtf += para('WebUACAD 不仅仅是安全的——它同样强大。你可以用自然语言与 AI 对话，像指挥一位经验丰富的绘图员一样，让它帮你完成专业级 CAD 绘图：')

rtf += quote_block('你说："画一个 200×100 的矩形，在其中心画一个半径为 30 的圆"')
rtf += quote_block('AI 做到：自动理解空间关系，调用 CAD 命令精确绘制，结果即刻呈现在画布上')

rtf += para('支持的绘图能力包括：直线、圆、矩形、多段线、圆弧、椭圆、正多边形、圆环、文字标注等全套基础绘图命令。AI 可以在一次对话中完成多步复合操作，从简单图形到复杂图纸，自然语言即是你的命令行。')

rtf += separator()

# ===== Section 4 =====
rtf += heading1('超越绘图：深度图纸理解与智能分析')

rtf += para('传统的 AI 绘图工具只能"盲写"代码，而 WebUACAD 赋予了 AI "看懂"图纸的能力。通过内置的智能查询与分析引擎，AI Agent 能够像专业工程师一样审查和理解复杂的 CAD 模型：')

rtf += bullet('全局认知与空间检索：AI 能够自动获取图纸的全局摘要（图层、块定义、实体总数），并支持基于空间范围（Bounding Box）的局部检索，精准定位"右下角标题栏"或"特定坐标区域"的图元。')
rtf += bullet('深度属性提取：不仅仅是几何形状，AI 可以提取图元的详细属性，如多段线的面积、块引用的属性值（Attributes）以及文字内容，为工程算量和数据统计提供支持。')
rtf += bullet('拓扑关系与碰撞检测：AI 能够分析图元之间的空间拓扑关系，自动进行干涉检查和碰撞检测，例如审查"管道是否穿墙"或"轮廓是否闭合"。')

rtf += separator()

# ===== Section 5 =====
rtf += heading1('契约驱动与闭环修复：确保工程级准确性')

rtf += para('在工程领域，"差不多"是不可接受的。WebUACAD 引入了先进的契约驱动（Contract-driven）执行机制，确保 AI 生成的图纸符合严格的几何与拓扑规则：')

rtf += bullet('闭环验证机制：当 AI 尝试执行非法的几何操作（如半径为负、线条自相交）时，系统会拦截错误并反馈给 AI，触发其进行自我修正（Self-Correction），直至满足工程契约。')
rtf += bullet('高阶参数化宏工具：摒弃低效的单步绘制，提供阵列、倒角、布尔运算等高阶宏指令。把复杂的几何计算交给底层引擎，让 AI 专注于理解你的设计意图，大幅降低幻觉，提升一次性成图率。')

rtf += separator()

# ===== Section 6 =====
rtf += heading1('技术架构：专业且透明')

rtf += '\\pard\\sb100\\sa160\\qc{\\f1\\fs22\\cf1 ' + to_rtf('用户自然语言 → LLM 智能理解与规划 → 工具调用与闭环验证 → WASM 引擎浏览器端执行 → 实时渲染') + '}\\par\n'

rtf += bullet('前端：React 构建的现代化 UI，工业级 WASM 引擎提供专业 CAD 渲染与几何计算能力')
rtf += bullet('后端：轻量 Node.js 服务，仅负责 AI 对话中转与 Agent 状态管理，不接触图纸数据')
rtf += bullet('AI：支持 GPT-4o、Claude 3.5、DeepSeek 等多种大语言模型，灵活切换')
rtf += bullet('RAG 知识库：内置 CAD 专业知识检索，AI 回答更精准、更专业')

rtf += para('API Key 安全保管在服务端，前端不接触任何密钥；图纸数据全程在浏览器内存中处理，不上传到任何第三方服务器。')

rtf += separator()

# ===== Section 7 =====
rtf += heading1('为什么选择 WebUACAD？')

rtf += heading3('对于企业用户')
rtf += bullet('无需在员工电脑上安装任何软件，降低 IT 管理成本')
rtf += bullet('图纸数据不离开浏览器，满足数据安全合规要求')
rtf += bullet('统一部署、统一更新，确保全员使用最新版本')

rtf += heading3('对于个人用户')
rtf += bullet('打开浏览器就能用，不占系统资源')
rtf += bullet('不用担心 AI Agent 在后台"偷偷做事"')
rtf += bullet('随时随地，任何设备，只要有浏览器就能绘图')

rtf += heading3('对于开发者')
rtf += bullet('开放的工具扩展体系，轻松添加新的 CAD 命令与分析工具')
rtf += bullet('支持多种 LLM 后端，一行配置即可切换')
rtf += bullet('前后端分离架构，可独立扩展和部署')

rtf += separator()

# ===== Vision =====
rtf += heading1('我们的愿景')

rtf += quote_block('让 AI 的力量服务于创造，而非侵入你的电脑。')

rtf += para('WebUACAD 证明了一件事：AI Agent 不需要获得你操作系统的控制权，也能为你完成专业的工作。浏览器沙箱为 AI 的能力划定了清晰的安全边界——在这个边界之内，AI 可以自由地理解你的意图、精确地执行绘图命令、深度分析复杂的工程图纸；在这个边界之外，你的系统、你的数据、你的隐私，安然无恙。')

rtf += para('这不仅是一款产品，更是我们对 AI Agent 安全范式的回答：')

rtf += '\\pard\\qc\\sb200\\sa200{\\b\\fs28\\cf1 ' + to_rtf('强大，但不越界。智能，且值得信赖。') + '}\\par\n'

rtf += separator()

rtf += '\\pard\\qc\\sb300\\sa100{\\i\\fs24\\cf2 WebUACAD AI Agent ' + to_rtf('— 专业 CAD 绘图与分析，就在你的浏览器中。') + '}\\par\n'

# Close RTF
rtf += '}'

# Write file
output_path = os.path.join(os.path.dirname(__file__), 'WebUACAD_AI_Agent_Promo_V2.rtf')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(rtf)

print(f'RTF file generated: {output_path}')
