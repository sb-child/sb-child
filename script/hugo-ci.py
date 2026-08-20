import argparse
import subprocess
import sys
import time
from pathlib import Path
import requests


def wait_for_server(url: str, timeout: int = 60):
    print(f"Waiting for {url} to be ready...")
    start_time = time.time()

    while True:
        try:
            resp = requests.get(url, timeout=1)
            print(f"Server is up! (status: {resp.status_code})")
            return
        except requests.exceptions.RequestException:
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Timed out waiting for {url} after {timeout}s")
            time.sleep(0.5)


def run_cmd(cmd: list[str], cwd: Path, description: str = ""):
    """辅助函数：执行命令并在失败时打印直观提示"""
    if description:
        print(f"==> {description}")
    print(f"$ {' '.join(cmd)}")

    res = subprocess.run(cmd, cwd=cwd)
    if res.returncode != 0:
        print(f"Error: Command failed with exit code {res.returncode}", file=sys.stderr)
        sys.exit(res.returncode)


def main():
    parser = argparse.ArgumentParser(description="Hugo site build script")
    parser.add_argument("--base-url", required=True, help="Base URL for Hugo build")
    parser.add_argument(
        "--runner-temp", required=True, help="Runner temporary directory"
    )
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    print(f"Workdir: {project_root}")
    print(f"Script dir: {script_dir}")

    server_proc = None

    try:
        # 1. 启动后台服务器
        print("Starting backend server (uv run main.py)...")
        server_proc = subprocess.Popen(["uv", "run", "main.py"], cwd=script_dir)

        wait_for_server("http://127.0.0.1:8964/ping", timeout=10)

        if server_proc.poll() is not None:
            raise RuntimeError(
                f"Backend exited early with code {server_proc.returncode}"
            )

        # 2. 前置构建步骤：Svelte 组件与前端依赖
        run_cmd(
            ["pnpm", "i"],
            cwd=project_root,
            description="Installing frontend dependencies",
        )
        run_cmd(
            ["pnpm", "build"],
            cwd=project_root,
            description="Building Svelte components",
        )

        # 3. 执行 Hugo 构建
        hugo_cmd = [
            "hugo",
            "build",
            "--gc",
            "--minify",
            "--baseURL",
            f"{args.base_url}/",
            "--cacheDir",
            f"{args.runner_temp}/hugo_cache",
        ]
        run_cmd(hugo_cmd, cwd=project_root, description="Building Hugo site")

        print("Build completed successfully!")

    except Exception as e:
        print(f"Build failed with error: {e}", file=sys.stderr)
        sys.exit(1)

    finally:
        if server_proc and server_proc.poll() is None:
            print("Stopping backend server...")
            server_proc.terminate()
            try:
                server_proc.wait(timeout=10)
                print("Server stopped cleanly.")
            except subprocess.TimeoutExpired:
                print("Server didn't stop in time, forcing kill...", file=sys.stderr)
                server_proc.kill()
                server_proc.wait()


if __name__ == "__main__":
    main()
