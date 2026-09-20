# -*- coding: utf-8 -*-
"""
Matheus Henrique Da Silva
"""

import ast
import io
import os
import tokenize


def line_number(input_filename: str, output_filename: str) -> None:
    """
    read a text file and write its contents to another file with
    each line prefixed by its line number.
    """
    try:
        with open(input_filename, "r", encoding="utf-8") as input_file:
            lines = input_file.readlines()

        with open(output_filename, "w", encoding="utf-8") as output_file:
            for number, line in enumerate(lines, start=1):
                output_file.write(
                    f"{number}. {line.rstrip(chr(10))}\n"
                )

    except Exception as error:
        print(
            f"Error while numbering lines in "
            f"'{input_filename}': {error}"
        )
        raise


def parse_functions(
        filename: str
) -> tuple[tuple[int, str, str, str], ...]:
    """
    parse a Python file and return information about its top-level
    functions.

    each returned tuple contains the function's line number,
    function name, formal argument list, and function code.
    empty lines and comments are removed from the function code.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            source = file.read()

        tree = ast.parse(source, filename=filename)

        source_lines = source.splitlines(keepends=True)

        functions = []

        for node in tree.body:

            if isinstance(
                    node,
                    (ast.FunctionDef, ast.AsyncFunctionDef)
            ):

                line_num = node.lineno

                function_name = node.name

                arguments = ast.unparse(node.args)

                function_source = "".join(
                    source_lines[
                        node.lineno - 1:
                        node.end_lineno
                    ]
                )

                tokens = tokenize.generate_tokens(
                    io.StringIO(function_source).readline
                )

                tokens_without_comments = [
                    token
                    for token in tokens
                    if token.type != tokenize.COMMENT
                ]

                cleaned_source = tokenize.untokenize(
                    tokens_without_comments
                )

                cleaned_lines = [
                    line.rstrip()
                    for line in cleaned_source.splitlines()
                    if line.strip()
                ]

                function_code = "\n".join(cleaned_lines) + "\n"

                functions.append(
                    (
                        line_num,
                        function_name,
                        arguments,
                        function_code
                    )
                )

        functions.sort(
            key=lambda item: item[1]
        )

        return tuple(functions)

    except Exception as error:
        print(
            f"Error while parsing "
            f"'{filename}': {error}"
        )
        raise


def main() -> None:
    """
    test line_number and parse_functions using this
    """
    print("Name: Matheus Henrique Da Silva - Z23704669")
    print()

    source_file = os.path.abspath(__file__)

    output_file = os.path.join(
        os.path.dirname(source_file),
        "p1_DaSilva_MatheusHenrique_numbered.txt"
    )

    print("PART A - line_number")
    line_number(source_file, output_file)
    print(f"Numbered file created: {output_file}")

    print("\nPART B - parse_functions")
    parsed_functions = parse_functions(source_file)

    print("Returned tuple from parse_functions:")
    print(parsed_functions)


if __name__ == "__main__":
    main()