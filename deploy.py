import codecs
codecs.register( lambda name: codecs.lookup( 'utf-8' ) if name == 'cp65001' else None )

import os, sys, subprocess, pysftp

should_clean = False

for arg in sys.argv[1:]:
  if arg == '--clean' or arg == '-c':
    should_clean = True
  else:
    raise Exception( 'Unknown argument' )

subprocess.check_call( 'npm run build', cwd='static', shell=True )

with pysftp.Connection( 'gloom.aluminumangel.org', username='gloom', password='mazSC!rf' ) as sftp:

  def handle_directory( directory ):
    clean_directory( directory )
    send_directory( directory )

  def clean_directory( directory ):
    if not should_clean:
      return
    sftp.chdir( directory )
    file_list = sftp.listdir()
    for file in file_list:
      delete_file( file )
    sftp.chdir( '..' )
    sftp.rmdir( directory )  
    print 'Remove - ' + directory + '/'

  def send_directory( directory ):
    try:
      sftp.mkdir( directory )
      print 'Make   - ' + directory + '/'
    except IOError:
      pass

    sftp.chdir( directory )
    os.chdir( directory )

    list = os.listdir( '.' )
    for file in list:
      send_file( file )
    sftp.chdir( '..' )
    os.chdir( '..' )

  def handle_file( file ):
    delete_file( file )
    send_file( file )

  def delete_file( file ):
    if not should_clean:
      return
    try:
      sftp.remove( file )
      print 'Delete - ' + file
    except IOError:
      pass

  def send_file( file ):
    sftp.put( file )
    print 'Send   - ' + file

  def rename_file( src, dest ):
    sftp.remove( dest )
    sftp.rename( src, dest )
    print 'Rename - ' + src + ' to ' + dest

  def change_directory( directory, local=True ):
    try:
      sftp.mkdir( directory )
      print 'Make   - ' + directory + '/'
    except IOError:
      pass
    sftp.chdir( directory )
    if local:
      os.chdir( directory )
    print 'Cd     - ' + directory

  sftp.chdir( 'gloom.aluminumangel.org' )

  change_directory( 'gloom', False )
  handle_file( '__init__.py' )
  change_directory( 'server' )
  handle_file( '__init__.py' )
  handle_file( 'print_map.py' )
  handle_file( 'scenarios.py' )
  handle_file( 'settings.py' )
  handle_file( 'solver.py' )
  handle_file( 'utils.py' )
  handle_file( 'production_true.py' )
  rename_file( 'production_true.py', 'production.py' )
  change_directory( '..' )
  change_directory( 'static' )
  handle_file( 'index.html' )
  handle_directory( 'dist' )
  change_directory( '..' )
  change_directory( '..', False )
  handle_directory( 'tmp' )