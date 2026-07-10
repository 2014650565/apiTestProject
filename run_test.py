"""
一键运行入口：启动 Mock 服务 → 跑 pytest → 生成 Allure 报告 → 关闭服务

用法：
    python run_test.py                        # 全量测试 + Allure 报告
    python run_test.py -m smoke               # 只跑冒烟测试
    python run_test.py -m "login or product"   # 跑登录或商品模块
    python run_test.py -n 4                    # 4 进程并行（需 pip install pytest-xdist）
    python run_test.py --reruns 3             # 失败重试 3 次
"""

# import subprocess
# import sys
# import time
# import os
# import signal
# import threading

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# def start_mock_server():
#     """后台启动 Flask mock 服务"""
#     print("正在启动 Mock API 服务器 ...")
#     proc = subprocess.Popen(
#         [sys.executable, os.path.join(BASE_DIR, "mock_server", "app.py")],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#     )
#     # 等待服务就绪
#     for _ in range(20):
#         try:
#             import urllib.request
#             urllib.request.urlopen("http://127.0.0.1:5000/api/health", timeout=1)
#             print("[OK] Mock API 服务器已就绪 -> http://127.0.0.1:5000\n")
#             return proc
#         except Exception:
#             time.sleep(0.3)
#     proc.kill()
#     raise RuntimeError("Mock 服务器启动超时！")


# def run_pytest(extra_args):
#     """运行 pytest，extra_args 是命令行额外参数"""
#     os.chdir(os.path.join(BASE_DIR, ))

#     # 构建 pytest 命令
#     cmd = [
#         sys.executable, "-m", "pytest", ,
#         ,
#         "--alluredir=../temps", "--clean-alluredir",
#         "--sensitive-url=''",
#         ,
#     ] + extra_args

#     print(f"\n[Test] 执行命令: {' '.join(cmd)}\n{'='*60}")
#     result = subprocess.run(cmd)
#     return result.returncode


# def generate_allure_report():
#     """生成 Allure HTML 报告"""
#     temps_dir = os.path.join(BASE_DIR, "temps")
#     reports_dir = os.path.join(BASE_DIR, "reports")
#     print(f"\n[Report] 正在生成 Allure 报告 ...")
#     subprocess.run(
#         ["allure", "generate", "-o", reports_dir, "-c", temps_dir],
#         cwd=BASE_DIR,
#     )
#     print(f"[OK] Allure 报告已生成 -> {reports_dir}/index.html")


# def main():
#     # 把命令行参数透传给 pytest
#     extra_args = sys.argv[1:] if len(sys.argv) > 1 else []

#     mock_proc = None
#     try:
#         mock_proc = start_mock_server()
#         exit_code = run_pytest(extra_args)
#         if exit_code in (0, 1):  # 0=全部通过, 1=有用例失败（正常范围）
#             generate_allure_report()
#         print(f"\n{'='*60}")
#         print(f"[Done] 测试完成 (exit={exit_code})")
#     finally:
#         if mock_proc:
#             print("正在关闭 Mock 服务器 ...")
#             mock_proc.terminate()
#             mock_proc.wait()
#             print("已关闭")


# if __name__ == "__main__":
#     main()
