#!/usr/bin/env python

import argparse

from lib import git
from lib.patches import patch_from_dir


patch_dirs = {
  'src/electron/patches/common/chromium':
    'src',

  'src/electron/patches/common/boringssl':
    'src/third_party/boringssl/src',

  'src/electron/patches/common/ffmpeg':
    'src/third_party/ffmpeg',

  'src/electron/patches/common/skia':
    'src/third_party/skia',

  'src/electron/patches/common/v8':
    'src/v8',
}


class ParsePatchDirs(argparse.Action):
  def __call__(self, parser, namespace, values, option_string=None):
    dirs = dict([v.split(':') for v in values])
    setattr(namespace, self.dest, dirs)


def parse_args():
  parser = argparse.ArgumentParser(description='Apply Electron patches')
  parser.add_argument('--from-to', nargs='+',
                      required=False, default=patch_dirs,
                      action=ParsePatchDirs, help='patch_dir:repo format')
  return parser.parse_args()


def apply_patches(dirs):
  for patch_dir, repo in dirs.iteritems():
    git.am(repo=repo, patch_data=patch_from_dir(patch_dir),
      committer_name="Electron Scripts", committer_email="scripts@electron")


def main():
  args = parse_args()
  apply_patches(args.from_to)


if __name__ == '__main__':
  main()
