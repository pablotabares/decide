# import ldap


# Funcion para importar usuarios de ldap,
# return lista de nombres
# def importUser(ldap_server,username,password,base_dn):

#     user_dn = "cn="+username+","+base_dn
#     connect = ldap.initialize(ldap_server)
#     #Filtro para buscar objectos de tipo persona
#     search_filter = "objectClass=inetOrgPerson"

#     try:
#         connect.bind_s(user_dn,password)
#         result = connect.search_s(base_dn,ldap.SCOPE_SUBTREE,search_filter)
#         listPerson=[]
#         for x in range(0,len(result)):
#             listPerson.append(result[x][1]['cn'][0].decode("utf-8"))
#         connect.unbind_s()
#         return listPerson
#     except ldap.LDAPError:
#         connect.unbind_s()
#         print( "Ldap error")


# #Datos de control
# ldap_server="ldap://ldap.forumsys.com:389"
# username = "read-only-admin"
# password= "password"
# base_dn = "dc=example,dc=com"
# user_dn = "cn="+username+","+base_dn
# lista=importLdap(ldap_server,username,password,base_dn)
# print(lista)

