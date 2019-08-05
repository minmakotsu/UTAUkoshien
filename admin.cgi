#!/usr/bin/perl

#↑perlのパスを自分の環境に合わせて書き直します。
#大抵は、「#!/usr/bin/perl」　か　「#!/usr/local/bin/perl」です。
#解らない場合はサーバー管理者(もしくはプロバイダー)に
#確認してください。

require 'pl/jcode.pl';
require 'pl/cfg.cgi';
require 'pl/temp.cgi';

## 目次 ##
#(1)ログイン画面(&login)
#(2)管理人室(&kanri)
#(3)HTMLログファイル更新処理(&mente_html)
#(3.1)HTMLログファイル更新処理実行(&mente_html_act)
#(4)CGIログファイル更新処理(&mente_cgi)
#(4.1)CGIログファイル更新処理実行(&mente_cgi_act)
#(5)登録待ち表示画面(&temp_to_regist)
#(5.1)登録待ちの処理決定実行(&temp_to_regist_act)
#(6)キーワードランキングの設定(&key_cfg)
#(6.1)キーワードランキングの設定実行(&key_cfg_act)
#(6.2)キーワードランキングの集計対象外のキーワードを一括登録実行(&key_cfg_del_word_act)
#(7)各種ログ変換(&log_conv)
#(7.1)各種ログ変換実行(&log_conv_act)
#(7.2)Ver3からカテゴリ設定インポート実行(&log_conv_kt_act)
#(7.3)カテゴリ・ソート変換実行(&log_conv_kt_sort)
#(8)ログデータの交換・移動・削除(&log_kt_change)
#(8.1)ログデータの交換・移動・削除実行(&log_kt_change_act)
#(9)ログ(登録データ)の修復(&log_repair)
#(9.1)ログ(登録データ)の修復実行(&log_repair_act)
#(10)ログ診断 (&log_mente)
#(10.1)ログ診断実行 (&log_mente_act)
#(11)環境設定 (&config)
#(12)カテゴリ設定 (&config_kt)
#(13)人気ランキングの設定(&rank_cfg)
#(13.1)人気ランキングの初期化実行(&rank_cfg_act)
#(14)デッドリンクチェック画面(&dl_check)
#(14.1)デッドリンクチェック用ファイルをダウンロード(&dl_check_dl)
#(14.2)デッドリンクチェック実行画面(&dl_check_act)
#(15)異常ロック解除ファイル操作(&ill_lock_del)
#(16)簡易デザイン設定(&design)
#(17)テンプレートファイルの修正(&template_cfg)
#(18)バージョン情報(&ver_info)
#(19)登録者のメッセージを見る(&look_mes)


#(cfg1)環境設定(%EST)を更新(&cfg_make)
#(cfg2)環境設定(&search_form/&menu_bar)を更新(&cfg_make_PR_menu)
#(cfg3)環境設定(登録処理関係)を更新 (&cfg_make_reg)
#(cfg4)カテゴリ説明文を更新 (&cfg_make_kt_ex)
#(cfg5)カテゴリ設定を更新 (&cfg_make_kt)
#(cron1)cronコマンドによる定期処理(&cron)
#(cron1.1)通常カテゴリと特殊カテゴリを更新(&cron_make_kt)

## 個別処理 ##
#(t1)フォーム入力データを書き込みデータに反映(仮登録→正規登録用)
#   (&form_to_temp)
#(t2)symlink関数の使用可否のチェック(&check_symlink)

&form_decode;
if($FORM{mode} eq "kanri"){&kanri;}
elsif($FORM{mode} eq "mente_html"){&mente_html;}
elsif($FORM{mode} eq "mente_html_act"){&mente_html_act;}
elsif($FORM{mode} eq "mente_cgi"){&mente_cgi;}
elsif($FORM{mode} eq "mente_cgi_act"){&mente_cgi_act;}
elsif($FORM{mode} eq "temp_to_regist"){&temp_to_regist;}
elsif($FORM{mode} eq "temp_to_regist_act"){&temp_to_regist_act;}
elsif($FORM{mode} eq "key_cfg"){&key_cfg;}
elsif($FORM{mode} eq "key_cfg_act"){&key_cfg_act;}
elsif($FORM{mode} eq "key_cfg_del_word_act"){&key_cfg_del_word_act;}
elsif($FORM{mode} eq "log_conv"){&log_conv;}
elsif($FORM{mode} eq "log_conv_act"){&log_conv_act;}
elsif($FORM{mode} eq "log_conv_kt_act"){&log_conv_kt_act;}
elsif($FORM{mode} eq "log_conv_kt_sort"){&log_conv_kt_sort;}
elsif($FORM{mode} eq "log_kt_change"){&log_kt_change;}
elsif($FORM{mode} eq "log_kt_change_act"){&log_kt_change_act;}
elsif($FORM{mode} eq "log_repair"){&log_repair;}
elsif($FORM{mode} eq "log_repair_act"){&log_repair_act;}
elsif($FORM{mode} eq "log_mente"){&log_mente;}
elsif($FORM{mode} eq "log_mente_act"){&log_mente_act;}
elsif($FORM{mode} eq "config"){&config;}
elsif($FORM{mode} eq "config_kt"){&config_kt;}
elsif($FORM{mode} eq "rank_cfg"){&rank_cfg;}
elsif($FORM{mode} eq "rank_cfg_act"){&rank_cfg_act;}
elsif($FORM{mode} eq "dl_check"){&dl_check;}
elsif($FORM{mode} eq "dl_check_dl"){&dl_check_dl;}
elsif($FORM{mode} eq "dl_check_act"){&dl_check_act;}
elsif($FORM{mode} eq "ill_lock_del"){&ill_lock_del;}
elsif($FORM{mode} eq "design"){&design;}
elsif($FORM{mode} eq "template_cfg"){&template_cfg;}
elsif($FORM{mode} eq "ver_info"){&ver_info;}
elsif($FORM{mode} eq "look_mes"){&look_mes;}


elsif($FORM{mode} eq "cfg_make"){&cfg_make;}
elsif($FORM{mode} eq "cfg_make_PR_menu"){&cfg_make_PR_menu;}
elsif($FORM{mode} eq "cfg_make_reg"){&cfg_make_reg;}
elsif($FORM{mode} eq "cfg_make_kt_ex"){&cfg_make_kt_ex;}
elsif($FORM{mode} eq "cfg_make_kt"){&cfg_make_kt;}
elsif($FORM{mode} eq "cron"){&cron;}
else{&login;}
exit;


sub login{
#(1)ログイン画面(&login)
print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/login.html";
}

sub kanri{
#(2)管理人室(&kanri)

#パスワードチェック
if($EST{pass} ne "setup"){
&pass_check;
}

#クッキーの設定
&get_cookie;
if($FORM{set}){
	if($FORM{set} eq "設定"){$CK_data[4]=1;}
	else{$CK_data[4]=0;}
	&set_cookie;
}
if($CK_data[4]){$PRset="設定";}
else{$PRset="解除";}

print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/admin.html";
}


sub mente_html{
#(3)HTMLログファイル更新処理(&mente_html)
&pass_check;

print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/mente_html.html";

}

sub mente_html_act{
#(3.1)HTMLログファイル更新処理実行(&mente_html_act)
&pass_check;
local(@TASK_list,%fl,%fl_kt,$kt,$k1,$k2);

##@TASK_flを設定
#all_fl
if($FORM{all_fl} eq "all"){ #すべてのカテゴリ
@TASK_list=sort keys %ganes;
}
else{ #その他
	foreach $kt(sort keys %ganes){
		($k1,$k2)=split(/_/,$kt);
		if($FORM{"kt_fl$kt"}){ #以下のカテゴリ
			$fl_kt{$k1}=1;
		}
		if($fl_kt{$k1} && !$fl{$kt}){push(@TASK_list,$kt); $fl{$kt}=1;}
		elsif($FORM{$kt} && !$fl{$kt}){push(@TASK_list,$kt); $fl{$kt}=1;}
	}
}

&lock();
&MK_html(*TASK_list);
require "$EST{log_path}task_ys.cgi";
if($FORM{new}){$TASK{new}=1;} #新着
if($FORM{renew}){$TASK{renew}=1;} #更新
foreach(1 .. 2){ #マーク数を増やす時は更新
	if($FORM{"m$_"}){$TASK{"m$_"}=1;}
}
&make_task; #タスクファイルを更新
&unlock();
if($FORM{continue}>0){
	$mes=<<"EOM";
カテゴリ用HTMLファイルの更新を続けますか？<br>
[更新状況]：<b>$FORM{continue_full}</b>カテゴリ中、<br>
　<b>$FORM{continue}</b>カテゴリが未作成です。
</ul>
	<div align=center><form action="$EST{admin}" method=post>
	<input type=hidden name=pass value="$FORM{pass}">
	<input type=hidden name=mode value="$FORM{mode}">
	<input type=hidden name=mode value="mente_html_act">
	<input type=hidden name=all_fl value="all">
	<input type=hidden name=continue value="on">
	<input type=submit value="続ける">
	</form></div>
<div style="margin:15px">
※「続ける」ボタンは2回以上連続で押さないでください。<br>
※途中で中断した後でも「HTMLログファイル更新処理」<br>　
から再び作成を続けることができます。
</div>
<hr>

EOM
	&mes($mes,"カテゴリHTMLファイル作成","kanri");
}
else{
	&mes("カテゴリ用HTMLファイルの更新が完了しました","更新完了","kanri");
}
}

sub mente_cgi{
#(4)CGIログファイル更新処理(&mente_cgi)
&pass_check;

print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/mente_cgi.html";


}

