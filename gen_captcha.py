# -*- coding:utf-8 -*-
import argparse
import string
import os
import uuid
from captcha.image import ImageCaptcha

import itertools

FLAGS = None


def get_choices():
    cate_map = [
        (FLAGS.digit, map(str, range(10))),
        (FLAGS.lower, string.ascii_lowercase),
        (FLAGS.upper, string.ascii_uppercase),
        ]
    return tuple([i for _flag, choices in cate_map for i in choices if _flag])


def _gen_captcha(img_dir, num_per_image, n, choices):
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    image = ImageCaptcha(width=40 + 20 * num_per_image, height=100)
    print 'generating %s captchas in %s' % (n, img_dir)

    for _ in range(n):
        for i in itertools.permutations(choices, num_per_image):
            captcha = ''.join(i)
            fn = os.path.join(img_dir, '%s_%s.png' % (captcha, uuid.uuid4()))
            image.write(captcha, fn)


def gen_dataset(root_dir):

    def _build_path(x):
        return os.path.join(root_dir, 'char-%s' % num_per_image, x)

    n_train = FLAGS.n
    n_test = max(int(FLAGS.n * FLAGS.t), 1)
    num_per_image = FLAGS.npi

    choices = get_choices()

    print '%s choices: %s' % (len(choices), ''.join(choices) or None)

    _gen_captcha(_build_path('train'), num_per_image, n_train, choices=choices)
    _gen_captcha(_build_path('test'), num_per_image, n_test, choices=choices)
    # meta info


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-n',
        default=1,
        type=int,
        help='number of captchas for one integer.')
    parser.add_argument(
        '-t',
        default=0.2,
        type=float,
        help='ratio of test / train.')
    parser.add_argument(
        '-d', '--digit',
        action='store_true',
        help='use digits in labels.')
    parser.add_argument(
        '-l', '--lower',
        action='store_true',
        help='use lowercase characters in labels.')
    parser.add_argument(
        '-u', '--upper',
        action='store_true',
        help='use uppercase characters in labels.')
    parser.add_argument(
        '--npi',
        default=1,
        type=int,
        help='number of characters per image.')

    FLAGS, unparsed = parser.parse_known_args()

    gen_dataset('images')