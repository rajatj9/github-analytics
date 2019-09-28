import tempfile 
import os
import csv
import time

def __parse_diff_stats(gitdiff):
    result = []
    for i in gitdiff:
        result.append(int(i.strip().split(" ")[0]))
    return tuple(result)

def __parse_cloc_stats(clocstat):
    result = []
    return (int(clocstat[0]), int(clocstat[-1])+int(clocstat[-2])+int(clocstat[-3]))

def get_repo_stats(url):
    with tempfile.TemporaryDirectory() as tempdir, tempfile.TemporaryDirectory() as csv_dir:
        os.system("git clone --depth 1 {} {}".format(url, tempdir))
        os.system("cloc --include-lang=Java --csv --out {}/cloc_report {}".format(csv_dir, tempdir))
        csv_reader = csv.reader(open(csv_dir+"/cloc_report"))
        cloc_report = []
        for row in csv_reader:
            cloc_report.append(row)
            # print(row)
        os.system("""
        java -jar binaries/google-java-format-1.7-all-deps.jar -i $(find {} -type f -name "*.java" | grep ".*/src/.*java")
        """.format(tempdir))
        os.system("cd {} && git --no-pager diff --shortstat >> {}/git_report".format(tempdir, csv_dir))
        # os.system("cat {}/git_report".format(csv_dir))
        csv_reader = csv.reader(open(csv_dir+"/git_report"))
        git_report = []
        for row in csv_reader:
            git_report.append(row)
            # print(row)
        result = {}
        git_field_names = ("files_changes", "insertions", "deletions")
        cloc_field_names = ("total_files", "total_lines")
        # print(__parse_diff_stats(git_report[0]))
        # print(__parse_cloc_stats(cloc_report[-1]))
        git_result = dict(zip(git_field_names, __parse_diff_stats(git_report[0])))
        cloc_result = dict(zip(cloc_field_names, __parse_cloc_stats(cloc_report[-1])))
        # print(git_result)
        # print(cloc_result)
        return {**git_result, **cloc_result}

if __name__ == "__main__":
    repo_url = "git://github.com/takezoe/amateras-html-editor.git"
    # repo_url = "https://github.com/google/guava.git"
    print(get_repo_stats(repo_url))