import json
import os
from compiler.lexer import Lexer
from compiler.parser_ import Parser
from compiler.compiler import Compiler
import sys
import tsru
import zipfile
import shutil

def run(codefile, projectfile, useSpinners):
    if useSpinners: spinner = tsru.LoadingSpinner("Extracting project")
    with zipfile.ZipFile(projectfile, "r") as fi:
        fi.extractall("extracted")
    if useSpinners: spinner.stop()

    if useSpinners: spinner = tsru.LoadingSpinner("Reading file")
    with open(codefile, "r") as fi: text = fi.read()
    if useSpinners: spinner.stop()

    if useSpinners: spinner = tsru.LoadingSpinner("Lexing file")
    lexer = Lexer(text)
    tokens = lexer.generate_tokens()
    if useSpinners: spinner.stop()
    
    if useSpinners: spinner = tsru.LoadingSpinner("Parsing tokens")
    parser = Parser(tokens)
    tree = parser.parse()
    if useSpinners: spinner.stop()

    if not tree: return
    if useSpinners: spinner = tsru.LoadingSpinner("Compiling tree")
    compiler = Compiler()
    compiled = compiler.visit(tree)
    if useSpinners: spinner.stop()

    if useSpinners: spinner = tsru.LoadingSpinner("Injecting code")
    with open("extracted/project.json", "r") as fi:
        project = fi.read()

    project = json.loads(project)
    toEdit = project["targets"][1]

    res = json.dumps(project).replace(json.dumps(toEdit["blocks"]),compiled.split('"blocks":')[1][:-1])

    with open("extracted/project.json", "w") as fi:
        fi.write(res)
    if useSpinners: spinner.stop()

    if useSpinners: spinner = tsru.LoadingSpinner("Rebuilding project")
    shutil.make_archive(projectfile, 'zip', "extracted")
    os.remove(projectfile)
    os.rename(projectfile + ".zip", projectfile.replace(".sb3.zip", ".sb3"))
    if useSpinners: spinner.stop()

    if useSpinners: spinner = tsru.LoadingSpinner("Cleaning up")
    shutil.rmtree("extracted")
    if useSpinners: spinner.stop()

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])