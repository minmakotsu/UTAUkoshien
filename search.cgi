#!/usr/bin/perl

#��perl�̃p�X�������̊��ɍ��킹�ď��������܂��B
#���́A�u#!/usr/bin/perl�v�@���@�u#!/usr/local/bin/perl�v�ł��B
#����Ȃ��ꍇ�̓T�[�o�[�Ǘ���(�������̓v���o�C�_�[)��
#�m�F���Ă��������B

require 'pl/jcode.pl';
require 'pl/cfg.cgi';
require 'pl/temp.cgi';

##�ڎ�##
#(1)�������ʕ\�����(&search)
#(2)�ڍ׌������(&search_ex)
#(3)�O�������N���(&meta)
#(4)���������p�f�[�^���n�b�V���ɓ����(&open_for_search)
#(5)�O�������G���W���ւ̃����N�ꗗ��\��(&PR_mata_page)
#(6)�L�[���[�h���ꎞ�����L���O�t�@�C��(keyrank_temp.cgi)�ɋL�^(&set_word)

##�e���v���[�g�t�@�C��
#�������ʉ��=>temp/search.html
#�ڍ׌������=>temp/search_ex.html
#�O�������N���=>temp/search_meta.html

#�y�J�e�S�������z
##[�I�v�V����]
#�J�e�S���w��([kt]&[option(b_all=�ȉ�)])
#���t�w��=>( today-x | year/mon/day | [str_day]-[end_day] )
#�V�K�E�B���h�E=>window=new

&form_decode();
	if(!$FORM{page}){$FORM{page}=1;}
if($FORM{mode} eq "search"){&search;} #�������ʕ\�����
elsif($FORM{mode} eq "meta"){&meta;} #�O�������N���
else{&search_ex;} #�ڍ׌������
exit;

