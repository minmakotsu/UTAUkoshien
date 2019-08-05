#!/usr/bin/perl

#↑perlのパスを自分の環境に合わせて書き直します。
#大抵は、「#!/usr/bin/perl」　か　「#!/usr/local/bin/perl」です。
#解らない場合はサーバー管理者(もしくはプロバイダー)に
#確認してください。

require 'pl/jcode.pl';
require 'pl/cfg.cgi';
require 'pl/temp.cgi';

##目次##
#(1)人気(OUT)ランキング表示画面(&PR_rank)
#(1.1)アクセス(IN)ランキング表示画面(&PR_rev)
#(1.1.1)アクセスランキングを更新(&make_rev)
#(1.1.2)累計人気ランキングを更新(&make_rank_rui)
#(2)リンクジャンプ処理(&link)
#(2.1)アクセスジャンプ処理(&r_link)
#(3)キーワードランキング表示画面(&PR_keyrank)

$rank_flag = 1; #ランキング実行フラグ

&form_decode();
	if(!$FORM{page}){$FORM{page}=1;}
if($FORM{mode} eq "link"){&link;}
elsif($FORM{mode} eq "r_link"){&r_link;}
elsif($FORM{mode} eq "keyrank"){&PR_keyrank;}
elsif($FORM{mode} eq "rev" || $FORM{mode} eq "rev_bf" || $FORM{mode} eq "rev_rui"){&PR_rev;}
else{&PR_rank;} #人気ランキング
exit;

sub PR_rank{
#(1)人気ランキング表示画面(&PR_rank)
if(!$EST{rank_fl}){&mes("人気ランキングは実施しない設定になっています","エラー","java");}
if(!$FORM{mode}){$FORM{mode}="rank";}
	require "$EST{temp_path}rank.html";

	print "Content-type: text/html\n\n";
	&print_rank($FORM{kt},$FORM{mode},$FORM{page});
}

sub PR_rev{
#(1.1)アクセス(IN)ランキング表示画面(&PR_rev)
if(!$EST{rev_fl}){&mes("アクセスランキングは実施しない設定になっています","エラー","java");}
	require "$EST{temp_path}rev_rank.html";

	print "Content-type: text/html\n\n";
	&print_rank($FORM{kt},$FORM{mode},$FORM{page});
}

