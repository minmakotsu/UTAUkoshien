#!/usr/bin/perl

#��perl�̃p�X�������̊��ɍ��킹�ď��������܂��B
#���́A�u#!/usr/bin/perl�v�@���@�u#!/usr/local/bin/perl�v�ł��B
#����Ȃ��ꍇ�̓T�[�o�[�Ǘ���(�������̓v���o�C�_�[)��
#�m�F���Ă��������B

require 'pl/jcode.pl';
require 'pl/cfg.cgi';
require 'pl/temp.cgi';

## �ڎ� ##
#(1)���O�C�����(&login)
#(2)�Ǘ��l��(&kanri)
#(3)HTML���O�t�@�C���X�V����(&mente_html)
#(3.1)HTML���O�t�@�C���X�V�������s(&mente_html_act)
#(4)CGI���O�t�@�C���X�V����(&mente_cgi)
#(4.1)CGI���O�t�@�C���X�V�������s(&mente_cgi_act)
#(5)�o�^�҂��\�����(&temp_to_regist)
#(5.1)�o�^�҂��̏���������s(&temp_to_regist_act)
#(6)�L�[���[�h�����L���O�̐ݒ�(&key_cfg)
#(6.1)�L�[���[�h�����L���O�̐ݒ���s(&key_cfg_act)
#(6.2)�L�[���[�h�����L���O�̏W�v�ΏۊO�̃L�[���[�h���ꊇ�o�^���s(&key_cfg_del_word_act)
#(7)�e�탍�O�ϊ�(&log_conv)
#(7.1)�e�탍�O�ϊ����s(&log_conv_act)
#(7.2)Ver3����J�e�S���ݒ�C���|�[�g���s(&log_conv_kt_act)
#(7.3)�J�e�S���E�\�[�g�ϊ����s(&log_conv_kt_sort)
#(8)���O�f�[�^�̌����E�ړ��E�폜(&log_kt_change)
#(8.1)���O�f�[�^�̌����E�ړ��E�폜���s(&log_kt_change_act)
#(9)���O(�o�^�f�[�^)�̏C��(&log_repair)
#(9.1)���O(�o�^�f�[�^)�̏C�����s(&log_repair_act)
#(10)���O�f�f (&log_mente)
#(10.1)���O�f�f���s (&log_mente_act)
#(11)���ݒ� (&config)
#(12)�J�e�S���ݒ� (&config_kt)
#(13)�l�C�����L���O�̐ݒ�(&rank_cfg)
#(13.1)�l�C�����L���O�̏��������s(&rank_cfg_act)
#(14)�f�b�h�����N�`�F�b�N���(&dl_check)
#(14.1)�f�b�h�����N�`�F�b�N�p�t�@�C�����_�E�����[�h(&dl_check_dl)
#(14.2)�f�b�h�����N�`�F�b�N���s���(&dl_check_act)
#(15)�ُ탍�b�N�����t�@�C������(&ill_lock_del)
#(16)�ȈՃf�U�C���ݒ�(&design)
#(17)�e���v���[�g�t�@�C���̏C��(&template_cfg)
#(18)�o�[�W�������(&ver_info)
#(19)�o�^�҂̃��b�Z�[�W������(&look_mes)


#(cfg1)���ݒ�(%EST)���X�V(&cfg_make)
#(cfg2)���ݒ�(&search_form/&menu_bar)���X�V(&cfg_make_PR_menu)
#(cfg3)���ݒ�(�o�^�����֌W)���X�V (&cfg_make_reg)
#(cfg4)�J�e�S�����������X�V (&cfg_make_kt_ex)
#(cfg5)�J�e�S���ݒ���X�V (&cfg_make_kt)
#(cron1)cron�R�}���h�ɂ��������(&cron)
#(cron1.1)�ʏ�J�e�S���Ɠ���J�e�S�����X�V(&cron_make_kt)

## �ʏ��� ##
#(t1)�t�H�[�����̓f�[�^���������݃f�[�^�ɔ��f(���o�^�����K�o�^�p)
#   (&form_to_temp)
#(t2)symlink�֐��̎g�p�ۂ̃`�F�b�N(&check_symlink)

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
#(1)���O�C�����(&login)
print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/login.html";
}

sub kanri{
#(2)�Ǘ��l��(&kanri)

#�p�X���[�h�`�F�b�N
if($EST{pass} ne "setup"){
&pass_check;
}

#�N�b�L�[�̐ݒ�
&get_cookie;
if($FORM{set}){
	if($FORM{set} eq "�ݒ�"){$CK_data[4]=1;}
	else{$CK_data[4]=0;}
	&set_cookie;
}
if($CK_data[4]){$PRset="�ݒ�";}
else{$PRset="����";}

print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/admin.html";
}


sub mente_html{
#(3)HTML���O�t�@�C���X�V����(&mente_html)
&pass_check;

print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/mente_html.html";

}

