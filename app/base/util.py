import hashlib, binascii, os

def hash_pass( password ):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash)

def verity_pass(provided_password, stored_password):
    stored_password = stored_password.decode('ascii')
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                provided_password.encode('utf-8'),
                                salt.encode('ascii'),
                                100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

##version_name="1.0.0.000"
def up_version(version_name:str,type:int):
    verlist = version_name.split('.')
    if type==1: ##小版本升级
        numsm = int(verlist[3]) + 1
        if numsm < 10:
            versm = "00" + str(numsm)
        elif numsm > 100:
            versm = str(numsm) ##一般不可能超过999个小版本
        else:
            versm = "0" + str(numsm)
        verlist[3] = versm
    elif type==2: ##升级大版本,小版本归零
        ##大版本第三位目前按十进制递进
        verlg1 = int(verlist[0])
        verlg2 = int(verlist[1])
        verlg3 = int(verlist[2])
        if verlg3 < 9:
            verlist[2] = str(verlg3 + 1)
        else: ##第二位进1，暂时不用十进制
            verlist[1] = str(verlg2 + 1)
            verlist[2] = "0"
        verlist[3] = "000"
        ##暂时不变第一位
    return ".".join(verlist)

def get_ver_lg(version_name:str):
    verlist = version_name.split('.')
    return ".".join(verlist[:3])



