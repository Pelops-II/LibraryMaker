import argparse

'''@package LibraryMaker
LibraryMaker is a tool for creating a library for the Pelops project.

'''


class LibraryMaker:
    '''@class LibraryMaker
    '''

    def __init__(self):
        self.args = self.parse_args()

    def parse_args(self):
        '''@brief Parse the arguments passed to the script

        @return The parsed arguments
        '''
        parser = argparse.ArgumentParser(
            prog='LibraryMaker',
            description='Library Maker for Pelops project',
        )

        parser.add_argument('-w', '--workdir', type=str,
                            help='Path to the working directory')
        parser.add_argument('-o', '--output', type=str,
                            help='Path for the output file')

        return parser.parse_args()


if __name__ == '__main__':
    lm = LibraryMaker()
    print(lm.args)
