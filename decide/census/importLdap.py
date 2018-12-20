import ldap

ldap_server="ldap://localhost:389"
username = "admin"
password= "admin"
# the following is the user_dn format provided by the ldap server
user_dn = "cn="+username+",dc=example,dc=org"
# adjust this to your base dn for searching
base_dn = "dc=example,dc=org"
connect = ldap.initialize(ldap_server)
search_filter = "cn="+username
try:
    #if authentication successful, get the full user data
    connect.bind_s(user_dn,password)
    result = connect.search_s(base_dn,ldap.SCOPE_SUBTREE,search_filter)
    # return all user data results
    connect.unbind_s()
    print (result)
except ldap.LDAPError:
    connect.unbind_s()
    print( "authentication error")