#!/usr/bin/perl

#↑perlのパスを自分の環境に合わせて書き直します。
#大抵は、「#!/usr/bin/perl」　か　「#!/usr/local/bin/perl」です。
#解らない場合はサーバー管理者(もしくはプロバイダー)に
#確認してください。

require 'pl/jcode.pl';
require 'pl/cfg.cgi';
&EST_reg;
require 'pl/temp.cgi';

################################################################
# Yomi-Search用データ登録用プログラム
################################################################
#(1)登録画面(新規登録・管理人代理登録・登録内容変更)(&regist)
#(2)プレビュー画面(&preview)
#(3)入力内容の整形(&join_fld)
#(4)入力内容のチェック(&check)
#(5)登録結果画面出力(&PRend)
#(6)修正・削除のためのパスワード認証(&enter)
#(7)ヘルプの表示(&help)
#(8)パスワードの再発行・変更(&act_repass)
#(9)リンク切れ報告フォーム(&no_link)

#(p1)新規登録実行(&act_regist)
#(p2)登録内容変更(&act_mente)
#(p3)削除実行(&act_del)

&form_decode;
$Eref=$ENV{'HTTP_REFERER'};
$ENV{'HTTP_REFERER'}="";
#-----------------#
if($FORM{'preview'} eq "on"){&preview;} #プレビュー画面
elsif($FORM{mode} eq "regist"){&regist;} #登録画面
elsif($FORM{mode} eq "act_regist"){&act_regist;} #新規登録実行
elsif($FORM{mode} eq "act_mente"){&act_mente;} #登録内容変更実行
elsif($FORM{mode} eq "act_del"){&act_del;} #削除実行
elsif($FORM{mode} eq "enter"){&enter;} #パスワード認証
elsif($FORM{mode} eq "help"){&help;} #ヘルプの表示
elsif($FORM{mode} eq "act_repass"){&act_repass;} #パスワードの再発行
elsif($FORM{mode} eq "no_link"){&no_link;} #リンク切れ報告フォーム
else{&regist;} #登録画面
exit;
#-----------------#

sub regist{
#(1)登録画面(新規登録・管理人代理登録・登録内容変更)(&regist)

#クッキーを記録
if($FORM{'in_mode'} eq "mente"){ #登録内容変更時
	&get_cookie;

	if($FORM{changer} ne "admin" && $FORM{pass}){$CK_data[0]=$FORM{pass};} #登録者パスワード
	$CK_data[1]=$FORM{id}; #ID
	if($FORM{changer} eq "admin"){$CK_data[2]="admin";} #変更者
	if($FORM{changer} eq "admin" && $FORM{pass}){$CK_data[3]=$FORM{pass};} #管理者パスワード
	
	if($FORM{cookie} eq "off"){&set_fo_cookie;}
	else{&set_cookie;}
}

#パスワード認証(管理者認証)
if($FORM{'changer'} eq "admin"){
local($cr_pass);
	if($EST{crypt}){$cr_pass=crypt($FORM{pass},$EST{pass});}
	else{$cr_pass=$FORM{pass};}
	if($cr_pass ne $EST{pass}){
		if(!$ENV{'REMOTE_HOST'}){$ENV{'REMOTE_HOST'}=gethostbyaddr(pack("C4", split(/\./, $ENV{'REMOTE_ADDR'})), 2);}
		&mes("パスワードの認証に失敗しました<br>認証したコンピュータのIPアドレス：<b>$ENV{'REMOTE_ADDR'}</b><br>認証したコンピュータのホスト名：<b>$ENV{'REMOTE_HOST'}</b>","パスワード認証失敗","java");
	}
}

#管理人のみが登録できるモード
if($EST_reg{no_regist} && $FORM{in_mode} ne "mente" && $FORM{changer} ne "admin"){
	&mes("現在、訪問者による新規登録は停止されています","エラー","java");
}

# 各フィールドのデータを「$P～」に入力
#$Pdata[0]=データID,$Pdata[1]=タイトル,$Pdata[2]=ホームページのURL,$Pdata[3]=マークデータ
#$Pdata[4]=更新日,$Pdata[5]=パスワード,$Pdata[6]=紹介文,$Pdata[7]=管理人コメント
#$Pdata[8]=お名前,$Pdata[9]=メールアドレス,$Pdata[10]=カテゴリ(リスト),$Pdata[11]=time
#$Pdata[12]=バナーURL,$Pdata[13]=アクセス数,$Pdata[14]=IP,$Pdata[15]=キーワード
# $Pmode=>送信先のモード
# $FORM{'in_mode'}=>概入力値設定モード(なし,new_dairi,mente,form)
# $Smode_name=>各モードの判定用の内部変数(なし,new_dairi,mente)
# $$FORM{'changer'}=>変更者(なし,admin)

##概入力値設定($FORM{'in_mode'})
#新規登録()
if(!$FORM{'in_mode'}){@Pdata=("","","http://","","","","","","","",$FORM{'kt'},"","http://","","","");}
#管理人代理登録(new_dairi)
elsif($FORM{'in_mode'} eq "new_dairi"){}
#内容変更(mente)
elsif($FORM{'in_mode'} eq "mente"){
local($cr_pass,$i=0);
	open(IN,"$EST{log_path}$EST{logfile}");
		while(<IN>){
			@Pdata=split(/<>/,$_);
			if($Pdata[0] eq $FORM{id}){
				if($EST{crypt}){$cr_pass=crypt($FORM{pass},$Pdata[5]);}
				else{$cr_pass=$FORM{pass};}
				if($FORM{changer} ne "admin" && $Pdata[5] ne $cr_pass){&mes("パスワードが違います","パスワード認証エラー","java");}
				$i=1;
				last;
			}
		}
	close(IN);
	if(!$i){&mes("該当するデータはありません","エラー","java");}
}
#外部入力(form)
elsif($FORM{'in_mode'} eq "form"){
	$FORM{'Fkt'}="";
	foreach $kt_no(1 .. $EST_reg{kt_max}){
		$FORM{'Fkt'} .= $FORM{"Fkt$kt_no"} . "&";
	}
	@Pdata=("",$FORM{'Ftitle'},$FORM{'Furl'},"","",$FORM{'Fpass'},$FORM{'Fsyoukai'},"",$FORM{'Fname'},$FORM{'Femail'},$FORM{'Fkt'},"",$FORM{'Fbana_url'},"","",$FORM{'Fkey'});
}
else{@Pdata=();}

##$Smode_nameの設定
#管理人代理登録
if($FORM{'changer'} eq "admin" && $FORM{'in_mode'} ne "mente"){$Smode_name="new_dairi";}
#登録内容変更
elsif($FORM{'in_mode'} eq "mente"){$Smode_name="mente";}
#登録者の新規登録
else{$Smode_name="";}

##$Pmodeの設定
#登録内容変更
if($FORM{'Smode_name'} eq "mente"){
	$Pmode="act_mente";
}
#新規登録
else{
	$Pmode="act_regist";
}

##その他の設定
#相互リンクの有無
$MES_sougo{1}=" checked"; $MES_sougo{0}="";



#テンプレートの読み込み
if($Smode_name eq "new_dairi"){
print "Content-type: text/html\n\n";
require "$EST{temp_path}regist_new_admin.html";
}
elsif($FORM{'changer'} ne "admin" && $Smode_name eq "mente"){
	if($EST{syoukai_br}){
		$Pdata[6]=~s/<br>/\n/g; $Pdata[7]=~s/<br>/\n/g;
	}
	if($EST_reg{no_mente}){&mes("現在、登録者による修正・削除は停止されています","エラー","java");}
	print "Content-type: text/html\n\n";
	require "$EST{temp_path}regist_mente.html";
}
elsif($FORM{'changer'} eq "admin" && $Smode_name eq "mente"){
	if($EST{syoukai_br}){
		$Pdata[6]=~s/<br>/\n/g; $Pdata[7]=~s/<br>/\n/g;
	}
	print "Content-type: text/html\n\n";
	require "$EST{temp_path}regist_mente_admin.html";
}
else{
print "Content-type: text/html\n\n";
require "$EST{temp_path}regist_new.html";
}

}

