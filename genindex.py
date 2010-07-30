#!/usr/bin/python
import os
import sys

HEADER = '''<html><body>'''
TEMPLATE = '''<a href="%s" target="_blank"><img src="%s" width="100" /></a>'''
FOOTER = '''</body></html>'''


def timeorder(filename, lst=None):
  if lst is None:
    lst = []

  if os.path.basename(filename) == 'thumbnails':
    return lst

  if os.path.isdir(filename):
    for fn in os.listdir(filename):
      lst.extend(timeorder(os.path.join(filename, fn)))
    return sorted(lst)
  elif os.path.isfile(filename):
    root, ext = os.path.splitext(filename)
    if ext in ('.jpg', '.gif', '.jpeg', '.png'):
      lst.append((os.stat(filename).st_ctime, filename))
    return lst


def order(filename):
  lst = timeorder(filename)
  return [y for (x, y) in lst]


def thumbnailize(filenames, outdir):
  for fn in filenames:
    bn = os.path.basename(fn)
    outname = os.path.join(outdir, fn)
    if not os.path.isfile(outname):
      print >>sys.stderr, 'Generating thumbnail for %s' % bn
      os.system('convert -thumbnail 100 %s %s' % (fn, outname))


def buildIndex(filenames, thumbdir):
  print HEADER
  for fn in filenames:
    bn = os.path.basename(fn)
    tn = os.path.join(thumbdir, bn)
    print TEMPLATE % (fn, tn)
  print FOOTER


def main():
  imgdir = os.path.dirname(sys.argv[0])
  thumbdir = os.path.join(imgdir, 'thumbnails')

  if not os.path.isdir(thumbdir):
    os.mkdir(thumbdir)
  filenames = order(imgdir)
  thumbnailize(filenames, thumbdir)

  buildIndex(filenames, thumbdir)


if __name__ == '__main__':
  main()