sub make_rev{
#(1.1.1)アクセスランキングを更新(&make_rev)
#$arg[0]=> 現在のランキングを更新(rev)/累計ランキングを更新(rev_rui)/初期化(format)
	##現在のランキングを更新&本体ファイルに反映(rev)
	if($_[0] eq "rev"){
		close(IN);
		&lock(); #ロック
		@log_lines=();
		local(@rank,%pt,%time_fl,$day=0,$st,@Slog,$line,%line,$i=0);
		open(IN,"$EST{log_path}rev_temp.cgi");
			while(<IN>){
				chop;
				@rank=split(/<>/,$_); #ID<>time形式<>IP\n
				if(!$day){$st=$rank[1];}
				if($st-$rank[1]>3600*$EST{rank_time}){$st=$rank[1];%time_fl=();}
				if(!$time_fl{"$rank[0]_$rank[2]"}){$pt{$rank[0]}++;}
				$time_fl{"$rank[0]_$rank[2]"}=1;
			}
		close(IN);
		undef %time_fl;
		
		open(OUT,">$EST{log_path}rev_temp.cgi");
		close(OUT);
		
		open(IN,"$EST{log_path}$EST{logfile}");
			while($line=<IN>){
				@Slog=split(/<>/,$line);
				local(@pt); @pt=split(/_/,$Slog[13]);
				if($pt{$Slog[0]}){
					$pt[2]+=$pt{$Slog[0]};
					$pt[3]+=$pt{$Slog[0]};
					$Slog[13]=join("_",@pt);
					$line=join("<>",@Slog);
				}
				$line{$i}=$pt[2];
				push(@log_lines,$line);
				$i++;
			}
		close(IN);

		$i=1;
		open(OUT,">$EST{log_path}rev_ys.cgi");
		print OUT time() . "_" . $last_time[1] . "\n";
		foreach $line(sort{$line{$b} <=> $line{$a}} keys %line){
			if($i<=$EST{rev_best} && $line{$line}>=$EST{rev_min}){print OUT $log_lines[$line];}
			else{last;}
			$i++;
		}
		close(OUT);
		
		open(OUT,">$EST{log_path}$EST{logfile}");
			print OUT @log_lines;
		close(OUT);
		@log_lines=();
		
		$i=1;
		open(IN,"$EST{log_path}rev_ys.cgi");
				$last_time=<IN>;
				while(<IN>){
				@Slog=split(/<>/,$_);
				local(@pt,$kt_fl=0,$pt,$kt);
				@pt=split(/_/,$Slog[13]); $pt=$pt[2];
					if(!$LC_kt){$kt_fl=1;} #カテゴリ指定なし
					else{
						local(@kt); @kt=split(/&/,$Slog[10]);
						foreach $kt(@kt){
							if($kt eq $LC_kt){$kt_fl=1; last;}
						}
					}
				if($kt_fl){
					if($pt ne $bf_pt){$rank=$rank_z;}
					if($str_no<=$i && $i<=$end_no){
						if($pre_pt_fl){$pre_pt=$bf_pt; $pre_rank=$rank; $pre_rank_z=$rank_z; $pre_pt_fl=0;}
						push(@log_lines,$_);
					}
					$i++;$Clog++;
					$rank_z++;
					$bf_pt=$pt;
				}
				}
		close(IN);
		
		&unlock(); #ロック解除
	}
	##累計のランキングを更新(rev_rui)
	elsif($_[0] eq "rev_rui"){
		close(IN);
		&lock_rev(); #ロック
		@log_lines=();
		local(@rank,%pt,%time_fl,$day=0,$st,@Slog,$line,%line,$i=0);
		
		open(IN,"$EST{log_path}$EST{logfile}");
			while($line=<IN>){
				@Slog=split(/<>/,$line);
				local(@pt); @pt=split(/_/,$Slog[13]);
				$line{$i}=$pt[3];
				push(@log_lines,$line);
				$i++;
			}
		close(IN);

		$i=1;
		open(OUT,">$EST{log_path}rev_rui.cgi");
		print OUT time() . "\n";
		foreach $line(sort{$line{$b} <=> $line{$a}} keys %line){
			if($i<=$EST{rev_best} && $line{$line}>=$EST{rev_min}){print OUT $log_lines[$line];}
			else{last;}
			$i++;
		}
		close(OUT);
		
		@log_lines=();
		
		$i=1;
		open(IN,"$EST{log_path}rev_rui.cgi");
				$last_time=<IN>;
				while(<IN>){
				@Slog=split(/<>/,$_);
				local(@pt,$kt_fl=0,$pt,$kt);
				@pt=split(/_/,$Slog[13]); $pt=$pt[3];
					if(!$LC_kt){$kt_fl=1;} #カテゴリ指定なし
					else{
						local(@kt); @kt=split(/&/,$Slog[10]);
						foreach $kt(@kt){
							if($kt eq $LC_kt){$kt_fl=1; last;}
						}
					}
				if($kt_fl){
					if($pt ne $bf_pt){$rank=$rank_z;}
					if($str_no<=$i && $i<=$end_no){
						if($pre_pt_fl){$pre_pt=$bf_pt; $pre_rank=$rank; $pre_rank_z=$rank_z; $pre_pt_fl=0;}
						push(@log_lines,$_);
					}
					$i++;$Clog++;
					$rank_z++;
					$bf_pt=$pt;
				}
				}
		close(IN);
		
		&unlock_rev(); #ロック解除
	}
	##初期化(format)
	elsif($_[0] eq "format"){
		close(IN);
		&lock(); #ロック
		open(IN,"$EST{log_path}rev_ys.cgi");
		open(OUT,">$EST{log_path}rev_bf.cgi");
			$last_time=<IN>; @last_time=split(/_/,$last_time);
			while(<IN>){
				print OUT $_;
			}
		close(OUT);
		close(IN);
		open(OUT,">$EST{log_path}rev_ys.cgi");
		print OUT $last_time[0] . "_" . time() . "\n";
		close(OUT);
		
		#本体ログを初期化
		@log_lines=(); local($line);
		open(IN,"$EST{log_path}$EST{logfile}");
			while($line=<IN>){
			@Slog=split(/<>/,$line);
			@pt=split(/_/,$Slog[13]);
			if($pt[2]){
			$pt[2]=0;
			$Slog[13]=join("_",@pt);
			$line=join("<>",@Slog);
			}
			push(@log_lines,$line);
			}
		close(IN);
		open(OUT,">$EST{log_path}$EST{logfile}");
		print OUT @log_lines;
		close(OUT);
		@log_lines=();
		
		&unlock(); #ロック解除
	}
	else{&mes("&make_revの引数が不正です","エラー","java");}



}

