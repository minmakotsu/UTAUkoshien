#!/usr/bin/perl

#��perl�̃p�X�������̊��ɍ��킹�ď��������܂��B
#���́A�u#!/usr/bin/perl�v�@���@�u#!/usr/local/bin/perl�v�ł��B
#����Ȃ��ꍇ�̓T�[�o�[�Ǘ���(�������̓v���o�C�_�[)��
#�m�F���Ă��������B

require 'pl/jcode.pl';
require 'pl/cfg.cgi';
&EST_reg;
require 'pl/temp.cgi';

################################################################
# Yomi-Search�p�f�[�^�o�^�p�v���O����
################################################################
#(1)�o�^���(�V�K�o�^�E�Ǘ��l�㗝�o�^�E�o�^���e�ύX)(&regist)
#(2)�v���r���[���(&preview)
#(3)���͓��e�̐��`(&join_fld)
#(4)���͓��e�̃`�F�b�N(&check)
#(5)�o�^���ʉ�ʏo��(&PRend)
#(6)�C���E�폜�̂��߂̃p�X���[�h�F��(&enter)
#(7)�w���v�̕\��(&help)
#(8)�p�X���[�h�̍Ĕ��s�E�ύX(&act_repass)
#(9)�����N�؂�񍐃t�H�[��(&no_link)

#(p1)�V�K�o�^���s(&act_regist)
#(p2)�o�^���e�ύX(&act_mente)
#(p3)�폜���s(&act_del)

&form_decode;
$Eref=$ENV{'HTTP_REFERER'};
$ENV{'HTTP_REFERER'}="";
#-----------------#
if($FORM{'preview'} eq "on"){&preview;} #�v���r���[���
elsif($FORM{mode} eq "regist"){&regist;} #�o�^���
elsif($FORM{mode} eq "act_regist"){&act_regist;} #�V�K�o�^���s
elsif($FORM{mode} eq "act_mente"){&act_mente;} #�o�^���e�ύX���s
elsif($FORM{mode} eq "act_del"){&act_del;} #�폜���s
elsif($FORM{mode} eq "enter"){&enter;} #�p�X���[�h�F��
elsif($FORM{mode} eq "help"){&help;} #�w���v�̕\��
elsif($FORM{mode} eq "act_repass"){&act_repass;} #�p�X���[�h�̍Ĕ��s
elsif($FORM{mode} eq "no_link"){&no_link;} #�����N�؂�񍐃t�H�[��
else{&regist;} #�o�^���
exit;
#-----------------#

