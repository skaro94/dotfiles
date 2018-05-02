#!/bin/env python

import cmd
import csv
import os
import argparse


def main():
    args = arg_parse()

    if args.interactive:
        InteractiveTermMemory(args).cmdloop('launching interactive mode...')
    else:
        obj = TermMemory(args)
        methods = get_method_list(obj)
        function = 'do_' + args.function
        if function not in methods:
            function = args.function

        getattr(obj, function)(*args.arg)
        getattr(obj, 'write_csv')()


def arg_parse():
    parser = argparse.ArgumentParser(description='term memory')

    parser.add_argument('-i', dest='interactive', action='store_true', help='interactive shell')
    parser.add_argument('-f', dest='term_memory_path', default='./terms.db', help='file path')
    parser.add_argument('function', default='do_search', nargs='?', help='function to execute')
    parser.add_argument('arg', default='CRAN', nargs='*', help='possible arguments')

    args = parser.parse_args()

    return args


def keynot(key):
    eprint("key not in dictionary: {}".format(key))


def eprint(string):
    print("EXCEPTION: " + string)


def create_file(path, headers):
    if not os.path.lexists(path):
        print("creating file...")
        with open(path, 'w') as csvfile:
            write = csv.DictWriter(csvfile, headers)
            write.writeheader()


def get_method_list(obj):
    return [method for method in dir(obj) if callable(getattr(obj, method))]


class TermMemory():
    def __init__(self, args):
        self.path = os.path.abspath(args.term_memory_path)
        self.headers = ['eng', 'kor']
        self.term_dict = self.read_csv()

    def read_csv(self):
        term_dict = {}
        create_file(self.path, self.headers)
        with open(self.path, 'r') as csvfile:
            read = csv.DictReader(csvfile)
            for row in read:
                term_dict[row[self.headers[0]]] = row[self.headers[1]]
            csvfile.close()
        return term_dict

    def write_csv(self):
        dict_to_write = [{self.headers[0]: key, self.headers[1]: val} for key, val in self.term_dict.items()]

        with open(self.path, 'w') as csvfile:
            csvfile.truncate()
            write = csv.DictWriter(csvfile, self.headers)
            write.writeheader()
            write.writerows(dict_to_write)
            csvfile.close()

    def do_search(self, key):
        if key in self.term_dict:
            print("{} : {}".format(key, self.term_dict[key]))
        else:
            keynot(key)

    def do_insert(self, key, val):
        if key not in self.term_dict:
            print("saving {} as {}".format(key, val))
            self.term_dict[key] = val
        else:
            eprint("key already in dictionary: {} : {}".format(key, self.term_dict[key]))

    def do_update(self, key, val):
        if key in self.term_dict:
            print("updating {} : {} -> {}".format(key, self.term_dict[key], val))
            self.term_dict[key] = val
        else:
            keynot(key)

    def do_append(self, key, val):
        if key in self.term_dict:
            print("appending {} : {} + {}".format(key, self.term_dict[key], val))
            self.term_dict[key] += '/' + val
        else:
            keynot(key)

    def do_remove(self, key):
        if key in self.term_dict:
            print("removing {} : {}".format(key, self.term_dict[key]))
            del self.term_dict[key]
        else:
            keynot(key)

    def do_save(self):
        print("saving...")
        self.write_csv()


class InteractiveTermMemory(cmd.Cmd):
    def __init__(self, args):
        super(InteractiveTermMemory, self).__init__()

        self.child = TermMemory(args)

        methods = get_method_list(self.child)
        for method in methods:
            if self.check_func(method):
                # print(method)
                setattr(self, method, getattr(self.child, method))

    def onecmd(self, line):
        """Mostly ripped from Python's cmd.py"""
        cmd, arg, line = self.parseline(line)
        if len(arg) > 0:
            args = arg.split(' ')
        else:
            args = arg

        if not line:
            return self.emptyline()
        if cmd is None:
            return self.default(line)
        self.lastcmd = line
        if cmd == '':
            return self.default(line)
        else:
            try:
                func = getattr(self, 'do_' + cmd)
            except AttributeError:
                return self.default(line)
            return func(*args)

    def check_func(self, method):
        return method[:3] == 'do_'

    def postloop(self):
        self.child.write_csv()

    def do_EOF(self):
        return True

    def do_quit(self):
        return self.do_EOF()


if __name__ == '__main__':
    main()
