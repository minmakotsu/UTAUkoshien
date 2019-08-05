#!/usr/bin/perl

#↑perlのパスを自分の環境に合わせて書き直します。
#大抵は、「#!/usr/bin/perl」　か　「#!/usr/local/bin/perl」です。
#解らない場合はサーバー管理者(もしくはプロバイダー)に
#確認してください。

require 'pl/jcode.pl';
require 'pl/cfg.cgi';
require 'pl/temp.cgi';

##目次##
#(1)検索結果表示画面(&search)
#(2)詳細検索画面(&search_ex)
#(3)外部リンク画面(&meta)
#(4)検索処理用データをハッシュに入れる(&open_for_search)
#(5)外部検索エンジンへのリンク一覧を表示(&PR_mata_page)
#(6)キーワードを一時ランキングファイル(keyrank_temp.cgi)に記録(&set_word)

##テンプレートファイル
#検索結果画面=>temp/search.html
#詳細検索画面=>temp/search_ex.html
#外部リンク画面=>temp/search_meta.html

#【カテゴリ検索】
##[オプション]
#カテゴリ指定([kt]&[option(b_all=以下)])
#日付指定=>( today-x | year/mon/day | [str_day]-[end_day] )
#新規ウィンドウ=>window=new

&form_decode();
	if(!$FORM{page}){$FORM{page}=1;}
if($FORM{mode} eq "search"){&search;} #検索結果表示画面
elsif($FORM{mode} eq "meta"){&meta;} #外部リンク画面
else{&search_ex;} #詳細検索画面
exit;

sub search{
#(1)検索結果表示画面(&search)
local(@words_a,@words_o,@words_n,$w_line,@words,$word,@kt_search_list);

	#検索オプションをクッキーに記録
		#オプション
		#[0]=>検索条件(a|o)/[1]=>検索式の使用有無(0|1)/[2]=>検索エンジン名(ID)/
		#[3]=>検索エンジン名(表示名)/[4]=>www.(0|1)/[5]=>カテゴリ指定(ID)
		#[6]=>カテゴリ指定(表示名)/[7]=>指定カテゴリ(0|1)/[8]=>日付指定(data)
		#[9]=>日付指定(表示名)/[10]=>日付指定コマンド(data)/[11]=>カテゴリ名検索(0|1)
	if($FORM{set_option} eq "on"){
		&get_cookie;
		local(@cookie_lines);
		if($FORM{method} eq "and"){$cookie_lines[0]="a";} #[0]
		else{$cookie_lines[0]="o";}
		if($FORM{use_str} eq "on"){$cookie_lines[1]="1";} #[1]
		else{$cookie_lines[1]="0";}
		$cookie_lines[2]=$FORM{engine}; #[2]
		if($FORM{engine} eq "pre"){$cookie_lines[3]="$EST{search_name}で";} #[3]
		else{
		open(IN,"pl/cfg.cgi");
			local($i=0);
			while(<IN>){
				if($_ eq "sub search_form{\n"){$i=1;}
				if($i){
					if(/<option value="$FORM{engine}">(.+)で/o){$cookie_lines[3]=$1; last;}
				}
			}
		close(IN);
		}
		$cookie_lines[3]=~s/,/，/g;
		if($FORM{www} eq "on"){$cookie_lines[4]="0";} #[4]
		else{$cookie_lines[4]="1";}
		$cookie_lines[5]=$FORM{search_kt}; #[5]
		if($FORM{search_kt}){$cookie_lines[6]=&full_kt($FORM{search_kt});} #[6]
		else{$cookie_lines[6]="指定しない";}
		if($FORM{search_kt_ex} ne "-b_all"){$cookie_lines[7]=0;} #[7]
		else{$cookie_lines[7]=1;}
		$cookie_lines[8]=$FORM{search_day}; #[8]
		if($FORM{search_day} eq "today"){$cookie_lines[9]="本日";} #[9]
		elsif($FORM{search_day}=~/^(\d+)-/){$cookie_lines[9]= $1 . "日以内";}
		else{$cookie_lines[9]="指定しない";}
		$cookie_lines[10]=$FORM{search_day_ex}; #[10]
		$cookie_lines[10]=~s/,/，/g;
		if($FORM{kt_search} eq "on"){$cookie_lines[11]=0;} #[11]
		else{$cookie_lines[11]=1;}
		
		$CK_data[5]=join(",",@cookie_lines);
		$CK_data[5]=~s/;//g;
		&set_cookie;
	}

	#入力値の整形
	if(!$FORM{engine}){$FORM{engine}="pre";}
	if($FORM{page}=~/\D/){&mes("ページ指定値が不正です","ページ指定エラー","java");}
	if(!$FORM{sort}){$FORM{sort}=$EST{defo_hyouji};}
	if($FORM{search_kt_ex}){$FORM{search_kt}=$FORM{search_kt} . $FORM{search_kt_ex};}
	if($FORM{search_day_ex}){$FORM{search_day}=$FORM{search_day_ex};}
	if($FORM{kn}>0 && $FORM{kn}<=20){ #キーワードの結合
		if($FORM{kn}=~/\D/){&mes("\$FORM{kn}が不正です","エラー","java");}
		foreach(1 .. $FORM{kn}){
			if($FORM{"word$_"}){$FORM{word} .= $FORM{"word$_"} . " ";}
		}
	}
	if(!$FORM{hyouji}){$FORM{hyouji}=$EST{hyouji};}
	
	if($EST{keyrank} && $FORM{page}==1){ #キーワードランキング用のデータを取得
		&set_word;
	}
	


	#検索構文の解析
	$w_line=$FORM{word};
	$w_line=~ s/　/ /g;
	$FORM{word}=$w_line;
	$w_line=~tr/[A-Z]/[a-z]/;
	if($FORM{use_str} eq "on"){ #検索式を使う
		@words=split(/ /,$w_line);
		local($w_fl="and");
		foreach $word(@words){
			if($word eq "and"){$w_fl="and";}
			elsif($word eq "or"){$w_fl="or";}
			elsif($word eq "not"){$w_fl="not";}
			elsif($w_fl eq "and"){push(@words_a,$word); $w_fl="and";}
			elsif($w_fl eq "or"){push(@words_o,$word); $w_fl="and";}
			elsif($w_fl eq "not"){push(@words_n,$word); $w_fl="and";}
			else{push(@words_a,$word);}
		}
	}
	else{ #検索式を使わない
		if($FORM{method} ne "or"){ @words_a=split(/ /,$w_line);}
		else{@words_o=split(/ /,$w_line);}
	}

	#外部検索へ分岐
		if($FORM{engine} ne "pre"){
			$FORM{target}=$FORM{window};
			require "pl/meta_ys.cgi";
			&meta("select");
		}
		
	if(!$FORM{word} && !$FORM{search_day}){ #キーワード・日付指定の両方が未指定のとき
		&mes("<b>キーワード</b>か<b>日付指定</b>のいずれかは必ず指定してください","記入ミス","java");
	}
	if(!$FORM{word}){$FORM{kt_search}="off";}

 	##検索処理
	#カテゴリ検索
	if($FORM{kt_search} ne "off"){
		local($kt,$kt_name,$kt_fl);
		
		foreach $kt(sort keys %ganes){
			$kt_fl=1;
			$kt_name=$ganes{$kt};
			$kt_name=~tr/[A-Z]/[a-z]/;
			
			foreach $word(@words_a){ #and検索
				if(index($kt_name,$word)<0){$kt_fl=0; last;}
			}
			
			foreach $word(@words_o){ #or検索
				$kt_fl=0;
				if(index($kt_name,$word)>=0){$kt_fl=1; last;}
			}
			
			foreach $word(@words_n){ #not検索
				if(index($kt_name,$word)>=0){$kt_fl=0; last;}
			}
			
			if($kt_fl){push(@kt_search_list,$kt);}
		}
	}
	

	#結果表示
	require "$EST{temp_path}search.html";

	print "Content-type: text/html\n\n";
	&print_search($FORM{word},$FORM{engine},$FORM{mode},$FORM{page},$FORM{sort},$FORM{search_kt},$FORM{search_day},$FORM{use_str},$FORM{method});

}