sub regist{
#(1)�o�^���(�V�K�o�^�E�Ǘ��l�㗝�o�^�E�o�^���e�ύX)(&regist)

#�N�b�L�[���L�^
if($FORM{'in_mode'} eq "mente"){ #�o�^���e�ύX��
	&get_cookie;

	if($FORM{changer} ne "admin" && $FORM{pass}){$CK_data[0]=$FORM{pass};} #�o�^�҃p�X���[�h
	$CK_data[1]=$FORM{id}; #ID
	if($FORM{changer} eq "admin"){$CK_data[2]="admin";} #�ύX��
	if($FORM{changer} eq "admin" && $FORM{pass}){$CK_data[3]=$FORM{pass};} #�Ǘ��҃p�X���[�h
	
	if($FORM{cookie} eq "off"){&set_fo_cookie;}
	else{&set_cookie;}
}

#�p�X���[�h�F��(�Ǘ��ҔF��)
if($FORM{'changer'} eq "admin"){
local($cr_pass);
	if($EST{crypt}){$cr_pass=crypt($FORM{pass},$EST{pass});}
	else{$cr_pass=$FORM{pass};}
	if($cr_pass ne $EST{pass}){
		if(!$ENV{'REMOTE_HOST'}){$ENV{'REMOTE_HOST'}=gethostbyaddr(pack("C4", split(/\./, $ENV{'REMOTE_ADDR'})), 2);}
		&mes("�p�X���[�h�̔F�؂Ɏ��s���܂���<br>�F�؂����R���s���[�^��IP�A�h���X�F<b>$ENV{'REMOTE_ADDR'}</b><br>�F�؂����R���s���[�^�̃z�X�g���F<b>$ENV{'REMOTE_HOST'}</b>","�p�X���[�h�F�؎��s","java");
	}
}

#�Ǘ��l�݂̂��o�^�ł��郂�[�h
if($EST_reg{no_regist} && $FORM{in_mode} ne "mente" && $FORM{changer} ne "admin"){
	&mes("���݁A�K��҂ɂ��V�K�o�^�͒�~����Ă��܂�","�G���[","java");
}

# �e�t�B�[���h�̃f�[�^���u$P�`�v�ɓ���
#$Pdata[0]=�f�[�^ID,$Pdata[1]=�^�C�g��,$Pdata[2]=�z�[���y�[�W��URL,$Pdata[3]=�}�[�N�f�[�^
#$Pdata[4]=�X�V��,$Pdata[5]=�p�X���[�h,$Pdata[6]=�Љ,$Pdata[7]=�Ǘ��l�R�����g
#$Pdata[8]=�����O,$Pdata[9]=���[���A�h���X,$Pdata[10]=�J�e�S��(���X�g),$Pdata[11]=time
#$Pdata[12]=�o�i�[URL,$Pdata[13]=�A�N�Z�X��,$Pdata[14]=IP,$Pdata[15]=�L�[���[�h
# $Pmode=>���M��̃��[�h
# $FORM{'in_mode'}=>�T���͒l�ݒ胂�[�h(�Ȃ�,new_dairi,mente,form)
# $Smode_name=>�e���[�h�̔���p�̓����ϐ�(�Ȃ�,new_dairi,mente)
# $$FORM{'changer'}=>�ύX��(�Ȃ�,admin)

##�T���͒l�ݒ�($FORM{'in_mode'})
#�V�K�o�^()
if(!$FORM{'in_mode'}){@Pdata=("","","http://","","","","","","","",$FORM{'kt'},"","http://","","","");}
#�Ǘ��l�㗝�o�^(new_dairi)
elsif($FORM{'in_mode'} eq "new_dairi"){}
#���e�ύX(mente)
elsif($FORM{'in_mode'} eq "mente"){
local($cr_pass,$i=0);
	open(IN,"$EST{log_path}$EST{logfile}");
		while(<IN>){
			@Pdata=split(/<>/,$_);
			if($Pdata[0] eq $FORM{id}){
				if($EST{crypt}){$cr_pass=crypt($FORM{pass},$Pdata[5]);}
				else{$cr_pass=$FORM{pass};}
				if($FORM{changer} ne "admin" && $Pdata[5] ne $cr_pass){&mes("�p�X���[�h���Ⴂ�܂�","�p�X���[�h�F�؃G���[","java");}
				$i=1;
				last;
			}
		}
	close(IN);
	if(!$i){&mes("�Y������f�[�^�͂���܂���","�G���[","java");}
}
#�O������(form)
elsif($FORM{'in_mode'} eq "form"){
	$FORM{'Fkt'}="";
	foreach $kt_no(1 .. $EST_reg{kt_max}){
		$FORM{'Fkt'} .= $FORM{"Fkt$kt_no"} . "&";
	}
	@Pdata=("",$FORM{'Ftitle'},$FORM{'Furl'},"","",$FORM{'Fpass'},$FORM{'Fsyoukai'},"",$FORM{'Fname'},$FORM{'Femail'},$FORM{'Fkt'},"",$FORM{'Fbana_url'},"","",$FORM{'Fkey'});
}
else{@Pdata=();}

##$Smode_name�̐ݒ�
#�Ǘ��l�㗝�o�^
if($FORM{'changer'} eq "admin" && $FORM{'in_mode'} ne "mente"){$Smode_name="new_dairi";}
#�o�^���e�ύX
elsif($FORM{'in_mode'} eq "mente"){$Smode_name="mente";}
#�o�^�҂̐V�K�o�^
else{$Smode_name="";}

##$Pmode�̐ݒ�
#�o�^���e�ύX
if($FORM{'Smode_name'} eq "mente"){
	$Pmode="act_mente";
}
#�V�K�o�^
else{
	$Pmode="act_regist";
}

##���̑��̐ݒ�
#���݃����N�̗L��
$MES_sougo{1}=" checked"; $MES_sougo{0}="";



#�e���v���[�g�̓ǂݍ���
if($Smode_name eq "new_dairi"){
print "Content-type: text/html\n\n";
require "$EST{temp_path}regist_new_admin.html";
}
elsif($FORM{'changer'} ne "admin" && $Smode_name eq "mente"){
	if($EST{syoukai_br}){
		$Pdata[6]=~s/<br>/\n/g; $Pdata[7]=~s/<br>/\n/g;
	}
	if($EST_reg{no_mente}){&mes("���݁A�o�^�҂ɂ��C���E�폜�͒�~����Ă��܂�","�G���[","java");}
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
##�}�[�N
if($FORM{'changer'} eq "admin"){
local(@mark); @mark=split(/_/,$Pdata[3]);
print<<"EOM";
	<li>�y�}�[�N�z
		<ul>
EOM
foreach(1 .. 2){ #���}�[�N���𑝂₷�Ƃ��͏C��
		print "<input type=checkbox name=Fmark$_ value=1";
			if($mark[$_-1]){print " checked";}
		print ">" . $EST{"name_m$_"} . "�@ ";
}
print<<"EOM";
		</ul><br>
EOM
}
}


sub PR_kt{
##�o�^����J�e�S����\��(&PR_kt)

print<<"EOM";
EOM

 local($PRbf_kt,@kt_list,@kt,$kt_no=1,$line,@Pkt,$PRselect=" selected");
@Pkt=split(/&/,$Pdata[10]);

	if($EST_reg{kt_min} ne $EST_reg{kt_max}){print "<ul>��<b>$EST_reg{kt_min}</b>�`<b>$EST_reg{kt_max}</b>�܂őI���ł��܂�<br>";}
	else{print "<ul>��<b>$EST_reg{kt_max}</b>�I�����Ă�������<br>";}
print<<"EOM";
		���e�J�e�S���̏ڍׂ́u<a href="$EST{html_path_url}sitemap.html">�J�e�S���ꗗ</a>�v���Q�l�ɂ��Ă�������<br>
EOM
&gane_st; #�W�������X�e�[�^�X�����[�h
@kt_list=sort keys(%ganes);
foreach $kt_no(1 .. $EST_reg{kt_max}){
$PRselect=" selected";
print<<"EOM";
		<select name=Fkt$kt_no size=7>
EOM

if($Pkt[$kt_no-1]){print "<option value=\"" . $Pkt[$kt_no-1] . "\"$PRselect>" . &full_kt($Pkt[$kt_no-1]) . "\n"; $PRselect="";}
print<<"EOM";
			<option value=""$PRselect>--�w�肵�Ȃ�--
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
#���쌠�\��(�폜�E�ύX�����Ȃ��ł��������B�������A���񂹁E���񂹂͉�)

print<<"EOM";
<p><div align=center>- <a href="http://yomi.pekori.to" target="_blank">Yomi-Search</a> -</div></p>
EOM
}

sub preview{
#(2)�v���r���[���(&preview)
#���o�^�҂̐V�K�o�^���ɂ̂ݎg�p
&check("url_no_check");

##���̑��̐ݒ�
#���݃����N�̗L��
$MES_sougo{1}=" checked"; $MES_sougo{0}="";

	#�Љ�̉��s��ϊ�(<br>��\n)
	$FORM{Fsyoukai}=~s/<br>/\n/g;

print "Content-type: text/html\n\n";

require "$EST{temp_path}regist_new_preview.html";

}


sub PR_preview_kt1{
#(2.1)�J�e�S����\��1
foreach $kt_no(1 .. $EST_reg{kt_max}){
print "	<input type=hidden name=Fkt" . $kt_no . " value=\"" . $FORM{"Fkt$kt_no"} . "\">\n";
}
}

sub PR_preview_kt2{
#(2.2)�J�e�S����\��2
foreach $kt_no(1 .. $EST_reg{kt_max}){
print &full_kt($FORM{"Fkt$kt_no"});
print<<"<!--HTML-->";
<input type=hidden name=Fkt$kt_no value="$FORM{"Fkt$kt_no"}">
<br>
<!--HTML-->
}
}


sub join_fld{
#(3)���͓��e�̐��`(&join_fld)
@Slog=(); #�o�^�X�V�p�̃f�[�^�z��
local @arg=@_;
#$arg[0]=�o�^�p�̃f�[�^ID
#[���[�h]
# $Smode_name=>�e���[�h�̔���p�̓����ϐ�(�Ȃ�,new_dairi,mente)
# $FORM{'changer'}=>�ύX��(�Ȃ�,admin)
#���o�^���e�ύX�̏ꍇ�̕ύX�O�f�[�^�́u@Spre_log�v�Ɋi�[����Ă���

##�o�^No(�f�[�^ID)(0)
$Slog[0]=$arg[0];

##�^�C�g��(1)
$Slog[1]=$FORM{'Ftitle'};

##URL(2)
$Slog[2]=$FORM{'Furl'};

##�}�[�N�f�[�^(3)
if($FORM{'changer'} eq "admin"){ #�ύX�҂��Ǘ��l
$FORM{'Fmark'}="";
foreach(1 .. 2){ #���}�[�N���𑝂₷�Ƃ��͏C��
	if($FORM{"Fmark$_"}){$FORM{'Fmark'} .= "1_";}
	else{$FORM{'Fmark'} .= "0_";}
}
$FORM{'Fmark'}=substr($FORM{'Fmark'},0,-1);
$Slog[3]=$FORM{'Fmark'};
}
elsif(!$Smode_name){$Slog[3]="0_0";} #�o�^�҂̐V�K�o�^
else{$Slog[3]=$Spre_log[3];} #�o�^�҂̕ύX

##�X�V��(4)
	#�����̎擾
	$Slog[4]=&get_time(0,1);

##�p�X���[�h(5)
if($Smode_name eq "mente"){$Slog[5]=$Spre_log[5];} #���e�ύX��
else{ #�V�K�o�^��
$Spass=$FORM{'Fpass'}; #�Í����O�̃p�X���[�h��ۑ�
	if($EST{crypt}){$Slog[5]=crypt($FORM{'Fpass'},"ys");} #crypt�g�p�\
	else{$Slog[5]=$FORM{'Fpass'};} #crypt�g�p�s��
}

##�Љ(6)
$Slog[6]=$FORM{'Fsyoukai'};

##�Ǘ��l�R�����g(7)
if($FORM{'changer'} eq "admin"){ #�ύX�҂��Ǘ��l
$Slog[7]=$FORM{'Fkanricom'};
}
elsif(!$Smode_name){$Slog[7]="";} #�o�^�҂̐V�K�o�^
else{$Slog[7]=$Spre_log[7];} #�o�^�҂̕ύX

##�����O(8)
$Slog[8]=$FORM{'Fname'};

##E-mail(9)
$Slog[9]=$FORM{'Femail'};

##�J�e�S��(10)
if($EST{user_change_kt} && $FORM{mode} eq "act_mente" && $FORM{'changer'} ne "admin"){ #�o�^�҂̕ύX�ŃJ�e�S���ύX�֎~�̏ꍇ
local(@kt,$kt,$i=1);
@kt=split(/&/,$Spre_log[10]);
$Slog[10]=$Spre_log[10];
	foreach $kt(@kt){
	$FORM{"Fkt$i"}=$kt;
	$i++;
	}
}
else{ #���̑��̏ꍇ
$FORM{'Fkt'}="";
	foreach(1 .. $EST_reg{kt_max}){
		$FORM{'Fkt'} .= $FORM{"Fkt$_"} . "&";
	}
	$FORM{'Fkt'}=substr($FORM{'Fkt'},0,-1);
	$Slog[10]=$FORM{'Fkt'};
}

##time�`��(11)
{local(@time);
@time=split(/_/,$Spre_log[11]); $times=time();
if($Smode_name eq "mente"){ #���e�ύX��
	if(!$time[1] && $times-$time[0]<$EST{new_time}*86400){$Slog[11]= $times . "_0";}
	else{$Slog[11]= $times . "_1";}
}
else{$Slog[11]= $times . "_0";} #�V�K�o�^��
}

##�o�i�[URL(12)
$Slog[12]=$FORM{'Fbana_url'};

##�A�N�Z�X��(13)
if($Smode_name eq "mente"){$Slog[13]=$Spre_log[13];} #���e�ύX��
else{$Slog[13]="0_0_0_0";} #�V�K�o�^��

##�ŏI�A�N�Z�XIP(14)
if($Smode_name eq "mente"){$Slog[14]=$Spre_log[14];} #���e�ύX��
else{$Slog[14]="";} #�V�K�o�^��

##�L�[���[�h(15)
$Slog[15]=$FORM{'Fkey'};

##</�����܂�>

##���o�^���[�h�̏ꍇ�̐ݒ�
if($EST{user_check} && $FORM{changer} ne "admin" && $FORM{mode} eq "act_regist"){
	$Slog[14]=join("<1>",$FORM{Fsougo},$FORM{Fadd_kt},$FORM{'Fto_admin'})
}

}

sub check{
#(4)���͓��e�̃`�F�b�N(&check)

##�֎~���[�h�̃`�F�b�N
	if($EST_reg{kt_no_word}){
		local(@no_words,$word,$check_str);
			#���[�h�`�F�b�N�Ώۂ̍���
			$check_str=join(" ",$FORM{Fname},$FORM{Femail},$FORM{Furl},$FORM{Fbana_url},$FORM{Ftitle},$FORM{Fsyoukai},$FORM{Fkey});
		@no_words=split(/ /,$EST_reg{kt_no_word});
		foreach $word(@no_words){
			if(index($check_str,$word)>=0){&mes("�o�^�f�[�^�̒��ɂ��֎~����Ă��錾�t�������Ă��܂��B<br>�o�^���悤�Ƃ��Ă���f�[�^�̃W�����������̃T�[�`�G���W�����֎~���Ă���\\��������܂��B","���[�h�`�F�b�N�G���[","back_reg");}
		}
		local($addr_host);
			if(!$ENV{'REMOTE_HOST'}){$ENV{'REMOTE_HOST'}=gethostbyaddr(pack("C4", split(/\./, $ENV{'REMOTE_ADDR'})), 2);}
			$addr_host=$ENV{REMOTE_ADDR} . " " . $ENV{'REMOTE_HOST'};
		foreach $word(@no_words){
			if(index($addr_host,$word)>=0){&mes("����IP���̓z�X�g������̓o�^�͋֎~����Ă���\\��������܂��B<br>$ENV{'REMOTE_ADDR'}/$ENV{'REMOTE_HOST'}<br>","IP/HOST�`�F�b�N�G���[","back_reg");}
		}
	}

##���O
	if($EST_reg{Fname} && !$FORM{Fname}){&mes("<b>�����O</b>��<font color=red>�L���K�{����</font>�ł�","�L���~�X","back_reg");}
	if(($_=length($FORM{Fname})-($EST_reg{Mname}*2))>0){&mes("<b>�����O</b>�͑S�p<b>$EST_reg{Mname}</b>�����ȓ��ł��L����������","�������I�[�o�[(���p���Z��$_������)","back_reg");}
	$FORM{Fname}=~ s/\n//g;


##���[���A�h���X
	if($EST_reg{Femail} && !$FORM{Femail}){&mes("<b>���[���A�h���X</b>��<font color=red>�L���K�{����</font>�ł�","�L���~�X","back_reg");}
	elsif(($_=length($FORM{Femail})-$EST_reg{Memail})>0){&mes("<b>���[���A�h���X</b>�͔��p<b>$EST_reg{Memail}</b>�����ȓ��ł��L����������","�������I�[�o�[(���p���Z��$_������)","back_reg");}
	elsif($EST_reg{Femail} && $FORM{Femail} !~ /(.*)\@(.*)\.(.*)/){&mes("<b>���[���A�h���X</b>�̓��͂�����������܂���","�L���~�X","back_reg");}
	$FORM{Femail}=~ s/\n//g;


##�p�X���[�h
if($FORM{mode} ne "act_mente"){
	if(!$FORM{Fpass}){&mes("<b>�p�X���[�h</b>��<font color=red>�L���K�{����</font>�ł�","�L���~�X","back_reg");}
	elsif(($_=length($FORM{'Fpass'})-8)>0){&mes("<b>�p�X���[�h</b>�͔��p<b>8</b>�����ȓ��ł��L����������","�������I�[�o�[(���p���Z��$_������)","back_reg");}
	elsif($FORM{Fpass} ne $FORM{Fpass2}){&mes("�Q���<b>�p�X���[�h</b>���͂���v���܂���ł���","���̓~�X","back_reg");}
	$FORM{Fpass}=~ s/\n//g;
}

##�z�[���y�[�W�A�h���X(�Q�d�o�^�`�F�b�N�͕ʂ̂Ƃ���ɋL�q)
	if($FORM{Furl} eq "http://"){$FORM{Furl}="";}
	if($EST_reg{Furl} && !$FORM{Furl}){&mes("<b>�z�[���y�[�W�A�h���X</b>��<font color=red>�L���K�{����</font>�ł�","�L���~�X","back_reg");}
	elsif(($_=length($FORM{Furl})-$EST_reg{Murl})>0){&mes("<b>�z�[���y�[�W�A�h���X</b>�͔��p<b>$EST_reg{Murl}</b>�����ȓ��ł��L����������","�������I�[�o�[(���p���Z��$_������)","back_reg");}
	elsif($FORM{Furl} && $FORM{Furl} !~ /^https?:\/\/.+\..+/){&mes("<b>�z�[���y�[�W�A�h���X</b>�̓��͂�����������܂���","�L���~�X","back_reg");}
	$FORM{Furl}=~ s/\n//g;


##�^�C�g���o�i�[��URL
	if($EST_reg{bana_url}){
		if($FORM{Fbana_url} eq "http://"){$FORM{Fbana_url}="";}
		if($EST_reg{Fbana_url} && !$FORM{Fbana_url}){&mes("<b>�^�C�g���o�i�[��URL</b>��<font color=red>�L���K�{����</font>�ł�","�L���~�X","back_reg");}
		elsif(($_=length($FORM{Fbana_url})-$EST_reg{Mbana_url})>0){&mes("<b>�^�C�g���o�i�[��URL</b>�͔��p<b>$EST_reg{Mbana_url}</b>�����ȓ��ł��L����������","�������I�[�o�[(���p���Z��$_������)","back_reg");}
		elsif($FORM{Fbana_url} && $FORM{Fbana_url} !~ /^https?:\/\/.+\..+(\.gif|\.jpg|\.jpeg|\.png)$/i){&mes("<b>�^�C�g���o�i�[��URL</b>�̓��͂�����������܂���","�L���~�X","back_reg");}
	}
	else{$FORM{Fbana_url}="";}
	$FORM{Fbana_url}=~ s/\n//g;


##�z�[���y�[�W�̃^�C�g��
	if($EST_reg{Ftitle} && !$FORM{Ftitle}){&mes("<b>�z�[���y�[�W�̃^�C�g��</b>��<font color=red>�L���K�{����</font>�ł�","�L���~�X","back_reg");}
	if(($_=length($FORM{Ftitle})-($EST_reg{Mtitle}*2))>0){&mes("<b>�z�[���y�[�W�̃^�C�g��</b>�͑S�p<b>$EST_reg{Mtitle}</b>�����ȓ��ł��L����������","�������I�[�o�[(���p���Z��$_������)","back_reg");}
	$FORM{Ftitle}=~ s/\n//g;

##�z�[���y�[�W�̏Љ
	if($EST_reg{Fsyoukai} && !$FORM{Fsyoukai}){&mes("<b>�z�[���y�[�W�̏Љ</b>��<font color=red>�L���K�{����</font>�ł�","�L���~�X","back_reg");}
	if(($_=length($FORM{Fsyoukai})-($EST_reg{Msyoukai}*2))>0){&mes("<b>�z�[���y�[�W�̏Љ</b>�͑S�p<b>$EST_reg{Msyoukai}</b>�����ȓ��ł��L����������","�������I�[�o�[(���p���Z��$_������)","back_reg");}
	if(!$EST{syoukai_br}){$FORM{Fsyoukai}=~ s/\n//g;}
	else{$FORM{Fsyoukai}=~ s/\n/<br>/g;}

##�Ǘ��l�R�����g
	$FORM{Fkanricom}=~ s/\n/<br>/g;

##�J�e�S��
{local(%kt_fl,$i,$j=0,$PR_kt);
&gane_st; #�W�������X�e�[�^�X�����[�h
	foreach $i(1 .. $EST_reg{kt_max}){
		$FORM{"Fkt$i"}=~s/\n//g;
		if($kt_fl{$FORM{"Fkt$i"}}){$FORM{"Fkt$i"}="";}
		elsif($ganes{$FORM{"Fkt$i"}}){$kt_fl{$FORM{"Fkt$i"}}=1;}
		else{$FORM{"Fkt$i"}="";}
		##�֎~�J�e�S���ɓo�^���悤�Ƃ����ꍇ
		if($FORM{changer} ne "admin" && $gane_UR{$FORM{"Fkt$i"}}){
			&mes("�o�^�҂̓o�^���ł��Ȃ��J�e�S���ɕύX���悤�Ƃ��Ă��܂�","�J�e�S���I���~�X","back_reg");
		}
	}
	foreach(keys %kt_fl){$j++;}
	if($EST_reg{kt_min} eq $EST_reg{kt_max}){$PR_kt="<b>$EST_reg{kt_max}</b>��";}
	else{$PR_kt="<b>$EST_reg{kt_min}</b>�`<b>$EST_reg{kt_max}</b>��";}
	if($EST_reg{kt_min}>$j || $j>$EST_reg{kt_max}){&mes("<b>�J�e�S��</b>��$PR_kt�I�����Ă�������","�I�𐔃~�X","back_reg");}
}


##�L�[���[�h
	if($EST_reg{Fkey} && !$FORM{Fkey}){&mes("<b>�L�[���[�h</b>��<font color=red>�L���K�{����</font>�ł�","�L���~�X","back_reg");}
	if(($_=length($FORM{Fkey})-($EST_reg{Mkey}*2))>0){&mes("<b>�L�[���[�h</b>�͑S�p<b>$EST_reg{Mkey}</b>�����ȓ��ł��L����������","�������I�[�o�[(���p���Z��$_������)","back_reg");}
	$FORM{Fkey}=~ s/\n//g;


##�ǉ����ė~�����J�e�S��
	if($FORM{mode} ne "act_mente" && $FORM{changer} ne "admin"){
		if($EST_reg{Fadd_kt} && !$FORM{Fadd_kt}){&mes("<b>�ǉ����ė~�����J�e�S��</b>��<font color=red>�L���K�{����</font>�ł�","�L���~�X","back_reg");}
		if(($_=length($FORM{Fadd_kt})-($EST_reg{Madd_kt}*2))>0){&mes("<b>�ǉ����ė~�����J�e�S��</b>�͑S�p<b>$EST_reg{Madd_kt}</b>�����ȓ��ł��L����������","�������I�[�o�[(���p���Z��$_������)","back_reg");}
		$FORM{Fadd_kt}=~ s/\n//g;
	}

##���݃����N�̗L��
	$MES_sougo{1}="����"; $MES_sougo{0}="���Ȃ�";
	if($FORM{Fsougo} ne "1"){$FORM{Fsougo}=0;}

##�Ǘ��l�ւ̃��b�Z�[�W
	if($FORM{mode} ne "act_mente" && $FORM{changer} ne "admin"){
		if($EST_reg{Fto_admin} && !$FORM{Fto_admin}){&mes("<b>�Ǘ��l�ւ̃��b�Z�[�W</b>��<font color=red>�L���K�{����</font>�ł�","�L���~�X","back_reg");}
		if(($_=length($FORM{Fto_admin})-($EST_reg{Mto_admin}*2))>0){&mes("<b>�Ǘ��l�ւ̃��b�Z�[�W</b>�͑S�p<b>$EST_reg{Mto_admin}</b>�����ȓ��ł��L����������","�������I�[�o�[(���p���Z��$_������)","back_reg");}
		if(!$EST{syoukai_br}){$FORM{Fto_admin}=~ s/\n//g;}
		else{$FORM{Fto_admin}=~ s/\n/<br>/g;}
	}

}

sub PRend{
#(5)�o�^���ʉ�ʏo��(&PRend)
print "Content-type: text/html\n\n";
require "$EST{temp_path}regist_new_end.html";

}

sub enter{
#(6)�C���E�폜�̂��߂̃p�X���[�h�F��(&enter)

#�N�b�L�[�̓ǂݍ���
&get_cookie;
	if($CK_data[4] && $CK_data[3] && $FORM{id}){ #���ڔF��
		$FORM{pass}=$CK_data[3];
		$FORM{changer}="admin";
		$FORM{in_mode}="mente";
		&regist;
		exit;
	}
if(!$FORM{id}){
	$FORM{id}=$CK_data[1];
}

#�T���͒l�̐ݒ�
$FORM{id}=~s/\D//g;
if($FORM{id}){
local(@Tlog,$i=0);
	open(IN,"$EST{log_path}$EST{logfile}");
		while(<IN>){
			@Tlog=split(/<>/,$_,4);
			if($Tlog[0] eq "$FORM{id}"){$i=1; last;}
		}
	close(IN);
	if(!$i){&mes("�w�肳�ꂽID�̃f�[�^�͑��݂��܂���","�G���[","java");}

$PR_data=<<"EOM";
[�o�^�f�[�^]<br>
<table width=200><tr><td>
���^�C�g���F<br>$Tlog[1]<br>
��URL�F<br><a href="$Tlog[2]">$Tlog[2]</a>
<div align=right>[<a href="$Tlog[2]" target="_blank">�m�F</a>]</div>
</td></tr>
</table>
EOM

}

print "Content-type: text/html\n\n";
require "$EST{temp_path}enter.html";

}

sub help{
#(7)�w���v�̕\��(&help)
print "Content-type: text/html\n\n";
require "$EST{temp_path}help.html";
}

sub act_repass{
#(8)�p�X���[�h�̍Ĕ��s�E�ύX(&act_repass)

local($new_pass,$cr_new_pass,@log_lines,$line,$id,$mail_to,@Slog);

	if($FORM{repass_mode} eq "repass"){ #�p�X���[�h�Ĕ��s��
		if($FORM{repass_check} ne "on"){&mes("�p�X���[�h�Ĕ��s�̊m�F�`�F�b�N������܂���B������x�߂��Ă���`�F�b�N�����čēx���s���Ă�������","�m�F�`�F�b�N�����Ă�������","java");}
		if(!$EST{re_pass_fl}){&mes("�p�X���[�h�̍Ĕ��s�͂ł��Ȃ��ݒ�ɂȂ��Ă��܂�","�G���[","java");}
		#�V�����p�X���[�h���쐬
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
		
		
		if($EST{mail_pass}){$PR_mes="�p�X���[�h�̍Ĕ��s���������܂���<br>�V�����p�X���[�h�̓��[���A�h���X�ɑ��M����܂�";}
		else{$PR_mes="�p�X���[�h�̍Ĕ��s���������܂���<br>�V�����p�X���[�h�́u <b>$new_pass</b> �v�ł�";}

	}
	else{ #�p�X���[�h�ύX��
		$FORM{new_pass}=~s/\W//g;
		$new_pass=$FORM{new_pass};
		if($EST{crypt}){$cr_new_pass=crypt($new_pass,"ys");}
		else{$cr_new_pass=$new_pass;}

		if($EST{mail_pass}){$PR_mes="�p�X���[�h�̕ύX���������܂���<br>�V�����p�X���[�h�̓��[���A�h���X�ɑ��M����܂�";}
		else{$PR_mes="�p�X���[�h�̕ύX���������܂���<br>�V�����p�X���[�h�́u <b>$new_pass</b> �v�ł�";}
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
					if($cr_pass ne $Slog[5]){&unlock(); &mes("�p�X���[�h���Ԉ���Ă��܂�","�G���[","java");}
				}
				else{
					if($cr_pass ne $EST{pass}){&unlock(); &mes("�Ǘ��p�X���[�h���Ԉ���Ă��܂�","�G���[","java");}
				}
			}
			else{
				if($FORM{email} ne $Slog[9]){&unlock(); &mes("ID�ƃ��[���A�h���X����v���܂���ł���","�G���[","java");}
			}
			$mail_to=$Slog[9];
			$Slog[5]=$cr_new_pass;
			$line=join("<>",@Slog);
			$fl=1;
		}
		push(@log_lines,$line);
	}
	if(!$fl){&unlock(); &mes("�Y������ID�͂���܂���","�G���[","java");}
close(IN);
open(OUT,">$EST{log_path}$EST{logfile}");
	print OUT @log_lines;
close(OUT);
@log_lines=();
if($EST{mail_pass}){require "pl/mail_ys.cgi"; &mail($mail_to,$EST{admin_email},"$EST{search_name} �p�X���[�h�ύX�ʒm","pass","",*Slog);}
&unlock();

&mes($PR_mes,"�p�X���[�h�ύX����","$EST{home}");
}

sub no_link{
#(9)�����N�؂�񍐃t�H�[��(&no_link)

if($FORM{"pre"} eq "on"){
$Eref=~s/(\W)/'%' . unpack('H2',$1)/eg;
$mes=<<"EOM";
�Ǘ��҂Ɂu<b>$FORM{title}</b>�v�ɂ��Ă̒ʒm���s���܂�<br>
�u�ʒm����v�{�^���������ƊǗ��҂֒ʒm�ł��܂�
<br><br>





<form action="regist_ys.cgi" method=post target="">
  <input type=hidden name=mode value="no_link">
  <input type=hidden name=id value="$FORM{id}">
  <input type=hidden name=pre value="">
  <input type=hidden name=ref value="$Eref">
  <input type=hidden name=title value="$FORM{title}">

	<ul>
	[�ʒm���]<br>
		<input type=checkbox name=type_no_link value="1">�����N�؂�<br>
		<input type=checkbox name=type_move value="2">�z�[���y�[�W�ړ]<br>
		<input type=checkbox name=type_bana_no_link value="3">�o�i�[�����N�؂�<br>
		<input type=checkbox name=type_ill value="4">�K��ᔽ[<a href="$EST{cgi_path_url}regist_ys.cgi?mode=new">�K��͂�����</a>]<br>
		<input type=checkbox name=type_other value="5">���̑�(�R�����g���ɂ����L����������)<br>
	<br>
	[�R�����g](�K�v������΂��L����������)<br>
		<textarea name=com cols=40 rows=4></textarea><br>
	<br>
	[�����O](�C��)<br>
	<input type=text name=c_name><br>
	[E-Mail](�C��)<br>
	<input type=text name=c_email><br>
	</ul>

</ul>
<center>
  <input type=submit value="�ʒm����">
</center>
</form>

<hr width="90%">
<center>
<form><input type=button value=" �O�̉�ʂɖ߂� " onClick="history.back()"></form>
</center>
EOM
&mes($mes,"�Ǘ��҂ւ̒ʒm���");
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
		#�񍐎��(�����N�؂�=0/�T�C�g�ړ]=1/�o�i�[�����N�؂�=2/�K��ᔽ=3/���̑�=4)
		if($FORM{type_no_link}){$Dhoukoku.="1,";$fl=1;}
		if($FORM{type_move}){$Dhoukoku.="2,";$fl=1;}
		if($FORM{type_bana_no_link}){$Dhoukoku.="3,";$fl=1;}
		if($FORM{type_ill}){$Dhoukoku.="4,";$fl=1;}
		if($FORM{type_other}){$Dhoukoku.="5,";$fl=1;}
			if(!$fl){&mes("�u�ʒm��ʁv�ɍŒ��̓`�F�b�N���Ă�������","�`�F�b�N�~�X","java");}
		#�R�����g
		$FORM{com}=~s/\n/<br>/g; $Dcom=$FORM{com};
		#���O
		$FORM{c_name}=~s/\n//g; $Dname=$FORM{c_name};
		#E-Mail
		$FORM{c_email}=~s/\n//g; $Demail=$FORM{c_email};
		if(length("$Dcom$Dname$Demail")>500){&mes("�R�����g�A�����O�AE-Mail�̕�������<br>���v��250����(�S�p���Z)�܂łŁA���肢���܂��B","�������I�[�o�[","java");}
	open(OUT,">>$EST{log_path}no_link_temp.cgi");
		print OUT "$FORM{id}<>$ENV{'REMOTE_ADDR'}<>$Dhoukoku<>$Dcom<>$Dname<>$Demail<>\n";
	close(OUT);
	}
}

$FORM{ref}=~s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2',$1)/eg;
&mes("���񍐂��肪�Ƃ��������܂���<br>�Ǘ��l�Ɂu<b>$FORM{title}</b>�v�ɂ��Ă̒ʒm���s���܂���","���񍐂��肪�Ƃ��������܂�",$FORM{ref});
}

sub act_regist{
#(p1)�V�K�o�^���s(&act_regist)
require "$EST{log_path}task_ys.cgi";
local($new,$new_id,@hyouji_log);
#$new=>�ǉ��f�[�^�������ݗp/%TASK=>�X�V����J�e�S�����X�g
#@hyouji_log=>���ʕ\���p�̃��O�f�[�^


#�p�X���[�h�F��(�Ǘ��ҔF��)
if($FORM{'changer'} eq "admin"){
local($cr_pass);
	if($EST{crypt}){$cr_pass=crypt($FORM{pass},$EST{pass});}
	else{$cr_pass=$FORM{pass};}
	if($cr_pass ne $EST{pass}){
		if(!$ENV{'REMOTE_HOST'}){$ENV{'REMOTE_HOST'}=gethostbyaddr(pack("C4", split(/\./, $ENV{'REMOTE_ADDR'})), 2);}
		&mes("�p�X���[�h�̔F�؂Ɏ��s���܂���<br>�F�؂����R���s���[�^��IP�A�h���X�F<b>$ENV{'REMOTE_ADDR'}</b><br>�F�؂����R���s���[�^�̃z�X�g���F<b>$ENV{'REMOTE_HOST'}</b>","�p�X���[�h�F�؎��s","java");
	}
}

&check; #���͓��e�̃`�F�b�N

&lock; #���b�N

#ID�擾&�Q�dURL�o�^�`�F�b�N
$Cgane_pre=0; #���o�^��
if($EST_reg{nijyu_url}){$new_id=&get_id_url_ch(1);}
else{$new_id=&get_id;}

&join_fld($new_id); #���͓��e�̐��`
$new=join("<>",@Slog,"\n");
@hyouji_log=@Slog;

if($EST{user_check} && $FORM{changer} ne "admin" && $FORM{mode} eq "act_regist"){ #<���o�^��>

#���o�^���O�f�[�^�ɒǉ���������
open(OUT,">>$EST{log_path}$EST{temp_logfile}");
	print OUT $new;
close(OUT);

##���[���𑗐M
	#�����ɕt����}�[�N��ݒ�
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
if($EST{mail_to_admin} && $EST{mail_temp}){ #�Ǘ��l�փ��[�����M
	&mail($EST{admin_email},$Slog[9],"$EST{search_name} ���o�^�����ʒm$PR_mail_add_line","temp","admin",*Slog,$FORM{Fsougo},$FORM{Fadd_kt},$FORM{Fto_admin});
}
if($EST{mail_to_register} && $EST{mail_temp}){ #�o�^�҂փ��[�����M
	&mail($Slog[9],$EST{admin_email},"$EST{search_name} ���o�^�����ʒm","temp","",*Slog,$FORM{Fsougo},$FORM{Fadd_kt},$FORM{Fto_admin});
}
$Slog[6]=~s/\n/<br>/g; $Slog[7]=~s/\n/<br>/g;


&unlock(); #���b�N����

##�o�^���ʏo��
print "Content-type: text/html\n\n";
require "$EST{temp_path}regist_new_end_temp.html";


} #</���o�^��>
else{ #<�V�K�o�^��>

#�{�̃��O�f�[�^�ɒǉ���������
open(OUT,">>$EST{log_path}$EST{logfile}");
	print OUT $new;
close(OUT);

##�o�^�҂̃��b�Z�[�W��ۑ�����ݒ�̏ꍇ
if(($FORM{Fadd_kt} || $FORM{Fto_admin}) && $EST_reg{look_mes} && $EST_reg{look_mes}=~/(\d+)(\w*)/){
local(@look_mes_list,@look_mes,$look_mes,$i=0,$max=$1);
	open(IN,"$EST{log_path}look_mes.cgi");
	while(<IN>){
	if($i<$max){push(@look_mes_list,$_);}
	else{last;}
	$i++;
	}
	close(IN);
	#�ꊇ���M����ꍇ
	if($2 eq "m" && $i>=$max){
		$mail_mes=<<"EOM";
## $EST{search_name} �o�^�҂���̃��b�Z�[�W�ʒm ##

EOM
local(@tlook_mes);
		foreach(@look_mes_list){
		@tlook_mes=split(/<>/,$_);
		$mail_mes.=<<"EOM";
+-------------------------+
�o�^���F$tlook_mes[1] / �����O�F$tlook_mes[5] / Email�F $tlook_mes[4]
�^�C�g���F$tlook_mes[7]
URL�F
$tlook_mes[6]
�C���pURL�F
$EST{cgi_path_url}regist_ys.cgi?mode=enter&id=$tlook_mes[0]
EOM
		if($tlook_mes[2]){$mail_mes.="�V�݊�]�J�e�S���F$tlook_mes[2]\n";}
		if($tlook_mes[3]){
		$tlook_mes[3]=~s/<br>/\n/g;
		$mail_mes.=$tlook_mes[3] . "\n";
		}
		}
		$mail_mes.="+-------------------------+\n";
		require "pl/mail_ys.cgi";
		&mail($EST{admin_email},$EST{admin_email},"$EST{search_name} �o�^�҂���̃��b�Z�[�W�ʒm($max��)","any","","","","","","",$mail_mes);
		$i=0;
		@look_mes_list=();
		open(OUT,">$EST{log_path}look_mes.cgi");
		close(OUT);
	}
	if($i eq $max){pop @look_mes_list;}
	#�V�K�ǉ��f�[�^($look_mes)���쐬
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

##���[���𑗐M
unless($FORM{FCmail} eq "no" && $FORM{changer} eq "admin"){ #���M����ݒ�Ȃ�
	#�����ɕt����}�[�N��ݒ�
	local($PR_mail_sougo,$PR_mail_com,$PR_mail_kt);
	&kenmei_put_mark;
$Slog[6]=~s/<br>/\n/g; $Slog[7]=~s/<br>/\n/g;
if($EST{mail_new}){require "pl/mail_ys.cgi";}
if($EST{mail_to_admin} && $EST{mail_new}){ #�Ǘ��l�փ��[�����M
	&mail($EST{admin_email},$Slog[9],"$EST{search_name} �V�K�o�^�����ʒm$PR_mail_add_line","new","admin",*Slog,$FORM{Fsougo},$FORM{Fadd_kt},$FORM{Fto_admin});
}
if($EST{mail_to_register} && $EST{mail_new}){ #�o�^�҂փ��[�����M
	&mail($Slog[9],$EST{admin_email},"$EST{search_name} �V�K�o�^�����ʒm","new","",*Slog,$FORM{Fsougo},$FORM{Fadd_kt},$FORM{Fto_admin});
}
$Slog[6]=~s/\n/<br>/g; $Slog[7]=~s/\n/<br>/g;
}

#�X�V����J�e�S�����X�g���쐬
#%TASK/@TASK_list���g�p
@TASK_list=();
$TASK{"new"}=1; #�V�����
if($FORM{'changer'} eq "admin"){ #�}�[�N�J�e�S���̍X�V
	foreach(1 .. 2){ #���}�[�N���𑝂₷�Ƃ��͏C��
		if($FORM{"Fmark$_"}){$TASK{"m$_"}=1;}
	}
}
if($EST{html}){ #�J�e�S����HTML�t�@�C���ŕ\������ꍇ
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
else{ #�J�e�S����CGI�œ��I�ɕ\������ꍇ
local($kt,$i);
	foreach $i(1 .. $EST_reg{kt_max}){
		if($FORM{"Fkt$i"}){
			($kt)=split(/_/,$FORM{"Fkt$i"});
			$TASK{$kt}=1;
		}
	}
}

##�h���t�@�C���̏���
if($EST{html} && $EST{task} ne "2"){ #��������(html && !cron)
&MK_html(*TASK_list);
&make_task;
}
else{&make_task;} #�^�X�N�t�@�C���ɏ�������

##���o�^�����L�^
open(OUT,">$EST{log_path}total_url.log");
	print OUT $Cgane_pre+1;
close(OUT);

&unlock(); #���b�N����

##�o�^���ʏo��
@Slog=@hyouji_log;
print "Content-type: text/html\n\n";
require "$EST{temp_path}regist_new_end.html";

} #</�V�K�o�^��>

}


sub get_id_url_ch{
##�V�K�o�^�p��ID���擾&�Q�dURL�o�^�`�F�b�N
#�`�F�b�N�Ɋ|�������ꍇ�ɂ̓��b�N������
#$arg=>(�V�K�o�^=1/���e�ύX=2)
local($id,$line,@Tlog,$fl=$_[0],$i=0,$pre_title);
	open(IN,"$EST{log_path}$EST{logfile}");
		while($line=<IN>){
			@Tlog=split(/<>/,$line);
			if($FORM{Furl} eq $Tlog[2]){$i++; $pre_title=$Tlog[1];}
			if($FORM{id} eq $Tlog[0]){@Spre_log=@Tlog;}
			if($fl<=$i){&unlock; &mes("����URL�͂��łɓo�^����Ă��܂�<br><br>$Tlog[1] :<br>$Tlog[2]","�Q�d�o�^�G���[","java");}
			$id=$Tlog[0];
			$Cgane_pre++;
		}
		if($fl eq "2" && $i eq "1" && $Spre_log[2] ne $FORM{Furl}){&unlock; &mes("����URL�͂��łɓo�^����Ă��܂�<br><br>$pre_title :<br>$FORM{Furl}","�Q�d�o�^�G���[","java");}
	close(IN);
	if($FORM{changer} ne "admin" && $EST{user_check} && $FORM{mode} eq "act_regist"){
	 #���o�^���[�h�Ń��[�U�̐V�K�o�^��
		open(IN,"$EST{log_path}$EST{temp_logfile}");
			while($line=<IN>){
				@Tlog=split(/<>/,$line,5);
				if($FORM{Furl} eq $Tlog[2]){$i++;}
				if($fl<=$i){&unlock; &mes("����URL�͌��ݓo�^�\\�����ł�<br><br>$Tlog[1] :<br>$Tlog[2]","�Q�d�o�^�G���[","java");}
				$id=$Tlog[0];
			}
		close(IN);
	}
return $id+1;
}

sub get_id{
##�V�K�o�^�p��ID���擾
local($id,$line);
		if($FORM{changer} ne "admin" && $EST{user_check} && $FORM{mode} eq "act_regist"){ #���o�^���[�h�Ń��[�U�̐V�K�o�^��
			open(IN,"$EST{log_path}$EST{temp_logfile}");
		}
		else{ #���̑�
			open(IN,"$EST{log_path}$EST{logfile}");
		}
		while(<IN>){$line=$_; $Cgane_pre++;} 
	close(IN);
	($id)=split(/<>/,$line);
return $id+1;
}


sub act_mente{
#(p2)�o�^���e�ύX(&act_mente)

if($FORM{changer} ne "admin" && $EST_reg{no_mente}){&mes("���݁A�o�^�҂ɂ��C���E�폜�͒�~����Ă��܂�","�G���[","java");}

require "$EST{log_path}task_ys.cgi";
local($new,@log_lines,$line,@TASK_list);
#$new=>�ǉ��f�[�^�������ݗp/%TASK=>�X�V����J�e�S�����X�g

#�p�X���[�h�F��(�Ǘ��ҔF��)
if($FORM{'changer'} eq "admin"){
local($cr_pass);
	if($EST{crypt}){$cr_pass=crypt($FORM{pass},$EST{pass});}
	else{$cr_pass=$FORM{pass};}
	if($cr_pass ne $EST{pass}){
		if(!$ENV{'REMOTE_HOST'}){$ENV{'REMOTE_HOST'}=gethostbyaddr(pack("C4", split(/\./, $ENV{'REMOTE_ADDR'})), 2);}
		&mes("�p�X���[�h�̔F�؂Ɏ��s���܂���<br>�F�؂����R���s���[�^��IP�A�h���X�F<b>$ENV{'REMOTE_ADDR'}</b><br>�F�؂����R���s���[�^�̃z�X�g���F<b>$ENV{'REMOTE_HOST'}</b>","�p�X���[�h�F�؎��s","java");
	}
}

##���̑��̐ݒ�
$Smode_name="mente";

&check; #���͓��e�̃`�F�b�N

&lock; #���b�N

#@Spre_log�擾&�Q�dURL�o�^�`�F�b�N
if($EST_reg{nijyu_url}){&get_id_url_ch(2);}
else{
	open(IN,"$EST{log_path}$EST{logfile}");
		while(<IN>){
			@Spre_log=split(/<>/,$_);
			if($Spre_log[0] eq $FORM{id}){last;}
		}
	close(IN);
}

#�o�^�҂̃p�X���[�h�F��
if($FORM{changer} ne "admin"){
local($cr_pass);
	if($EST{crypt}){$cr_pass=crypt($FORM{pass},$Spre_log[5]);}
	else{$cr_pass=$FORM{pass};}
	if($Spre_log[5] ne $cr_pass){&unlock(); &mes("�p�X���[�h���Ԉ���Ă��܂�$cr_pass $Spre_log[5]","�p�X���[�h�F�؃G���[","java");}
}

&join_fld($Spre_log[0]); #���͓��e�̐��`
$new=join("<>",@Slog);
$new=~s/\n//g; $new .="<>\n";


#�{�̃��O�f�[�^�ɏ�������
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

##���[���𑗐M
$Slog[6]=~s/<br>/\n/g; $Slog[7]=~s/<br>/\n/g;
if($EST{mail_new}){require "pl/mail_ys.cgi";}
if($EST{mail_to_admin} && $EST{mail_ch}){ #�Ǘ��l�փ��[�����M
	&mail($EST{admin_email},$Slog[9],"$EST{search_name} �o�^���e�ύX�����ʒm","mente","admin",*Slog);
}
if($EST{mail_to_register} && $EST{mail_ch}){ #�o�^�҂փ��[�����M
	&mail($Slog[9],$EST{admin_email},"$EST{search_name} �o�^���e�ύX�����ʒm","mente","",*Slog);
}
$Slog[6]=~s/\n/<br>/g; $Slog[7]=~s/\n/<br>/g;



##�X�V����J�e�S�����X�g���쐬
#%TASK���g�p
#�X�V���or�V�����
{local(@time);
@time=split(/_/,$Spre_log[11]);
if(!$time[1] && $times-$time[0]<$EST{new_time}*86400){$TASK{"new"}=1;}
else{$TASK{"renew"}=1;}
}

#�}�[�N�J�e�S���̍X�V
{local(@mark,$mark,$i=1);
if($FORM{'changer'} eq "admin"){
	foreach(1 .. 2){ #���}�[�N���𑝂₷�Ƃ��͏C��
		if($FORM{"Fmark$_"}){$TASK{"m$_"}=1;}
	}
}
@mark=split(/_/,$Spre_log[3]);
	foreach $mark(@mark){
		if($mark){$TASK{"m$i"}=1;}
	$i++;
	}
}

if($EST{html}){ #�J�e�S����HTML�t�@�C���ŕ\������ꍇ
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
else{ #�J�e�S����CGI�œ��I�ɕ\������ꍇ
local($kt,$i);
	foreach $i(1 .. $EST_reg{kt_max}){
		if($FORM{"Fkt$i"}){
			($kt)=split(/_/,$FORM{"Fkt$i"});
			$TASK{$kt}=1;
		}
	}
}


##�h���t�@�C���̏���
if($EST{html} && $EST{task} ne "2"){ #��������(html && !cron)
&MK_html(*TASK_list);
&make_task;
}
else{&make_task;} #�^�X�N�t�@�C���ɏ�������

&unlock(); #���b�N����

#�}�[�N�̕\���ݒ�
{local(@mark,$mark,$i=1); $PR_mark="";
@mark=split(/_/,$Slog[3]);
	foreach $mark(@mark){
		if($mark){$PR_mark .= $EST{"name_m$i"} . " ";}
	$i++;
	}
}
#�J�e�S���̕ύX�\���ݒ�
if($EST{user_change_kt}){$PR_kt="���o�^�҂ɂ��J�e�S���ύX�͌��݋֎~����Ă��܂�";}
else{$PR_kt="";}

##�\���p�ϐ���ݒ�
@Slog=split(/<>/,$new);

##�o�^���ʏo��
print "Content-type: text/html\n\n";
require "$EST{temp_path}regist_mente_end.html";


}


sub act_del{
#(p3)�폜���s(&act_del)
local($Cdel=0,%kousin_list);

require "$EST{log_path}task_ys.cgi";

if($FORM{del_mode} eq "single"){ #del_mode:single
	if($FORM{del_check} ne "on"){&mes("�폜�m�F�̂��߂Ƀ`�F�b�N�����Ă���폜�{�^���������Ă�������","�m�F�`�F�b�N�����Ă�������","java");}
	if($FORM{changer} ne "admin" && $EST_reg{no_mente}){&mes("���݁A�o�^�҂ɂ��C���E�폜�͒�~����Ă��܂�","�G���[","java");}
	if($FORM{changer} eq "admin"){&pass_check;}
	&lock;
	local(@log_lines,@Slog,$line,$fl=0);
	open(IN,"$EST{log_path}$EST{logfile}");
		while($line=<IN>){
			@Slog=split(/<>/,$line);
			if($FORM{id} eq $Slog[0]){
				if($FORM{changer} ne "admin"){ #�폜����l���o�^�҂̏ꍇ
					local($cr_pass);
					if($EST{crypt}){$cr_pass=crypt($FORM{pass},$Slog[5]);}
					else{$cr_pass=$FORM{pass};}
					if($cr_pass ne $Slog[5]){&unlock; &mes("�p�X���[�h�̔F�؂Ɏ��s���܂���","�G���[","java");}
				}
				local(@kt,$kt,@mark,$mark,$i=1,@time);
				@kt=split(/&/,$Slog[10]);
				foreach $kt(@kt){ #�J�e�S��
					$kousin_list{$kt}=1;
				}
				@mark=split(/_/,$Slog[3]);
				foreach $mark(@mark){ #�}�[�N
					if($mark){$TASK{"m$i"}=1;}
					$i++;
				}
				@time=split(/_/,$Slog[11]);
				if(time - $time[0]<86400*$EST{new_time}){ #�V���E�X�V
					if($time[1]){$TASK{renew}=1;}
					else{$TASK{new}=1;}
				}
				$Cdel++;
				$fl=1;
			}
			else{push(@log_lines,$line);}
		}
	close(IN);
		if(!$fl){&unlock; &mes("�Y������f�[�^�͌�����܂���","�G���[","java");}
	open(OUT,">$EST{log_path}$EST{logfile}");
		print OUT @log_lines;
	close(OUT);
	@log_lines=();
}
else{ #del_mode:multi
	if($FORM{changer} ne "admin"){&mes("�ύX�Ҏw�肪�s���ł�","�G���[","java");}
	&pass_check;
	&lock();
		#�����N�؂ꃊ�X�g����̍폜�̏ꍇ
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
		#�f�b�h�����N�`�F�b�N�ς݃��X�g����̍폜�̏ꍇ
		if($FORM{dl_check} eq "on"){
			unless(-T $FORM{checkfile}){&unlock(); &mes("�t�@�C���w�肪�ُ�ł�","�G���[","java");}
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
			if($FORM{"id_$Slog[0]"} eq "on"){ #�폜���X�g�ɓ����Ă���ꍇ
				local(@kt,$kt,@mark,$mark,$i=1,@time);
				@kt=split(/&/,$Slog[10]);
				foreach $kt(@kt){ #�J�e�S��
					$kousin_list{$kt}=1;
				}
				@mark=split(/_/,$Slog[3]);
				foreach $mark(@mark){ #�}�[�N
					if($mark){$TASK{"m$i"}=1;}
					$i++;
				}
				@time=split(/_/,$Slog[11]);
				if(time - $time[0]<86400*$EST{new_time}){ #�V���E�X�V
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

##%kousin_list�̓��e��CGI/HTML�ɉ�����%TASK/@TASK_list�ɓ����

##�h���t�@�C���̏���
if($EST{html} && $EST{task} ne "2"){ #��������(html && !cron)
		foreach(keys %kousin_list){
			$TASK{$_}=1;
			push(@TASK_list,$_);
		}
&MK_html(*TASK_list);
}
else{ #����ȊO�̏ꍇ
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

##���o�^�����L�^
open(IN,"$EST{log_path}total_url.log");
	$Cgane_pre=<IN> - $Cdel;
close(IN);
open(OUT,">$EST{log_path}total_url.log");
	print OUT $Cgane_pre;
close(OUT);

&unlock();

if($FORM{changer} eq "admin" && ($FORM{no_link} eq "on" || $FORM{dl_check} eq "on")){&mes("�폜�������������܂���","�폜����","kanri");}
else{&mes("�폜�������������܂���","�폜����",$EST{home});}


}




####�ʏ���####
##�ڎ�##



#�t�H�[���f�[�^�̃f�R�[�h(&form_decode)
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




#(6)���b�Z�[�W��ʏo��(&mes)
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

print "Content-type: text/html\n\n";
$Munlock=$_[3];
	if($Munlock eq "unlock"){&unlock();}
$MES=$_[0];
		if($_[1]){$TITLE=$_[1];}
		else{$TITLE="���b�Z�[�W���";}
	if($_[2] eq "java" || ($_[2] eq "back_reg" && $FORM{mode} eq "act_mente")){
	$BACK_URL="<form><input type=button value=\"&nbsp;&nbsp;&nbsp;&nbsp;�߂�&nbsp;&nbsp;&nbsp;&nbsp;\" onClick=\"history.back()\"></form>"
	}
	elsif($_[2] eq "env"){
	$BACK_URL="�y<a href=\"$ENV{'HTTP_REFERER'}\">�߂�</a>�z";
	}
	elsif($_[2] eq "kanri"){
	$BACK_URL="<form action=\"$EST{admin}\" method=post><input type=hidden name=mode value=kanri><input type=hidden name=pass value=\"$FORM{'pass'}\"><input type=submit value=\"�Ǘ�����\"></form>"
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
	
	<input type=submit value="�o�^��ʂɖ߂�">
EOM
	}
	else{$BACK_URL="�y<a href=\"$_[2]\">�߂�</a>�z";}

require "$EST{temp_path}mes.html";

exit;
}



##-- end of regist_ys.cgi --##
