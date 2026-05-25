import argparse
import subprocess
import sys
import time
import requests
from pathlib import Path


def wait_for_server(url: str, timeout: int = 60):
    print(f"正在等待 {url} 上线...")
    start_time = time.time()
    while True:
        try:
            response = requests.get(url, timeout=1)
            print(f"服务器 {url} 已成功响应！(状态码: {response.status_code})")
            return
        except requests.exceptions.RequestException:
            if time.time() - start_time > timeout:
                raise TimeoutError(f"等待服务器 {url} 上线超时（{timeout}秒）。")
            time.sleep(0.5)


def main():
    parser = argparse.ArgumentParser(description="Hugo CI 构建脚本")
    parser.add_argument("--base-url", required=True,
                        help="对应 steps.pages.outputs.base_url")
    parser.add_argument("--runner-temp", required=True, help="对应 runner.temp")
    args = parser.parse_args()
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    print(f"工作目录信息:\n - 脚本目录: {script_dir}\n - 根目录: {project_root}")
    server_process = None
    try:
        print("正在启动后台 HTTP 服务器 (uv run main.py)...")
        server_process = subprocess.Popen(
            ["uv", "run", "main.py"],
            cwd=script_dir
        )
        wait_for_server("http://127.0.0.1:8964/ping", timeout=10)
        if server_process.poll() is not None:
            raise RuntimeError(
                f"HTTP 服务器启动后意外退出，退出码: {server_process.returncode}")
        hugo_command = [
            "hugo", "build",
            "--gc",
            "--minify",
            "--baseURL", f"{args.base_url}/",
            "--cacheDir", f"{args.runner_temp}/hugo_cache"
        ]
        print(f"正在执行 Hugo 构建命令: {' '.join(hugo_command)}")
        subprocess.run(hugo_command, cwd=project_root, check=True)
        print("Hugo 构建成功完成！")
    except subprocess.CalledProcessError as e:
        print(f"Hugo 构建失败，退出码: {e.returncode}", file=sys.stderr)
        sys.exit(e.returncode)
    except Exception as e:
        print(f"脚本执行过程中发生错误: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if server_process is not None:
            if server_process.poll() is None:
                print("正在关闭后台 HTTP 服务器...")
                server_process.terminate()
                try:
                    server_process.wait(timeout=10)
                    print("后台服务器已安全关闭。")
                except subprocess.TimeoutExpired:
                    print("服务器未能在规定时间内响应关闭信号，正在强制终止 (kill)...", file=sys.stderr)
                    server_process.kill()
                    server_process.wait()
            else:
                if server_process.returncode != 0:
                    print(
                        f"警告: HTTP 服务器以非正常状态退出，退出码: {server_process.returncode}", file=sys.stderr)
                    sys.exit(server_process.returncode)


if __name__ == "__main__":
    main()
