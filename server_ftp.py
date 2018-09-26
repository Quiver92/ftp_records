try:
    from settingsftp import BASE_DIR, LDAP_SERVER, make_ldap_string, LISTEN_IP, LISTEN_PORT, LOG_DIR

except ImportError:
    print('Could not load required data from settings file - make sure you have created it as instructed in the README')
    exit(1)

import os
import sys
from hashlib import md5
import ldap
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer, AuthenticationFailed

ARCHIVE = 'archive'
CURRENT = 'current'
UPLOAD = 'upload'

class LdapAuthorizer(DummyAuthorizer):
    global_perm="elradfmwMT"
    allowed_users=None
    ejected_users=None
    anonymous_user=None
    anonymous_password=""
    msg_login="Login successful."
    msg_quit="Goodbye."

    def validate_authentication(self, username, password, handler):
          connect = ldap.initialize(LDAP_SERVER)
          connect.protocol_version = 3
          connect.set_option(ldap.OPT_REFERRALS, 0)
          result = connect.simple_bind_s(make_ldap_string(username), password)
          if result is not None:
             return True
          else:
             return False
    def impersonate_user(self, username, password):
        # This would involve actual OS permissions, so we don't care
        pass

    def terminate_impersonation(self, username):
        # This would involve actual OS permissions, so we don't care
        pass

    def has_perm(self, username, perm, path=None):
        """ Path is the full OS path of the target file"""
        if perm in self.global_perm:
            return True

        # only privileged users can upload
#        if perm not in self.READUPLOAD or username not in UPLOADERS:
#            return False

        # don't allow "confusing" zip names
#        for name in (UPLOAD, CURRENT, ARCHIVE):
#            if path.endswith(os.sep + name + '.zip'):
#                return False

        # can only upload zip files
#        if os.path.splitext(path)[1].lower() != '.zip':
#            return False

        # file must be going into uploads directory
#        if os.path.relpath(path, os.path.join(BASE_DIR, UPLOAD))[0] == '.':
            # don't allow file names that begin with '.', and
            # definitely don't allow paths that aren't below BASE_DIR
#            return False

#        return True

    def get_perms(self, username):
        return self.global_perm
        

    def get_home_dir(self, username):
        """ All users have the same home directory"""
        return BASE_DIR

    def get_msg_login(self, username):
#        if _is_anonymous(username):
#            return "Welcome anonymous user"

#        if username in UPLOADERS:
#            return "Welcome " + username + "!  You have upload privileges."

        return "Welcome " + username

    def get_msg_quit(self, username):
        return "Goodbye" 
def main():
    # get a hash digest from a clear-text password
    authorizer = LdapAuthorizer()
    handler = FTPHandler
    handler.authorizer = authorizer
    server = FTPServer(('', LISTEN_PORT), handler)
    server.serve_forever()

if __name__ == "__main__":
    main()