sub search_ex{
#(2)詳細検索画面(&search_ex)

print "Content-type: text/html\n\n";
require "$EST{temp_path}search_ex.html";

}

sub meta{
#(3)外部リンク画面(&meta)
	if($EST{keyrank} && $FORM{page}==1){ #キーワードランキング用のデータを取得
		&set_word;
	}
require "pl/meta_ys.cgi";
print "Content-type: text/html\n\n";
require "$EST{temp_path}search_meta.html";

}

sub open_for_search{
#(4)検索処理用データをハッシュに入れる(&open_for_search)
#対象全配列を@writeに入れる
#$arg1=>カテゴリ指定([kt]-[option(b_all=以下)])
#$arg2=>日付指定=>( today-x | year/mon/day | [str_day]-[end_day]_[option(re)] )
#$arg3=>ソート方法(id/time/ac/mark)
local($target_kt=$_[0],$target_day=$_[1],$sort=$_[2],
$eval_line,$oya_kt,$target_kt1,$target_kt2,
$line,$s_line,@Slog,@kt,$kt,$fl,$word,$i=0);
($sort)=split(/_/,$sort);


	##検索用$eval_lineを作成
		#while開始
$eval_line .=<<'EOM';
		while($line=<IN>){
			$fl=1;
			$s_line=$line;
			$s_line=~tr/[A-Z]/[a-z]/;
			@Slog=split(/<>/,$line);
EOM

	#カテゴリ指定部分
	if($target_kt){
		($target_kt1,$target_kt2)=split(/-/,$target_kt);
		($oya_kt)=split(/_/,$target_kt1);
		if(!$ganes{$oya_kt}){&mes("カテゴリ指定が不正です","カテゴリ指定エラー","java");}
		
$eval_line .=<<'EOM';
	@kt=split(/&/,$Slog[10]);
	$fl=0;
	foreach $kt(@kt){
EOM
	if($target_kt2){$eval_line .='if($kt=~/^$target_kt1/){$fl=1; last;}';}
	else{$eval_line .='if($kt eq $target_kt1){$fl=1; last;}';}
$eval_line .=<<'EOM';
	}
EOM
	}
	#ワード検索部分
	if($#words_a>=0){ #and検索
$eval_line .=<<'EOM';
	if($fl){
	foreach $word(@words_a){
		if(index($s_line,$word) < 0){$fl=0; last;}
	}
	}
EOM
	}
	if($#words_o>=0){ #or検索
$eval_line .=<<'EOM';
	if($fl){
	$fl=0;
	foreach $word(@words_o){
		if(index($s_line,$word) >= 0){$fl=1; last;}
	}
	}
EOM
	}
	if($#words_n>=0){ #not検索
$eval_line .=<<'EOM';
	if($fl){
	foreach $word(@words_n){
		if(index($s_line,$word) >= 0){$fl=0; last;}
	}
	}
EOM
	}
	#日付検索部分
	if($target_day){
		if($target_day=~/^today-?(\d*)$/){ #today-x
			if($1>100000){$1=0;}
			local($bf_times=time()-86400*$1,$bf_day,$sec,$min,$hour,$mday,$mon,$year);
			$ENV{'TZ'} = "JST-9";
			($sec,$min,$hour,$mday,$mon,$year) = localtime($bf_times);
			$year+=1900;$mon++;
			$bf_day=sprintf("%04d\\/%02d\\/%02d",$year,$mon,$mday);
			$eval_line .='if($fl){ if($Slog[4]!~/^' . $bf_day . '/){$fl=0;}}';
		}
		elsif($target_day=~/^(\d+)\-(\d+)$/){ #[str_day]-[end_day]
		
			local($str_times=time()-86400*$1,$end_times=time()-86400*$2);
			$eval_line .='if($fl){if(' . $str_times . '>$Slog[11] || $Slog[11]>' . $end_times . '){$fl=0;}}';
		}
		elsif($target_day=~/^(\d+)\/(\d+)\/(\d+)$/){ #year/mon/day
			$eval_line .='if($fl){ if($Slog[4]!~/^' . $1 . '\/' . $2 . '\/' . $3 . '/){$fl=0;}}';
		}
		else{&mes("日付指定のコマンドが正しくありません","エラー","java");}
	}
	#データ格納部分
	$eval_line .='if($fl){$line{$i}='; 
		if($sort eq "id"){$eval_line .='$Slog[0]';}
		elsif($sort eq "time"){$eval_line .='(split(/_/,$Slog[11]))[0]';}
		elsif($sort eq "ac"){$eval_line .='$Slog[1]';}
		else{$eval_line .='$Slog[3]';} #mark
	$eval_line .='; push(@write,$line); $i++;}';

$eval_line .='}';

	##検索処理実行
	if(!$EST{html} && $target_kt){open(IN,"$EST{log_path}$oya_kt.cgi") || &mes("ファイルが開けませんでした","ファイルが開けません","java");}
	else{open(IN,"$EST{log_path}$EST{logfile}");}
	

			eval $eval_line;
		

	close(IN);
#&mes("$eval_line");
	if($#write<0){$i=0;}

	return $i;
}

sub PR_meta_page{
#(5)外部検索エンジンへのリンク一覧を表示(&PR_mata_page)
local($T_flag=1,$Durl,$Dengine,*location_list=$_[0]);
print "<table width=\"90%\" cellpadding=8>";
	foreach $list(@location_list){
	($Dengine,$Durl)=split(/<>/,$list);
if($T_flag==5){print "</tr>"; $T_flag=1;}
if($T_flag==1){print "<tr>";}
print<<"EOM";
<th><a href="$Durl" target="$FORM{'target'}"><font size="+1">$Dengine</font></a></th>
EOM
$T_flag++;
	}
if($T_flag!=2){print "</tr>";}
print "</table>";
}

sub set_word{
#(6)キーワードを一時ランキングファイル(keyrank_temp.cgi)に記録(&set_word)
	local(@keyword,$keyword=$FORM{word});
	$keyword=~s/'/’/g;
	if(length($keyword)<50){
	$keyword=~s/　/ /g;
	@keyword=split(/ /,$keyword);
	if($#keyword>=0){
local($i);
	&lock_key;
	open(OUT,">>$EST{log_path}keyrank_temp_ys.cgi");
		foreach $i(@keyword){
			if($i ne "and" && $i ne "or" && $i ne "not"){
				if($i!~/\W/){$i=~tr/A-Z/a-z/;}
			$i=~s/\n//g;
			print OUT "$i<>$ENV{REMOTE_ADDR}<>\n";
			}
		}
	close(OUT);
	&unlock_key;
	}
	}
}

#(t1)メッセージ画面出力(&mes)
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
           &jcode'convert(*value,'sjis');
           &jcode'convert(*name,'sjis'); $FORM{$name} = $value;
   }
}






