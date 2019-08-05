#!/usr/bin/perl

#↑perlのパスを自分の環境に合わせて書き直します。
#大抵は、「#!/usr/bin/perl」　か　「#!/usr/local/bin/perl」です。
#解らない場合はサーバー管理者(もしくはプロバイダー)に
#確認してください。

require 'pl/jcode.pl';
require 'pl/cfg.cgi';
require 'pl/temp.cgi';

################################################################
# Yomi-Search Ver4 [サーチエンジン] (Since:1999/09/22)
#   (C) 1999-2001 by yomi
#   Eメール: yomi@pekori.to
#   ホームページ: http://yomi.pekori.to/
################################################################

## ---[利用規約]------------------------------------------------------------+
## 1. このスクリプトはフリーソフトです。このスクリプトを使用した
##    いかなる損害に対して作者は一切の責任を負いません。
## 2. このスクリプトを使用した時点で利用規約(http://yomi.pekori.to/kiyaku.html)
##    に同意したものとみなさせていただきます。
##    ご使用になる前に必ずお読みください。
## 3. 同梱の「アイコン (new.gif/recom.gif/sougogif.gif) 」の著作権は
##   「牛飼いとアイコンの部屋  (http://www.ushikai.com/)」に帰属しています。
## -------------------------------------------------------------------------+

&form_decode();
if($EST{task}==1){&go_TASK;}

#各モードへ分岐
#-----------------#
if($FORM{mode}){
if(!$EST{home}){$EST{home}=$EST{script};}
if($FORM{mode} eq "kt"){$Stitle=$ganes{$FORM{'kt'}};($Spre_kt_file)=split(/_/,$FORM{'kt'});} #各カテゴリの時の表示タイトル
elsif($FORM{mode} eq "new"){$Stitle="新着サイト"; $Spre_kt_file="new_ys";} #新着サイトの表示タイトル,ファイル名
elsif($FORM{mode} eq "renew"){$Stitle="更新サイト"; $Spre_kt_file="renew_ys";} #更新サイトの表示タイトル,ファイル名
elsif($FORM{mode} eq "random"){&random;} #ランダムジャンプ
elsif($FORM{mode} eq "link"){&link;} #リンクジャンプ
else{&mes("指定したモードは存在しません(mode=$FORM{mode})","モード選択エラー","java");}
##ページ設定
$FORM{'page'}=~s/\D//g;
if($FORM{'page'}<1 || $FORM{'page'}>1000){$FORM{'page'}=1;}

print "Content-type: text/html\n\n";
require "$EST{temp_path}kt.html";

&print_kt($FORM{kt},$FORM{mode},$FORM{page},$FORM{sort});

}
elsif($EST{home} && $EST{top}){&location($EST{home});}
else{&print_index;}
#-----------------#
exit;

#(6)メッセージ画面出力(&mes)
#書式:&mes($arg1,$arg2,$arg3);
#機能:メッセージ画面を出力する
#引数:$arg1=>表示するメッセージ
#     $arg2=>ページのタイトル(省略時は「メッセージ画面」)
#     $arg3=>・JavaScriptによる「戻る」ボタン表示=java
#            ・$ENV{'HTTP_REFERER'}を使う場合=env
#            ・管理室へのボタン=kanri
#            ・通常のURL又はパスを指定する場合にはそのURL又はパスを記入
#            ・省略時は非表示
#     $arg4=>ロック解除=unlock
#戻り値:なし
sub mes{
local($MES,$Munlock,$BACK_URL,);
print "Content-type: text/html\n\n";
$Munlock=$_[3];
	if($Munlock eq "unlock"){&unlock();}
$MES=$_[0];
		if($_[1]){$TITLE=$_[1];}
		else{$TITLE="メッセージ画面";}
	if($_[2] eq "java"){
	$BACK_URL="<form><input type=button value=\"&nbsp;&nbsp;&nbsp;&nbsp;戻る&nbsp;&nbsp;&nbsp;&nbsp;\" onClick=\"history.back()\"></form>"
	}
	elsif($_[2] eq "env"){
	$BACK_URL="【<a href=\"$ENV{'HTTP_REFERER'}\">戻る</a>】";
	}
	elsif(!$_[2]){$BACK_URL="";}
	else{$BACK_URL="【<a href=\"$_[2]\">戻る</a>】";}

require "$EST{temp_path}mes.html";

exit;
}

