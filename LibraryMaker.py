import argparse
import os
import re
import json


class Function:
    def __init__(self, name, return_type, args, description):
        self.name = name
        self.return_type = return_type
        self.args = args
        self.description = description

    def __str__(self):
        return f'{self.return_type} {self.name}({", ".join(self.args)}) : {self.description}'

    def json(self):
        return {
            'name': self.name,
            'return': self.return_type,
            'args': self.args,
            'description': self.description
        }


class LibraryMaker:
    def __init__(self):
        self.args = self.parse_args()
        self.headers = self.get_headers()
        self.functions = self.parse_headers()
        self.json = [function.json() for function in self.functions]
        self.output = self.json_output()

    def reg_word(self, content):
        return re.match(r'^\W*([\w-]+)', content).group(1)

    def parse_args(self):
        parser = argparse.ArgumentParser(
            prog='LibraryMaker',
            description='Library Maker for Pelops project',
        )

        parser.add_argument('-w', '--workdir', type=str,
                            help='Path to the working directory')
        parser.add_argument('-o', '--output', type=str,
                            help='Path for the output file')

        args = parser.parse_args()

        if args.workdir is None:
            args.workdir = '.'
        if args.output is None:
            args.output = './config.json'

        return args

    def get_headers(self):
        headers = []

        for root, dirs, files in os.walk(self.args.workdir):
            for file in files:
                if file.endswith('.hpp' or '.h'):
                    headers.append(os.path.join(root, file))

        return headers

    def get_function(self, decorators, results, index):
        name = self.reg_word(results[index])
        return_type = 'void'
        args = []
        description = 'None'

        for cpt in range(index + 1, len(decorators)):
            if decorators[cpt] == '@name':
                break
            if decorators[cpt] == '@param':
                args.append(self.reg_word(results[cpt]))
            if decorators[cpt] == '@description':
                description = results[cpt]
                for char in ['\n', '\t', ' ', '*']:
                    description = description.replace(char, ' ')
                description = re.sub(r'\s+', ' ', description)
            if decorators[cpt] == '@return':
                return_type = self.reg_word(results[cpt])

        return Function(name, return_type, args, description)

    def parse_headers(self):
        functions = []

        for file_path in self.headers:
            with open(file_path, 'r') as file:
                content = file.read()

                decorators = re.findall(r'@\w{2,}', content)
                results = re.findall(r'@\w{2,}\s+([^@|^\/]+)', content)

                for cpt in range(len(decorators)):
                    if decorators[cpt] == '@name':
                        functions.append(self.get_function(
                            decorators, results, cpt))

        return functions

    def json_output(self):
        if self.json is None:
            print('No functions found')
            return

        with open(self.args.output, 'w') as file:
            file.write(json.dumps(self.json, indent=4))
        print("%d functions found, %s created" %
              (len(self.json), self.args.output))


if __name__ == '__main__':
    lm = LibraryMaker()
    for function in lm.functions:
        print(function.json())
