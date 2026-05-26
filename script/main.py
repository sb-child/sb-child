import re
import requests
import base64
import uvicorn
# import nh3
from pathlib import Path
from typing import Callable
from datetime import datetime
from fastapi import FastAPI
from markdown_it import MarkdownIt
from mdit_py_plugins.anchors import anchors_plugin


app = FastAPI()
md = MarkdownIt("commonmark")
anchors_plugin(md, min_level=1, max_level=6)
md_link_pattern = re.compile(r"\[(.*?)\]\((.*?)\)", flags=re.MULTILINE)


def match_root(m: str, p: str) -> bool:
    return m == p or m == f"/{p}" or m == f"./{p}"


def fetch_gh_file(
    repo: str,
    file: str,
    branch: str | None = None,
    tag: str | None = None,
    rev: str | None = None
) -> dict:
    """
    从 GitHub 仓库下载指定文件，并返回内容、实际使用的修订号(commit SHA)和最后更新时间。

    :param repo: 格式为 "owner/repo_name" 的字符串，例如 "encode/httpx"
    :param file: 仓库内的文件路径，例如 "README.md" 或 "src/main.py"
    """
    provided_params = [p for p in [branch, tag, rev] if p is not None]
    ref = provided_params[0] if len(provided_params) == 1 else None
    base_url = f"https://api.github.com/repos/{repo}"
    gh_api_token_file = Path(".gh_api_token")
    if gh_api_token_file.is_file():
        try:
            with open(gh_api_token_file) as f:
                gh_api_token = f.read().strip()
        except Exception as e:
            print("读取 gh_api_token 失败: {e}")
            gh_api_token = None
    else:
        gh_api_token = None
    headers = {"Accept": "application/vnd.github.v3+json"}
    if gh_api_token:
        print("使用 gh_api_token")
        headers["Authorization"] = f"Bearer {gh_api_token}"
    content_url = f"{base_url}/contents/{file}"
    content_params = {}
    if ref:
        content_params["ref"] = ref
    content_res = requests.get(
        content_url, headers=headers, params=content_params)
    if content_res.status_code == 404:
        raise FileNotFoundError(f"找不到指定的仓库、分支或文件: {repo}/{file} (ref: {ref})")
    elif content_res.status_code != 200:
        raise RuntimeError(
            f"GitHub API 请求失败，状态码: {content_res.status_code}, 错误信息: {content_res.text}")
    content_json = content_res.json()
    if isinstance(content_json, list) or content_json.get("type") != "file":
        raise ValueError(f"指定的路径 '{file}' 不是一个标准文件。")
    encoded_content = content_json.get("content", "")
    try:
        decoded_bytes = base64.b64decode(encoded_content.replace("\n", ""))
        content_str = decoded_bytes.decode("utf-8", errors="replace")
    except Exception as e:
        content_str = f"文件解码失败: {e}"
    commits_url = f"{base_url}/commits"
    commits_params = {"path": file, "per_page": 1}
    if ref:
        commits_params["sha"] = ref
    commits_res = requests.get(
        commits_url, headers=headers, params=commits_params)
    if commits_res.status_code != 200:
        raise RuntimeError(f"无法获取文件的提交历史，状态码: {commits_res.status_code}")
    commits_json = commits_res.json()
    if not commits_json:
        raise FileNotFoundError(f"未能找到文件 '{file}' 的提交历史。")
    last_commit = commits_json[0]
    actual_rev = last_commit.get("sha")
    commit_date_str = last_commit.get(
        "commit", {}).get("committer", {}).get("date")
    if commit_date_str:
        commit_date_str = commit_date_str.replace("Z", "+00:00")
        dt = datetime.fromisoformat(commit_date_str)
        updated_at_timestamp = int(dt.timestamp())
    else:
        updated_at_timestamp = 0
    return {
        "content": content_str,
        "rev": actual_rev,
        "updated_at": updated_at_timestamp
    }