sub PR_mark{
##マーク
if($FORM{'changer'} eq "admin"){
local(@mark); @mark=split(/_/,$Pdata[3]);
print<<"EOM";
	<li>【マーク】
		<ul>
EOM
foreach(1 .. 2){ #←マーク数を増やすときは修正
		print "<input type=checkbox name=Fmark$_ value=1";
			if($mark[$_-1]){print " checked";}
		print ">" . $EST{"name_m$_"} . "　 ";
}
print<<"EOM";
		</ul><br>
EOM
}
}


sub PR_kt{
##登録するカテゴリを表示(&PR_kt)

print<<"EOM";
EOM

 local($PRbf_kt,@kt_list,@kt,$kt_no=1,$line,@Pkt,$PRselect=" selected");
@Pkt=split(/&/,$Pdata[10]);

	if($EST_reg{kt_min} ne $EST_reg{kt_max}){print "<ul>※<b>$EST_reg{kt_min}</b>～<b>$EST_reg{kt_max}</b>個まで選択できます<br>";}
	else{print "<ul>※<b>$EST_reg{kt_max}</b>個選択してください<br>";}
print<<"EOM";
		※各カテゴリの詳細は「<a href="$EST{html_path_url}sitemap.html">カテゴリ一覧</a>」を参考にしてください<br>
EOM
&gane_st; #ジャンルステータスをロード
@kt_list=sort keys(%ganes);
foreach $kt_no(1 .. $EST_reg{kt_max}){
$PRselect=" selected";
print<<"EOM";
		<select name=Fkt$kt_no size=7>
EOM

if($Pkt[$kt_no-1]){print "<option value=\"" . $Pkt[$kt_no-1] . "\"$PRselect>" . &full_kt($Pkt[$kt_no-1]) . "\n"; $PRselect="";}
print<<"EOM";
			<option value=""$PRselect>--指定しない--
EOM
	foreach $line(@kt_list){
		if($FORM{changer} eq "admin" || !$gane_UR{$line}){
			print "<option value=\"$line\">" . &full_kt($line) . "\n";
		}
	}
print<<"EOM";
		</select><br><br>
EOM
}
print "</ul><br>";

}


sub cr{
#著作権表示(削除・変更をしないでください。ただし、中寄せ・左寄せは可)

print<<"EOM";
<p><div align=center>- <a href="http://yomi.pekori.to" target="_blank">Yomi-Search</a> -</div></p>
EOM
}

sub preview{
#(2)プレビュー画面(&preview)
#※登録者の新規登録時にのみ使用
&check("url_no_check");

##その他の設定
#相互リンクの有無
$MES_sougo{1}=" checked"; $MES_sougo{0}="";

	#紹介文の改行を変換(<br>→\n)
	$FORM{Fsyoukai}=~s/<br>/\n/g;

print "Content-type: text/html\n\n";

require "$EST{temp_path}regist_new_preview.html";

}


sub PR_preview_kt1{
#(2.1)カテゴリを表示1
foreach $kt_no(1 .. $EST_reg{kt_max}){
print "	<input type=hidden name=Fkt" . $kt_no . " value=\"" . $FORM{"Fkt$kt_no"} . "\">\n";
}
}

sub PR_preview_kt2{
#(2.2)カテゴリを表示2
foreach $kt_no(1 .. $EST_reg{kt_max}){
print &full_kt($FORM{"Fkt$kt_no"});
print<<"<!--HTML-->";
<input type=hidden name=Fkt$kt_no value="$FORM{"Fkt$kt_no"}">
<br>
<!--HTML-->
}
}


sub join_fld{
#(3)入力内容の整形(&join_fld)
@Slog=(); #登録更新用のデータ配列
local @arg=@_;
#$arg[0]=登録用のデータID
#[モード]
# $Smode_name=>各モードの判定用の内部変数(なし,new_dairi,mente)
# $FORM{'changer'}=>変更者(なし,admin)
#※登録内容変更の場合の変更前データは「@Spre_log」に格納されている

##登録No(データID)(0)
$Slog[0]=$arg[0];

##タイトル(1)
$Slog[1]=$FORM{'Ftitle'};

##URL(2)
$Slog[2]=$FORM{'Furl'};

##マークデータ(3)
if($FORM{'changer'} eq "admin"){ #変更者が管理人
$FORM{'Fmark'}="";
foreach(1 .. 2){ #←マーク数を増やすときは修正
	if($FORM{"Fmark$_"}){$FORM{'Fmark'} .= "1_";}
	else{$FORM{'Fmark'} .= "0_";}
}
$FORM{'Fmark'}=substr($FORM{'Fmark'},0,-1);
$Slog[3]=$FORM{'Fmark'};
}
elsif(!$Smode_name){$Slog[3]="0_0";} #登録者の新規登録
else{$Slog[3]=$Spre_log[3];} #登録者の変更

##更新日(4)
	#日時の取得
	$Slog[4]=&get_time(0,1);

##パスワード(5)
if($Smode_name eq "mente"){$Slog[5]=$Spre_log[5];} #内容変更時
else{ #新規登録時
$Spass=$FORM{'Fpass'}; #暗号化前のパスワードを保存
	if($EST{crypt}){$Slog[5]=crypt($FORM{'Fpass'},"ys");} #crypt使用可能
	else{$Slog[5]=$FORM{'Fpass'};} #crypt使用不可
}

##紹介文(6)
$Slog[6]=$FORM{'Fsyoukai'};

##管理人コメント(7)
if($FORM{'changer'} eq "admin"){ #変更者が管理人
$Slog[7]=$FORM{'Fkanricom'};
}
elsif(!$Smode_name){$Slog[7]="";} #登録者の新規登録
else{$Slog[7]=$Spre_log[7];} #登録者の変更

##お名前(8)
$Slog[8]=$FORM{'Fname'};

##E-mail(9)
$Slog[9]=$FORM{'Femail'};

##カテゴリ(10)
if($EST{user_change_kt} && $FORM{mode} eq "act_mente" && $FORM{'changer'} ne "admin"){ #登録者の変更でカテゴリ変更禁止の場合
local(@kt,$kt,$i=1);
@kt=split(/&/,$Spre_log[10]);
$Slog[10]=$Spre_log[10];
	foreach $kt(@kt){
	$FORM{"Fkt$i"}=$kt;
	$i++;
	}
}
else{ #その他の場合
$FORM{'Fkt'}="";
	foreach(1 .. $EST_reg{kt_max}){
		$FORM{'Fkt'} .= $FORM{"Fkt$_"} . "&";
	}
	$FORM{'Fkt'}=substr($FORM{'Fkt'},0,-1);
	$Slog[10]=$FORM{'Fkt'};
}

##time形式(11)
{local(@time);
@time=split(/_/,$Spre_log[11]); $times=time();
if($Smode_name eq "mente"){ #内容変更時
	if(!$time[1] && $times-$time[0]<$EST{new_time}*86400){$Slog[11]= $times . "_0";}
	else{$Slog[11]= $times . "_1";}
}
else{$Slog[11]= $times . "_0";} #新規登録時
}

##バナーURL(12)
$Slog[12]=$FORM{'Fbana_url'};

##アクセス数(13)
if($Smode_name eq "mente"){$Slog[13]=$Spre_log[13];} #内容変更時
else{$Slog[13]="0_0_0_0";} #新規登録時

##最終アクセスIP(14)
if($Smode_name eq "mente"){$Slog[14]=$Spre_log[14];} #内容変更時
else{$Slog[14]="";} #新規登録時

##キーワード(15)
$Slog[15]=$FORM{'Fkey'};

##</ここまで>

##仮登録モードの場合の設定
if($EST{user_check} && $FORM{changer} ne "admin" && $FORM{mode} eq "act_regist"){
	$Slog[14]=join("<1>",$FORM{Fsougo},$FORM{Fadd_kt},$FORM{'Fto_admin'})
}

}

