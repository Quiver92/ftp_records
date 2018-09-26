# ftp_records
ftp with LDAP/Active Directory authentication

BASE_DIR = r'/some_dir'
LOG_DIR = r'/dir_for_logs'
LDAP_SERVER = 'ldap://121.121.121.121'

def make_ldap_string(username):
    return username + "@example.domain"
LISTEN_IP = '0.0.0.0'
LISTEN_PORT = 2121