sub make_rank_rui{
#(1.1.2)累計人気ランキングを更新(&make_rank_rui)
	close(IN);
		&lock_rev(); #ロック
		@log_lines=();
		local(@rank,%pt,%time_fl,$day=0,$st,@Slog,$line,%line,$i=0);
		
		open(IN,"$EST{log_path}$EST{logfile}");
			while($line=<IN>){
				@Slog=split(/<>/,$line);
				local(@pt); @pt=split(/_/,$Slog[13]);
				$line{$i}=$pt[1];
				push(@log_lines,$line);
				$i++;
			}
		close(IN);

		$i=1;
		open(OUT,">$EST{log_path}rank_rui.cgi");
		print OUT time() . "\n";
		foreach $line(sort{$line{$b} <=> $line{$a}} keys %line){
			if($i<=$EST{rank_best} && $line{$line}>=$EST{rank_min}){print OUT $log_lines[$line];}
			else{last;}
			$i++;
		}
		close(OUT);
		
		@log_lines=();
		
		$i=1;
		open(IN,"$EST{log_path}rank_rui.cgi");
				$last_time=<IN>;
				while(<IN>){
				@Slog=split(/<>/,$_);
				local(@pt,$kt_fl=0,$pt,$kt);
				@pt=split(/_/,$Slog[13]); $pt=$pt[1];
					if(!$LC_kt){$kt_fl=1;} #カテゴリ指定なし
					else{
						local(@kt); @kt=split(/&/,$Slog[10]);
						foreach $kt(@kt){
							if($kt eq $LC_kt){$kt_fl=1; last;}
						}
					}
				if($kt_fl){
					if($pt ne $bf_pt){$rank=$rank_z;}
					if($str_no<=$i && $i<=$end_no){
						if($pre_pt_fl){$pre_pt=$bf_pt; $pre_rank=$rank; $pre_rank_z=$rank_z; $pre_pt_fl=0;}
						push(@log_lines,$_);
					}
					$i++;$Clog++;
					$rank_z++;
					$bf_pt=$pt;
				}
				}
		close(IN);
		
		&unlock_rev(); #ロック解除

}

sub link{
#(2)リンクジャンプ処理(&link)
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

sub r_link{
#(2.1)アクセスジャンプ処理(&r_link)
if($EST{rev_fl}){
$FORM{id}=~s/\D//g;
if($FORM{id}){
	local($fl=0,@ref_list);
		$FORM{id}=~s/\n//g;
		&lock_rev();
		open(OUT,">>$EST{log_path}rev_temp.cgi");
			print OUT "$FORM{id}<>" . time() . "<>$ENV{'REMOTE_ADDR'}\n";
		close(OUT);
		&unlock_rev();
}
}
$EST{location}=0; #refreshジャンプにする
&location($EST{rev_url});
}

#(3)キーワードランキング表示画面(&PR_keyrank)
sub PR_keyrank{
require "$EST{log_path}task_ys.cgi";
print "Content-type: text/html\n\n";
require "$EST{temp_path}keyrank.html";
&print_keyrank;
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






