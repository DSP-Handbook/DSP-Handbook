#! /usr/bin/python3
""" make.py for DSP-Handbook"""

if __name__ == "__main__":
    import os
    import shutil
    import subprocess
    import argparse
    import glob
    import itertools

    parser = argparse.ArgumentParser(description="Build Document")
    parser.add_argument("--action", default="build", required=False, choices=["build", "clean"])
    action = parser.parse_args().action

    if action == "build":
        os.chdir('src')
        commit_id = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], capture_output=True, check=True
        ).stdout.decode("utf-8").strip()
        for _ in range(2):
            subprocess.run([
                "latexmk", "-xelatex", 
                fr'-usepretex="\providecommand{{\commitId}}{{{commit_id}}}"', "main.tex"
            ], check=True)

        if not os.path.exists("../build"):
            os.mkdir("../build")
        shutil.copy('main.pdf', '../build')
    elif action == "clean":
        exts = [
            ".aux", ".log", ".out", ".pdf", ".bcf",
            ".run.xml", ".toc", ".ptc", ".synctex.gz",
            ".dvi", ".fdb_latexmk", ".fls", ".xdv"
        ]
        for _ in itertools.chain(*map(glob.glob, map(lambda ext: f"**/*{ext}", exts))):
            os.remove(_)
        shutil.rmtree("build", ignore_errors=True)
