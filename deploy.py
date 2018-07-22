import os, sys, ftplib, subprocess

should_clean = False

for arg in sys.argv[1:]:
  if arg == '--clean' or arg == '-c':
    should_clean = True
  else:
    raise Exception( 'Unknown argument' )

subprocess.check_call( 'npm run build', cwd='static', shell=True )

ftplib.FTP.maxline *= 48
ftp = ftplib.FTP( 'gloom.aluminumangel.org', 'gloom', 'mazSC!rf' )

def handle_directory( directory ):
  clean_directory( directory )
  send_directory( directory )

def clean_directory( directory ):
  if not should_clean:
    return
  dir = directory[0]
  if len( directory ) == 1:
    list = ftp.nlst()
    if dir in list:
      ftp.cwd( dir )
      list = ftp.nlst()
      for file in list:
        delete_file( file, path=dir )
      ftp.cwd( '..' )
      ftp.rmd( dir )  
      print 'Remove - ' + dir + '/'
  else:
    list = ftp.nlst()
    if dir in list:
      ftp.cwd( dir )
      clean_directory( directory[1:] )
      ftp.cwd( '..' )
      try:
        ftp.rmd( dir )
        print 'Remove - ' + dir + '/'
      except ftplib.error_perm:
        pass

def send_directory( directory ):
  for dir in directory:
    try:
      ftp.mkd( dir )
      print 'Make   - ' + dir + '/'
    except ftplib.error_perm:
      pass
    ftp.cwd( dir )

  path = '/'.join( directory )
  list = os.listdir( path )
  os.chdir( path )
  for file in list:
    send_file( file, path=path )
  for dir in directory:
    ftp.cwd( '..' )
    os.chdir( '..' )

def handle_file( file ):
  delete_file( file )
  send_file( file )

def delete_file( file, path='' ):
  if not should_clean:
    return
  try:
    ftp.delete( file )
    print 'Delete - ' + path + '/' + file
  except ftplib.error_perm:
    pass

def send_file( file, path='' ):
  if file.endswith( '.bin' ):
    ftp.storbinary( 'STOR ' + file, open( file, 'rb' ) )
  else:
    ftp.storlines( 'STOR ' + file, open( file, 'r' ) )
  print 'Send   - ' + path + '/' + file

def rename_file( src, dest ):
  ftp.rename( src, dest )
  print 'Rename - ' + src + ' to ' + dest

def change_directory( directory, local=False ):
  ftp.cwd( directory )
  if local:
    os.chdir( directory )

ftp.cwd( 'gloom.aluminumangel.org' )

change_directory( 'gloom' )
handle_file( '__init__.py' )
change_directory( 'server', True )
handle_file( '__init__.py' )
handle_file( 'print_map.py' )
handle_file( 'senarios.py' )
handle_file( 'settings.py' )
handle_file( 'solver.py' )
handle_file( 'utils.py' )
handle_file( 'production_true.py' )
rename_file( 'production_true.py', 'production.py' )
change_directory( '..', True )
change_directory( 'static', True )
handle_file( 'index.html' )
handle_directory( [ 'dist' ] )
change_directory( '..', True )
change_directory( '..' )
handle_directory( [ 'tmp' ] )