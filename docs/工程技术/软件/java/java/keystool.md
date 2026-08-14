# 参考: https://zhuanlan.zhihu.com/p/31385073
# 生成
# .\keytool -genkey -alias tomcat -dname "CN=Andy,OU=kfit,O=kfit,L=HaiDian,ST=BeiJing,C=CN" -storetype PKCS12 -keyalg RSA -keysize 2048 -keystore keys.p12 -validity 365
# 导出
# .\keytool -exportcert -rfc -keystore keys.p12 -file c:\keys.p12 -alias tomcat -storepass qwerty