sub mente_cgi_act{
#(4.1)CGIログファイル更新処理実行(&mente_cgi_act)
&pass_check;
local(@kt,$kt,$k1,$k2);

#all_fl
if($FORM{all_fl} eq "all"){ #すべてのカテゴリ
	foreach $kt(sort keys %ganes){
		($k1,$k2)=split(/_/,$kt);
		if(!$k2){push(@TASK_list,$kt);}
	}
}
else{ #その他
	foreach $kt(sort keys %ganes){
		($k1,$k2)=split(/_/,$kt);
		if(!$k2 && $FORM{$kt}){push(@TASK_list,$kt);}
	}
}

&lock();
&MK_cgi(*TASK_list);
require "$EST{log_path}task_ys.cgi";
if($FORM{new}){$TASK{new}=1;} #新着
if($FORM{renew}){$TASK{renew}=1;} #更新
foreach(1 .. 2){ #マーク数を増やす時は更新
	if($FORM{"m$_"}){$TASK{"m$_"}=1;}
}
&make_task; #タスクファイルを更新
&unlock();
&mes("カテゴリ用CGIファイルの更新が完了しました","更新完了","kanri");


}

sub temp_to_regist{
#(5)登録待ち表示画面(&temp_to_regist)
&pass_check;
local($Ctemp=0);
&EST_reg; #登録関連の設定をロード
open(IN,"$EST{log_path}$EST{temp_logfile}");
	while(<IN>){
	$Ctemp++;
	}
close(IN);

print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/temp_to_regist.html";

}

sub temp_to_regist_act{
#(5.1)登録待ちの処理決定実行(&temp_to_regist_act)
&pass_check;
require "$EST{log_path}task_ys.cgi";
&EST_reg; #登録用の設定をロード
local(
@TASK_list, #更新するカテゴリリスト
@log_lines, #正規ログへの書き込み用ログリスト
@temp_lines, #仮登録ログへの書き込み用ログリスト
@Slog, #登録データの一時保存用
$Clog_id=1, #新規登録用の登録ID
$temp_id, #仮登録時のID
$line,$new,@kt,$kt,@mark,$i,
);

&lock(); #ロック

	#新規登録用のIDを取得
	open(IN,"$EST{log_path}$EST{logfile}");
		while(<IN>){$line=$_;}
	close(IN);
	if($line){($Clog_id)=split(/<>/,$line); $Clog_id++;}


#メール送信用ライブラリを読み込み
if($EST{mail_new}){require "pl/mail_ys.cgi";}


open(IN,"$EST{log_path}$EST{temp_logfile}");
	while(<IN>){
		@Tlog=split(/<>/,$_);
		if($FORM{"R$Tlog[0]"} eq "reg"){ #登録
			&form_to_temp;
			$new=join("<>",@Slog);
			$new=~s/\n//g; $new .="<>\n";
			push(@log_lines,$new);
			if($EST{mail_new}){
				&temp_to_regist_mail; #メールを送信
			}
			@kt=split(/&/,$Slog[10]);
			
			foreach $kt(@kt){ #カテゴリリストを更新
				if(!$EST{html}){
					($kt)=split(/_/,$kt);
					if(!$TASK{$kt}){push(@TASK_list,$kt);}
					$TASK{$kt}=1;
				}
				else{
					if(!$TASK{$kt}){push(@TASK_list,$kt);}
					$TASK{$kt}=1;
				}
			}
			@mark=split(/_/,$Slog[3]);
			$i=1;
			foreach(@mark){ #マークを更新
				if($_){$TASK{"m$i"}=1;}
				$i++;
			}
			$TASK{"new"}=1; #新着を更新
			
		}
		elsif(!$FORM{"R$Tlog[0]"}){ #保留
			push(@temp_lines,$_);
		}
	}
close(IN);


#本体ログデータに書き込み
open(OUT,">>$EST{log_path}$EST{logfile}");
	print OUT @log_lines;
close(OUT);

#仮登録データを更新
open(OUT,">$EST{log_path}$EST{temp_logfile}");
	print OUT @temp_lines;
close(OUT);


sub temp_to_regist_mail{
#仮登録→新規登録時のメールを送信
$Slog[6]=~s/<br>/\n/g; $Slog[7]=~s/<br>/\n/g;
if($EST{mail_to_admin} && $EST{mail_new}){ #管理人へメール送信
	&mail($EST{admin_email},$Slog[9],"$EST{search_name} 新規登録完了通知","new","admin",*Slog,$FORM{"Fsougo$Tlog[0]"},$FORM{"Fadd_kt$Tlog[0]"},$FORM{"Fto_admin$Tlog[0]"},$FORM{"Fto_reg$Tlog[0]"});
}
if($EST{mail_to_register} && $EST{mail_new}){ #登録者へメール送信
	&mail($Slog[9],$EST{admin_email},"$EST{search_name} 新規登録完了通知","new","",*Slog,$FORM{"Fsougo$Tlog[0]"},$FORM{"Fadd_kt$Tlog[0]"},$FORM{"Fto_admin$Tlog[0]"},$FORM{"Fto_reg$Tlog[0]"});
}
$Slog[6]=~s/\n/<br>/g; $Slog[7]=~s/\n/<br>/g;
}

##派生ファイルの処理
if($EST{html} && $EST{task} ne "2"){ #即時処理(html && !cron)
local($data_fl,$data_no); #フラグ/フィールドの添え字番号
	($data_fl)=split(/_/,$EST{defo_hyouji});
	if($data_fl eq "mark"){$data_no=3;}
	elsif($data_fl eq "id"){$data_no=0;}
	elsif($data_fl eq "time"){$data_no=11;}
	elsif($data_fl eq "ac"){$data_no=1;}
	else{$data_no=3;}

&MK_html(*TASK_list);
&make_task;
}
else{&make_task;} #タスクファイルに書き込み

&count_log;

&unlock(); #ロック解除

&mes("仮登録データの処理が完了しました","仮登録データ処理完了","kanri");

}


sub key_cfg{
#(6)キーワードランキングの設定(&key_cfg)
&pass_check;
if(-s "$EST{log_path}keyrank_temp_ys.cgi"){&keyrank_trace;} #一時ファイル→集計ファイル
else{require "$EST{log_path}keyrank_ys.cgi";}
print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/key_cfg.html";
}

sub key_cfg_act{
#(6.1)キーワードランキングの設定実行(&key_cfg_act)
&pass_check;
	 #管理人によるキーワードランキングの更新を実行
	if($FORM{make_keyrank} eq "on"){
		#$kousin_flが「1」のときはランキングを初期化(過去のランキングにデータを移行
		if($FORM{keyrank_format}){
		$kousin_fl=1;
		$BK_last_keyrank=time();
		&make_task; #タスクファイルを更新
		}
		else{$kousin_fl=0;}
		&key_cfg_make_rank($kousin_fl); #キーワードランキングを作成
		&mes("キーワードランキングの更新が完了しました","キーワードランキング更新完了","kanri");
	}
&lock_key();
local(@bad_key,@open_key);
require "$EST{log_path}keyrank_ys.cgi";

open(OUT,">$EST{log_path}keyrank_ys.cgi");

print OUT<<"EOM";
%keyrank=(
EOM
	foreach(keys %keyrank){
		if($FORM{"pt_$_"}){$keyrank{$_}=$FORM{"pt_$_"};}
		if($FORM{"bb_$_"}!=2){print OUT "\'$_\'=>\'$keyrank{$_}\',\n";}
		else{push(@bad_key,$_);} #bad
		if($FORM{"oo_$_"}==1 && $FORM{"del_oo_$_"} ne "on"){push(@open_key,$_);} #open
	}
	local($key);
	while(($key)=each %bad_key){
		if($FORM{"del_bb_$key"} ne "on"){push(@bad_key,$key);}
	}
	while(($key)=each %open_key){
		if($FORM{"del_oo_$key"} ne "on"){push(@open_key,$key);}
	}
print OUT<<"EOM";
);
%bad_key=(
EOM
	local(%check);
	foreach(@bad_key){
		if(!$check{$_}){print OUT "\'$_\'=>\'1\',\n"; $check{$_}=1;}
	}
print OUT<<"EOM";
);
%open_key=(
EOM
	local(%check);
	foreach(@open_key){
		if(!$check{$_}){
			if(!$FORM{"hm_$_"} && $open_key{$_} ne "1"){print OUT "\'$_\'=>\'1\',\n";}
			elsif(!$FORM{"hm_$_"}){print OUT "\'$_\'=>\'$open_key{$_}\',\n";}
			else{print OUT "\'$_\'=>\'$FORM{\"hm_$_\"} \',\n";}
		$check{$_}=1;
		}
	}
print OUT<<"EOM";
);
1;
EOM

close(OUT);

&unlock_key();

&mes("キーワード表\示設定の変更が完了しました","キーワード表\示設定の変更完了","kanri");
}

sub key_cfg_del_word_act{
#(6.2)キーワードランキングの集計対象外のキーワードを一括登録実行(&key_cfg_del_word_act)
&pass_check;

&lock_key();
local(@bad_key,@open_key);
require "$EST{log_path}keyrank_ys.cgi";

open(OUT,">$EST{log_path}keyrank_ys.cgi");

print OUT<<"EOM";
%keyrank=(
EOM
	local($key,$value);
	while(($key,$value)=each %keyrank){
	print OUT "\'$key\'=>\'$value\',\n";
	}
print OUT<<"EOM";
);
%bad_key=(
EOM
	local($key,$value);
	while(($key,$value)=each %bad_key){
	print OUT "\'$key\'=>\'$value\',\n";
	}
	local(@del_key_list);
	@del_key_list=split(/,/,$FORM{del_key_list});
	foreach(@del_key_list){
	$_=~s/\n//g;
	print OUT "\'$_\'=>\'1\',\n";
	}
print OUT<<"EOM";
);
%open_key=(
EOM
	local($key,$value);
	while(($key,$value)=each %open_key){
	print OUT "\'$key\'=>\'$value\',\n";
	}
print OUT<<"EOM";
);
1;
EOM

close(OUT);

&unlock_key();


&mes("集計対象外のキーワードの一括登録が完了しました","登録完了","kanri");
}

