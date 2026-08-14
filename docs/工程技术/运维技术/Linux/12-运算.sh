#!/bin/bash
echo "-----------shell运算符演示-------"
# 第一种语法
val=`expr 2 + 2`
echo "2+2 = $val"
# 第二种语法
val=$(((2+3)*4))
echo "(2+3)*4 = $val"
# 第三种语法 [推荐]
val=$[(2+4)*3]
echo "(2+4)*3 = $val"
echo "-----------算术运算符------------"
a=10
b=20
# 变量三种写法
# c=`expr $a + $b`
# echo "a + b = $c"
# c=$[$a+$b]
# echo "a + b = $c"
c=$[a+b]
echo "a+b=$c"
c=$[a-b]
echo "a-b=$c"
c=$[a*b]
echo "a*b=$c"
c=$[a/b]
echo "a/b=$c"
c=$[a%b]
echo "a%b=$c"
c=$[a==b]
echo "a==b=$c"
if [ $a == $b ] # 注意空格,缺少空格会报错
then 
echo "a等于b"
fi
c=$[a!=b]
echo "a!=b=$c"
if [ $a != $b ]
then 
echo "a不等于b"
fi
echo "-----------关系运算符------------"
a=10
b=20
# 是否相等
if [ $a -eq $b ]
then
echo "$a -eq $b : a 等于 b"
else
echo "$a -eq $b : a 不等于 b"
fi
# 是否不相等
if [ $a -ne $b ]
then
echo "$a -ne $b : a 不等于 b"
else
echo "$a -ne $b : a 等于 b"
fi
# 是否大于
if [ $a -gt $b ]
then
echo "$a -gt $b : a 大于 b"
else
echo "$a -gt $b : a 不大于 b"
fi
# 是否小于
if [ $a -lt $b ]
then
echo "$a -lt $b : a 小于 b"
else
echo "$a -lt $b : a 不小于 b"
fi
# 是否大于等于
if [ $a -ge $b ]
then
echo "$a -ge $b : a 大于等于 b"
else
echo "$a -ge $b : a 不大于等于 b"
fi
# 是否小于等于
if [ $a -le $b ]
then
echo "$a -le $b : a 小于等于 b"
else
echo "$a -le $b : a 不小于等于 b"
fi
echo "-----------布尔运算符------------"
a=10
b=20
if true
then
echo "true"
fi
if [ $a != $b ]
then
   echo "$a != $b : a 不等于 b"
else
   echo "$a == $b: a 等于 b"
fi
if [ $a -lt 100 -a $b -gt 15 ]
then
   echo "$a 小于 100 且 $b 大于 15 : 返回 true"
else
   echo "$a 小于 100 且 $b 大于 15 : 返回 false"
fi
if [ $a -lt 100 -o $b -gt 100 ]
then
   echo "$a 小于 100 或 $b 大于 100 : 返回 true"
else
   echo "$a 小于 100 或 $b 大于 100 : 返回 false"
fi
if [ $a -lt 5 -o $b -gt 100 ]
then
   echo "$a 小于 5 或 $b 大于 100 : 返回 true"
else
   echo "$a 小于 5 或 $b 大于 100 : 返回 false"
fi
echo "-----------逻辑运算符------------"
a=10
b=20

if [[ $a -lt 100 && $b -gt 100 ]]
then
   echo "返回 true"
else
   echo "返回 false"
fi

if [[ $a -lt 100 || $b -gt 100 ]]
then
   echo "返回 true"
else
   echo "返回 false"
fi
echo "-----------字符串运算符----------"
a="abc"
b="efg"

if [ $a = $b ]
then
   echo "$a = $b : a 等于 b"
else
   echo "$a = $b: a 不等于 b"
fi
if [ $a != $b ]
then
   echo "$a != $b : a 不等于 b"
else
   echo "$a != $b: a 等于 b"
fi
if [ -z $a ]
then
   echo "-z $a : 字符串长度为 0"
else
   echo "-z $a : 字符串长度不为 0"
fi
if [ -n "$a" ]
then
   echo "-n $a : 字符串长度不为 0"
else
   echo "-n $a : 字符串长度为 0"
fi
if [ $a ]
then
   echo "$a : 字符串不为空"
else
   echo "$a : 字符串为空"
fi
echo "-----------文件测试运算符------------"
file="/var/www/runoob/test.sh"
if [ -r $file ]
then
   echo "文件可读"
else
   echo "文件不可读"
fi
if [ -w $file ]
then
   echo "文件可写"
else
   echo "文件不可写"
fi
if [ -x $file ]
then
   echo "文件可执行"
else
   echo "文件不可执行"
fi
if [ -f $file ]
then
   echo "文件为普通文件"
else
   echo "文件为特殊文件"
fi
if [ -d $file ]
then
   echo "文件是个目录"
else
   echo "文件不是个目录"
fi
if [ -s $file ]
then
   echo "文件不为空"
else
   echo "文件为空"
fi
if [ -e $file ]
then
   echo "文件存在"
else
   echo "文件不存在"
fi