def md_reloc(src_text: str, proc: Callable[[str], str]) -> str:
    def rep(g1, g2):
        # g1_new =
        g2_new = proc(g2)
        return g1, g2_new

    def repl_func(match):
        g1 = match.group(1)
        g2 = match.group(2)
        g1_new, g2_new = rep(g1, g2)
        return f"[{g1_new}]({g2_new})"

    result = md_link_pattern.sub(repl_func, src_text)
    return result


def md_to_html(src_text: str) -> str:
    html_content = md.render(src_text)
    # html_content = nh3.clean(html_content)
    return html_content


@app.get("/ping")
def ping():
    return {'hello': 'pong'}


@app.get("/func_the_forge_of_trans")
def func_the_forge_of_trans(root_url: str = "/"):
    base = root_url.rstrip('/')
    src = fetch_gh_file("sb-child/notes", "trans.md")
    src_content = src["content"]
    src_rev = src["rev"]
    src_updated_at = src["updated_at"]

    def rep(link: str) -> str:
        s = link.split("#", 2)
        link = s[0]
        hash = "" if len(s) == 1 else s[1]
        # 没有上一个层级了
        if match_root(link, "README.md"):
            return "#top"
        # 资源
        if link.startswith("assets/"):
            return f"https://github.com/sb-child/notes/blob/main/{link}"
        # 药
        if match_root(link, "sleep.md") or match_root(link, "medicine2.md") or match_root(link, "medicine.md"):
            return f"https://github.com/sb-child/notes/blob/main/{link}#{hash}"
        # emo
        if match_root(link, "emo.md"):
            return f"{base}/trans/emotional-damage"
        # 传记
        if match_root(link, "mention/README.md") or match_root(link, "mention") or match_root(link, "mention/"):
            return f"{base}/trans/mention"
        if match_root(link, "mention/person-huai-xu.md"):
            return f"{base}/trans/mention/person-huai-xu#" + hash
        if match_root(link, "mention/person-li-yongmin.md"):
            return f"{base}/trans/mention/person-li-yongmin#" + hash
        # 倾听药娘的故事
        if match_root(link, "trans-story.md"):
            return f"{base}/trans/story"
        return f"{link}#{hash}"

    src_content_converted = md_reloc(src_content, rep)
    src_content_html = md_to_html(src_content_converted)
    return {
        'content': src_content_html,
        'rev': src_rev,
        'updated_at': src_updated_at,
    }


@app.get("/func_emotional_damage")
def func_emotional_damage(root_url: str = "/"):
    base = root_url.rstrip('/')
    src = fetch_gh_file("sb-child/notes", "emo.md")
    src_content = src["content"]
    src_rev = src["rev"]
    src_updated_at = src["updated_at"]

    def rep(link: str) -> str:
        s = link.split("#", 2)
        link = s[0]
        hash = "" if len(s) == 1 else s[1]
        # 回去
        if match_root(link, "README.md"):
            return f"{base}/trans"
        if match_root(link, "trans.md"):
            return f"{base}/trans#{hash}"
        return f"{link}#{hash}"

    src_content_converted = md_reloc(src_content, rep)
    src_content_html = md_to_html(src_content_converted)
    return {
        'content': src_content_html,
        'rev': src_rev,
        'updated_at': src_updated_at,
    }


@app.get("/func_trans_story")
def func_trans_story(root_url: str = "/"):
    base = root_url.rstrip('/')
    src = fetch_gh_file("sb-child/notes", "trans-story.md")
    src_content = src["content"]
    src_rev = src["rev"]
    src_updated_at = src["updated_at"]

    def rep(link: str) -> str:
        s = link.split("#", 2)
        link = s[0]
        hash = "" if len(s) == 1 else s[1]
        # 回去
        if match_root(link, "README.md"):
            return f"{base}/trans"
        if match_root(link, "trans.md"):
            return f"{base}/trans#{hash}"
        # 资源
        if link.startswith("assets/"):
            return f"https://github.com/sb-child/notes/blob/main/{link}"
        return f"{link}#{hash}"

    src_content_converted = md_reloc(src_content, rep)
    src_content_html = md_to_html(src_content_converted)
    return {
        'content': src_content_html,
        'rev': src_rev,
        'updated_at': src_updated_at,
    }


def main():
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8964)
