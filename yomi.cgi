#!/usr/bin/perl

#��perl�̃p�X�������̊��ɍ��킹�ď��������܂��B
#���́A�u#!/usr/bin/perl�v�@���@�u#!/usr/local/bin/perl�v�ł��B
#����Ȃ��ꍇ�̓T�[�o�[�Ǘ���(�������̓v���o�C�_�[)��
#�m�F���Ă��������B

require 'pl/jcode.pl';
require 'pl/cfg.cgi';
require 'pl/temp.cgi';

################################################################
# Yomi-Search Ver4 [�T�[�`�G���W��] (Since:1999/09/22)
#   (C) 1999-2001 by yomi
#   E���[��: yomi@pekori.to
#   �z�[���y�[�W: http://yomi.pekori.to/
################################################################

## ---[���p�K��]------------------------------------------------------------+
## 1. ���̃X�N���v�g�̓t���[�\�t�g�ł��B���̃X�N���v�g���g�p����
##    �����Ȃ鑹�Q�ɑ΂��č�҂͈�؂̐ӔC�𕉂��܂���B
## 2. ���̃X�N���v�g���g�p�������_�ŗ��p�K��(http://yomi.pekori.to/kiyaku.html)
##    �ɓ��ӂ������̂Ƃ݂Ȃ����Ă��������܂��B
##    ���g�p�ɂȂ�O�ɕK�����ǂ݂��������B
## 3. �����́u�A�C�R�� (new.gif/recom.gif/sougogif.gif) �v�̒��쌠��
##   �u�������ƃA�C�R���̕���  (http://www.ushikai.com/)�v�ɋA�����Ă��܂��B
## -------------------------------------------------------------------------+

&form_decode();
if($EST{task}==1){&go_TASK;}

#�e���[�h�֕���
#-----------------#
if($FORM{mode}){
if(!$EST{home}){$EST{home}=$EST{script};}
if($FORM{mode} eq "kt"){$Stitle=$ganes{$FORM{'kt'}};($Spre_kt_file)=split(/_/,$FORM{'kt'});} #�e�J�e�S���̎��̕\���^�C�g��
elsif($FORM{mode} eq "new"){$Stitle="�V���T�C�g"; $Spre_kt_file="new_ys";} #�V���T�C�g�̕\���^�C�g��,�t�@�C����
elsif($FORM{mode} eq "renew"){$Stitle="�X�V�T�C�g"; $Spre_kt_file="renew_ys";} #�X�V�T�C�g�̕\���^�C�g��,�t�@�C����
elsif($FORM{mode} eq "random"){&random;} #�����_���W�����v
elsif($FORM{mode} eq "link"){&link;} #�����N�W�����v
else{&mes("�w�肵�����[�h�͑��݂��܂���(mode=$FORM{mode})","���[�h�I���G���[","java");}
##�y�[�W�ݒ�
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
           &jcode::convert(\$value,'sjis');
           &jcode::convert(\$name,'sjis'); $FORM{$name} = $value;
   }
}

#(5)�����_���W�����v(&random)
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
#(6)�����N�W�����v����(&link)
$FORM{id}=~s/\D//g;
if($FORM{id}){
	local($fl=0,@ref_list);
		#referer�`�F�b�N
		if(!$ENV{'HTTP_REFERER'}){$fl=1;} #referer�������Ƃ��ɃJ�E���g���Ȃ��ꍇ�ɂ͂��̍s���폜
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
else{ #���O�t�@�C������URL����������(Ver3�ƌ݊�)
	open(IN,"$EST{log_path}$EST{logfile}");
	my $link_fl=0; my($link);
	while(<IN>){
		@Slog=split(/<>/,$_,4);
		if($Slog[0] eq $FORM{id}){$link=$Slog[2];$link_fl=1;last;}
	}
	close(IN);
	if(!$link_fl){&mes("�Y������f�[�^��������܂���","�G���[","java");}
	else{&location($link);}
}
}

##-- end of yomi.cgi --##