sub search{
#(1)�������ʕ\�����(&search)
local(@words_a,@words_o,@words_n,$w_line,@words,$word,@kt_search_list);

	#�����I�v�V�������N�b�L�[�ɋL�^
		#�I�v�V����
		#[0]=>��������(a|o)/[1]=>�������̎g�p�L��(0|1)/[2]=>�����G���W����(ID)/
		#[3]=>�����G���W����(�\����)/[4]=>www.(0|1)/[5]=>�J�e�S���w��(ID)
		#[6]=>�J�e�S���w��(�\����)/[7]=>�w��J�e�S��(0|1)/[8]=>���t�w��(data)
		#[9]=>���t�w��(�\����)/[10]=>���t�w��R�}���h(data)/[11]=>�J�e�S��������(0|1)
	if($FORM{set_option} eq "on"){
		&get_cookie;
		local(@cookie_lines);
		if($FORM{method} eq "and"){$cookie_lines[0]="a";} #[0]
		else{$cookie_lines[0]="o";}
		if($FORM{use_str} eq "on"){$cookie_lines[1]="1";} #[1]
		else{$cookie_lines[1]="0";}
		$cookie_lines[2]=$FORM{engine}; #[2]
		if($FORM{engine} eq "pre"){$cookie_lines[3]="$EST{search_name}��";} #[3]
		else{
		open(IN,"pl/cfg.cgi");
			local($i=0);
			while(<IN>){
				if($_ eq "sub search_form{\n"){$i=1;}
				if($i){
					if(/<option value="$FORM{engine}">(.+)��/o){$cookie_lines[3]=$1; last;}
				}
			}
		close(IN);
		}
		$cookie_lines[3]=~s/,/�C/g;
		if($FORM{www} eq "on"){$cookie_lines[4]="0";} #[4]
		else{$cookie_lines[4]="1";}
		$cookie_lines[5]=$FORM{search_kt}; #[5]
		if($FORM{search_kt}){$cookie_lines[6]=&full_kt($FORM{search_kt});} #[6]
		else{$cookie_lines[6]="�w�肵�Ȃ�";}
		if($FORM{search_kt_ex} ne "-b_all"){$cookie_lines[7]=0;} #[7]
		else{$cookie_lines[7]=1;}
		$cookie_lines[8]=$FORM{search_day}; #[8]
		if($FORM{search_day} eq "today"){$cookie_lines[9]="�{��";} #[9]
		elsif($FORM{search_day}=~/^(\d+)-/){$cookie_lines[9]= $1 . "���ȓ�";}
		else{$cookie_lines[9]="�w�肵�Ȃ�";}
		$cookie_lines[10]=$FORM{search_day_ex}; #[10]
		$cookie_lines[10]=~s/,/�C/g;
		if($FORM{kt_search} eq "on"){$cookie_lines[11]=0;} #[11]
		else{$cookie_lines[11]=1;}
		
		$CK_data[5]=join(",",@cookie_lines);
		$CK_data[5]=~s/;//g;
		&set_cookie;
	}

	#���͒l�̐��`
	if(!$FORM{engine}){$FORM{engine}="pre";}
	if($FORM{page}=~/\D/){&mes("�y�[�W�w��l���s���ł�","�y�[�W�w��G���[","java");}
	if(!$FORM{sort}){$FORM{sort}=$EST{defo_hyouji};}
	if($FORM{search_kt_ex}){$FORM{search_kt}=$FORM{search_kt} . $FORM{search_kt_ex};}
	if($FORM{search_day_ex}){$FORM{search_day}=$FORM{search_day_ex};}
	if($FORM{kn}>0 && $FORM{kn}<=20){ #�L�[���[�h�̌���
		if($FORM{kn}=~/\D/){&mes("\$FORM{kn}���s���ł�","�G���[","java");}
		foreach(1 .. $FORM{kn}){
			if($FORM{"word$_"}){$FORM{word} .= $FORM{"word$_"} . " ";}
		}
	}
	if(!$FORM{hyouji}){$FORM{hyouji}=$EST{hyouji};}
	
	if($EST{keyrank} && $FORM{page}==1){ #�L�[���[�h�����L���O�p�̃f�[�^���擾
		&set_word;
	}
	


	#�����\���̉��
	$w_line=$FORM{word};
	$w_line=~ s/�@/ /g;
	$FORM{word}=$w_line;
	$w_line=~tr/[A-Z]/[a-z]/;
	if($FORM{use_str} eq "on"){ #���������g��
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
	else{ #���������g��Ȃ�
		if($FORM{method} ne "or"){ @words_a=split(/ /,$w_line);}
		else{@words_o=split(/ /,$w_line);}
	}

	#�O�������֕���
		if($FORM{engine} ne "pre"){
			$FORM{target}=$FORM{window};
			require "pl/meta_ys.cgi";
			&meta("select");
		}
		
	if(!$FORM{word} && !$FORM{search_day}){ #�L�[���[�h�E���t�w��̗��������w��̂Ƃ�
		&mes("<b>�L�[���[�h</b>��<b>���t�w��</b>�̂����ꂩ�͕K���w�肵�Ă�������","�L���~�X","java");
	}
	if(!$FORM{word}){$FORM{kt_search}="off";}

 	##��������
	#�J�e�S������
	if($FORM{kt_search} ne "off"){
		local($kt,$kt_name,$kt_fl);
		
		foreach $kt(sort keys %ganes){
			$kt_fl=1;
			$kt_name=$ganes{$kt};
			$kt_name=~tr/[A-Z]/[a-z]/;
			
			foreach $word(@words_a){ #and����
				if(index($kt_name,$word)<0){$kt_fl=0; last;}
			}
			
			foreach $word(@words_o){ #or����
				$kt_fl=0;
				if(index($kt_name,$word)>=0){$kt_fl=1; last;}
			}
			
			foreach $word(@words_n){ #not����
				if(index($kt_name,$word)>=0){$kt_fl=0; last;}
			}
			
			if($kt_fl){push(@kt_search_list,$kt);}
		}
	}
	

	#���ʕ\��
	require "$EST{temp_path}search.html";

	print "Content-type: text/html\n\n";
	&print_search($FORM{word},$FORM{engine},$FORM{mode},$FORM{page},$FORM{sort},$FORM{search_kt},$FORM{search_day},$FORM{use_str},$FORM{method});

}

sub search_ex{
#(2)�ڍ׌������(&search_ex)

print "Content-type: text/html\n\n";
require "$EST{temp_path}search_ex.html";

}

sub meta{
#(3)�O�������N���(&meta)
	if($EST{keyrank} && $FORM{page}==1){ #�L�[���[�h�����L���O�p�̃f�[�^���擾
		&set_word;
	}
require "pl/meta_ys.cgi";
print "Content-type: text/html\n\n";
require "$EST{temp_path}search_meta.html";

}

sub open_for_search{
#(4)���������p�f�[�^���n�b�V���ɓ����(&open_for_search)
#�ΏۑS�z���@write�ɓ����
#$arg1=>�J�e�S���w��([kt]-[option(b_all=�ȉ�)])
#$arg2=>���t�w��=>( today-x | year/mon/day | [str_day]-[end_day]_[option(re)] )
#$arg3=>�\�[�g���@(id/time/ac/mark)
local($target_kt=$_[0],$target_day=$_[1],$sort=$_[2],
$eval_line,$oya_kt,$target_kt1,$target_kt2,
$line,$s_line,@Slog,@kt,$kt,$fl,$word,$i=0);
($sort)=split(/_/,$sort);


	##�����p$eval_line���쐬
		#while�J�n
$eval_line .=<<'EOM';
		while($line=<IN>){
			$fl=1;
			$s_line=$line;
			$s_line=~tr/[A-Z]/[a-z]/;
			@Slog=split(/<>/,$line);
EOM

	#�J�e�S���w�蕔��
	if($target_kt){
		($target_kt1,$target_kt2)=split(/-/,$target_kt);
		($oya_kt)=split(/_/,$target_kt1);
		if(!$ganes{$oya_kt}){&mes("�J�e�S���w�肪�s���ł�","�J�e�S���w��G���[","java");}
		
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
	#���[�h��������
	if($#words_a>=0){ #and����
$eval_line .=<<'EOM';
	if($fl){
	foreach $word(@words_a){
		if(index($s_line,$word) < 0){$fl=0; last;}
	}
	}
EOM
	}
	if($#words_o>=0){ #or����
$eval_line .=<<'EOM';
	if($fl){
	$fl=0;
	foreach $word(@words_o){
		if(index($s_line,$word) >= 0){$fl=1; last;}
	}
	}
EOM
	}
	if($#words_n>=0){ #not����
$eval_line .=<<'EOM';
	if($fl){
	foreach $word(@words_n){
		if(index($s_line,$word) >= 0){$fl=0; last;}
	}
	}
EOM
	}
	#���t��������
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
		else{&mes("���t�w��̃R�}���h������������܂���","�G���[","java");}
	}
	#�f�[�^�i�[����
	$eval_line .='if($fl){$line{$i}='; 
		if($sort eq "id"){$eval_line .='$Slog[0]';}
		elsif($sort eq "time"){$eval_line .='(split(/_/,$Slog[11]))[0]';}
		elsif($sort eq "ac"){$eval_line .='$Slog[1]';}
		else{$eval_line .='$Slog[3]';} #mark
	$eval_line .='; push(@write,$line); $i++;}';

$eval_line .='}';

	##�����������s
	if(!$EST{html} && $target_kt){open(IN,"$EST{log_path}$oya_kt.cgi") || &mes("�t�@�C�����J���܂���ł���","�t�@�C�����J���܂���","java");}
	else{open(IN,"$EST{log_path}$EST{logfile}");}
	

			eval $eval_line;
		

	close(IN);
#&mes("$eval_line");
	if($#write<0){$i=0;}

	return $i;
}

sub PR_meta_page{
#(5)�O�������G���W���ւ̃����N�ꗗ��\��(&PR_mata_page)
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
#(6)�L�[���[�h���ꎞ�����L���O�t�@�C��(keyrank_temp.cgi)�ɋL�^(&set_word)
	local(@keyword,$keyword=$FORM{word});
	$keyword=~s/'/�f/g;
	if(length($keyword)<50){
	$keyword=~s/�@/ /g;
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

#(t1)���b�Z�[�W��ʏo��(&mes)
#����:&mes($arg1,$arg2,$arg3);
#�@�\:���b�Z�[�W��ʂ��o�͂���
#����:$arg1=>�\�����郁�b�Z�[�W
#     $arg2=>�y�[�W�̃^�C�g��(�ȗ����́u���b�Z�[�W��ʁv)
#     $arg3=>�EJavaScript�ɂ��u�߂�v�{�^���\��=java
#            �E$ENV{'HTTP_REFERER'}���g���ꍇ=env
#            �E�Ǘ����ւ̃{�^��=kanri
#            �E�ʏ��URL���̓p�X���w�肷��ꍇ�ɂ͂���URL���̓p�X���L��
#            �E�ȗ����͔�\��
#     $arg4=>���b�N����=unlock
#�߂�l:�Ȃ�
sub mes{
local($MES,$Munlock,$BACK_URL,);
print "Content-type: text/html\n\n";
$Munlock=$_[3];
	if($Munlock eq "unlock"){&unlock();}
$MES=$_[0];
		if($_[1]){$TITLE=$_[1];}
		else{$TITLE="���b�Z�[�W���";}
	if($_[2] eq "java"){
	$BACK_URL="<form><input type=button value=\"&nbsp;&nbsp;&nbsp;&nbsp;�߂�&nbsp;&nbsp;&nbsp;&nbsp;\" onClick=\"history.back()\"></form>"
	}
	elsif($_[2] eq "env"){
	$BACK_URL="�y<a href=\"$ENV{'HTTP_REFERER'}\">�߂�</a>�z";
	}
	elsif(!$_[2]){$BACK_URL="";}
	else{$BACK_URL="�y<a href=\"$_[2]\">�߂�</a>�z";}

require "$EST{temp_path}mes.html";

exit;
}


#(7)�t�H�[���f�[�^�̃f�R�[�h(&form_decode)
#����:&form_decode($arg1,$arg2);
#�@�\:�t�H�[���f�[�^���f�R�[�h����
#����:$arg1=>�u>�v�Ɓu<�v���i�����ɂ���(�ȗ���)=0/�L���ɂ���=1�j
#     $arg2=>�u\n�v�Ɓu\r�v���i�����ɂ���(�ȗ���)=0/�L���ɂ���=1�j
#�߂�l:�Ȃ�
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






