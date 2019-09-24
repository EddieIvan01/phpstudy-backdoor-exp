# phpstudy-backdoor-exp

杭州网警的公告是官网被入侵，PHPStudy作者单方面声明是其他下载站的版本被植入后门（我居然信了）

本来都没打算测试自己的版本，因为是从官网下的，结果一测试真的有后门。所以别存侥幸心理，别信利益相关者的话

后门存在于`php/ext/php_xmlrpc.dll`中，strings即可看到eval字符串

