import re
import os
import argparse

from functools import partial


def parse_arg():
    parser = argparse.ArgumentParser(description='process html')

    parser.add_argument('-f', dest='filepath', type=str, help='file path', default='./books.html')
    parser.add_argument('-n', dest='no_page_indicator', type=str, help='<unk>token', default='None')
    parser.add_argument('-t', dest='tab_size', type=int, help='tab size', default=4)
    parser.add_argument('-v', dest='verbose', action='store_true', help='log verbosity', default=False)
    parser.add_argument('-i', dest='img_width', help='img width', default=600)
    parser.add_argument('-c', dest='const_img_size', action='store_false')

    args = parser.parse_args()

    return args


def main():
    args = parse_arg()

    args.tab = "".join([' ' for x in range(args.tab_size)])
    args.vpp = partial(vp, verbose=args.verbose)
    config = vars(args)

    run(config)


def img_resize(line, **config):

    block_start = '<img '
    sidx = line.find(block_start)
    if sidx >= 0:
        sidx += len(block_start)
        eidx = line.find('/>', sidx)

        imgblock = line[sidx:eidx]
        if config['const_img_size']:
            x = imgblock.replace('src=\"', '', 1)
            x = x[:-1]
            y = x.rsplit('/', 1)
            y = y[0] + '/post_' + y[1]

            return line.replace(x, y)

        else:
            newimgblock = 'width=\"{}\" '.format(config['img_width']) + imgblock
            return line.replace(imgblock, newimgblock)

    else:
        return line


def run(config):
    filepath = os.path.abspath(config['filepath'])

    filename = os.path.basename(filepath)
    sp = filename.split('.')
    outname = sp[0] + '.post.' + sp[1]
    outpath = os.path.join(os.path.dirname(filepath), outname)
    print('{} to {}'.format(filepath, outpath))

    fi = open(filepath, 'r')
    fo = open(outpath, 'w')

    lines = []
    reg = re.compile(r'\[ [0-9A-Za-z]+ \]')
    pnum_prev = None

    def writewrapper(counter, strings, reg, pnum, fo, **config):
        write_change(strings, reg, pnum, fo, **config)
        return counter+1

    counter=0
    for line in fi:
        lines.append(img_resize(line, **config))

        next_pnum = has_pnum(line, **config)

        if next_pnum:
            lines = lines[:-1]
            counter = writewrapper(counter, lines, reg, pnum_prev, fo, **config)
            pnum_prev = next_pnum
            lines = [img_resize(line, **config)]

    # write the rest
    last_item, the_rest = split_last(lines, **config)
    if pnum_prev.isdigit():
        counter = writewrapper(counter, last_item, reg, pnum_prev, fo, **config)

    config['vpp'](the_rest)
    counter = writewrapper(counter, the_rest, reg, None, fo, **config)
    print("written {} lines".format(counter))


def vp(string, verbose):
    if verbose:
        print(string)


def split_last(lines, **config):
    iidx = -1

    for idx, line in enumerate(lines):
        if check_body(False, line):
            config['vpp']("checking_body")
            iidx = idx
            break

    if iidx >= 0:
        iidx -= 1
        return lines[:iidx - 1], lines[iidx - 1:]
    else:
        return lines, []


def check_body(start, line):
    crit = '<body>' if start else '</body>'
    return line.find(crit)


def write_change(lines, reg, pnum, fo, **config):
    if pnum:
        config['vpp']("writing {} p".format(pnum))
        to_write = do_change(lines, reg, pnum, **config)
    else:
        config['vpp']("writing rest")
        to_write = lines
    return write_list(fo, to_write)


def write_list(fo, to_write):
    for line in to_write:
        fo.writelines(line)
    return True


def check_for_phrase(line, func, crit, end='>'):
    idx = line.find(crit)
    if idx >= 0:
        idx += len(crit)
        bra_end = line.find(end, idx)
        p_num = line[idx:bra_end]
        return func(p_num), idx
    return None, None


def strip_bracket(string):
    return string[2:-2]


def ret_self(x):
    return x


def has_pnum(line, **config):
    pnum, idx = check_for_phrase(line, ret_self, '<a name=')
    return pnum


def do_change(lines, reg, pnum, **config):
    x = lines
    pidx = None
    pidxline = None

    # get pidx, pidxline
    for idx, line in enumerate(lines):
        match = re.search(reg, line)
        if match:
            ptxt = match[0]
            pidx = strip_bracket(ptxt)
            pidxline = idx
            break

    if not pidx:
        pidx = config['no_page_indicator']
    if pnum:
        # change <b>
        if pidxline:
            x[pidxline] = add_b_pdix_name(x[pidxline])

        # wrap in div
        for idx, line in enumerate(x):
            x[idx] = config['tab'] + line
        x.insert(0, '<div name=\"pn_{}\" id=\"pid_{}\">\n'.format(pnum, pidx))
        x.append('</div>\n')

        return x

    print("Error: failed change")
    return None


def add_b_pdix_name(line):
    string_to_insert = 'name=\"page_index\"'

    def strip_white(string):
        return string.strip()

    item, idx = check_for_phrase(line, strip_white, '<b>[', ']</b>')
    if item:
        return line[idx:] + string_to_insert + line[:idx]

    print("no <b> found!")
    return None


if __name__ == '__main__':
    main()