#(7)フォームデータのデコード(&form_decode)
#書式:&form_decode($arg1,$arg2);
#機能:フォームデータをデコードする
#引数:$arg1=>「>」と「<」を（無効にする(省略時)=0/有効にする=1）
#     $arg2=>「\n」と「\r」を（無効にする(省略時)=0/有効にする=1）
#戻り値:なし
sub form_decode{
$arg1=$_[0];
$arg2=$_[1];
   if ($ENV{'REQUEST_METHOD'} eq "POST") { read(STDIN, $form, $ENV{'CONTENT_LENGTH'}); }
   else { $form = $ENV{'QUERY_STRING'}; }   @pairs = split(/&/,$form);
   foreach $pair (@pairs) {           ($name, $value) = split(/=/, $pair);
           $value =~ tr/+/ /;
           $value =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
           $name =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
if(!$arg1){
   $value =~ s/>/&gt;/g;
   $value =~ s/</&lt;/g;
   }
if(!$arg2){
   if(!$EST{syoukai_br}){$value =~ s/\n//g;}
   else{$value =~ s/\n/<br>/g;}
   $value =~ s/\r//g;
   }
           &jcode::convert(\$value,'sjis');
           &jcode::convert(\$name,'sjis'); $FORM{$name} = $value;
   }
}

#(5)ランダムジャンプ(&random)
sub random{
local($total_url,$id,$i=1,$jump_url,@Slog);
open(IN,"$EST{log_path}total_url.log");
	$total_url=<IN>;
close(IN);
srand(time ^ ($$ + ($$ << 15)));
$id = int(rand($total_url))+1;

open(IN,"$EST{log_path}$EST{logfile}");
	while(<IN>){
		if($i eq $id){@Slog=split(/<>/,$_); $jump_url=$Slog[2]; last;}
	$i++;
	}
close(IN);

&location($jump_url);
exit;
}

sub link{
#(6)リンクジャンプ処理(&link)
$FORM{id}=~s/\D//g;
if($FORM{id}){
	local($fl=0,@ref_list);
		#refererチェック
		if(!$ENV{'HTTP_REFERER'}){$fl=1;} #refererが無いときにカウントしない場合にはこの行を削除
		@ref_list=split(/,/,$EST{rank_ref});
		if(!$EST{rank_ref}){$fl=1;}
		else{
			foreach(@ref_list){
				if(index($ENV{'HTTP_REFERER'},$_)>=0){$fl=1;}
			}
		}
	if($fl){
		$FORM{id}=~s/\n//g;
		&lock_rank();
		open(OUT,">>$EST{log_path}rank_temp_ys.cgi");
			print OUT "$FORM{id}<>" . time() . "<>$ENV{'REMOTE_ADDR'}\n";
		close(OUT);
		&unlock_rank();
	}
}
if($FORM{url}){&location($FORM{url});}
else{ #ログファイルからURLを検索する(Ver3と互換)
	open(IN,"$EST{log_path}$EST{logfile}");
	my $link_fl=0; my($link);
	while(<IN>){
		@Slog=split(/<>/,$_,4);
		if($Slog[0] eq $FORM{id}){$link=$Slog[2];$link_fl=1;last;}
	}
	close(IN);
	if(!$link_fl){&mes("該当するデータが見つかりません","エラー","java");}
	else{&location($link);}
}
}

##-- end of yomi.cgi --##
