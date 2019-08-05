#!/usr/bin/perl

#↑perlのパスを自分の環境に合わせて書き直します。
#大抵は、「#!/usr/bin/perl」　か　「#!/usr/local/bin/perl」です。
#解らない場合はサーバー管理者(もしくはプロバイダー)に
#確認してください。

##カウンタモードの設定
#SSIを使用(文字表示)=1/JavaScriptを使用(画像表示)=2/
$Ec_mode="2";

##カウンタ用画像ディレクトリへのパス
#count.cgiを設置するディレクトリからのパスを指定する
#SSI式カウンタの場合には不要
$Ec_dir="img/count/";

#-----↑ここまで設定↑-----#
$hyouji="";
if($ENV{QUERY_STRING} eq "today"){$hyouji=2;}
elsif($ENV{QUERY_STRING} eq "yesterday"){$hyouji=3;}
else{$hyouji=1;}

require "pl/count/count_ys.cgi";
&index_count(1,$hyouji,$Ec_mode);
exit;