sub mente_html_act{
#(3.1)HTML���O�t�@�C���X�V�������s(&mente_html_act)
&pass_check;
local(@TASK_list,%fl,%fl_kt,$kt,$k1,$k2);

##@TASK_fl��ݒ�
#all_fl
if($FORM{all_fl} eq "all"){ #���ׂẴJ�e�S��
@TASK_list=sort keys %ganes;
}
else{ #���̑�
	foreach $kt(sort keys %ganes){
		($k1,$k2)=split(/_/,$kt);
		if($FORM{"kt_fl$kt"}){ #�ȉ��̃J�e�S��
			$fl_kt{$k1}=1;
		}
		if($fl_kt{$k1} && !$fl{$kt}){push(@TASK_list,$kt); $fl{$kt}=1;}
		elsif($FORM{$kt} && !$fl{$kt}){push(@TASK_list,$kt); $fl{$kt}=1;}
	}
}

&lock();
&MK_html(*TASK_list);
require "$EST{log_path}task_ys.cgi";
if($FORM{new}){$TASK{new}=1;} #�V��
if($FORM{renew}){$TASK{renew}=1;} #�X�V
foreach(1 .. 2){ #�}�[�N���𑝂₷���͍X�V
	if($FORM{"m$_"}){$TASK{"m$_"}=1;}
}
&make_task; #�^�X�N�t�@�C�����X�V
&unlock();
if($FORM{continue}>0){
	$mes=<<"EOM";
�J�e�S���pHTML�t�@�C���̍X�V�𑱂��܂����H<br>
[�X�V��]�F<b>$FORM{continue_full}</b>�J�e�S�����A<br>
�@<b>$FORM{continue}</b>�J�e�S�������쐬�ł��B
</ul>
	<div align=center><form action="$EST{admin}" method=post>
	<input type=hidden name=pass value="$FORM{pass}">
	<input type=hidden name=mode value="$FORM{mode}">
	<input type=hidden name=mode value="mente_html_act">
	<input type=hidden name=all_fl value="all">
	<input type=hidden name=continue value="on">
	<input type=submit value="������">
	</form></div>
<div style="margin:15px">
���u������v�{�^����2��ȏ�A���ŉ����Ȃ��ł��������B<br>
���r���Œ��f������ł��uHTML���O�t�@�C���X�V�����v<br>�@
����Ăэ쐬�𑱂��邱�Ƃ��ł��܂��B
</div>
<hr>

EOM
	&mes($mes,"�J�e�S��HTML�t�@�C���쐬","kanri");
}
else{
	&mes("�J�e�S���pHTML�t�@�C���̍X�V���������܂���","�X�V����","kanri");
}
}

sub mente_cgi{
#(4)CGI���O�t�@�C���X�V����(&mente_cgi)
&pass_check;

print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/mente_cgi.html";


}

sub mente_cgi_act{
#(4.1)CGI���O�t�@�C���X�V�������s(&mente_cgi_act)
&pass_check;
local(@kt,$kt,$k1,$k2);

#all_fl
if($FORM{all_fl} eq "all"){ #���ׂẴJ�e�S��
	foreach $kt(sort keys %ganes){
		($k1,$k2)=split(/_/,$kt);
		if(!$k2){push(@TASK_list,$kt);}
	}
}
else{ #���̑�
	foreach $kt(sort keys %ganes){
		($k1,$k2)=split(/_/,$kt);
		if(!$k2 && $FORM{$kt}){push(@TASK_list,$kt);}
	}
}

&lock();
&MK_cgi(*TASK_list);
require "$EST{log_path}task_ys.cgi";
if($FORM{new}){$TASK{new}=1;} #�V��
if($FORM{renew}){$TASK{renew}=1;} #�X�V
foreach(1 .. 2){ #�}�[�N���𑝂₷���͍X�V
	if($FORM{"m$_"}){$TASK{"m$_"}=1;}
}
&make_task; #�^�X�N�t�@�C�����X�V
&unlock();
&mes("�J�e�S���pCGI�t�@�C���̍X�V���������܂���","�X�V����","kanri");


}

sub temp_to_regist{
#(5)�o�^�҂��\�����(&temp_to_regist)
&pass_check;
local($Ctemp=0);
&EST_reg; #�o�^�֘A�̐ݒ�����[�h
open(IN,"$EST{log_path}$EST{temp_logfile}");
	while(<IN>){
	$Ctemp++;
	}
close(IN);

print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/temp_to_regist.html";

}

sub temp_to_regist_act{
#(5.1)�o�^�҂��̏���������s(&temp_to_regist_act)
&pass_check;
require "$EST{log_path}task_ys.cgi";
&EST_reg; #�o�^�p�̐ݒ�����[�h
local(
@TASK_list, #�X�V����J�e�S�����X�g
@log_lines, #���K���O�ւ̏������ݗp���O���X�g
@temp_lines, #���o�^���O�ւ̏������ݗp���O���X�g
@Slog, #�o�^�f�[�^�̈ꎞ�ۑ��p
$Clog_id=1, #�V�K�o�^�p�̓o�^ID
$temp_id, #���o�^����ID
$line,$new,@kt,$kt,@mark,$i,
);

&lock(); #���b�N

	#�V�K�o�^�p��ID���擾
	open(IN,"$EST{log_path}$EST{logfile}");
		while(<IN>){$line=$_;}
	close(IN);
	if($line){($Clog_id)=split(/<>/,$line); $Clog_id++;}


#���[�����M�p���C�u������ǂݍ���
if($EST{mail_new}){require "pl/mail_ys.cgi";}


open(IN,"$EST{log_path}$EST{temp_logfile}");
	while(<IN>){
		@Tlog=split(/<>/,$_);
		if($FORM{"R$Tlog[0]"} eq "reg"){ #�o�^
			&form_to_temp;
			$new=join("<>",@Slog);
			$new=~s/\n//g; $new .="<>\n";
			push(@log_lines,$new);
			if($EST{mail_new}){
				&temp_to_regist_mail; #���[���𑗐M
			}
			@kt=split(/&/,$Slog[10]);
			
			foreach $kt(@kt){ #�J�e�S�����X�g���X�V
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
			foreach(@mark){ #�}�[�N���X�V
				if($_){$TASK{"m$i"}=1;}
				$i++;
			}
			$TASK{"new"}=1; #�V�����X�V
			
		}
		elsif(!$FORM{"R$Tlog[0]"}){ #�ۗ�
			push(@temp_lines,$_);
		}
	}
close(IN);


#�{�̃��O�f�[�^�ɏ�������
open(OUT,">>$EST{log_path}$EST{logfile}");
	print OUT @log_lines;
close(OUT);

#���o�^�f�[�^���X�V
open(OUT,">$EST{log_path}$EST{temp_logfile}");
	print OUT @temp_lines;
close(OUT);


sub temp_to_regist_mail{
#���o�^���V�K�o�^���̃��[���𑗐M
$Slog[6]=~s/<br>/\n/g; $Slog[7]=~s/<br>/\n/g;
if($EST{mail_to_admin} && $EST{mail_new}){ #�Ǘ��l�փ��[�����M
	&mail($EST{admin_email},$Slog[9],"$EST{search_name} �V�K�o�^�����ʒm","new","admin",*Slog,$FORM{"Fsougo$Tlog[0]"},$FORM{"Fadd_kt$Tlog[0]"},$FORM{"Fto_admin$Tlog[0]"},$FORM{"Fto_reg$Tlog[0]"});
}
if($EST{mail_to_register} && $EST{mail_new}){ #�o�^�҂փ��[�����M
	&mail($Slog[9],$EST{admin_email},"$EST{search_name} �V�K�o�^�����ʒm","new","",*Slog,$FORM{"Fsougo$Tlog[0]"},$FORM{"Fadd_kt$Tlog[0]"},$FORM{"Fto_admin$Tlog[0]"},$FORM{"Fto_reg$Tlog[0]"});
}
$Slog[6]=~s/\n/<br>/g; $Slog[7]=~s/\n/<br>/g;
}

##�h���t�@�C���̏���
if($EST{html} && $EST{task} ne "2"){ #��������(html && !cron)
local($data_fl,$data_no); #�t���O/�t�B�[���h�̓Y�����ԍ�
	($data_fl)=split(/_/,$EST{defo_hyouji});
	if($data_fl eq "mark"){$data_no=3;}
	elsif($data_fl eq "id"){$data_no=0;}
	elsif($data_fl eq "time"){$data_no=11;}
	elsif($data_fl eq "ac"){$data_no=1;}
	else{$data_no=3;}

&MK_html(*TASK_list);
&make_task;
}
else{&make_task;} #�^�X�N�t�@�C���ɏ�������

&count_log;

&unlock(); #���b�N����

&mes("���o�^�f�[�^�̏������������܂���","���o�^�f�[�^��������","kanri");

}


sub key_cfg{
#(6)�L�[���[�h�����L���O�̐ݒ�(&key_cfg)
&pass_check;
if(-s "$EST{log_path}keyrank_temp_ys.cgi"){&keyrank_trace;} #�ꎞ�t�@�C�����W�v�t�@�C��
else{require "$EST{log_path}keyrank_ys.cgi";}
print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/key_cfg.html";
}

sub key_cfg_act{
#(6.1)�L�[���[�h�����L���O�̐ݒ���s(&key_cfg_act)
&pass_check;
	 #�Ǘ��l�ɂ��L�[���[�h�����L���O�̍X�V�����s
	if($FORM{make_keyrank} eq "on"){
		#$kousin_fl���u1�v�̂Ƃ��̓����L���O��������(�ߋ��̃����L���O�Ƀf�[�^���ڍs
		if($FORM{keyrank_format}){
		$kousin_fl=1;
		$BK_last_keyrank=time();
		&make_task; #�^�X�N�t�@�C�����X�V
		}
		else{$kousin_fl=0;}
		&key_cfg_make_rank($kousin_fl); #�L�[���[�h�����L���O���쐬
		&mes("�L�[���[�h�����L���O�̍X�V���������܂���","�L�[���[�h�����L���O�X�V����","kanri");
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

&mes("�L�[���[�h�\\���ݒ�̕ύX���������܂���","�L�[���[�h�\\���ݒ�̕ύX����","kanri");
}

sub key_cfg_del_word_act{
#(6.2)�L�[���[�h�����L���O�̏W�v�ΏۊO�̃L�[���[�h���ꊇ�o�^���s(&key_cfg_del_word_act)
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


&mes("�W�v�ΏۊO�̃L�[���[�h�̈ꊇ�o�^���������܂���","�o�^����","kanri");
}

sub log_conv{
#(7)�e�탍�O�ϊ�(&log_conv)
&pass_check;

print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/log_conv.html";

}

sub log_conv_act{
#(7.1)�e�탍�O�ϊ����s(&log_conv_act)
&pass_check;
if($FORM{check} ne "on"){&mes("�m�F�`�F�b�N������Ă��܂���B<br>�߂��ă`�F�b�N���Ă�����s���Ă��������B","�`�F�b�N�G���[","java");}

unless(-f $FORM{bf_file}){&mes("�G���[�F$bf_file ��������܂���","�t�@�C����������܂���","java");}
else{
&lock;
	if($FORM{log_mode} eq "v3tov4"){
		&henkan_v3tov4();
		$PR_msg="Ver3�`����Ver4�`���ւ̕ϊ����������܂���";
	}
	if($FORM{log_mode} eq "v2tov4"){
		&henkan_v2tov4();
		$PR_msg="Ver2�`����Ver4�`���ւ̕ϊ����������܂���";
	}
	elsif($FORM{log_mode} eq "v4tocsv"){
		if(!$FORM{download}){&henkan_v4tocsv();}
		else{
			&unlock;
				print "Content-type: application/octet-stream .csv\n\n";
				open(IN,"./$FORM{bf_file}");
					while(<IN>){
						$i=0;
						$_=~s/,/�C/g; $_=~s/"/�h/g; $_=~s/\n//g;
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
		$PR_msg="Ver4�`����CSV�`���ւ̕ϊ����������܂���";
	}
	elsif($FORM{log_mode} eq "csvtov4"){
		&henkan_csvtov4();
		$PR_msg="CSV�`����Ver4�`���ւ̕ϊ����������܂���";
	}
&unlock;
}

&mes("$PR_msg","�ϊ��I��","kanri");

}

sub henkan_v3tov4{
local($line,@Slog);

open(IN,"./$FORM{bf_file}");
open(OUT,">./$FORM{af_file}");
	while(<IN>){
		@Slog=split(/<>/,$_);
			#�}�[�N
			if($Slog[3]==0){$Slog[3]="0_0";}
			elsif($Slog[3]==1){$Slog[3]="1_0";}
			elsif($Slog[3]==2){$Slog[3]="0_1";}
			else{$Slog[3]="1_1";}
			#�J�e�S��
			$Slog[10]=~s/,/&/g;
			#�A�N�Z�X�����L���O
			$Slog[13]=$Slog[13] . "_" . $Slog[13] . "_0_0";
			#�L�[���[�h
			$Slog[15]=~s/,/ /g;
		$line=join("<>",@Slog);
		$line=~s/\n//g;
		$line=~s/,/�C/g; $line=~s/"/�h/g;
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
			#�}�[�N
			if($Slog[3]==0){$Slog[3]="0_0";}
			elsif($Slog[3]==1){$Slog[3]="1_0";}
			elsif($Slog[3]==2){$Slog[3]="0_1";}
			else{$Slog[3]="1_1";}
			#�J�e�S��
			$Slog[10]=~s/,/&/g;
			#�A�N�Z�X�����L���O
			$Slog[13]=$Slog[13] . "_" . $Slog[13] . "_0_0";
			#�L�[���[�h
			$Slog[15]=" ";
		$line=join("<>",@Slog);
		$line=~s/\n//g;
		$line=~s/,/�C/g; $line=~s/"/�h/g;
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
		$_=~s/,/�C/g; $_=~s/"/�h/g; $_=~s/\n//g;
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
#(7.2)Ver3����J�e�S���ݒ�C���|�[�g���s(&log_conv_kt_act)
&pass_check;

if($FORM{check} ne "on"){&mes("�m�F�`�F�b�N�Ƀ`�F�b�N�����Ă��������x���s���Ă�������","�m�F�`�F�b�N�����Ă�������","java");}

unless(-f $FORM{cfg_bf_file}){&mes("$FORM{cfg_bf_file}�͑��݂��܂���","�G���[","java");}

local(%t_kt,%t_kt_top,%t_kt_ref,%t_kt_ex);
#�J�e�S������%t_kt(�J�e�S���ԍ�,�J�e�S����)
#�g�b�v�\��������%t_kt_top(�J�e�S���ԍ�,1)
#�o�^�s������%t_kt_no_regist(�J�e�S���ԍ�,1)
#�Q�ƃJ�e�S��������%t_kt_ref(�J�e�S���ԍ�,(�J�e�S��&�J�e�S���c))
#�J�e�S����������%t_kt_ex(�J�e�S���ԍ�,������)

	#%KTEX��%KTEX_pre�ɃR�s�[
	%KTEX_pre=%KTEX;
	%KTEX=();

require $FORM{cfg_bf_file};

	if($#ganes<0){&mes("$FORM{cfg_bk_file}�́A�J�e�S���ݒ�t�@�C���ł͂���܂���","�G���[","java");}

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

	if($FORM{r_mode} eq "change"){ #�����ւ����[�h�̂Ƃ�
		if($FORM{kt_no_name} eq "on"){%ganes=();} #�J�e�S��
		if($FORM{kt_top} eq "on"){%gane_top=();} #�g�b�v�\������
		if($FORM{kt_no_regist} eq "on"){%gane_UR=();} #�o�^�s����
		if($FORM{kt_ref} eq "on"){%gane_ref=();} #�Q�ƃJ�e�S������
		if($FORM{kt_ex} eq "on"){%KTEX=();} #�J�e�S��������
	}
	
local($key,$value);
	if($FORM{kt_no_name} eq "on"){ #�J�e�S��
		while(($key,$value)=each %t_kt){
			$ganes{$key}=$value;
		}
	}
	if($FORM{kt_no_regist} eq "on"){ #�o�^�s����
		while(($key,$value)=each %t_kt_no_regist){
			$gane_UR{$key}=$value;
		}
	}
	if($FORM{kt_top} eq "on"){ #�g�b�v�\������
		while(($key,$value)=each %t_kt_top){
			$gane_top{$key}=$value;
		}
	}
	if($FORM{kt_ref} eq "on"){ #�Q�ƃJ�e�S������
		while(($key,$value)=each %t_kt_ref){
			$gane_ref{$key}=$value;
		}
	}
	if($FORM{kt_ex} eq "on"){ #�J�e�S��������
		while(($key,$value)=each %t_kt_ex){
			$KTEX{$key}=$value;
		}
	}
	
	if($FORM{r_mode} eq "rewrite"){
		while(($key,$value)=each %KTEX_pre){
			$KTEX{$key}=$value;
		}
	}

	#���̑��̃J�e�S����������
	@gane_other=();
	foreach(sort keys %ganes){
		if(index($_,"_")<0){push(@gane_other,$_);}
	}
	
	#�J�e�S���������ɓ���J�e�S����������ǉ�
	$KTEX{new_ys}="��14���ȓ��ɓo�^���ꂽ�T�C�g";
	$KTEX{renew_ys}="��14���ȓ��ɍX�V���ꂽ�T�C�g";
	$KTEX{rank}="���l�C�����L���O���x�X�g100�ʂ܂ŏЉ�Ă��܂�";
	$KTEX{rank_bf}="���O��̃����L���O���x�X�g100�ʂ܂ŏЉ�Ă��܂�";


	#�������ޑO�ɔO�̂��߁A�t�H�[��������s�K�v�ȏ���
	delete $FORM{cfg_bf_file}; delete $FORM{r_mode};
	delete $FORM{kt_no_name}; delete $FORM{kt_top};
	delete $FORM{kt_no_regist}; delete $FORM{kt_ref};
	delete $FORM{kt_ex}; delete $FORM{check};

&cfg_set(0,1,1);

&mes("Ver3����̃J�e�S���ݒ�̈ڍs���������܂���","�ݒ芮��","kanri");
}

sub log_conv_kt_sort{
#(7.3)�J�e�S���E�\�[�g�ϊ����s(&log_conv_kt_sort)
&pass_check;
if($FORM{check} ne "on"){&mes("�m�F�`�F�b�N�Ƀ`�F�b�N���Ă���ϊ��{�^���������Ă�������","�`�F�b�N�~�X","java");}

	if($FORM{bk_mode} eq "on"){ #�������[�h�̂Ƃ�
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
	&mes("���ݒ�̕������������܂���","��������","kanri");
	}

	#$FORM{all}�̏���
	if($FORM{all} eq "on"){
		local($key,$value);
		while(($key,$value)=each %ganes){
			if(index($key,"_")<0){$FORM{$key}="on";}
		}
	}

	#$FORM{kt_str}�����
	if($FORM{kt_str}){
		if($FORM{kt_str}=~/[^\w\-\,]/){&mes("�J�e�S���w�蕶�ɑS�p�������܂܂�Ă��܂�","�G���[","java");}
		local(@kt_str,@del_list);
		@kt_str=split(/,/,$FORM{kt_str});
		foreach(@kt_str){
			if(/^(\d+)(n*)\-(\d+)(n*)$/){
				local($kt1=$1,$kt2=$3,$keta1,$keta2,$n_fl=0);
				if($4 eq "n"){$n_fl=1;}
				$kt1=~m/(0*)([1-9]+)/; $keta1=length($kt1);
				$kt2=~m/(0*)([1-9]+)/; $keta2=length($kt2);
					if($keta1 ne $keta2){&mes("�J�e�S���w�蕶���Ԉ���Ă��܂��F<b>$_</b>","�G���[","java");}
					local($i=1,$kt1_j);
					while($kt1 ne $kt2){
						$kt1_j=sprintf("%d",$kt1);
							if(!$n_fl){$FORM{$kt1}="on";}
							else{push(@del_list,$kt1);}
						$kt1_j++;
						$kt1=sprintf("%0${keta1}d",$kt1_j);
						$i++;
						if($i>5000){&mes("<b>-</b> �� 5000�ȏ�̘A������J�e�S�����w�肷�邱�Ƃ͂ł��܂���","�G���[","java");}
					}
						if(!$n_fl){$FORM{$kt2}="on";}
						else{push(@del_list,$kt2);}
			}
			elsif(/(\d+)(n*)/){
				if($2 eq "n"){push(@del_list,$1);}
				else{$FORM{$1}="on";}
			}
			else{&mes("�J�e�S���w�蕶���Ԉ���Ă��܂�","�G���[","java");}
		}
		foreach(@del_list){
			$FORM{$_}="";
		}
	}
	
	
	#�J�e�S�����X�g����ϊ��Ώۂ̃J�e�S���p��%kt_af,%kt_name_af���쐬
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
	
		#�ekt���ω�����J�e�S�����Ē�`
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
	
	#���b�N
	&lock();
	
	#%ganes��ϊ����A��������
		#/pl/cfg.cgi���o�b�N�A�b�v
		if($FORM{bk_cfg_no} ne "on"){
		open(IN,"pl/cfg.cgi");
		open(OUT,">$FORM{bk_file_cfg}");
			while(<IN>){
				print OUT $_;
			}
		close(OUT);
		close(IN);
		}
		#/$EST{log_path}$EST{logfile}���o�b�N�A�b�v
		if($FORM{bk_ys4_no} ne "on"){
		open(IN,"$EST{log_path}$EST{logfile}");
		open(OUT,">$FORM{bk_file_ys4}");
			while(<IN>){
				print OUT $_;
			}
		close(OUT);
		close(IN);
		}
		#/$EST{log_path}other_cfg.cgi���o�b�N�A�b�v
		if($FORM{bk_other_cfg_no} ne "on"){
		open(IN,"pl/other_cfg.cgi");
		open(OUT,">$FORM{bk_file_other_cfg}");
			while(<IN>){
				print OUT $_;
			}
		close(OUT);
		close(IN);
		}
		
		#�����������[�h
		&EST_reg; &gane_st; &gane_guide;
		%gane_top_bk=%gane_top;
		%gane_st_bk=%ganes_st; %gane_ref_bk=%gane_ref;
		%gane_UR_bk=%gane_UR; %KTEX_bk=%KTEX;
	while(($key,$value)=each %ganes){
		if($kt_af{$key}){
			delete $ganes{$key};
			#������ %gane_top/%gane_st/%gane_ref/%gane_UR/%KTEX/ 
			delete $gane_top{$key};
			delete $gane_st{$key};
			delete $gane_ref{$key};
			delete $gane_UR{$key};
			delete $KT_EX{$key};
		}
	}
	while(($key,$value)=each %kt_af){
		$ganes{$value}=$kt_name_af{$value};
		#������
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
	
	#���̑��̊��ݒ�t�@�C��(other_cfg.cgi)��ϊ����A��������
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
	
	#�{�̃��O���X�V
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
	
	#�h���J�e�S�����X�V
	require "$EST{log_path}task_ys.cgi";
	
	#�X�V����J�e�S�����X�g���쐬
		#%TASK/@TASK_list���g�p
		@TASK_list=();
		$TASK{"new"}=$TASK{"renew"}=$TASK{"m1"}=$TASK{"m2"}=1; #����J�e�S��

		while(($key,$value)=each %ganes){
			if(index($key,"_")<0 && $FORM{$key} eq "on"){$TASK{$key}=1;}
		}
		##�h���t�@�C���̏���
		unless($EST{html} && $EST{task} ne "2"){&make_task;} #�^�X�N�t�@�C���ɏ�������
	
	#���b�N����
	&unlock();

&mes("�J�e�S���E�\\�[�g�ϊ����������܂���","�J�e�S���E�\\�[�g�ϊ�����","kanri");
}

sub log_kt_change{
#(8)���O�f�[�^�̌����E�ړ��E�폜(&log_kt_change)
&pass_check;

print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/log_kt_change.html";

}

sub log_kt_change_act{
#(8.1)���O�f�[�^�̌����E�ړ��E�폜���s(&log_kt_change_act)
&pass_check;
if($FORM{check} ne "on"){&mes("�m�F�`�F�b�N������Ă��܂���B<br>�߂��ă`�F�b�N���Ă�����s���Ă��������B","�`�F�b�N�G���[","java");}
	
	#�L���R��̃`�F�b�N
	if($FORM{log_mode} eq "change"){
		if(!$FORM{change_kt1} || !$FORM{change_kt2}){&mes("�����Ώۂ̃J�e�S�����w�肵�Ă�������","�J�e�S���I���~�X","java");}
	}
	elsif($FORM{log_mode} eq "move"){
		if(!$FORM{bf_move_kt} || !$FORM{af_move_kt}){&mes("�ړ��Ώۂ̃J�e�S�����w�肵�Ă�������","�J�e�S���I���~�X","java");}
	}
	elsif($FORM{log_mode} eq "del"){
		if(!$FORM{del_kt}){&mes("�폜�Ώۂ̃J�e�S����I�����Ă�������","�J�e�S���I���~�X","java");}
	}
	else{&mes("log_mode���I������Ă��܂���","log_mode�I���G���[","java");}

&lock;
require "$EST{log_path}task_ys.cgi";
local($PR_mes,@kousin_kt);
	if($FORM{log_mode} eq "change"){ #change
		#���O�f�[�^�̌���
		$PR_mes="���O�f�[�^�̌������������܂���<br>�w" . &full_kt($FORM{change_kt1}) . "}�x�Ɓw" . &full_kt($FORM{change_kt2}) . "�x���������܂���";
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
		#���O�f�[�^�̈ړ�
		$PR_mes="���O�f�[�^�̈ړ����������܂���<br>�w" . &full_kt($FORM{bf_move_kt}) . "�x���w" . &full_kt($FORM{af_move_kt}) . "�x�Ɉړ����܂���";
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
		#���O�f�[�^�̍폜
		$PR_mes="���O�f�[�^�̍폜���������܂���<br>�w" . &full_kt($FORM{del_kt}) . "�x���폜���܂���";
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

	##�ύX�����f�[�^�Ɋւ���h���t�@�C�����X�V
	if($EST{html} && $EST{task}){
		&MK_html(*kousin_kt);
	}
	else{
		#cgi�`���̏ꍇ�ɂ̓J�e�S�����J�e�S��������
		local($i=0,$kt,@kt,%fl);
		foreach $kt(@kousin_kt){
			($kt)=split(/_/,$kt);
			if(!$fl{$kt}){$kousin_kt[$i]=$kt; $fl{$kt}=1;}
			else{$kousin_kt[$i]="";}
			$i++;
		}
		&MK_cgi(*kousin_kt);
	}

	#���ׂĂ̓���J�e�S�����X�V
	$TASK{new}=$TASK{renew}=1;
	foreach(1 .. 2){ #�}�[�N���𑝂₷���͏C��
		$TASK{"m$_"}=1;
	}
	&make_task;

##�o�^�����Čv�Z
&count_log;

&unlock;

&mes($PR_mes,"���O�f�[�^�̌����E�ړ��E�폜����","kanri");

}

sub log_repair{
#(9)���O(�o�^�f�[�^)�̏C��(&log_repair)
print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/log_repair.html";
}

sub log_repair_act{
#(9.1)���O(�o�^�f�[�^)�̏C�����s(&log_repair_act)
require "$EST{log_path}task_ys.cgi";
local($BK_file,$i);
	#�C���Ώۂ̃��O��ݒ�
	if($BK_file_no-1>0){$BK_file=$BK_file_no-1;}
	else{$BK_file=$EST{bk_days};}
	$i=$BK_file;
	foreach(1 .. $EST{bk_days}){
		if($FORM{bk_day} eq "$_���O�̃f�[�^�ɖ߂�"){
			if($FORM{"check$_"} ne "on"){&mes("�C���m�F�̂��߁A�m�F�`�F�b�N�����Ă��������x���s���Ă�������","�m�F�`�F�b�N�����Ă�������","java");}
			$BK_file="$EST{log_path}bkup" . $i . ".cgi";
		}
		if($i<=1){$i=$EST{bk_days};}
		else{$i--;}
	}

unless(-f $BK_file){&mes("$BK_file ��������܂���","�G���[","java");}
&lock();

open(IN,"$BK_file");
open(OUT,">$EST{log_path}$EST{logfile}");
	while(<IN>){
		print OUT $_;
	}
close(OUT);
close(IN);

&unlock();

&mes("�f�[�^�̏C�����������܂���\$BK_file=$BK_file","�C������","kanri");
}

sub log_mente{
#(10)���O�f�f (&log_mente)
#	�E�t�B�[���h���𐳏�ɂ���
#	�E����`�J�e�S�����폜
#	�E�����J�e�S����0�̃f�[�^��C�ӂ̃J�e�S���Ɉړ����͍폜

&pass_check;

print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/log_mente.html";
}

sub log_mente_act{
#(10.1)���O�f�f���s (&log_mente_act)
&pass_check;

	#���̓R�}���h�̐����`�F�b�N�����`
	##�f�[�^�t�B�[���h���̐��`
	$FORM{fld_custom}=~s/\D//g;
	if($FORM{set_fld} eq "custom" && (!$FORM{fld_custom} || $FORM{fld_custom}<15)){
		&mes("�f�[�^�t�B�[���h�����w�肵�Ă�������<br>$Efld�����̐��͎w��ł��܂���","�L���~�X","java");
	}
	local($Cfld,$plus_fld);
	if($FORM{set_fld} eq "custom"){$Cfld=$FORM{fld_custom};}
	else{$Cfld=$Efld;} #�f�t�H���g�l(temp.cgi�Őݒ�)
	local($fld=$FORM{fld_custom}-$Efld);
	if($fld>0){
		foreach(1 .. $fld+1){
			$plus_fld .="<>";
		}
	}
	
	##����`�f�[�^�̈ړ���̐ݒ�
	if($FORM{set_no} eq "move" && !$FORM{set_no_move_kt}){
		&mes("�ړ���̃J�e�S�����w�肵�Ă�������","�L���~�X","java");
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
			$kt=""; $del_fl=0; #�폜�t���O
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
&mes("���O�f�f���������܂���","���O�f�f����","kanri");
}

sub config{
#(11)���ݒ� (&config)
print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/config.html";
}

sub config_kt{
#(12)�J�e�S���ݒ� (&config_kt)
print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/config_kt.html";
}

sub rank_cfg{
#(13)�l�C�����L���O�̐ݒ�(&rank_cfg)
&pass_check;

print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/rank_cfg.html";
}

sub rank_cfg_act{
#(13.1)�l�C�����L���O�̏��������s(&rank_cfg_act)
&pass_check;

if($FORM{rank_format}){
	require "$EST{log_path}task_ys.cgi";
	&lock;
	&rank_cfg_make_rank(1);
	$BK_last_rank=$BK_last_rank_t=time();
	&make_task; #�^�X�N�t�@�C�����X�V
	&unlock;
}
else{&mes("�l�C�����L���O�������̂��߂̊m�F�`�F�b�N������Ă��܂���̂ł�����x�߂��ă`�F�b�N�����Ă�����s���Ă�������","�m�F�`�F�b�N�����Ă�������","java");}
&mes("�l�C�����L���O�̏��������������܂���","�l�C�����L���O����������","kanri");

}

#(13.2)�l�C�����L���O�t�@�C�����X�V(&rank_cfg_make_rank)
#��temp.cgi��

sub dl_check{
#(14)�f�b�h�����N�`�F�b�N���(&dl_check)
&pass_check;

	#no_link_temp.cgi ���� no_link.cgi �Ƀf�[�^���ڍs����
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
				$count{"${_}_$data[0]"}++; #�f�[�^�̕񍐐�
				$count{$data[0]}++;
				}
				$fl{"$data[0]_$data[1]"}=1; #�Q�d�`�F�b�N
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
#(14.1)�f�b�h�����N�`�F�b�N�p�t�@�C�����_�E�����[�h(&dl_check_dl)
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
#(14.2)�f�b�h�����N�`�F�b�N���s���(&dl_check_act)
&pass_check;
unless(-f $FORM{checkfile}){&mes("�w�肳�ꂽ�t�@�C���͑��݂��܂���","�G���[","java");}

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
#(15)�ُ탍�b�N�����t�@�C������(&ill_lock_del)

$FORM{file}=~s/[^\w.]//g;

if($FORM{act} ne "on"){
print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/ill_lock_del.html";
}
else{ #�������s
&pass_check;
	unless(-f "lock/$FORM{file}"){&mes("lock/$FORM{file}�͑��݂��܂���","�G���[","java");}
	if($FORM{set} eq "�폜����" && $FORM{check} ne "on"){&mes("�폜�m�F�̃`�F�b�N�����Ă�������","�G���[","java");}
	if($FORM{set} eq "�폜����"){ #�폜
		unlink("lock/$FORM{file}");
		&mes("<b>lock/$FORM{file}</b>���폜���܂���","�폜����",$EST{home});
	}
	else{ #�_�E�����[�h
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
#(16)�ȈՃf�U�C���ݒ�(&design)
&pass_check;

if($FORM{set} eq "�ݒ���s"){
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
&mes("�ȈՃf�U�C���ݒ肪�������܂���","�ȈՃf�U�C���ݒ芮��","kanri");
}
else{
print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/design.html";
}

}

sub template_cfg{
&pass_check;
#(17)�e���v���[�g�t�@�C���̏C��(&template_cfg)
$FORM{read_file}=~s/\|//g;
	if($FORM{read_file}){ #�ǂݍ��ރt�@�C���̃`�F�b�N
		unless(-f "./$EST{temp_path}$FORM{read_file}"){&mes("�w�肳�ꂽ�t�@�C���͉{���s�ł�","�G���[","java");}
	}

if(!$FORM{set}){
print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/template_cfg.html";
}
elsif($FORM{set} eq "�ҏW���s"){
	open(OUT,">./$EST{temp_path}$FORM{write_file}");
		$FORM{file_str}=~s/�f/'/g;
		print OUT $FORM{file_str};
	close(OUT);

&mes("�u$FORM{write_file}�v�̕ҏW���������܂���","�ҏW����","kanri");
}
else{&mes("���[�h���s���ł�","�G���[","java");}

}

sub ver_info{
#(18)�o�[�W�������(&ver_info)
&pass_check;
print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/ver_info.html";
}

sub look_mes{
#(19)�o�^�҂̃��b�Z�[�W������(&look_mes)
&pass_check;
print "Content-type: text/html\n\n";
require "$EST{temp_path}admin/look_mes.html";
}

sub cfg_make{
#(cfg1)���ݒ�(%EST)���X�V(&cfg_make)

#�p�X���[�h�`�F�b�N
if($EST{pass} ne "setup"){
&pass_check;
}

local($key,$bf_pass=$FORM{pass});

		##�p�X���[�h���Í�������
		if($FORM{new_pass}){$bf_pass=$FORM{pass}=$FORM{new_pass};}
		if($EST{crypt}){$FORM{pass}=crypt("$FORM{pass}","ys");}

	foreach $key(keys %EST){ #���ݒ�(%EST)���X�V
		if(defined $FORM{$key}){$EST{$key}=$FORM{$key}}
	}
	
		##�p�X���[�h���Í����O�ɖ߂�
		$FORM{pass}=$bf_pass;
	
	##
	

	&cfg_set();
}

sub cfg_set{
#(cfg1.1)���ݒ�t�@�C�����X�V(&cfg_set)
local(
$EST_reg_fl=$_[0], #sub EST_reg���X�V(1/0)
$gane_st_fl=$_[1], #sub gane_st���X�V(1/0)
$gane_guide_fl=$_[2], #sub gane_guide���X�V(1/0)
$exit_fl=$_[3], #�I������=0/���Ȃ�=1)
);

#�C���t���O�œǂݍ��ނ��ǂ����𔻒�
if(!$EST_reg_fl){&EST_reg;}
if(!$gane_st_fl){&gane_st;}
if(!$gane_guide_fl){&gane_guide;}

#&search_form/&menu_bar/&head_sp/&foot_sp��ǂݍ���
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

##%EST���X�V
require "$EST{temp_path}admin/cfg_lib.cgi";

close(OUT);

##�o�^�����Čv�Z
&count_log;

if(!$exit_fl){
	&mes("���ݒ�̕ύX/�J�e�S���̐ݒ肪�������܂���","���ݒ�/�J�e�S���ݒ芮��","kanri");
}

}

sub cfg_make_PR_menu{
#(cfg2)���ݒ�(&search_form/&menu_bar)���X�V(&cfg_make_PR_menu)
&pass_check;

local($fl=0,$p_fl=1,$bf_data,@file_data);
$FORM{search_form}=~s/&lt;/</g; $FORM{search_form}=~s/&gt;/>/g; $FORM{search_form}=~s/�f/'/g;
$FORM{menu_bar}=~s/&lt;/</g; $FORM{menu_bar}=~s/&gt;/>/g; $FORM{menu_bar}=~s/�f/'/g;
$FORM{head_sp}=~s/&lt;/</g; $FORM{head_sp}=~s/&gt;/>/g; $FORM{head_sp}=~s/�f/'/g;
$FORM{foot_sp}=~s/&lt;/</g; $FORM{foot_sp}=~s/&gt;/>/g; $FORM{foot_sp}=~s/�f/'/g;

	#���@�`�F�b�N
	{local($mes="");
	open(DM,"<./lock/index.html");
	select(DM);
	eval $FORM{search_form};
	if($@){$mes="�O�������G���W���̐ݒ�";}
	eval $FORM{menu_bar};
	if($@){$mes="���j���[�o�[�̐ݒ�";}
	eval $FORM{head_sp};
	if($@){$mes="�w�b�_�X�y�[�X�̐ݒ�";}
	eval $FORM{foot_sp};
	if($@){$mes="�t�b�^�X�y�[�X�̐ݒ�";}
	
	if($mes){select(stdout);&mes("�u<b>$mes</b>�v�̋L���ŃG���[���o�܂����B<br>(1)��s�ڂ́uprint<<\"EOM\";�v�ƍŏI�s�́uEOM�v��<br>�@\�폜����Ă��Ȃ����m�F���Ă�������<br>(2)�u\@�v�Ǝg�p����ꍇ�ɂ́u\\\@�v�ƋL�����Ă�������","�L���G���[","java");}
	
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

&mes("���j���[�o�[/�O�������G���W��/�w�b�_�E�t�b�^�X�y�[�X�̐ݒ肪�������܂���","�X�V����","kanri");
}

sub cfg_make_reg{
#(cfg3)���ݒ�(�o�^�����֌W)���X�V (&cfg_make_reg)
&pass_check;
&EST_reg;
local($key);
	foreach $key(keys %EST_reg){ #���ݒ�(%EST_reg)���X�V
		if(defined $FORM{$key}){$EST_reg{$key}=$FORM{$key}}
	}
	&cfg_set(1);
}

sub cfg_make_kt_ex{
#(cfg4)�J�e�S�����������X�V (&cfg_make_kt_ex)
&pass_check;
&gane_guide;
local($key,@new,@ktex);
	foreach $key(keys %KTEX){ #���ݒ�(%KTEX)���X�V
		if($FORM{"d_$key"}){delete $KTEX{$key};}
		elsif(defined $FORM{"ex_$key"}){$KTEX{$key}=$FORM{"ex_$key"}}
	}
		#�V�K�ǉ������`
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
#(cfg5)�J�e�S���ݒ���X�V (&cfg_make_kt)
&pass_check;
&gane_st;
require "pl/other_cfg.cgi";
local($key,@new,@kt);
	
	if($FORM{mente_mode} eq "mente"){
	@gane_other=();
	foreach $key(keys %ganes){ #�J�e�S���ݒ�(%ganes)���X�V
		if($FORM{"d_$key"}){delete $ganes{$key};}
		elsif(defined $FORM{"kt_$key"}){ #�J�e�S���������
			$ganes{$key}=$FORM{"kt_$key"};
				if($FORM{"t_$key"}){$gane_top{$key}=1;}
				elsif($gane_top{$key}){delete $gane_top{$key};}
				if($FORM{"o_$key"}){push(@gane_other,$key);}
				if($FORM{"no_$key"}){$gane_UR{$key}=1;}
				elsif($gane_UR{$key}){delete $gane_UR{$key};}
				if($FORM{"ref_$key"}){$gane_ref{$key}=$FORM{"ref_$key"};}
				elsif($gane_ref{$key}){delete $gane_ref{$key};}
		}
			#���̑��̃J�e�S�����`
			@gane_other=sort @gane_other;
			
			#�ӂ肪�Ȃ̐ݒ�
			$EST_furi{$key}=$FORM{"furi_$key"}; #$EST_furi{$key}=~s/'/�f/g;
	}
		#�ӂ肪�Ȃ�ݒ�
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
		#�V�K�ǉ������`
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
#(cfg6)�T�C�g�}�b�v���쐬(&sitemap_make)
open(OUT,">$EST{html_path}sitemap.html");
	select(OUT);
	require "$EST{temp_path}sitemap.html";
	select(stdout);
close(OUT);
}


sub cron{
#(cron1)cron�R�}���h�ɂ��������(&cron)
&pass_check;
&go_TASK;
&mes("cron�R�}���h�ɂ�����������������܂���","�X�V����","java");
}

sub cron_make_kt{
#(cron1.1)�ʏ�J�e�S���Ɠ���J�e�S�����X�V(&cron_make_kt)
#��&go_TASK����Ăяo�����(���b�N�͈͓�)
local(@kt_list,@other_kt_list,$kt);

#�X�V���郊�X�g���i�[
foreach $kt(keys %TASK){
	if($ganes{$kt}){push(@kt_list,$kt);} #�ʏ�J�e�S��
	else{push(@other_kt_list,$kt);} #����J�e�S��
}

##�ʏ�J�e�S�����X�V
if($#kt_list>=0){
	if(!$EST{html}){ #CGI�Ń��O�\��
		&MK_cgi(*kt_list);
	}
	else{ #HTML�Ń��O�\��
		&MK_html(*kt_list);
	}
}

##����J�e�S�����X�V
if($#other_kt_list>=0){
	foreach $kt(@other_kt_list){
		local(@kt_list);
		@kt_list=($kt);
		&MK_cgi_other(*kt_list,$kt);
	}
}

%TASK=();



}



##-- �ʏ��� --#

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
	if($_[2] eq "java"){
	$BACK_URL="<form><input type=button value=\"&nbsp;&nbsp;&nbsp;&nbsp;�߂�&nbsp;&nbsp;&nbsp;&nbsp;\" onClick=\"history.back()\"></form>"
	}
	elsif($_[2] eq "env"){
	$BACK_URL="�y<a href=\"$ENV{'HTTP_REFERER'}\">�߂�</a>�z";
	}
	elsif($_[2] eq "kanri"){
	$BACK_URL="<form action=\"$EST{admin}\" method=post><input type=hidden name=mode value=kanri><input type=hidden name=pass value=\"$FORM{pass}\"><input type=submit value=\"�Ǘ�����\"></form>"
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
           $name=~tr/+/ /;
           $value =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
           $name =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
					 $value=~s/'/�f/g;
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
#(t1)�t�H�[�����̓f�[�^���������݃f�[�^�ɔ��f(���o�^�����K�o�^�p)
#   (&form_to_temp)
$temp_id=$Tlog[0];

#�o�^ID(0)
$Slog[0]=$Clog_id;

#�^�C�g��(1)
$Slog[1]=$FORM{"Ftitle$temp_id"};

#URL(2)
$Slog[2]=$FORM{"Furl$temp_id"};

#�}�[�N�f�[�^(3)
$Slog[3]="";
foreach(1 .. 2){ #���}�[�N���𑝂₷�ꍇ�ɂ͏C��
	if(!$FORM{"Fmark${_}_$temp_id"}){$FORM{"Fmark${_}_$temp_id"}=0;}
$Slog[3] .= $FORM{"Fmark${_}_$temp_id"} . "_";
}
$Slog[3]=substr($Slog[3],0,-1);

#�X�V��(4)
	#�����̎擾
	$ENV{'TZ'} = "JST-9"; $times = time();
	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($times);
	$youbi = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat') [$wday];
$Slog[4]=&get_time(0,1);

#�p�X���[�h(5)
#(���ύX)
$Slog[5]=$Tlog[5];

#�Љ(6)
$Slog[6]=$FORM{"Fsyoukai$temp_id"};
$Slog[6]=~s/\r//g; $Slog[6]=~s/\n/<br>/g;

#�Ǘ��l�R�����g(7)
$Slog[7]=$FORM{"Fkanricom$temp_id"};
$Slog[7]=~s/\r//g; $Slog[7]=~s/\n/<br>/g;

#�����O(8)
$Slog[8]=$FORM{"Fname$temp_id"};

#E-Mail(9)
$Slog[9]=$FORM{"Femail$temp_id"};

#�J�e�S��(10)
$Slog[10]="";
foreach(1 .. $EST_reg{kt_max}){
	$Slog[10] .= $FORM{"F${temp_id}kt$_"} . "&";
}
$Slog[10]=substr($Slog[10],0,-1);

#time�`��(11)
$Slog[11]= time() . "_0";

#�o�i�[URL(12)
$Slog[12]=$FORM{"Fbana_url$temp_id"};

#�A�N�Z�X��(13)
$Slog[13]="0_0_0_0";

#�ŏI�A�N�Z�XIP(14)
$Slog[14]="";

#�L�[���[�h(15)
$Slog[15]=$FORM{"Fkey$temp_id"};

##���̑�
$Clog_id++; #���̃f�[�^�̂��߂�+1

}

#(t2)symlink�֐��̎g�p�ۂ̃`�F�b�N(&check_symlink)
sub check_symlink{
local($check_fl);
	eval{symlink("","");};
	if($@){$check_fl=0;}
	else{$check_fl=1;}
return $check_fl;
}

#(t3)�o�^�����Čv�Z
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

#(t4)���^�������N�I�[�g
sub quote_str{
	my $ret=shift;
	if(substr($ret,-1,1) eq "\\"){$ret.="\\";}
	return $ret;
}

##-- end of temp.cgi --##