sub check{
#(4)入力内容のチェック(&check)

##禁止ワードのチェック
	if($EST_reg{kt_no_word}){
		local(@no_words,$word,$check_str);
			#ワードチェック対象の項目
			$check_str=join(" ",$FORM{Fname},$FORM{Femail},$FORM{Furl},$FORM{Fbana_url},$FORM{Ftitle},$FORM{Fsyoukai},$FORM{Fkey});
		@no_words=split(/ /,$EST_reg{kt_no_word});
		foreach $word(@no_words){
			if(index($check_str,$word)>=0){&mes("登録データの中にが禁止されている言葉が入っています。<br>登録しようとしているデータのジャンルをこのサーチエンジンが禁止している可能\性があります。","ワードチェックエラー","back_reg");}
		}
		local($addr_host);
			if(!$ENV{'REMOTE_HOST'}){$ENV{'REMOTE_HOST'}=gethostbyaddr(pack("C4", split(/\./, $ENV{'REMOTE_ADDR'})), 2);}
			$addr_host=$ENV{REMOTE_ADDR} . " " . $ENV{'REMOTE_HOST'};
		foreach $word(@no_words){
			if(index($addr_host,$word)>=0){&mes("このIP又はホスト名からの登録は禁止されている可能\性があります。<br>$ENV{'REMOTE_ADDR'}/$ENV{'REMOTE_HOST'}<br>","IP/HOSTチェックエラー","back_reg");}
		}
	}

##名前
	if($EST_reg{Fname} && !$FORM{Fname}){&mes("<b>お名前</b>は<font color=red>記入必須項目</font>です","記入ミス","back_reg");}
	if(($_=length($FORM{Fname})-($EST_reg{Mname}*2))>0){&mes("<b>お名前</b>は全角<b>$EST_reg{Mname}</b>文字以内でご記入ください","文字数オーバー(半角換算で$_文字分)","back_reg");}
	$FORM{Fname}=~ s/\n//g;


##メールアドレス
	if($EST_reg{Femail} && !$FORM{Femail}){&mes("<b>メールアドレス</b>は<font color=red>記入必須項目</font>です","記入ミス","back_reg");}
	elsif(($_=length($FORM{Femail})-$EST_reg{Memail})>0){&mes("<b>メールアドレス</b>は半角<b>$EST_reg{Memail}</b>文字以内でご記入ください","文字数オーバー(半角換算で$_文字分)","back_reg");}
	elsif($EST_reg{Femail} && $FORM{Femail} !~ /(.*)\@(.*)\.(.*)/){&mes("<b>メールアドレス</b>の入力が正しくありません","記入ミス","back_reg");}
	$FORM{Femail}=~ s/\n//g;


##パスワード
if($FORM{mode} ne "act_mente"){
	if(!$FORM{Fpass}){&mes("<b>パスワード</b>は<font color=red>記入必須項目</font>です","記入ミス","back_reg");}
	elsif(($_=length($FORM{'Fpass'})-8)>0){&mes("<b>パスワード</b>は半角<b>8</b>文字以内でご記入ください","文字数オーバー(半角換算で$_文字分)","back_reg");}
	elsif($FORM{Fpass} ne $FORM{Fpass2}){&mes("２回の<b>パスワード</b>入力が一致しませんでした","入力ミス","back_reg");}
	$FORM{Fpass}=~ s/\n//g;
}

##ホームページアドレス(２重登録チェックは別のところに記述)
	if($FORM{Furl} eq "http://"){$FORM{Furl}="";}
	if($EST_reg{Furl} && !$FORM{Furl}){&mes("<b>ホームページアドレス</b>は<font color=red>記入必須項目</font>です","記入ミス","back_reg");}
	elsif(($_=length($FORM{Furl})-$EST_reg{Murl})>0){&mes("<b>ホームページアドレス</b>は半角<b>$EST_reg{Murl}</b>文字以内でご記入ください","文字数オーバー(半角換算で$_文字分)","back_reg");}
	elsif($FORM{Furl} && $FORM{Furl} !~ /^https?:\/\/.+\..+/){&mes("<b>ホームページアドレス</b>の入力が正しくありません","記入ミス","back_reg");}
	$FORM{Furl}=~ s/\n//g;


##タイトルバナーのURL
	if($EST_reg{bana_url}){
		if($FORM{Fbana_url} eq "http://"){$FORM{Fbana_url}="";}
		if($EST_reg{Fbana_url} && !$FORM{Fbana_url}){&mes("<b>タイトルバナーのURL</b>は<font color=red>記入必須項目</font>です","記入ミス","back_reg");}
		elsif(($_=length($FORM{Fbana_url})-$EST_reg{Mbana_url})>0){&mes("<b>タイトルバナーのURL</b>は半角<b>$EST_reg{Mbana_url}</b>文字以内でご記入ください","文字数オーバー(半角換算で$_文字分)","back_reg");}
		elsif($FORM{Fbana_url} && $FORM{Fbana_url} !~ /^https?:\/\/.+\..+(\.gif|\.jpg|\.jpeg|\.png)$/i){&mes("<b>タイトルバナーのURL</b>の入力が正しくありません","記入ミス","back_reg");}
	}
	else{$FORM{Fbana_url}="";}
	$FORM{Fbana_url}=~ s/\n//g;


##ホームページのタイトル
	if($EST_reg{Ftitle} && !$FORM{Ftitle}){&mes("<b>ホームページのタイトル</b>は<font color=red>記入必須項目</font>です","記入ミス","back_reg");}
	if(($_=length($FORM{Ftitle})-($EST_reg{Mtitle}*2))>0){&mes("<b>ホームページのタイトル</b>は全角<b>$EST_reg{Mtitle}</b>文字以内でご記入ください","文字数オーバー(半角換算で$_文字分)","back_reg");}
	$FORM{Ftitle}=~ s/\n//g;

##ホームページの紹介文
	if($EST_reg{Fsyoukai} && !$FORM{Fsyoukai}){&mes("<b>ホームページの紹介文</b>は<font color=red>記入必須項目</font>です","記入ミス","back_reg");}
	if(($_=length($FORM{Fsyoukai})-($EST_reg{Msyoukai}*2))>0){&mes("<b>ホームページの紹介文</b>は全角<b>$EST_reg{Msyoukai}</b>文字以内でご記入ください","文字数オーバー(半角換算で$_文字分)","back_reg");}
	if(!$EST{syoukai_br}){$FORM{Fsyoukai}=~ s/\n//g;}
	else{$FORM{Fsyoukai}=~ s/\n/<br>/g;}

##管理人コメント
	$FORM{Fkanricom}=~ s/\n/<br>/g;

##カテゴリ
{local(%kt_fl,$i,$j=0,$PR_kt);
&gane_st; #ジャンルステータスをロード
	foreach $i(1 .. $EST_reg{kt_max}){
		$FORM{"Fkt$i"}=~s/\n//g;
		if($kt_fl{$FORM{"Fkt$i"}}){$FORM{"Fkt$i"}="";}
		elsif($ganes{$FORM{"Fkt$i"}}){$kt_fl{$FORM{"Fkt$i"}}=1;}
		else{$FORM{"Fkt$i"}="";}
		##禁止カテゴリに登録しようとした場合
		if($FORM{changer} ne "admin" && $gane_UR{$FORM{"Fkt$i"}}){
			&mes("登録者の登録ができないカテゴリに変更しようとしています","カテゴリ選択ミス","back_reg");
		}
	}
	foreach(keys %kt_fl){$j++;}
	if($EST_reg{kt_min} eq $EST_reg{kt_max}){$PR_kt="<b>$EST_reg{kt_max}</b>個";}
	else{$PR_kt="<b>$EST_reg{kt_min}</b>～<b>$EST_reg{kt_max}</b>個";}
	if($EST_reg{kt_min}>$j || $j>$EST_reg{kt_max}){&mes("<b>カテゴリ</b>は$PR_kt選択してください","選択数ミス","back_reg");}
}


##キーワード
	if($EST_reg{Fkey} && !$FORM{Fkey}){&mes("<b>キーワード</b>は<font color=red>記入必須項目</font>です","記入ミス","back_reg");}
	if(($_=length($FORM{Fkey})-($EST_reg{Mkey}*2))>0){&mes("<b>キーワード</b>は全角<b>$EST_reg{Mkey}</b>文字以内でご記入ください","文字数オーバー(半角換算で$_文字分)","back_reg");}
	$FORM{Fkey}=~ s/\n//g;


##追加して欲しいカテゴリ
	if($FORM{mode} ne "act_mente" && $FORM{changer} ne "admin"){
		if($EST_reg{Fadd_kt} && !$FORM{Fadd_kt}){&mes("<b>追加して欲しいカテゴリ</b>は<font color=red>記入必須項目</font>です","記入ミス","back_reg");}
		if(($_=length($FORM{Fadd_kt})-($EST_reg{Madd_kt}*2))>0){&mes("<b>追加して欲しいカテゴリ</b>は全角<b>$EST_reg{Madd_kt}</b>文字以内でご記入ください","文字数オーバー(半角換算で$_文字分)","back_reg");}
		$FORM{Fadd_kt}=~ s/\n//g;
	}

##相互リンクの有無
	$MES_sougo{1}="する"; $MES_sougo{0}="しない";
	if($FORM{Fsougo} ne "1"){$FORM{Fsougo}=0;}

##管理人へのメッセージ
	if($FORM{mode} ne "act_mente" && $FORM{changer} ne "admin"){
		if($EST_reg{Fto_admin} && !$FORM{Fto_admin}){&mes("<b>管理人へのメッセージ</b>は<font color=red>記入必須項目</font>です","記入ミス","back_reg");}
		if(($_=length($FORM{Fto_admin})-($EST_reg{Mto_admin}*2))>0){&mes("<b>管理人へのメッセージ</b>は全角<b>$EST_reg{Mto_admin}</b>文字以内でご記入ください","文字数オーバー(半角換算で$_文字分)","back_reg");}
		if(!$EST{syoukai_br}){$FORM{Fto_admin}=~ s/\n//g;}
		else{$FORM{Fto_admin}=~ s/\n/<br>/g;}
	}

}

sub PRend{
#(5)登録結果画面出力(&PRend)
print "Content-type: text/html\n\n";
require "$EST{temp_path}regist_new_end.html";

}

sub enter{
#(6)修正・削除のためのパスワード認証(&enter)

#クッキーの読み込み
&get_cookie;
	if($CK_data[4] && $CK_data[3] && $FORM{id}){ #直接認証
		$FORM{pass}=$CK_data[3];
		$FORM{changer}="admin";
		$FORM{in_mode}="mente";
		&regist;
		exit;
	}
if(!$FORM{id}){
	$FORM{id}=$CK_data[1];
}

#概入力値の設定
$FORM{id}=~s/\D//g;
if($FORM{id}){
local(@Tlog,$i=0);
	open(IN,"$EST{log_path}$EST{logfile}");
		while(<IN>){
			@Tlog=split(/<>/,$_,4);
			if($Tlog[0] eq "$FORM{id}"){$i=1; last;}
		}
	close(IN);
	if(!$i){&mes("指定されたIDのデータは存在しません","エラー","java");}

$PR_data=<<"EOM";
[登録データ]<br>
<table width=200><tr><td>
■タイトル：<br>$Tlog[1]<br>
■URL：<br><a href="$Tlog[2]">$Tlog[2]</a>
<div align=right>[<a href="$Tlog[2]" target="_blank">確認</a>]</div>
</td></tr>
</table>
EOM

}

print "Content-type: text/html\n\n";
require "$EST{temp_path}enter.html";

}

sub help{
#(7)ヘルプの表示(&help)
print "Content-type: text/html\n\n";
require "$EST{temp_path}help.html";
}

sub act_repass{
#(8)パスワードの再発行・変更(&act_repass)

local($new_pass,$cr_new_pass,@log_lines,$line,$id,$mail_to,@Slog);

	if($FORM{repass_mode} eq "repass"){ #パスワード再発行時
		if($FORM{repass_check} ne "on"){&mes("パスワード再発行の確認チェックがありません。もう一度戻ってからチェックを入れて再度実行してください","確認チェックをしてください","java");}
		if(!$EST{re_pass_fl}){&mes("パスワードの再発行はできない設定になっています","エラー","java");}
		#新しいパスワードを作成
		local($tane,$data_temp,@pass_rm);
		@pass_rm = (a .. z , 1 .. 9);
		srand($tane ^ ($$ + ($$ << 15)));
		foreach (1 .. 7) {
		$tane = time() + ($_ * 291);
		$data_temp = int(rand(34));
		$new_pass .= "$pass_rm[$data_temp]";
		}
		if($EST{crypt}){$cr_new_pass=crypt($new_pass,"ys");}
		else{$cr_new_pass=$new_pass;}
		
		
		if($EST{mail_pass}){$PR_mes="パスワードの再発行が完了しました<br>新しいパスワードはメールアドレスに送信されます";}
		else{$PR_mes="パスワードの再発行が完了しました<br>新しいパスワードは「 <b>$new_pass</b> 」です";}

	}
	else{ #パスワード変更時
		$FORM{new_pass}=~s/\W//g;
		$new_pass=$FORM{new_pass};
		if($EST{crypt}){$cr_new_pass=crypt($new_pass,"ys");}
		else{$cr_new_pass=$new_pass;}

		if($EST{mail_pass}){$PR_mes="パスワードの変更が完了しました<br>新しいパスワードはメールアドレスに送信されます";}
		else{$PR_mes="パスワードの変更が完了しました<br>新しいパスワードは「 <b>$new_pass</b> 」です";}
	}

&lock();
local($fl=0);
open(IN,"$EST{log_path}$EST{logfile}");
	while($line=<IN>){
		($id)=split(/<>/,$line,2);
		if($id eq $FORM{id}){
			@Slog=split(/<>/,$line);
			if($FORM{repass_mode} ne "repass"){
				if($EST{crypt} && $FORM{changer} ne "admin"){$cr_pass=crypt($FORM{pass},$Slog[5]);}
				elsif($EST{crypt} && $FORM{changer} eq "admin"){$cr_pass=crypt($FORM{pass},$EST{pass});}
				else{$cr_pass=$FORM{pass};}
				if($FORM{changer} ne "admin"){
					if($cr_pass ne $Slog[5]){&unlock(); &mes("パスワードが間違っています","エラー","java");}
				}
				else{
					if($cr_pass ne $EST{pass}){&unlock(); &mes("管理パスワードが間違っています","エラー","java");}
				}
			}
			else{
				if($FORM{email} ne $Slog[9]){&unlock(); &mes("IDとメールアドレスが一致しませんでした","エラー","java");}
			}
			$mail_to=$Slog[9];
			$Slog[5]=$cr_new_pass;
			$line=join("<>",@Slog);
			$fl=1;
		}
		push(@log_lines,$line);
	}
	if(!$fl){&unlock(); &mes("該当するIDはありません","エラー","java");}
close(IN);
open(OUT,">$EST{log_path}$EST{logfile}");
	print OUT @log_lines;
close(OUT);
@log_lines=();
if($EST{mail_pass}){require "pl/mail_ys.cgi"; &mail($mail_to,$EST{admin_email},"$EST{search_name} パスワード変更通知","pass","",*Slog);}
&unlock();

&mes($PR_mes,"パスワード変更完了","$EST{home}");
}

sub no_link{
#(9)リンク切れ報告フォーム(&no_link)

if($FORM{"pre"} eq "on"){
$Eref=~s/(\W)/'%' . unpack('H2',$1)/eg;
$mes=<<"EOM";
管理者に「<b>$FORM{title}</b>」についての通知を行います<br>
「通知する」ボタンを押すと管理者へ通知できます
<br><br>





<form action="regist_ys.cgi" method=post target="">
  <input type=hidden name=mode value="no_link">
  <input type=hidden name=id value="$FORM{id}">
  <input type=hidden name=pre value="">
  <input type=hidden name=ref value="$Eref">
  <input type=hidden name=title value="$FORM{title}">

	<ul>
	[通知種別]<br>
		<input type=checkbox name=type_no_link value="1">リンク切れ<br>
		<input type=checkbox name=type_move value="2">ホームページ移転<br>
		<input type=checkbox name=type_bana_no_link value="3">バナーリンク切れ<br>
		<input type=checkbox name=type_ill value="4">規約違反[<a href="$EST{cgi_path_url}regist_ys.cgi?mode=new">規約はこちら</a>]<br>
		<input type=checkbox name=type_other value="5">その他(コメント欄にもご記入ください)<br>
	<br>
	[コメント](必要があればご記入ください)<br>
		<textarea name=com cols=40 rows=4></textarea><br>
	<br>
	[お名前](任意)<br>
	<input type=text name=c_name><br>
	[E-Mail](任意)<br>
	<input type=text name=c_email><br>
	</ul>

</ul>
<center>
  <input type=submit value="通知する">
</center>
</form>

<hr width="90%">
<center>
<form><input type=button value=" 前の画面に戻る " onClick="history.back()"></form>
</center>
EOM
&mes($mes,"管理者への通知画面");
}

$FORM{id}=~s/\D//g;

if($FORM{id} && (index($ENV{HTTP_USER_AGENT},"Mozilla")>=0 || index($ENV{HTTP_USER_AGENT},"Lynx")>=0)){
	local($ip_fl=1,@ip);
	
	if($EST{no_link_ip}){
		@ip=split(/,/,$EST{no_link_ip});
		foreach(@ip){if(index($ENV{REMOTE_ADDR},$_)>=0){$ip_fl=0;last;}}
	}
	if($ip_fl){
		local($Dhoukoku,$Dcom,$Dname,$Demail,$fl=0);
		#報告種別(リンク切れ=0/サイト移転=1/バナーリンク切れ=2/規約違反=3/その他=4)
		if($FORM{type_no_link}){$Dhoukoku.="1,";$fl=1;}
		if($FORM{type_move}){$Dhoukoku.="2,";$fl=1;}
		if($FORM{type_bana_no_link}){$Dhoukoku.="3,";$fl=1;}
		if($FORM{type_ill}){$Dhoukoku.="4,";$fl=1;}
		if($FORM{type_other}){$Dhoukoku.="5,";$fl=1;}
			if(!$fl){&mes("「通知種別」に最低一つはチェックしてください","チェックミス","java");}
		#コメント
		$FORM{com}=~s/\n/<br>/g; $Dcom=$FORM{com};
		#名前
		$FORM{c_name}=~s/\n//g; $Dname=$FORM{c_name};
		#E-Mail
		$FORM{c_email}=~s/\n//g; $Demail=$FORM{c_email};
		if(length("$Dcom$Dname$Demail")>500){&mes("コメント、お名前、E-Mailの文字数は<br>合計で250文字(全角換算)までで、お願いします。","文字数オーバー","java");}
	open(OUT,">>$EST{log_path}no_link_temp.cgi");
		print OUT "$FORM{id}<>$ENV{'REMOTE_ADDR'}<>$Dhoukoku<>$Dcom<>$Dname<>$Demail<>\n";
	close(OUT);
	}
}

$FORM{ref}=~s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2',$1)/eg;
&mes("ご報告ありがとうございました<br>管理人に「<b>$FORM{title}</b>」についての通知を行いました","ご報告ありがとうございます",$FORM{ref});
}

sub act_regist{
#(p1)新規登録実行(&act_regist)
require "$EST{log_path}task_ys.cgi";
local($new,$new_id,@hyouji_log);
#$new=>追加データ書き込み用/%TASK=>更新するカテゴリリスト
#@hyouji_log=>結果表示用のログデータ


#パスワード認証(管理者認証)
if($FORM{'changer'} eq "admin"){
local($cr_pass);
	if($EST{crypt}){$cr_pass=crypt($FORM{pass},$EST{pass});}
	else{$cr_pass=$FORM{pass};}
	if($cr_pass ne $EST{pass}){
		if(!$ENV{'REMOTE_HOST'}){$ENV{'REMOTE_HOST'}=gethostbyaddr(pack("C4", split(/\./, $ENV{'REMOTE_ADDR'})), 2);}
		&mes("パスワードの認証に失敗しました<br>認証したコンピュータのIPアドレス：<b>$ENV{'REMOTE_ADDR'}</b><br>認証したコンピュータのホスト名：<b>$ENV{'REMOTE_HOST'}</b>","パスワード認証失敗","java");
	}
}

&check; #入力内容のチェック

&lock; #ロック

#ID取得&２重URL登録チェック
$Cgane_pre=0; #総登録数
if($EST_reg{nijyu_url}){$new_id=&get_id_url_ch(1);}
else{$new_id=&get_id;}

&join_fld($new_id); #入力内容の整形
$new=join("<>",@Slog,"\n");
@hyouji_log=@Slog;

if($EST{user_check} && $FORM{changer} ne "admin" && $FORM{mode} eq "act_regist"){ #<仮登録時>

#仮登録ログデータに追加書き込み
open(OUT,">>$EST{log_path}$EST{temp_logfile}");
	print OUT $new;
close(OUT);

##メールを送信
	#件名に付けるマークを設定
	local($PR_mail_add_line,$PR_mail_sougo,$PR_mail_com,$PR_mail_kt);
	&kenmei_put_mark;
	sub kenmei_put_mark{
		if($FORM{Fsougo}){$PR_mail_sougo="(link)";}
		else{$PR_mail_sougo="";}
		if($FORM{Fto_admin}){$PR_mail_com="(com)";}
		else{$PR_mail_com="";}
		if($FORM{Fadd_kt}){$PR_mail_kt="(kt)";}
		else{$PR_mail_kt="";}
		$PR_mail_add_line=$PR_mail_sougo . $PR_mail_com . $PR_mail_kt;
	}
$Slog[6]=~s/<br>/\n/g; $Slog[7]=~s/<br>/\n/g;
if($EST{mail_temp}){require "pl/mail_ys.cgi";}
if($EST{mail_to_admin} && $EST{mail_temp}){ #管理人へメール送信
	&mail($EST{admin_email},$Slog[9],"$EST{search_name} 仮登録完了通知$PR_mail_add_line","temp","admin",*Slog,$FORM{Fsougo},$FORM{Fadd_kt},$FORM{Fto_admin});
}
if($EST{mail_to_register} && $EST{mail_temp}){ #登録者へメール送信
	&mail($Slog[9],$EST{admin_email},"$EST{search_name} 仮登録完了通知","temp","",*Slog,$FORM{Fsougo},$FORM{Fadd_kt},$FORM{Fto_admin});
}
$Slog[6]=~s/\n/<br>/g; $Slog[7]=~s/\n/<br>/g;


&unlock(); #ロック解除

##登録結果出力
print "Content-type: text/html\n\n";
require "$EST{temp_path}regist_new_end_temp.html";


} #</仮登録時>
else{ #<新規登録時>

#本体ログデータに追加書き込み
open(OUT,">>$EST{log_path}$EST{logfile}");
	print OUT $new;
close(OUT);

##登録者のメッセージを保存する設定の場合
if(($FORM{Fadd_kt} || $FORM{Fto_admin}) && $EST_reg{look_mes} && $EST_reg{look_mes}=~/(\d+)(\w*)/){
local(@look_mes_list,@look_mes,$look_mes,$i=0,$max=$1);
	open(IN,"$EST{log_path}look_mes.cgi");
	while(<IN>){
	if($i<$max){push(@look_mes_list,$_);}
	else{last;}
	$i++;
	}
	close(IN);
	#一括送信する場合
	if($2 eq "m" && $i>=$max){
		$mail_mes=<<"EOM";
## $EST{search_name} 登録者からのメッセージ通知 ##

EOM
local(@tlook_mes);
		foreach(@look_mes_list){
		@tlook_mes=split(/<>/,$_);
		$mail_mes.=<<"EOM";
+-------------------------+
登録日：$tlook_mes[1] / お名前：$tlook_mes[5] / Email： $tlook_mes[4]
タイトル：$tlook_mes[7]
URL：
$tlook_mes[6]
修正用URL：
$EST{cgi_path_url}regist_ys.cgi?mode=enter&id=$tlook_mes[0]
EOM
		if($tlook_mes[2]){$mail_mes.="新設希望カテゴリ：$tlook_mes[2]\n";}
		if($tlook_mes[3]){
		$tlook_mes[3]=~s/<br>/\n/g;
		$mail_mes.=$tlook_mes[3] . "\n";
		}
		}
		$mail_mes.="+-------------------------+\n";
		require "pl/mail_ys.cgi";
		&mail($EST{admin_email},$EST{admin_email},"$EST{search_name} 登録者からのメッセージ通知($max件)","any","","","","","","",$mail_mes);
		$i=0;
		@look_mes_list=();
		open(OUT,">$EST{log_path}look_mes.cgi");
		close(OUT);
	}
	if($i eq $max){pop @look_mes_list;}
	#新規追加データ($look_mes)を作成
	$look_mes[0]=$Slog[0];
	$look_mes[1]=$Slog[4];
	$look_mes[2]=$FORM{Fadd_kt};
	$look_mes[3]=$FORM{Fto_admin}; $look_mes[4]=~s/\n/<br>/g;
	$look_mes[4]=$Slog[9];
	$look_mes[5]=$Slog[8];
	$look_mes[6]=$Slog[2];
	$look_mes[7]=$Slog[1];
	$look_mes=join("<>",@look_mes); $look_mes=~s/\n//g;
	$look_mes.="<>\n";
	unshift(@look_mes_list,$look_mes);
	open(OUT,">$EST{log_path}look_mes.cgi");
		print OUT @look_mes_list;
	close(OUT);
}

##メールを送信
unless($FORM{FCmail} eq "no" && $FORM{changer} eq "admin"){ #送信する設定なら
	#件名に付けるマークを設定
	local($PR_mail_sougo,$PR_mail_com,$PR_mail_kt);
	&kenmei_put_mark;
$Slog[6]=~s/<br>/\n/g; $Slog[7]=~s/<br>/\n/g;
if($EST{mail_new}){require "pl/mail_ys.cgi";}
if($EST{mail_to_admin} && $EST{mail_new}){ #管理人へメール送信
	&mail($EST{admin_email},$Slog[9],"$EST{search_name} 新規登録完了通知$PR_mail_add_line","new","admin",*Slog,$FORM{Fsougo},$FORM{Fadd_kt},$FORM{Fto_admin});
}
if($EST{mail_to_register} && $EST{mail_new}){ #登録者へメール送信
	&mail($Slog[9],$EST{admin_email},"$EST{search_name} 新規登録完了通知","new","",*Slog,$FORM{Fsougo},$FORM{Fadd_kt},$FORM{Fto_admin});
}
$Slog[6]=~s/\n/<br>/g; $Slog[7]=~s/\n/<br>/g;
}

#更新するカテゴリリストを作成
#%TASK/@TASK_listを使用
@TASK_list=();
$TASK{"new"}=1; #新着情報
if($FORM{'changer'} eq "admin"){ #マークカテゴリの更新
	foreach(1 .. 2){ #←マーク数を増やすときは修正
		if($FORM{"Fmark$_"}){$TASK{"m$_"}=1;}
	}
}
if($EST{html}){ #カテゴリをHTMLファイルで表示する場合
local(@kt,$i,$tmp);
	foreach $i(1 .. $EST_reg{kt_max}){
		if($FORM{"Fkt$i"}){
			$TASK{$FORM{"Fkt$i"}}=1;
			push(@TASK_list,$FORM{"Fkt$i"});
			@kt=split(/_/,$FORM{"Fkt$i"});
			if($#kt>0){
				pop(@kt); $tmp=join("_",@kt);
				$TASK{$tmp}=1;
				push(@TASK_list,$tmp);
			}
		}
	}
}
else{ #カテゴリをCGIで動的に表示する場合
local($kt,$i);
	foreach $i(1 .. $EST_reg{kt_max}){
		if($FORM{"Fkt$i"}){
			($kt)=split(/_/,$FORM{"Fkt$i"});
			$TASK{$kt}=1;
		}
	}
}

##派生ファイルの処理
if($EST{html} && $EST{task} ne "2"){ #即時処理(html && !cron)
&MK_html(*TASK_list);
&make_task;
}
else{&make_task;} #タスクファイルに書き込み

##総登録数を記録
open(OUT,">$EST{log_path}total_url.log");
	print OUT $Cgane_pre+1;
close(OUT);

&unlock(); #ロック解除

##登録結果出力
@Slog=@hyouji_log;
print "Content-type: text/html\n\n";
require "$EST{temp_path}regist_new_end.html";

} #</新規登録時>

}


sub get_id_url_ch{
##新規登録用のIDを取得&２重URL登録チェック
#チェックに掛かった場合にはロックも解除
#$arg=>(新規登録=1/内容変更=2)
local($id,$line,@Tlog,$fl=$_[0],$i=0,$pre_title);
	open(IN,"$EST{log_path}$EST{logfile}");
		while($line=<IN>){
			@Tlog=split(/<>/,$line);
			if($FORM{Furl} eq $Tlog[2]){$i++; $pre_title=$Tlog[1];}
			if($FORM{id} eq $Tlog[0]){@Spre_log=@Tlog;}
			if($fl<=$i){&unlock; &mes("そのURLはすでに登録されています<br><br>$Tlog[1] :<br>$Tlog[2]","２重登録エラー","java");}
			$id=$Tlog[0];
			$Cgane_pre++;
		}
		if($fl eq "2" && $i eq "1" && $Spre_log[2] ne $FORM{Furl}){&unlock; &mes("そのURLはすでに登録されています<br><br>$pre_title :<br>$FORM{Furl}","２重登録エラー","java");}
	close(IN);
	if($FORM{changer} ne "admin" && $EST{user_check} && $FORM{mode} eq "act_regist"){
	 #仮登録モードでユーザの新規登録時
		open(IN,"$EST{log_path}$EST{temp_logfile}");
			while($line=<IN>){
				@Tlog=split(/<>/,$line,5);
				if($FORM{Furl} eq $Tlog[2]){$i++;}
				if($fl<=$i){&unlock; &mes("そのURLは現在登録申\請中です<br><br>$Tlog[1] :<br>$Tlog[2]","２重登録エラー","java");}
				$id=$Tlog[0];
			}
		close(IN);
	}
return $id+1;
}

sub get_id{
##新規登録用のIDを取得
local($id,$line);
		if($FORM{changer} ne "admin" && $EST{user_check} && $FORM{mode} eq "act_regist"){ #仮登録モードでユーザの新規登録時
			open(IN,"$EST{log_path}$EST{temp_logfile}");
		}
		else{ #その他
			open(IN,"$EST{log_path}$EST{logfile}");
		}
		while(<IN>){$line=$_; $Cgane_pre++;} 
	close(IN);
	($id)=split(/<>/,$line);
return $id+1;
}


sub act_mente{
#(p2)登録内容変更(&act_mente)

if($FORM{changer} ne "admin" && $EST_reg{no_mente}){&mes("現在、登録者による修正・削除は停止されています","エラー","java");}

require "$EST{log_path}task_ys.cgi";
local($new,@log_lines,$line,@TASK_list);
#$new=>追加データ書き込み用/%TASK=>更新するカテゴリリスト

#パスワード認証(管理者認証)
if($FORM{'changer'} eq "admin"){
local($cr_pass);
	if($EST{crypt}){$cr_pass=crypt($FORM{pass},$EST{pass});}
	else{$cr_pass=$FORM{pass};}
	if($cr_pass ne $EST{pass}){
		if(!$ENV{'REMOTE_HOST'}){$ENV{'REMOTE_HOST'}=gethostbyaddr(pack("C4", split(/\./, $ENV{'REMOTE_ADDR'})), 2);}
		&mes("パスワードの認証に失敗しました<br>認証したコンピュータのIPアドレス：<b>$ENV{'REMOTE_ADDR'}</b><br>認証したコンピュータのホスト名：<b>$ENV{'REMOTE_HOST'}</b>","パスワード認証失敗","java");
	}
}

##その他の設定
$Smode_name="mente";

&check; #入力内容のチェック

&lock; #ロック

#@Spre_log取得&２重URL登録チェック
if($EST_reg{nijyu_url}){&get_id_url_ch(2);}
else{
	open(IN,"$EST{log_path}$EST{logfile}");
		while(<IN>){
			@Spre_log=split(/<>/,$_);
			if($Spre_log[0] eq $FORM{id}){last;}
		}
	close(IN);
}

#登録者のパスワード認証
if($FORM{changer} ne "admin"){
local($cr_pass);
	if($EST{crypt}){$cr_pass=crypt($FORM{pass},$Spre_log[5]);}
	else{$cr_pass=$FORM{pass};}
	if($Spre_log[5] ne $cr_pass){&unlock(); &mes("パスワードが間違っています$cr_pass $Spre_log[5]","パスワード認証エラー","java");}
}

&join_fld($Spre_log[0]); #入力内容の整形
$new=join("<>",@Slog);
$new=~s/\n//g; $new .="<>\n";


#本体ログデータに書き込み
open(IN,"$EST{log_path}$EST{logfile}");
	while($line=<IN>){
		@Tlog=split(/<>/,$line);
		if($Tlog[0] ne $Spre_log[0]){push(@log_lines,$line);}
		else{push(@log_lines,$new);}
	}
close(IN);

open(OUT,">$EST{log_path}$EST{logfile}");
	print OUT @log_lines;
close(OUT);

##メールを送信
$Slog[6]=~s/<br>/\n/g; $Slog[7]=~s/<br>/\n/g;
if($EST{mail_new}){require "pl/mail_ys.cgi";}
if($EST{mail_to_admin} && $EST{mail_ch}){ #管理人へメール送信
	&mail($EST{admin_email},$Slog[9],"$EST{search_name} 登録内容変更完了通知","mente","admin",*Slog);
}
if($EST{mail_to_register} && $EST{mail_ch}){ #登録者へメール送信
	&mail($Slog[9],$EST{admin_email},"$EST{search_name} 登録内容変更完了通知","mente","",*Slog);
}
$Slog[6]=~s/\n/<br>/g; $Slog[7]=~s/\n/<br>/g;



##更新するカテゴリリストを作成
#%TASKを使用
#更新情報or新着情報
{local(@time);
@time=split(/_/,$Spre_log[11]);
if(!$time[1] && $times-$time[0]<$EST{new_time}*86400){$TASK{"new"}=1;}
else{$TASK{"renew"}=1;}
}

#マークカテゴリの更新
{local(@mark,$mark,$i=1);
if($FORM{'changer'} eq "admin"){
	foreach(1 .. 2){ #←マーク数を増やすときは修正
		if($FORM{"Fmark$_"}){$TASK{"m$_"}=1;}
	}
}
@mark=split(/_/,$Spre_log[3]);
	foreach $mark(@mark){
		if($mark){$TASK{"m$i"}=1;}
	$i++;
	}
}

if($EST{html}){ #カテゴリをHTMLファイルで表示する場合
local(@kt,$i,$tmp);
	foreach $i(1 .. $EST_reg{kt_max}){
		if($FORM{"Fkt$i"}){
			$TASK{$FORM{"Fkt$i"}}=1;
			push(@TASK_list,$FORM{"Fkt$i"});
			@kt=split(/_/,$FORM{"Fkt$i"});
			if($#kt>0){
				pop(@kt); $tmp=join("_",@kt);
				if(!$TASK{$tmp}){push(@TASK_list,$tmp);}
				$TASK{$tmp}=1;
			}
		}
	}
}
else{ #カテゴリをCGIで動的に表示する場合
local($kt,$i);
	foreach $i(1 .. $EST_reg{kt_max}){
		if($FORM{"Fkt$i"}){
			($kt)=split(/_/,$FORM{"Fkt$i"});
			$TASK{$kt}=1;
		}
	}
}


##派生ファイルの処理
if($EST{html} && $EST{task} ne "2"){ #即時処理(html && !cron)
&MK_html(*TASK_list);
&make_task;
}
else{&make_task;} #タスクファイルに書き込み

&unlock(); #ロック解除

#マークの表示設定
{local(@mark,$mark,$i=1); $PR_mark="";
@mark=split(/_/,$Slog[3]);
	foreach $mark(@mark){
		if($mark){$PR_mark .= $EST{"name_m$i"} . " ";}
	$i++;
	}
}
#カテゴリの変更表示設定
if($EST{user_change_kt}){$PR_kt="※登録者によるカテゴリ変更は現在禁止されています";}
else{$PR_kt="";}

##表示用変数を設定
@Slog=split(/<>/,$new);

##登録結果出力
print "Content-type: text/html\n\n";
require "$EST{temp_path}regist_mente_end.html";


}


sub act_del{
#(p3)削除実行(&act_del)
local($Cdel=0,%kousin_list);

require "$EST{log_path}task_ys.cgi";

if($FORM{del_mode} eq "single"){ #del_mode:single
	if($FORM{del_check} ne "on"){&mes("削除確認のためにチェックを入れてから削除ボタンを押してください","確認チェックをしてください","java");}
	if($FORM{changer} ne "admin" && $EST_reg{no_mente}){&mes("現在、登録者による修正・削除は停止されています","エラー","java");}
	if($FORM{changer} eq "admin"){&pass_check;}
	&lock;
	local(@log_lines,@Slog,$line,$fl=0);
	open(IN,"$EST{log_path}$EST{logfile}");
		while($line=<IN>){
			@Slog=split(/<>/,$line);
			if($FORM{id} eq $Slog[0]){
				if($FORM{changer} ne "admin"){ #削除する人が登録者の場合
					local($cr_pass);
					if($EST{crypt}){$cr_pass=crypt($FORM{pass},$Slog[5]);}
					else{$cr_pass=$FORM{pass};}
					if($cr_pass ne $Slog[5]){&unlock; &mes("パスワードの認証に失敗しました","エラー","java");}
				}
				local(@kt,$kt,@mark,$mark,$i=1,@time);
				@kt=split(/&/,$Slog[10]);
				foreach $kt(@kt){ #カテゴリ
					$kousin_list{$kt}=1;
				}
				@mark=split(/_/,$Slog[3]);
				foreach $mark(@mark){ #マーク
					if($mark){$TASK{"m$i"}=1;}
					$i++;
				}
				@time=split(/_/,$Slog[11]);
				if(time - $time[0]<86400*$EST{new_time}){ #新着・更新
					if($time[1]){$TASK{renew}=1;}
					else{$TASK{new}=1;}
				}
				$Cdel++;
				$fl=1;
			}
			else{push(@log_lines,$line);}
		}
	close(IN);
		if(!$fl){&unlock; &mes("該当するデータは見つかりません","エラー","java");}
	open(OUT,">$EST{log_path}$EST{logfile}");
		print OUT @log_lines;
	close(OUT);
	@log_lines=();
}
else{ #del_mode:multi
	if($FORM{changer} ne "admin"){&mes("変更者指定が不正です","エラー","java");}
	&pass_check;
	&lock();
		#リンク切れリストからの削除の場合
		if($FORM{no_link} eq "on"){
			local(@data,@lines);
			open(IN,"$EST{log_path}no_link.cgi");
				while(<IN>){
					@data=split(/<>/,$_); #id<>count<>ip<>url<>\n
					if(!$FORM{"id_$data[0]"}){push(@lines,$_);}
				}
			close(IN);
			open(OUT,">$EST{log_path}no_link.cgi");
				print OUT @lines;
			close(OUT);
		}
		#デッドリンクチェック済みリストからの削除の場合
		if($FORM{dl_check} eq "on"){
			unless(-T $FORM{checkfile}){&unlock(); &mes("ファイル指定が異常です","エラー","java");}
			local(@data,@lines);
			open(IN,"./$FORM{checkfile}");
				while(<IN>){
					@data=split(/\t/,$_); #id=0<><><>url=13<>\n
					if(!$FORM{"id_$data[0]"}){push(@lines,$_);}
				}
			close(IN);
			open(OUT,">./$FORM{checkfile}");
				print OUT @lines;
			close(OUT);
		}
	
	local(@log_lines,@Slog,$line);
	open(IN,"$EST{log_path}$EST{logfile}");
		while($line=<IN>){
			@Slog=split(/<>/,$line);
			if($FORM{"id_$Slog[0]"} eq "on"){ #削除リストに入っている場合
				local(@kt,$kt,@mark,$mark,$i=1,@time);
				@kt=split(/&/,$Slog[10]);
				foreach $kt(@kt){ #カテゴリ
					$kousin_list{$kt}=1;
				}
				@mark=split(/_/,$Slog[3]);
				foreach $mark(@mark){ #マーク
					if($mark){$TASK{"m$i"}=1;}
					$i++;
				}
				@time=split(/_/,$Slog[11]);
				if(time - $time[0]<86400*$EST{new_time}){ #新着・更新
					if($time[1]){$TASK{renew}=1;}
					else{$TASK{new}=1;}
				}
				$Cdel++;
			}
			else{push(@log_lines,$line);}
		}
	close(IN);
	open(OUT,">$EST{log_path}$EST{logfile}");
		print OUT @log_lines;
	close(OUT);
	@log_files=();
}

##%kousin_listの内容をCGI/HTMLに応じて%TASK/@TASK_listに入れる

##派生ファイルの処理
if($EST{html} && $EST{task} ne "2"){ #即時処理(html && !cron)
		foreach(keys %kousin_list){
			$TASK{$_}=1;
			push(@TASK_list,$_);
		}
&MK_html(*TASK_list);
}
else{ #それ以外の場合
	if($EST{html}){ #html
		foreach(keys %kousin_list){
			$TASK{$_}=1;
		}
	}
	else{ #CGI
		local(@kt,$kt);
		foreach(keys %kousin_list){
			@kt=split(/_/,$_);
			$TASK{$kt[0]}=1;
		}
	}
}
&make_task;

##総登録数を記録
open(IN,"$EST{log_path}total_url.log");
	$Cgane_pre=<IN> - $Cdel;
close(IN);
open(OUT,">$EST{log_path}total_url.log");
	print OUT $Cgane_pre;
close(OUT);

&unlock();

if($FORM{changer} eq "admin" && ($FORM{no_link} eq "on" || $FORM{dl_check} eq "on")){&mes("削除処理が完了しました","削除完了","kanri");}
else{&mes("削除処理が完了しました","削除完了",$EST{home});}


}




####個別処理####
##目次##



#フォームデータのデコード(&form_decode)
sub form_decode{
   if ($ENV{'REQUEST_METHOD'} eq "POST") { read(STDIN,$form,$ENV{'CONTENT_LENGTH'}); }
   else { $form=$ENV{'QUERY_STRING'}; }
   @pairs=split(/&/,$form);
		foreach $pair (@pairs) {
			($name,$value) = split(/=/,$pair);
			$value =~ tr/+/ /;
      $value =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
      $name =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
			$value =~ s/>/&gt;/g;
			$value =~ s/</&lt;/g;
			$value =~ s/\r//g;
			&jcode'convert(*value,'sjis');
			&jcode'convert(*name,'sjis');
			$FORM{$name} = $value;
		}
}




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

print "Content-type: text/html\n\n";
$Munlock=$_[3];
	if($Munlock eq "unlock"){&unlock();}
$MES=$_[0];
		if($_[1]){$TITLE=$_[1];}
		else{$TITLE="メッセージ画面";}
	if($_[2] eq "java" || ($_[2] eq "back_reg" && $FORM{mode} eq "act_mente")){
	$BACK_URL="<form><input type=button value=\"&nbsp;&nbsp;&nbsp;&nbsp;戻る&nbsp;&nbsp;&nbsp;&nbsp;\" onClick=\"history.back()\"></form>"
	}
	elsif($_[2] eq "env"){
	$BACK_URL="【<a href=\"$ENV{'HTTP_REFERER'}\">戻る</a>】";
	}
	elsif($_[2] eq "kanri"){
	$BACK_URL="<form action=\"$EST{admin}\" method=post><input type=hidden name=mode value=kanri><input type=hidden name=pass value=\"$FORM{'pass'}\"><input type=submit value=\"管理室へ\"></form>"
	}
	elsif(!$_[2]){$BACK_URL="";}
	elsif($_[2] eq "back_reg"){
$FORM{Fsyoukai}=~s/<br>/\n/g;
	if($FORM{changer} eq "admin"){$FORM{in_mode}="new_dairi";}
	else{$FORM{in_mode}="form";}
$BACK_URL=<<"EOM";
<form action="regist_ys.cgi" method=post>
	<input type=hidden name="in_mode" value="form">
	<input type=hidden name="pass" value="$FORM{pass}">
	<input type=hidden name="changer" value="$FORM{changer}">

	<input type=hidden name="Fname" value="$FORM{Fname}">
	<input type=hidden name="Femail" value="$FORM{Femail}">
	<input type=hidden name="Fpass" value="$FORM{Fpass}">
	<input type=hidden name="Fpass2" value="$FORM{Fpass2}">
	<input type=hidden name="Furl" value="$FORM{Furl}">
	<input type=hidden name="Fbana_url" value="$FORM{Fbana_url}">
	<input type=hidden name="Ftitle" value="$FORM{Ftitle}">
	<input type=hidden name="Fsyoukai" value="$FORM{Fsyoukai}">
	<input type=hidden name="Fkanricom" value="$FORM{Fkanricom}">
	
EOM
foreach(1 .. $EST_reg{kt_max}){
	$BACK_URL .="<input type=hidden name=\"Fkt$_\" value=\"$FORM{\"Fkt$_\"}\">\n";
}
$BACK_URL .=<<"EOM";
	<input type=hidden name="Fkey" value="$FORM{Fkey}">
	<input type=hidden name="Fadd_kt" value="$FORM{Fadd_kt}">
	<input type=hidden name="Fto_admin" value="$FORM{Fto_admin}">
	<input type=hidden name=Fsougo value="$FORM{Fsougo}">
	
	<input type=submit value="登録画面に戻る">
EOM
	}
	else{$BACK_URL="【<a href=\"$_[2]\">戻る</a>】";}

require "$EST{temp_path}mes.html";

exit;
}



##-- end of regist_ys.cgi --##
