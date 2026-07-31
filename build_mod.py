#!/usr/bin/env python3
"""
SCUM Vehicle Max Weight Mod — Build & Deploy Script

把 source/ 目录下的修改版 .uasset/.uexp 打包成 Vehicle_MaxWeight.pak，
然后部署到 SCUM/Saved/Mods/ 目录。

依赖:
  - repak (https://github.com/trumank/repak) — 在 PATH 或 SCUMMod/tools/
  - UAssetCLI (可选,仅用于从 JSON 重新生成 .uasset)

用法:
  python build_mod.py build           # 仅打包 PAK 到 ./dist/
  python build_mod.py deploy          # 打包 + 复制到 SCUM/Saved/Mods/
  python build_mod.py deploy --game-dir <PATH>   # 自定义游戏路径
  python build_mod.py verify          # 验证 PAK 内容
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

# === 配置 ===
TARGET_VALUE = 2147483520.0  # float32 可精确表示的最大整数 (= 21,474,835,20)
SOURCE_DIR = Path("source")
DIST_DIR = Path("dist")
PAK_NAME = "Vehicle_MaxWeight.pak"
SCUM_MODS_DIR = Path(os.environ.get(
    "LOCALAPPDATA",
    str(Path.home() / "AppData/Local")
)) / "SCUM" / "Saved" / "Mods"
MOUNT_POINT_DEFAULT = "../../../"  # repak 默认挂载点


def find_repak():
    """查找 repak 可执行文件"""
    candidates = [
        Path("repak.exe"), Path("repak"),
        Path("../repak.exe"), Path("../repak"),
        Path("SCUMMod/repak.exe"), Path("SCUMMod/tools/repak.exe"),
        Path("R:/Program Files/SCUMMod/repak.exe"),
        Path.home() / ".cargo/bin/repak.exe",
        Path.home() / ".cargo/bin/repak",
    ]
    for c in candidates:
        if c.exists():
            return c
    raise FileNotFoundError("repak not found. Install from https://github.com/trumank/repak")


def build_pak():
    """打包 source/ 为 PAK"""
    if not SOURCE_DIR.exists():
        sys.exit(f"ERROR: {SOURCE_DIR} not found")
    DIST_DIR.mkdir(exist_ok=True)
    repak = find_repak()
    
    # SCUM PAK 路径必须以 SCUM/Content/... 开头
    # repak 默认 mount-point ../../../,所以输入目录结构应是
    #   source/SCUM/Content/ConZ_Files/Vehicles/<file>.uasset
    # PAK 内路径会是 SCUM/Content/.../...
    
    out_pak = DIST_DIR / PAK_NAME
    if out_pak.exists():
        out_pak.unlink()
    
    cmd = [str(repak), "pack", str(SOURCE_DIR), "--version", "V8B"]
    print(f"$ {' '.join(cmd)}")
    r = subprocess.run(cmd, check=True, timeout=120)
    
    # repak 输出在 SOURCE_DIR 旁边
    built = SOURCE_DIR.parent / (SOURCE_DIR.name + ".pak")
    if built.exists() and built != out_pak:
        shutil.move(built, out_pak)
    
    if out_pak.exists():
        size = out_pak.stat().st_size
        print(f"\n✓ Built {out_pak} ({size:,} bytes)")
        return out_pak
    sys.exit("ERROR: PAK not generated")


def deploy(pak_path, game_dir=None):
    """部署 PAK 到 SCUM/Saved/Mods/"""
    target = Path(game_dir) if game_dir else SCUM_MODS_DIR
    target.mkdir(parents=True, exist_ok=True)
    dst = target / PAK_NAME
    shutil.copy(pak_path, dst)
    print(f"✓ Deployed to {dst}")


def verify(pak_path):
    """验证 PAK 内容"""
    repak = find_repak()
    r = subprocess.run([str(repak), "list", str(pak_path)], capture_output=True, text=True, timeout=30)
    print(r.stdout)
    # Check for SCUM/ prefix
    if "SCUM/Content" not in r.stdout:
        sys.exit("ERROR: PAK paths missing SCUM/ prefix - game won't find files!")
    print("✓ PAK paths look correct")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    
    p_build = sub.add_parser("build", help="仅打包")
    p_build.set_defaults(func=lambda a: build_pak())
    
    p_deploy = sub.add_parser("deploy", help="打包 + 部署到游戏目录")
    p_deploy.add_argument("--game-dir", help="游戏 Saved/Mods 路径 (默认: $LOCALAPPDATA/SCUM/Saved/Mods)")
    p_deploy.set_defaults(func=lambda a: deploy(build_pak(), a.game_dir))
    
    p_verify = sub.add_parser("verify", help="验证 PAK 内容")
    p_verify.add_argument("--pak", default=str(DIST_DIR / PAK_NAME))
    p_verify.set_defaults(func=lambda a: verify(a.pak))
    
    args = parser.parse_args()
    args.func(args)