sub log_conv{
#(7)各種ログ変換(&log_conv)
&pass_check;

print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/log_conv.html";

}

sub log_conv_act{
#(7.1)各種ログ変換実行(&log_conv_act)
&pass_check;
if($FORM{check} ne "on"){&mes("確認チェックがされていません。<br>戻ってチェックしてから実行してください。","チェックエラー","java");}

unless(-f $FORM{bf_file}){&mes("エラー：$bf_file が見つかりません","ファイルが見つかりません","java");}
else{
&lock;
	if($FORM{log_mode} eq "v3tov4"){
		&henkan_v3tov4();
		$PR_msg="Ver3形式→Ver4形式への変換が完了しました";
	}
	if($FORM{log_mode} eq "v2tov4"){
		&henkan_v2tov4();
		$PR_msg="Ver2形式→Ver4形式への変換が完了しました";
	}
	elsif($FORM{log_mode} eq "v4tocsv"){
		if(!$FORM{download}){&henkan_v4tocsv();}
		else{
			&unlock;
				print "Content-type: application/octet-stream .csv\n\n";
				open(IN,"./$FORM{bf_file}");
					while(<IN>){
						$i=0;
						$_=~s/,/，/g; $_=~s/"/”/g; $_=~s/\n//g;
						@Slog=split(/<>/,$_);
						foreach $Slog(@Slog){
							$Slog[$i]= '"' . $Slog[$i] . '"';
							$i++;
						}
						$line=join(",",@Slog);
						$line.="\n";

					print $line;
					}
				close(IN);
				exit;
		}
		$PR_msg="Ver4形式→CSV形式への変換が完了しました";
	}
	elsif($FORM{log_mode} eq "csvtov4"){
		&henkan_csvtov4();
		$PR_msg="CSV形式→Ver4形式への変換が完了しました";
	}
&unlock;
}

&mes("$PR_msg","変換終了","kanri");

}

sub henkan_v3tov4{
local($line,@Slog);

open(IN,"./$FORM{bf_file}");
open(OUT,">./$FORM{af_file}");
	while(<IN>){
		@Slog=split(/<>/,$_);
			#マーク
			if($Slog[3]==0){$Slog[3]="0_0";}
			elsif($Slog[3]==1){$Slog[3]="1_0";}
			elsif($Slog[3]==2){$Slog[3]="0_1";}
			else{$Slog[3]="1_1";}
			#カテゴリ
			$Slog[10]=~s/,/&/g;
			#アクセスランキング
			$Slog[13]=$Slog[13] . "_" . $Slog[13] . "_0_0";
			#キーワード
			$Slog[15]=~s/,/ /g;
		$line=join("<>",@Slog);
		$line=~s/\n//g;
		$line=~s/,/，/g; $line=~s/"/”/g;
		$line .="<>\n";
		
		print OUT $line;
	}
close(OUT);
close(IN);
}

sub henkan_v2tov4{
local($line,@Slog);

open(IN,"./$FORM{bf_file}");
open(OUT,">./$FORM{af_file}");
	while(<IN>){
		@Slog=split(/<>/,$_);
			#マーク
			if($Slog[3]==0){$Slog[3]="0_0";}
			elsif($Slog[3]==1){$Slog[3]="1_0";}
			elsif($Slog[3]==2){$Slog[3]="0_1";}
			else{$Slog[3]="1_1";}
			#カテゴリ
			$Slog[10]=~s/,/&/g;
			#アクセスランキング
			$Slog[13]=$Slog[13] . "_" . $Slog[13] . "_0_0";
			#キーワード
			$Slog[15]=" ";
		$line=join("<>",@Slog);
		$line=~s/\n//g;
		$line=~s/,/，/g; $line=~s/"/”/g;
		$line .="<>\n";
		
		print OUT $line;
	}
close(OUT);
close(IN);
}

sub henkan_v4tocsv{
local($line,@Slog,$Slog,$i);

open(IN,"./$FORM{bf_file}");
open(OUT,">./$FORM{af_file}");
	while(<IN>){
		$i=0;
		$_=~s/,/，/g; $_=~s/"/”/g; $_=~s/\n//g;
		@Slog=split(/<>/,$_);
		foreach $Slog(@Slog){
			$Slog[$i]= '"' . $Slog[$i] . '"';
			$i++;
		}
		$line=join(",",@Slog);
		$line.="\n";
		

		print OUT $line;
	}
close(OUT);
close(IN);
}

sub henkan_csvtov4{
local($line,@Slog);

open(IN,"./$FORM{bf_file}");
open(OUT,">./$FORM{af_file}");
	while($line=<IN>){
		$i=0;
		$line=~s/([^"]),([^"])/$1,$2/g;
		$line=~s/"//g; $line=~s/\n//g;

		@Slog=split(/,/,$line);
		
		$line=join("<>",@Slog);
		$line.="\n";
		
		print OUT $line;
	}
close(OUT);
close(IN);
}

