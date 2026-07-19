# -*- coding: utf-8 -*-
#
# Copyright (c) 2026 yangyangkeai
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import json
from pathlib import Path

from google import genai


# ===========================
# 可编辑 Prompt
# ===========================
PROMPT = """
你是一名专业的HTML解析专家。我将提供的是一段HTML内容。

你的任务：
提取该HTML的关键信息，将内容整理成JSON对象，格式大概是这样子：
  "page-container": {
    "description": "页面容器，“假页”容器组件，效果类似于 popup 弹出层，页面内存在该容器时，当用户进行返回操作，关闭该容器不关闭页面。返回操作包括三种情形，右滑手势、安卓物理返回键和调用 navigateBack 接口。",
    "attributeDescriptors": [
      {
        "key": "duration",
        "types": [
          "NUMBER"
        ],
        "default": 300,
        "required": false,
        "enums": [],
        "requiredInEnums": true,
        "description": "动画时长，单位毫秒。"
      },
      {
        "key": "z-index",
        "types": [
          "NUMBER"
        ],
        "default": 100,
        "required": false,
        "enums": [],
        "requiredInEnums": true,
        "description": "z-index 层级"
      },
      {
        "key": "overlay",
        "types": [
          "BOOLEAN"
        ],
        "default": true,
        "required": false,
        "enums": [],
        "requiredInEnums": true,
        "description": "是否显示遮罩层。"
      },
      {
        "key": "position",
        "types": [
          "STRING"
        ],
        "default": "bottom",
        "required": false,
        "enums": [
          "top",
          "bottom",
          "right",
          "center"
        ],
        "requiredInEnums": true,
        "description": "弹出位置。"
      }
    ],
    "events": [
      "beforeenter",
      "enter"
    ],
    "canOpen": true,
    "canClose": false,
    "url": "https://developers.weixin.qq.com/miniprogram/dev/component/page-container.html"
  }

要求：
1. 返回纯JSON
2. 不要输出Markdown
3. 不要输出```json
4. 不要输出任何解释

HTML内容：
----------------
{{CONTENT}}
----------------

当前的标签（属性名/对象名）：{{TAG}}

"""


def main():
    api_key = (
        os.getenv("_GOOGLE_API_KEY")
    )

    if not api_key:
        print("错误：未找到 Google API Key。")
        print("请设置环境变量：")
        print("Windows:")
        print("    set _GOOGLE_API_KEY=你的Key")
        print("Linux/macOS:")
        print("    export _GOOGLE_API_KEY=你的Key")
        print("powershell:")
        print("    $env:_GOOGLE_API_KEY='你的Key'")
        return

    client = genai.Client(api_key=api_key)

    output_dir = Path("output")

    if not output_dir.exists():
        print("output 目录不存在。")
        return

    html_files = sorted(output_dir.glob("*.html"))

    if not html_files:
        print("没有找到 html 文件。")
        return

    for html_file in html_files:
        tag = html_file.stem

        print(f"处理：{tag}")

        content = html_file.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        prompt = PROMPT.replace("{{CONTENT}}", content).replace("{{TAG}}", tag)

        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt,
            )

            result = response.text

            json_file = output_dir / f"{tag}.json"

            # 如果模型返回的是合法JSON，则格式化保存
            try:
                obj = json.loads(result)

                with open(json_file, "w", encoding="utf-8") as f:
                    json.dump(
                        obj,
                        f,
                        ensure_ascii=False,
                        indent=2
                    )
            except Exception:
                # 不是合法JSON则原样保存
                with open(json_file, "w", encoding="utf-8") as f:
                    f.write(result)

            print(f"完成：{json_file.name}")

        except Exception as e:
            print(f"{tag} 处理失败：{e}")


if __name__ == "__main__":
    main()