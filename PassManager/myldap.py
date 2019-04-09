import ldap


host = "ldap://192.168.30.81"
#

connect = ldap.initialize(host)

#accoding to the cn  search all item and get dn
def get_info(cn):
        connect.simple_bind_s('cn=Manager,dc=xbniao,dc=com', '11111')
        filters = '(cn=%s)' %cn
        dns_list = connect.search_s('dc=xbniao,dc=com', ldap.SCOPE_SUBTREE, filters)
        if len(dns_list) == 1:
            # print(dns_list)
            dn = dns_list[0]
            return dn
        else:
            return "err! please connect administrator!"


def ldaplogin(cn, passwd):
    if cn:
        dn = str(get_info(cn)[0])
    if passwd:
        password = str(passwd)
    try:
        connect.bind_s(dn, password)
    except Exception as e:
        return e
    else:
        return 0



def setpasswd(cn,oldp, newpwd):
        if cn:
            dn = str(get_info(cn)[0])
        if oldp:
            oldpassword = oldp
        if newpwd:
            newpassword = newpwd

        try:
            connect.bind_s(dn, oldpassword)
            connect.passwd_s(dn, oldpassword, newpassword)
        except Exception as  e:
            result = e
        else:
            result = "Password Changed Succesed!"
        finally:
            return result



# # print(setpasswd('test1', '123', '123'))
# # print(ldaplogin('test1', '1223'))
#
#
# # print(get_info('test1')[1]['userPassword'])
# print(get_info('aaa'))