sub log_conv_kt_act{
#(7.2)Ver3からカテゴリ設定インポート実行(&log_conv_kt_act)
&pass_check;

if($FORM{check} ne "on"){&mes("確認チェックにチェックをしてからもう一度実行してください","確認チェックをしてください","java");}

unless(-f $FORM{cfg_bf_file}){&mes("$FORM{cfg_bf_file}は存在しません","エラー","java");}

local(%t_kt,%t_kt_top,%t_kt_ref,%t_kt_ex);
#カテゴリ名→%t_kt(カテゴリ番号,カテゴリ名)
#トップ表示属性→%t_kt_top(カテゴリ番号,1)
#登録不可属性→%t_kt_no_regist(カテゴリ番号,1)
#参照カテゴリ属性→%t_kt_ref(カテゴリ番号,(カテゴリ&カテゴリ…))
#カテゴリ説明文→%t_kt_ex(カテゴリ番号,説明文)

	#%KTEXを%KTEX_preにコピー
	%KTEX_pre=%KTEX;
	%KTEX=();

require $FORM{cfg_bf_file};

	if($#ganes<0){&mes("$FORM{cfg_bk_file}は、カテゴリ設定ファイルではありません","エラー","java");}

local($kt_no,$kt_name,$kt_no_regist,$kt_top,$kt_ref,@kt_name);
foreach(@ganes){
	($kt_no,$kt_name,$kt_no_regist,$kt_top,$kt_ref)=split(/&/,$_);
	@kt_name=split(/:/,$kt_name);
	$t_kt{$kt_no}=$kt_name[$#kt_name];
	if($kt_no_regist eq "no"){$t_kt_no_regist{$kt_no}=1;}
	if($kt_top eq "t"){$t_kt_top{$kt_no}=1;}
	if($kt_ref){$kt_ref=~s/,/&/g; $t_kt_ref{$kt_no}=$kt_ref;}
}
foreach(sort keys %KTEX){
	$t_kt_ex{$_}=$KTEX{$_};
}

&gane_st; &gane_guide;

	if($FORM{r_mode} eq "change"){ #差し替えモードのとき
		if($FORM{kt_no_name} eq "on"){%ganes=();} #カテゴリ
		if($FORM{kt_top} eq "on"){%gane_top=();} #トップ表示属性
		if($FORM{kt_no_regist} eq "on"){%gane_UR=();} #登録不可属性
		if($FORM{kt_ref} eq "on"){%gane_ref=();} #参照カテゴリ属性
		if($FORM{kt_ex} eq "on"){%KTEX=();} #カテゴリ説明文
	}
	
local($key,$value);
	if($FORM{kt_no_name} eq "on"){ #カテゴリ
		while(($key,$value)=each %t_kt){
			$ganes{$key}=$value;
		}
	}
	if($FORM{kt_no_regist} eq "on"){ #登録不可属性
		while(($key,$value)=each %t_kt_no_regist){
			$gane_UR{$key}=$value;
		}
	}
	if($FORM{kt_top} eq "on"){ #トップ表示属性
		while(($key,$value)=each %t_kt_top){
			$gane_top{$key}=$value;
		}
	}
	if($FORM{kt_ref} eq "on"){ #参照カテゴリ属性
		while(($key,$value)=each %t_kt_ref){
			$gane_ref{$key}=$value;
		}
	}
	if($FORM{kt_ex} eq "on"){ #カテゴリ説明文
		while(($key,$value)=each %t_kt_ex){
			$KTEX{$key}=$value;
		}
	}
	
	if($FORM{r_mode} eq "rewrite"){
		while(($key,$value)=each %KTEX_pre){
			$KTEX{$key}=$value;
		}
	}

	#その他のカテゴリを初期化
	@gane_other=();
	foreach(sort keys %ganes){
		if(index($_,"_")<0){push(@gane_other,$_);}
	}
	
	#カテゴリ説明文に特殊カテゴリ説明文を追加
	$KTEX{new_ys}="★14日以内に登録されたサイト";
	$KTEX{renew_ys}="★14日以内に更新されたサイト";
	$KTEX{rank}="★人気ランキングをベスト100位まで紹介しています";
	$KTEX{rank_bf}="★前回のランキングをベスト100位まで紹介しています";


	#書き込む前に念のため、フォーム属性を不必要な消去
	delete $FORM{cfg_bf_file}; delete $FORM{r_mode};
	delete $FORM{kt_no_name}; delete $FORM{kt_top};
	delete $FORM{kt_no_regist}; delete $FORM{kt_ref};
	delete $FORM{kt_ex}; delete $FORM{check};

&cfg_set(0,1,1);

&mes("Ver3からのカテゴリ設定の移行が完了しました","設定完了","kanri");
}

sub log_conv_kt_sort{
#(7.3)カテゴリ・ソート変換実行(&log_conv_kt_sort)
&pass_check;
if($FORM{check} ne "on"){&mes("確認チェックにチェックしてから変換ボタンを押してください","チェックミス","java");}

	if($FORM{bk_mode} eq "on"){ #復元モードのとき
		&lock();
		if($FORM{bk_cfg_no} ne "on"){
		open(IN,"$FORM{bk_file_cfg}");
		open(OUT,">pl/cfg.cgi");
			while(<IN>){
				print OUT $_;
			}
		close(OUT);
		close(IN);
		}
		if($FORM{bk_other_cfg_no} ne "on"){
		open(IN,"$FORM{bk_file_other_cfg}");
		open(OUT,">pl/other_cfg.cgi");
			while(<IN>){
				print OUT $_;
			}
		close(OUT);
		close(IN);
		}
		if($FORM{bk_ys4_no} ne "on"){
		open(IN,"$FORM{bk_file_ys4}");
		open(OUT,">$EST{log_path}$EST{logfile}");
			while(<IN>){
				print OUT $_;
			}
		close(OUT);
		close(IN);
		}
		
		&unlock();
	&mes("環境設定の復元が完了しました","復元完了","kanri");
	}

	#$FORM{all}の処理
	if($FORM{all} eq "on"){
		local($key,$value);
		while(($key,$value)=each %ganes){
			if(index($key,"_")<0){$FORM{$key}="on";}
		}
	}

	#$FORM{kt_str}を解析
	if($FORM{kt_str}){
		if($FORM{kt_str}=~/[^\w\-\,]/){&mes("カテゴリ指定文に全角文字が含まれています","エラー","java");}
		local(@kt_str,@del_list);
		@kt_str=split(/,/,$FORM{kt_str});
		foreach(@kt_str){
			if(/^(\d+)(n*)\-(\d+)(n*)$/){
				local($kt1=$1,$kt2=$3,$keta1,$keta2,$n_fl=0);
				if($4 eq "n"){$n_fl=1;}
				$kt1=~m/(0*)([1-9]+)/; $keta1=length($kt1);
				$kt2=~m/(0*)([1-9]+)/; $keta2=length($kt2);
					if($keta1 ne $keta2){&mes("カテゴリ指定文が間違っています：<b>$_</b>","エラー","java");}
					local($i=1,$kt1_j);
					while($kt1 ne $kt2){
						$kt1_j=sprintf("%d",$kt1);
							if(!$n_fl){$FORM{$kt1}="on";}
							else{push(@del_list,$kt1);}
						$kt1_j++;
						$kt1=sprintf("%0${keta1}d",$kt1_j);
						$i++;
						if($i>5000){&mes("<b>-</b> で 5000以上の連続するカテゴリを指定することはできません","エラー","java");}
					}
						if(!$n_fl){$FORM{$kt2}="on";}
						else{push(@del_list,$kt2);}
			}
			elsif(/(\d+)(n*)/){
				if($2 eq "n"){push(@del_list,$1);}
				else{$FORM{$1}="on";}
			}
			else{&mes("カテゴリ指定文が間違っています","エラー","java");}
		}
		foreach(@del_list){
			$FORM{$_}="";
		}
	}
	
	
	#カテゴリリストから変換対象のカテゴリ用の%kt_af,%kt_name_afを作成
	local(@kt,$kt,$oya_kt,%ch_line,%ch_cnt,$key,$value);
	while (($key)=each %ganes){
		$oya_kt=$key; $oya_kt=~s/_\d+$//;
		if(index($key,"_")>=0){
			$ch_cnt{$oya_kt}++;
			$ch_line{$oya_kt}.=$key . ",";
		}
	}
	
	local($top_kt,%kt_list,$i,$kt);
	require "pl/other_cfg.cgi";
	while (($key)=each %ch_cnt){
		($top_kt)=split(/_/,$key,2);
		if($ch_cnt{$key}>1 && $FORM{$top_kt} eq "on"){
			@kt=split(/,/,$ch_line{$key}); @kt=sort @kt;
			$i=0; $kt="";
			foreach $kt(sort{$EST_furi{$a} cmp $EST_furi{$b}}@kt){
				$kt_af{$kt}=$kt[$i];
				$kt_name_af{$kt[$i]}=$ganes{$kt};
				$i++;
			}
		}
	}
	
		#親ktが変化するカテゴリを再定義
		local(@kt,$kt,$new_kt);
		foreach $key(sort keys %ch_line){
			if($kt_af{$key}){
			@kt=split(/,/,$ch_line{$key}); if(!$kt[$#kt]){pop @kt;}
				foreach $kt(@kt){
					if($kt_af{$kt}){$new_kt=$kt_af{$kt};}
					else{$new_kt=$kt;}
					
				$new_kt=~s/^(.+)_(\d+)$/$kt_af{$key}_$2/;
					$kt_af{$kt}=$new_kt;
					$kt_name_af{$new_kt}=$ganes{$kt};
				}
			}
		}
	
	#ロック
	&lock();
	
	#%ganesを変換し、書き換え
		#/pl/cfg.cgiをバックアップ
		if($FORM{bk_cfg_no} ne "on"){
		open(IN,"pl/cfg.cgi");
		open(OUT,">$FORM{bk_file_cfg}");
			while(<IN>){
				print OUT $_;
			}
		close(OUT);
		close(IN);
		}
		#/$EST{log_path}$EST{logfile}をバックアップ
		if($FORM{bk_ys4_no} ne "on"){
		open(IN,"$EST{log_path}$EST{logfile}");
		open(OUT,">$FORM{bk_file_ys4}");
			while(<IN>){
				print OUT $_;
			}
		close(OUT);
		close(IN);
		}
		#/$EST{log_path}other_cfg.cgiをバックアップ
		if($FORM{bk_other_cfg_no} ne "on"){
		open(IN,"pl/other_cfg.cgi");
		open(OUT,">$FORM{bk_file_other_cfg}");
			while(<IN>){
				print OUT $_;
			}
		close(OUT);
		close(IN);
		}
		
		#副属性をロード
		&EST_reg; &gane_st; &gane_guide;
		%gane_top_bk=%gane_top;
		%gane_st_bk=%ganes_st; %gane_ref_bk=%gane_ref;
		%gane_UR_bk=%gane_UR; %KTEX_bk=%KTEX;
	while(($key,$value)=each %ganes){
		if($kt_af{$key}){
			delete $ganes{$key};
			#副属性 %gane_top/%gane_st/%gane_ref/%gane_UR/%KTEX/ 
			delete $gane_top{$key};
			delete $gane_st{$key};
			delete $gane_ref{$key};
			delete $gane_UR{$key};
			delete $KT_EX{$key};
		}
	}
	while(($key,$value)=each %kt_af){
		$ganes{$value}=$kt_name_af{$value};
		#副属性
		$gane_top{$value}=$gane_top_bk{$key};
		$gane_st{$value}=$gane_st_bk{$key};
		$gane_ref{$value}=$gane_ref_bk{$key};
		$gane_UR{$value}=$gane_UR_bk{$key};
		$KT_EX{$value}=$KT_EX_bk{$key};
	}
		#@gane_other/
		$i=0;
		foreach(@gane_other){
			if($af_kt{$_}){$gane_other[$i]=$af_kt{$_};}
			$i++;
		}
	
	&cfg_set(1,1,1,1);
	
	#その他の環境設定ファイル(other_cfg.cgi)を変換し、書き換え
	%EST_furi_bk=%EST_furi;
	while(($key,$value)=each %EST_furi){
		if($kt_af{$key}){ delete $EST_furi{$key}; }
	}
	while(($key,$value)=each %kt_af){
		$EST_furi{$kt_af{$key}}=$EST_furi_bk{$key};
	}
		undef %EST_furi_bk;
	open(OUT,">pl/other_cfg.cgi");
		print OUT "\%EST_furi=(\n";
		foreach $key(sort keys %EST_furi){
			print OUT "\'$key\'=>\'$EST_furi{$key}\',\n";
		}
		print OUT ");\n1\n";
	close(OUT);
	
	#本体ログを更新
	local(@log_lines,@Slog,$kt_fl,$kt_line,$kt,$line);
	open(IN,"$EST{log_path}$EST{logfile}");
		while($line=<IN>){
		@Slog=split(/<>/,$line);
		$kt_fl=0; $kt_line="";
		@kt=split(/&/,$Slog[10]);
			foreach $kt(@kt){
				if($kt_af{$kt}){ $kt_fl=1; $kt_line .= $kt_af{$kt} . "&";}
				else{ $kt_line .= $kt . "&";}
			}
			if($kt_fl){
			chop $kt_line;
			$Slog[10]=$kt_line;
			push(@log_lines,join("<>",@Slog));
			}
			else{ push(@log_lines,$line); }
		}
	close(IN);
	open(OUT,">$EST{log_path}$EST{logfile}");
		print OUT @log_lines;
	close(OUT);
	
	#派生カテゴリを更新
	require "$EST{log_path}task_ys.cgi";
	
	#更新するカテゴリリストを作成
		#%TASK/@TASK_listを使用
		@TASK_list=();
		$TASK{"new"}=$TASK{"renew"}=$TASK{"m1"}=$TASK{"m2"}=1; #特殊カテゴリ

		while(($key,$value)=each %ganes){
			if(index($key,"_")<0 && $FORM{$key} eq "on"){$TASK{$key}=1;}
		}
		##派生ファイルの処理
		unless($EST{html} && $EST{task} ne "2"){&make_task;} #タスクファイルに書き込み
	
	#ロック解除
	&unlock();

&mes("カテゴリ・ソ\ート変換が完了しました","カテゴリ・ソ\ート変換完了","kanri");
}

sub log_kt_change{
#(8)ログデータの交換・移動・削除(&log_kt_change)
&pass_check;

print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/log_kt_change.html";

}

sub log_kt_change_act{
#(8.1)ログデータの交換・移動・削除実行(&log_kt_change_act)
&pass_check;
if($FORM{check} ne "on"){&mes("確認チェックがされていません。<br>戻ってチェックしてから実行してください。","チェックエラー","java");}
	
	#記入漏れのチェック
	if($FORM{log_mode} eq "change"){
		if(!$FORM{change_kt1} || !$FORM{change_kt2}){&mes("交換対象のカテゴリを指定してください","カテゴリ選択ミス","java");}
	}
	elsif($FORM{log_mode} eq "move"){
		if(!$FORM{bf_move_kt} || !$FORM{af_move_kt}){&mes("移動対象のカテゴリを指定してください","カテゴリ選択ミス","java");}
	}
	elsif($FORM{log_mode} eq "del"){
		if(!$FORM{del_kt}){&mes("削除対象のカテゴリを選択してください","カテゴリ選択ミス","java");}
	}
	else{&mes("log_modeが選択されていません","log_mode選択エラー","java");}

&lock;
require "$EST{log_path}task_ys.cgi";
local($PR_mes,@kousin_kt);
	if($FORM{log_mode} eq "change"){ #change
		#ログデータの交換
		$PR_mes="ログデータの交換が完了しました<br>『" . &full_kt($FORM{change_kt1}) . "}』と『" . &full_kt($FORM{change_kt2}) . "』を交換しました";
		local(@log_lines,@Slog,$change_kt1=$FORM{change_kt1},$change_kt2=$FORM{change_kt2},@kt,$kt,$i,$j,$line);
		@kousin_kt=($change_kt1,$change_kt2);
		open(IN,"$EST{log_path}$EST{logfile}");
			while($line=<IN>){
				$i=0; $j=0;
				@Slog=split(/<>/,$line);
				@kt=split(/&/,$Slog[10]);
				foreach $kt(@kt){
					if($kt eq $change_kt1){$kt[$i]=$change_kt2; $j=1;}
					elsif($kt eq $change_kt2){$kt[$i]=$change_kt1; $j=1;}
					$i++;
				}
				if($j){$Slog[10]=join("&",@kt); $line=join("<>",@Slog);}
				push(@log_lines,$line);
			}
		close(IN);
		open(OUT,">$EST{log_path}$EST{logfile}");
			print OUT @log_lines;
		close(OUT);
		@log_lines=();
	}
	elsif($FORM{log_mode} eq "move"){ #move
		#ログデータの移動
		$PR_mes="ログデータの移動が完了しました<br>『" . &full_kt($FORM{bf_move_kt}) . "』を『" . &full_kt($FORM{af_move_kt}) . "』に移動しました";
		local(@log_lines,@Slog,$bf_move_kt=$FORM{bf_move_kt},$af_move_kt=$FORM{af_move_kt},@kt,$kt,$i,$j,$line);
		@kousin_kt=($bf_move_kt,$af_move_kt);
		open(IN,"$EST{log_path}$EST{logfile}");
			while($line=<IN>){
				$i=0; $j=0;
				@Slog=split(/<>/,$line);
				@kt=split(/&/,$Slog[10]);
				foreach $kt(@kt){
					if($kt eq $bf_move_kt){
						if($j){$kt[$i]="";}
						else{$kt[$i]=$af_move_kt; $j=1;}
					}
					$i++;
				}
				if($j){$Slog[10]=join("&",@kt); $line=join("<>",@Slog);}
				push(@log_lines,$line);
			}
		close(IN);
		open(OUT,">$EST{log_path}$EST{logfile}");
			print OUT @log_lines;
		close(OUT);
		@log_lines=();
	}
	else{ #del
		#ログデータの削除
		$PR_mes="ログデータの削除が完了しました<br>『" . &full_kt($FORM{del_kt}) . "』を削除しました";
		local(@log_lines,@Slog,$del_kt=$FORM{del_kt},@kt,$kt,$i,$j,$k,$line);
		@kousin_kt=($del_kt);
		open(IN,"$EST{log_path}$EST{logfile}");
			while($line=<IN>){
				$i=0; $j=0; $k=0;
				@Slog=split(/<>/,$line);
				@kt=split(/&/,$Slog[10]);
				foreach $kt(@kt){
					if($kt eq $del_kt){$kt[$i]=""; $k=1;}
					else{$j=1;}
					$i++;
				}
				if($k){$Slog[10]=join("&",@kt); $line=join("<>",@Slog);}
				if($j){push(@log_lines,$line);}
			}
		close(IN);
		open(OUT,">$EST{log_path}$EST{logfile}");
			print OUT @log_lines;
		close(OUT);
		@log_lines=();
	}

	##変更したデータに関する派生ファイルを更新
	if($EST{html} && $EST{task}){
		&MK_html(*kousin_kt);
	}
	else{
		#cgi形式の場合にはカテゴリを大カテゴリ化する
		local($i=0,$kt,@kt,%fl);
		foreach $kt(@kousin_kt){
			($kt)=split(/_/,$kt);
			if(!$fl{$kt}){$kousin_kt[$i]=$kt; $fl{$kt}=1;}
			else{$kousin_kt[$i]="";}
			$i++;
		}
		&MK_cgi(*kousin_kt);
	}

	#すべての特殊カテゴリを更新
	$TASK{new}=$TASK{renew}=1;
	foreach(1 .. 2){ #マーク数を増やす時は修正
		$TASK{"m$_"}=1;
	}
	&make_task;

##登録数を再計算
&count_log;

&unlock;

&mes($PR_mes,"ログデータの交換・移動・削除完了","kanri");

}

sub log_repair{
#(9)ログ(登録データ)の修復(&log_repair)
print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/log_repair.html";
}

sub log_repair_act{
#(9.1)ログ(登録データ)の修復実行(&log_repair_act)
require "$EST{log_path}task_ys.cgi";
local($BK_file,$i);
	#修復対象のログを設定
	if($BK_file_no-1>0){$BK_file=$BK_file_no-1;}
	else{$BK_file=$EST{bk_days};}
	$i=$BK_file;
	foreach(1 .. $EST{bk_days}){
		if($FORM{bk_day} eq "$_日前のデータに戻す"){
			if($FORM{"check$_"} ne "on"){&mes("修復確認のため、確認チェックを入れてからもう一度実行してください","確認チェックをしてください","java");}
			$BK_file="$EST{log_path}bkup" . $i . ".cgi";
		}
		if($i<=1){$i=$EST{bk_days};}
		else{$i--;}
	}

unless(-f $BK_file){&mes("$BK_file が見つかりません","エラー","java");}
&lock();

open(IN,"$BK_file");
open(OUT,">$EST{log_path}$EST{logfile}");
	while(<IN>){
		print OUT $_;
	}
close(OUT);
close(IN);

&unlock();

&mes("データの修復が完了しました\$BK_file=$BK_file","修復完了","kanri");
}

sub log_mente{
#(10)ログ診断 (&log_mente)
#	・フィールド数を正常にする
#	・未定義カテゴリを削除
#	・所属カテゴリが0のデータを任意のカテゴリに移動又は削除

&pass_check;

print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/log_mente.html";
}

sub log_mente_act{
#(10.1)ログ診断実行 (&log_mente_act)
&pass_check;

	#入力コマンドの整合チェック＆整形
	##データフィールド数の整形
	$FORM{fld_custom}=~s/\D//g;
	if($FORM{set_fld} eq "custom" && (!$FORM{fld_custom} || $FORM{fld_custom}<15)){
		&mes("データフィールド数を指定してください<br>$Efld未満の数は指定できません","記入ミス","java");
	}
	local($Cfld,$plus_fld);
	if($FORM{set_fld} eq "custom"){$Cfld=$FORM{fld_custom};}
	else{$Cfld=$Efld;} #デフォルト値(temp.cgiで設定)
	local($fld=$FORM{fld_custom}-$Efld);
	if($fld>0){
		foreach(1 .. $fld+1){
			$plus_fld .="<>";
		}
	}
	
	##未定義データの移動先の設定
	if($FORM{set_no} eq "move" && !$FORM{set_no_move_kt}){
		&mes("移動先のカテゴリを指定してください","記入ミス","java");
	}
	local($move_kt,$del_mode);
	if($FORM{set_no} eq "move"){$move_kt=$FORM{set_no_move_kt}; $del_mode="off";}
	else{$move_kt=""; $del_mode="on";}

&lock();
local(@log_lines,@Slog,$line,@kt,$kt,$del_fl);
	open(IN,"$EST{log_path}$EST{logfile}");
		while($line=<IN>){
			$line=~s/\n//g; $line .=$plus_fld;
			@Slog=split(/<>/,$line,$Cfld+1);
				if($Slog[12] eq "http://"){$Slog[12]="";}
				@pt=split(/_/,$Slog[13]);
				foreach(0 .. 3){if(!$pt[$_]){$pt[$_]=0;}} $Slog[13]=join("_",@pt);
			pop(@Slog);
			@kt=split(/&/,$Slog[10]);
			$kt=""; $del_fl=0; #削除フラグ
			foreach(@kt){
				if($ganes{$_}){$kt .=$_ . "&";}
			}
			$Slog[10]=$kt;
			if(!$kt && $del_mode eq "on"){$del_fl=1;}
			elsif(!$kt){$Slog[10]=$move_kt;}
			
			$Slog[0]=~s/\D//g;
			if(!$del_fl && $Slog[0]){
				$line=join("<>",@Slog,"\n");
				push(@log_lines,$line);
			}
		}
	close(IN);
	
	open(OUT,">$EST{log_path}$EST{logfile}");
		print OUT @log_lines;
	close(OUT);
	@log_lines=();
&unlock();
&mes("ログ診断が完了しました","ログ診断完了","kanri");
}

sub config{
#(11)環境設定 (&config)
print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/config.html";
}

sub config_kt{
#(12)カテゴリ設定 (&config_kt)
print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/config_kt.html";
}

sub rank_cfg{
#(13)人気ランキングの設定(&rank_cfg)
&pass_check;

print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/rank_cfg.html";
}

sub rank_cfg_act{
#(13.1)人気ランキングの初期化実行(&rank_cfg_act)
&pass_check;

if($FORM{rank_format}){
	require "$EST{log_path}task_ys.cgi";
	&lock;
	&rank_cfg_make_rank(1);
	$BK_last_rank=$BK_last_rank_t=time();
	&make_task; #タスクファイルを更新
	&unlock;
}
else{&mes("人気ランキング初期化のための確認チェックがされていませんのでもう一度戻ってチェックをしてから実行してください","確認チェックをしてください","java");}
&mes("人気ランキングの初期化が完了しました","人気ランキング初期化完了","kanri");

}

#(13.2)人気ランキングファイルを更新(&rank_cfg_make_rank)
#→temp.cgiへ

sub dl_check{
#(14)デッドリンクチェック画面(&dl_check)
&pass_check;

	#no_link_temp.cgi から no_link.cgi にデータを移行する
	local(%fl,%count,%PR_ip,@data,@ip,$ip,$id,@count,%url,%com);
	
	open(IN,"$EST{log_path}no_link.cgi");
		while(<IN>){
			@data=split(/<>/,$_); #id<>count(,)<>ip<>url<>com<>\n
			@ip=split(/&/,$data[2]);
			$url{$data[0]}=$data[3];
			foreach $ip(@ip){
				$fl{"$data[0]_$ip"}=1;
			}
			$PR_ip{$data[0]}=$data[2];
			@count=split(/,/,$data[1]);
			$i=1;
			foreach(@count){
			$count{"${i}_$data[0]"}=$_;
			$count{$data[0]}+=$_;
			$i++;
			}
			$com{$data[0]}=$data[4];
			
		}
	close(IN);
	
	open(IN,"$EST{log_path}no_link_temp.cgi");
		while(<IN>){
			@data=split(/<>/,$_);
			if(!$fl{"$data[0]_$data[1]"}){
				@count=split(/,/,$data[2]);
				foreach(@count){
				$count{"${_}_$data[0]"}++; #データの報告数
				$count{$data[0]}++;
				}
				$fl{"$data[0]_$data[1]"}=1; #２重チェック
				$PR_ip{$data[0]}.="$data[1]&"; #ip
				$com{$data[0]}.="$data[4]<2>$data[5]<2>$data[3]<1>";
			}
		}
	close(IN);
	local($line,@Slog);
	open(IN,"$EST{log_path}$EST{logfile}");
		while($line=<IN>){
			@Slog=split(/<>/,$line,4);
			foreach(1 .. 5){
				if($count{"${_}_$Slog[0]"}){$url{$Slog[0]}=$Slog[2]; last;}
			}
		}
	close(IN);
	open(OUT,">$EST{log_path}no_link.cgi");
			foreach $id(sort{$count{"1_$b"}<=>$count{"1_$a"}} keys %url){
			print OUT "$id<>";
			foreach(1 .. 5){
				if(!$count{"${_}_$id"}){$count{"${_}_$id"}=0;}
				print OUT $count{"${_}_$id"} . ",";
			}
			print OUT "<>$PR_ip{$id}<>$url{$id}<>$com{$id}<>\n";
		}
	close(OUT);
	open(OUT,">$EST{log_path}no_link_temp.cgi");
	close(OUT);
	

print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/dl_check.html";
}

sub dl_check_dl{
#(14.1)デッドリンクチェック用ファイルをダウンロード(&dl_check_dl)
&pass_check;
print "Content-type: application/octet-stream\n\n";
open(IN,"$EST{log_path}$EST{logfile}");
	while(<IN>){
	@Slog=split(/<>/,$_);
	print "$Slog[0]\t$Slog[2]\t\t\t0\t\t\t\t\t\t\t\t0\t\t\t\t\n";
	}
close(IN);
exit;
}

sub dl_check_act{
#(14.2)デッドリンクチェック実行画面(&dl_check_act)
&pass_check;
unless(-f $FORM{checkfile}){&mes("指定されたファイルは存在しません","エラー","java");}

local(@lines,@data,%url);
open(IN,"./$FORM{checkfile}");
	while(<IN>){
		@data=split(/\t/,$_);
		if(index($data[13],"Not Found")>=0 || index($data[13],"Forbidden")>=0){
		$url{$data[0]}=$data[1];
		push(@lines,$_);
		}
	}
close(IN);

open(OUT,">./$FORM{checkfile}");
	print OUT @lines;
close(OUT);


print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/dl_check_act.html";
}

sub ill_lock_del{
#(15)異常ロック解除ファイル操作(&ill_lock_del)

$FORM{file}=~s/[^\w.]//g;

if($FORM{act} ne "on"){
print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/ill_lock_del.html";
}
else{ #処理実行
&pass_check;
	unless(-f "lock/$FORM{file}"){&mes("lock/$FORM{file}は存在しません","エラー","java");}
	if($FORM{set} eq "削除する" && $FORM{check} ne "on"){&mes("削除確認のチェックをしてください","エラー","java");}
	if($FORM{set} eq "削除する"){ #削除
		unlink("lock/$FORM{file}");
		&mes("<b>lock/$FORM{file}</b>を削除しました","削除完了",$EST{home});
	}
	else{ #ダウンロード
		print "Content-type: application/octet-stream\n\n";
		open(IN,"lock/$FORM{file}");
			while(<IN>){
			print $_;
			}
		close(IN);
		exit;
	}
}

}

sub design{
#(16)簡易デザイン設定(&design)
&pass_check;

if($FORM{set} eq "設定実行"){
local(@css_file);
	open(IN,"$EST{html_path}style.css");
		while(<IN>){push(@css_file,$_);}
	close(IN);
	open(OUT,">$EST{html_path}style.css");
		foreach(@css_file){
			if(/^a:link{(.*)color:(.*); }/i)
				{
				$_=~s/^a:link{(.*)color:.*; }(.*)/a:link{$1color:$FORM{a_link}; }$2/i;
				}
			elsif(/^a:visited{.*color:(.*); }/i)
				{
				$_=~s/^a:visited{(.*)color:.*; }(.*)/a:visited{$1color:$FORM{a_visited}; }$2/i;
				}
			elsif(/^a:active{.*color:(.+); }/i)
				{
				$_=~s/^a:active{(.*)color:.*; }(.*)/a:active{$1color:$FORM{a_active}; }$2/i;
				}
			elsif(/^a:hover{.*color:(.*); }/i)
				{
				$_=~s/^a:hover{(.*)color:.*; }(.*)/a:hover{$1color:$FORM{a_hover}; }$2/i;
				}
			elsif(/^body{ font-size:(.*)pt; color:(.*); background-color:(.*); background-image:url\((.*)\); margin-left:(.*); margin-right:(.*); }/i)
				{
				$_=~s/^body{(.*)font-size:.*pt; color:.*; background-color:.*; background-image:url\(.*\); margin-left:.*; margin-right:.*; }(.*)/body{$1font-size:$FORM{body_size}pt; color:$FORM{body_color}; background-color:$FORM{body_bk_color}; background-image:url\($FORM{body_bk_img}\); margin-left:$FORM{body_m_right}; margin-right:$FORM{body_m_left}; }$2/i;
				}
			elsif(/^tr,td{ font-size:(.*)pt; color:(.*); }/i)
				{
				$_=~s/^tr,td{(.*)font-size:.*pt; color:.*; }(.*)/tr,td{$1font-size:$FORM{tr_td_size}pt; color:$FORM{tr_td_color}; }$2/i;
				}
			elsif(/^hr{ color:(.*); }/i)
				{
				$_=~s/^hr{(.*)color:.*; }(.*)/hr{$1color:$FORM{hr_color}; }$2/i;
				}
			elsif(/^#mid{ font-size:(.*)pt; }/i)
				{
				$_=~s/^#mid{(.*)font-size:.*pt; }(.*)/#mid{$1font-size:$FORM{mid_size}pt; }$2/i;
				}
			elsif(/^#small{ font-size:(.*)pt; }/i)
				{
				$_=~s/^#small{(.*)font-size:.*pt; }(.*)/#small{$1font-size:$FORM{small_size}pt; }$2/i;
				}
			elsif(/^#kanri{ color:(.*); }/i)
				{
				$_=~s/^#kanri{(.*)color:.*; }(.*)/#kanri{$1color:$FORM{kanri_color}; }$2/i;
				}
			elsif(/^#log{ width:(.*); border-style:(.*); border-color:(.*); }/i)
				{
				$_=~s/^#log{(.*)width:.*; border-style:.*; border-color:.*; }(.*)/#log{$1width:$FORM{log_width}; border-style:$FORM{log_bor_style}; border-color:$FORM{log_bor_color}; }$2/i;
				}
			elsif(/^#log-0{ background-color:(.*); }/i)
				{
				$_=~s/^#log-0{(.*)background-color:.*; }(.*)/#log-0{$1background-color:$FORM{log_0_bk_color}; }$2/i;
				}
			elsif(/^#log-1{ background-color:(.*); }/i)
				{
				$_=~s/^#log-1{(.*)background-color:.*; }(.*)/#log-1{$1background-color:$FORM{log_1_bk_color}; }$2/i;
				}
			elsif(/^#log-2{ background-color:(.*); }/i)
				{
				$_=~s/^#log-2{(.*)background-color:.*; }(.*)/#log-2{$1background-color:$FORM{log_2_bk_color}; }$2/i;
				}
			elsif(/^#log-3{ background-color:(.*); }/i)
				{
				$_=~s/^#log-3{(.*)background-color:.*; }(.*)/#log-3{$1background-color:$FORM{log_3_bk_color}; }$2/i;
				}
			elsif(/^#log-4{ background-color:(.*); }/i)
				{
				$_=~s/^#log-4{(.*)background-color:.*; }(.*)/#log-4{$1background-color:$FORM{log_4_bk_color}; }$2/i;
				}
			elsif(/^#title-bar{ background-color:(.*); color:(.*); font-size:(.*)pt; }/i)
				{
				$_=~s/^#title-bar{(.*)background-color:.*; color:.*; font-size:.*pt; }(.*)/#title-bar{$1background-color:$FORM{title_bar_bk_color}; color:$FORM{title_bar_color}; font-size:$FORM{title_bar_size}pt; }$2/i;
				}
			elsif(/^#mid-bar{ background-color:(.*); }/i)
				{
				$_=~s/^#mid-bar{(.*)background-color:.*; }(.*)/#mid-bar{$1background-color:$FORM{mid_bar_bk_color}; }$2/i;
				}
		print OUT $_;
		}
	close(OUT);
&mes("簡易デザイン設定が完了しました","簡易デザイン設定完了","kanri");
}
else{
print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/design.html";
}

}

sub template_cfg{
&pass_check;
#(17)テンプレートファイルの修正(&template_cfg)
$FORM{read_file}=~s/\|//g;
	if($FORM{read_file}){ #読み込むファイルのチェック
		unless(-f "./$EST{temp_path}$FORM{read_file}"){&mes("指定されたファイルは閲覧不可です","エラー","java");}
	}

if(!$FORM{set}){
print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/template_cfg.html";
}
elsif($FORM{set} eq "編集実行"){
	open(OUT,">./$EST{temp_path}$FORM{write_file}");
		$FORM{file_str}=~s/’/'/g;
		print OUT $FORM{file_str};
	close(OUT);

&mes("「$FORM{write_file}」の編集が完了しました","編集完了","kanri");
}
else{&mes("モードが不正です","エラー","java");}

}

sub ver_info{
#(18)バージョン情報(&ver_info)
&pass_check;
print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/ver_info.html";
}

sub look_mes{
#(19)登録者のメッセージを見る(&look_mes)
&pass_check;
print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/look_mes.html";
}

sub cfg_make{
#(cfg1)環境設定(%EST)を更新(&cfg_make)

#パスワードチェック
if($EST{pass} ne "setup"){
&pass_check;
}

local($key,$bf_pass=$FORM{pass});

		##パスワードを暗号化する
		if($FORM{new_pass}){$bf_pass=$FORM{pass}=$FORM{new_pass};}
		if($EST{crypt}){$FORM{pass}=crypt("$FORM{pass}","ys");}

	foreach $key(keys %EST){ #環境設定(%EST)を更新
		if(defined $FORM{$key}){$EST{$key}=$FORM{$key}}
	}
	
		##パスワードを暗号化前に戻す
		$FORM{pass}=$bf_pass;
	
	##
	

	&cfg_set();
}

sub cfg_set{
#(cfg1.1)環境設定ファイルを更新(&cfg_set)
local(
$EST_reg_fl=$_[0], #sub EST_regを更新(1/0)
$gane_st_fl=$_[1], #sub gane_stを更新(1/0)
$gane_guide_fl=$_[2], #sub gane_guideを更新(1/0)
$exit_fl=$_[3], #終了する=0/しない=1)
);

#修正フラグで読み込むかどうかを判定
if(!$EST_reg_fl){&EST_reg;}
if(!$gane_st_fl){&gane_st;}
if(!$gane_guide_fl){&gane_guide;}

#&search_form/&menu_bar/&head_sp/&foot_spを読み込み
local($PR_search_form,$PR_menu_bar,$PR_head_sp,$PR_foot_sp,
$fl_sf=0,$fl_mb=0,$fl_hs=0,$fl_fs=0);
open(IN,"pl/cfg.cgi");
	while(<IN>){
		if($_ eq "sub search_form{\n"){$fl_sf=1;}
		elsif($_ eq "} #end of &search_form\n"){$fl_sf=0;}
		elsif($fl_sf){$PR_search_form.=$_;}
		
		elsif($_ eq "sub menu_bar{\n"){$fl_mb=1;}
		elsif($_ eq "} #end of &menu_bar\n"){$fl_mb=0;}
		elsif($fl_mb){$PR_menu_bar.=$_;}
		
		elsif($_ eq "sub head_sp{\n"){$fl_hs=1;}
		elsif($_ eq "} #end of &head_sp\n"){$fl_hs=0;}
		elsif($fl_hs){$PR_head_sp.=$_;}
		
		elsif($_ eq "sub foot_sp{\n"){$fl_fs=1;}
		elsif($_ eq "} #end of &foot_sp\n"){$fl_fs=0;}
		elsif($fl_fs){$PR_foot_sp.=$_;}
	}
close(IN);

open(OUT,">pl/cfg.cgi");

##%ESTを更新
require "$EST{temp_path}admin/cfg_lib.cgi";

close(OUT);

##登録数を再計算
&count_log;

if(!$exit_fl){
	&mes("環境設定の変更/カテゴリの設定が完了しました","環境設定/カテゴリ設定完了","kanri");
}

}

sub cfg_make_PR_menu{
#(cfg2)環境設定(&search_form/&menu_bar)を更新(&cfg_make_PR_menu)
&pass_check;

local($fl=0,$p_fl=1,$bf_data,@file_data);
$FORM{search_form}=~s/&lt;/</g; $FORM{search_form}=~s/&gt;/>/g; $FORM{search_form}=~s/’/'/g;
$FORM{menu_bar}=~s/&lt;/</g; $FORM{menu_bar}=~s/&gt;/>/g; $FORM{menu_bar}=~s/’/'/g;
$FORM{head_sp}=~s/&lt;/</g; $FORM{head_sp}=~s/&gt;/>/g; $FORM{head_sp}=~s/’/'/g;
$FORM{foot_sp}=~s/&lt;/</g; $FORM{foot_sp}=~s/&gt;/>/g; $FORM{foot_sp}=~s/’/'/g;

	#文法チェック
	{local($mes="");
	open(DM,"<./lock/index.html");
	select(DM);
	eval $FORM{search_form};
	if($@){$mes="外部検索エンジンの設定";}
	eval $FORM{menu_bar};
	if($@){$mes="メニューバーの設定";}
	eval $FORM{head_sp};
	if($@){$mes="ヘッダスペースの設定";}
	eval $FORM{foot_sp};
	if($@){$mes="フッタスペースの設定";}
	
	if($mes){select(stdout);&mes("「<b>$mes</b>」の記入でエラーが出ました。<br>(1)一行目の「print<<\"EOM\";」と最終行の「EOM」が<br>　\削除されていないか確認してください<br>(2)「\@」と使用する場合には「\\\@」と記入してください","記入エラー","java");}
	
	close(DM);
	select(stdout);
	}

open(IN,"pl/cfg.cgi");
	while(<IN>){
		if($_ eq "} #end of &search_form\n"){$p_fl=1; push(@file_data,"\n");}
		elsif($_ eq "} #end of &menu_bar\n"){$p_fl=1; push(@file_data,"\n");}
		elsif($_ eq "} #end of &head_sp\n"){$p_fl=1; push(@file_data,"\n");}
		elsif($_ eq "} #end of &foot_sp\n"){$p_fl=1; push(@file_data,"\n");}
		
		if($fl==1){push(@file_data,$FORM{search_form}); $fl=0;}
		elsif($fl==2){push(@file_data,$FORM{menu_bar}); $fl=0;}
		elsif($fl==3){push(@file_data,$FORM{head_sp}); $fl=0;}
		elsif($fl==4){push(@file_data,$FORM{foot_sp}); $fl=0;}
		
		if($p_fl){push(@file_data,$_);}
		
		if($_ eq "sub search_form{\n"){ #search
		$fl=1; $p_fl=0;
		}
		elsif($_ eq "sub menu_bar{\n"){ #menu
		$fl=2; $p_fl=0;
		}
		elsif($_ eq "sub head_sp{\n"){ #head
		$fl=3; $p_fl=0;
		}		
		elsif($_ eq "sub foot_sp{\n"){ #foot
		$fl=4; $p_fl=0;
		}		
	}
close(IN);

open(OUT,">pl/cfg.cgi");
	print OUT @file_data;
close(OUT);

&mes("メニューバー/外部検索エンジン/ヘッダ・フッタスペースの設定が完了しました","更新完了","kanri");
}

sub cfg_make_reg{
#(cfg3)環境設定(登録処理関係)を更新 (&cfg_make_reg)
&pass_check;
&EST_reg;
local($key);
	foreach $key(keys %EST_reg){ #環境設定(%EST_reg)を更新
		if(defined $FORM{$key}){$EST_reg{$key}=$FORM{$key}}
	}
	&cfg_set(1);
}

sub cfg_make_kt_ex{
#(cfg4)カテゴリ説明文を更新 (&cfg_make_kt_ex)
&pass_check;
&gane_guide;
local($key,@new,@ktex);
	foreach $key(keys %KTEX){ #環境設定(%KTEX)を更新
		if($FORM{"d_$key"}){delete $KTEX{$key};}
		elsif(defined $FORM{"ex_$key"}){$KTEX{$key}=$FORM{"ex_$key"}}
	}
		#新規追加分を定義
		if($FORM{ktex}){
		$FORM{ktex}=~s/&gt;/>/g; $FORM{ktex}=~s/&lt;/</g;
		@new=split(/\n/,$FORM{ktex});
			foreach(@new){
				@ktex=split(/<>/,$_);
				$KTEX{$ktex[0]}=$ktex[1];
			}
		}
	&cfg_set(0,0,1);
}

sub cfg_make_kt{
#(cfg5)カテゴリ設定を更新 (&cfg_make_kt)
&pass_check;
&gane_st;
require "pl/other_cfg.cgi";
local($key,@new,@kt);
	
	if($FORM{mente_mode} eq "mente"){
	@gane_other=();
	foreach $key(keys %ganes){ #カテゴリ設定(%ganes)を更新
		if($FORM{"d_$key"}){delete $ganes{$key};}
		elsif(defined $FORM{"kt_$key"}){ #カテゴリがあれば
			$ganes{$key}=$FORM{"kt_$key"};
				if($FORM{"t_$key"}){$gane_top{$key}=1;}
				elsif($gane_top{$key}){delete $gane_top{$key};}
				if($FORM{"o_$key"}){push(@gane_other,$key);}
				if($FORM{"no_$key"}){$gane_UR{$key}=1;}
				elsif($gane_UR{$key}){delete $gane_UR{$key};}
				if($FORM{"ref_$key"}){$gane_ref{$key}=$FORM{"ref_$key"};}
				elsif($gane_ref{$key}){delete $gane_ref{$key};}
		}
			#その他のカテゴリ整形
			@gane_other=sort @gane_other;
			
			#ふりがなの設定
			$EST_furi{$key}=$FORM{"furi_$key"}; #$EST_furi{$key}=~s/'/’/g;
	}
		#ふりがなを設定
		open(OUT,">pl/other_cfg.cgi");
			print OUT "\%EST_furi=(\n";
			foreach $key(sort keys %ganes){
				if($EST_furi{$key}){
					$EST_furi{$key}=&quote_str($EST_furi{$key});
					print OUT "\'$key\'=>\'$EST_furi{$key}\',\n";
				}
				else{
					local($ganes{$key})=$ganes{$key};
					$ganes{$key}=&quote_str($ganes{$key});
					print OUT "\'$key\'=>\'$ganes{$key}\',\n";
				}
			}
			print OUT ");\n1;\n";
		close(OUT);
	}
	
	if($FORM{mente_mode} eq "new"){
		#新規追加分を定義
		if($FORM{kt_new}){
		$FORM{kt_new}=~s/&gt;/>/g; $FORM{kt_new}=~s/&lt;/</g;
		@new=split(/\n/,$FORM{kt_new});
			foreach(@new){
				@kt=split(/<>/,$_);
				$ganes{$kt[0]}=$kt[1];
			}
		}
	}
	
	&sitemap_make;
	&cfg_set(0,1,0);
}

sub sitemap_make{
#(cfg6)サイトマップを作成(&sitemap_make)
open(OUT,">$EST{html_path}sitemap.html");
	select(OUT);
	require "$EST{temp_path}sitemap.html";
	select(stdout);
close(OUT);
}


sub cron{
#(cron1)cronコマンドによる定期処理(&cron)
&pass_check;
&go_TASK;
&mes("cronコマンドによる定期処理が完了しました","更新完了","java");
}

sub cron_make_kt{
#(cron1.1)通常カテゴリと特殊カテゴリを更新(&cron_make_kt)
#※&go_TASKから呼び出される(ロック範囲内)
local(@kt_list,@other_kt_list,$kt);

#更新するリストを格納
foreach $kt(keys %TASK){
	if($ganes{$kt}){push(@kt_list,$kt);} #通常カテゴリ
	else{push(@other_kt_list,$kt);} #特殊カテゴリ
}

##通常カテゴリを更新
if($#kt_list>=0){
	if(!$EST{html}){ #CGIでログ表示
		&MK_cgi(*kt_list);
	}
	else{ #HTMLでログ表示
		&MK_html(*kt_list);
	}
}

##特殊カテゴリを更新
if($#other_kt_list>=0){
	foreach $kt(@other_kt_list){
		local(@kt_list);
		@kt_list=($kt);
		&MK_cgi_other(*kt_list,$kt);
	}
}

%TASK=();



}



##-- 個別処理 --#

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
	if($_[2] eq "java"){
	$BACK_URL="<form><input type=button value=\"&nbsp;&nbsp;&nbsp;&nbsp;戻る&nbsp;&nbsp;&nbsp;&nbsp;\" onClick=\"history.back()\"></form>"
	}
	elsif($_[2] eq "env"){
	$BACK_URL="【<a href=\"$ENV{'HTTP_REFERER'}\">戻る</a>】";
	}
	elsif($_[2] eq "kanri"){
	$BACK_URL="<form action=\"$EST{admin}\" method=post><input type=hidden name=mode value=kanri><input type=hidden name=pass value=\"$FORM{pass}\"><input type=submit value=\"管理室へ\"></form>"
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
           $name=~tr/+/ /;
           $value =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
           $name =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
					 $value=~s/'/’/g;
if(!$arg1){
#   $value =~ s/>/&gt;/g;
#   $value =~ s/</&lt;/g;
   }
if(!$arg2){
   $value =~ s/\r//g;
   }
   				
           &jcode'convert(*value,'sjis');
           &jcode'convert(*name,'sjis'); $FORM{$name} = $value;
   }
}



sub form_to_temp{
#(t1)フォーム入力データを書き込みデータに反映(仮登録→正規登録用)
#   (&form_to_temp)
$temp_id=$Tlog[0];

#登録ID(0)
$Slog[0]=$Clog_id;

#タイトル(1)
$Slog[1]=$FORM{"Ftitle$temp_id"};

#URL(2)
$Slog[2]=$FORM{"Furl$temp_id"};

#マークデータ(3)
$Slog[3]="";
foreach(1 .. 2){ #←マーク数を増やす場合には修正
	if(!$FORM{"Fmark${_}_$temp_id"}){$FORM{"Fmark${_}_$temp_id"}=0;}
$Slog[3] .= $FORM{"Fmark${_}_$temp_id"} . "_";
}
$Slog[3]=substr($Slog[3],0,-1);

#更新日(4)
	#日時の取得
	$ENV{'TZ'} = "JST-9"; $times = time();
	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($times);
	$youbi = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat') [$wday];
$Slog[4]=&get_time(0,1);

#パスワード(5)
#(未変更)
$Slog[5]=$Tlog[5];

#紹介文(6)
$Slog[6]=$FORM{"Fsyoukai$temp_id"};
$Slog[6]=~s/\r//g; $Slog[6]=~s/\n/<br>/g;

#管理人コメント(7)
$Slog[7]=$FORM{"Fkanricom$temp_id"};
$Slog[7]=~s/\r//g; $Slog[7]=~s/\n/<br>/g;

#お名前(8)
$Slog[8]=$FORM{"Fname$temp_id"};

#E-Mail(9)
$Slog[9]=$FORM{"Femail$temp_id"};

#カテゴリ(10)
$Slog[10]="";
foreach(1 .. $EST_reg{kt_max}){
	$Slog[10] .= $FORM{"F${temp_id}kt$_"} . "&";
}
$Slog[10]=substr($Slog[10],0,-1);

#time形式(11)
$Slog[11]= time() . "_0";

#バナーURL(12)
$Slog[12]=$FORM{"Fbana_url$temp_id"};

#アクセス数(13)
$Slog[13]="0_0_0_0";

#最終アクセスIP(14)
$Slog[14]="";

#キーワード(15)
$Slog[15]=$FORM{"Fkey$temp_id"};

##その他
$Clog_id++; #次のデータのために+1

}

#(t2)symlink関数の使用可否のチェック(&check_symlink)
sub check_symlink{
local($check_fl);
	eval{symlink("","");};
	if($@){$check_fl=0;}
	else{$check_fl=1;}
return $check_fl;
}

#(t3)登録数を再計算
sub count_log{
local($total_url=0);
open(IN,"$EST{log_path}$EST{logfile}");
	while(<IN>){
		$total_url++;
	}
close(IN);
open(OUT,">$EST{log_path}total_url.log");
	print OUT $total_url;
close(OUT);
}

#(t4)メタ文字をクオート
sub quote_str{
	my $ret=shift;
	if(substr($ret,-1,1) eq "\\"){$ret.="\\";}
	return $ret;
}

##-- end of temp.cgi --##
