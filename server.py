#Quentin Mayo
#Basic Call-home Server for "Malware"



import cherrypy
from Crypto.PublicKey import RSA

class MrPWN(object):

    # Use random with db if you want random RSA Keys
    # Key changes if the server resets too :)
    def __init__(self): self.RSA_ = RSA.generate(2048)

    @cherrypy.expose
    def index(self): return index

    @cherrypy.expose  # Public Key
    def request_pwn_slip(self): return self.RSA_.publickey().exportKey()

    @cherrypy.expose  # Private Key
    def unpwn_me_please(self): return self.RSA_.exportKey()
index = """

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="../../favicon.ico">

    <title>A Hacker Home Page for All Hackers</title>

    <!-- Bootstrap core CSS -->
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">

  </head>

  <body>

    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">PWN</a>
        </div>
        <div id="navbar" class="collapse navbar-collapse">

        </div><!--/.nav-collapse -->
      </div>
    </nav>

    <div class="container" style="margin-top:100px">

      <div class="starter-template">
        <h1>Welcome, You are the chosen one of PWN</h1>
        <p class="lead"> There are 10 types of people in this world, those who are PWN and those who are not.</p>
		<img src="http://pre05.deviantart.net/63e7/th/pre/f/2012/156/e/3/____ponies_gonna_pwn_____black_by_poldekpl-d52e2rn.png"></img>
	  </div>

    </div><!-- /.container -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>
</html>


"""
cherrypy.server.socket_host = '0.0.0.0'
cherrypy.quickstart(MrPWN())
