import os


def main(
    work_dir_relative: str,
    project: str = "client",
) -> None:
    curr_dir = os.getcwd()
    work_dir_abs_full = os.path.join(curr_dir, work_dir_relative)
    work_dir_abs = os.path.abspath(work_dir_abs_full)
    print(f"-> Рабочая папка: {work_dir_abs}")
    os.chdir(work_dir_abs)
    os.system("ng build")
    print(f"-> Проект angular собран: {project}")
    os.system("npm run tauri build")
    os.system(f"rm -rf dist/{project}/")
