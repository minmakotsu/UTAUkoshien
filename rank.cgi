#!/usr/bin/perl

#��perl�̃p�X�������̊��ɍ��킹�ď��������܂��B
#���́A�u#!/usr/bin/perl�v�@���@�u#!/usr/local/bin/perl�v�ł��B
#����Ȃ��ꍇ�̓T�[�o�[�Ǘ���(�������̓v���o�C�_�[)��
#�m�F���Ă��������B

require 'pl/jcode.pl';
require 'pl/cfg.cgi';
require 'pl/temp.cgi';

##�ڎ�##
#(1)�l�C(OUT)�����L���O�\�����(&PR_rank)
#(1.1)�A�N�Z�X(IN)�����L���O�\�����(&PR_rev)
#(1.1.1)�A�N�Z�X�����L���O���X�V(&make_rev)
#(1.1.2)�݌v�l�C�����L���O���X�V(&make_rank_rui)
#(2)�����N�W�����v����(&link)
#(2.1)�A�N�Z�X�W�����v����(&r_link)
#(3)�L�[���[�h�����L���O�\�����(&PR_keyrank)

$rank_flag = 1; #�����L���O���s�t���O

&form_decode();
	if(!$FORM{page}){$FORM{page}=1;}
if($FORM{mode} eq "link"){&link;}
elsif($FORM{mode} eq "r_link"){&r_link;}
elsif($FORM{mode} eq "keyrank"){&PR_keyrank;}
elsif($FORM{mode} eq "rev" || $FORM{mode} eq "rev_bf" || $FORM{mode} eq "rev_rui"){&PR_rev;}
else{&PR_rank;} #�l�C�����L���O
exit;

sub PR_rank{
#(1)�l�C�����L���O�\�����(&PR_rank)
if(!$EST{rank_fl}){&mes("�l�C�����L���O�͎��{���Ȃ��ݒ�ɂȂ��Ă��܂�","�G���[","java");}
if(!$FORM{mode}){$FORM{mode}="rank";}
	require "$EST{temp_path}rank.html";

	print "Content-type: text/html\n\n";
	&print_rank($FORM{kt},$FORM{mode},$FORM{page});
}

sub PR_rev{
#(1.1)�A�N�Z�X(IN)�����L���O�\�����(&PR_rev)
if(!$EST{rev_fl}){&mes("�A�N�Z�X�����L���O�͎��{���Ȃ��ݒ�ɂȂ��Ă��܂�","�G���[","java");}
	require "$EST{temp_path}rev_rank.html";

	print "Content-type: text/html\n\n";
	&print_rank($FORM{kt},$FORM{mode},$FORM{page});
}

sub make_rev{
#(1.1.1)�A�N�Z�X�����L���O���X�V(&make_rev)
#$arg[0]=> ���݂̃����L���O���X�V(rev)/�݌v�����L���O���X�V(rev_rui)/������(format)
	##���݂̃����L���O���X�V&�{�̃t�@�C���ɔ��f(rev)
	if($_[0] eq "rev"){
		close(IN);
		&lock(); #���b�N
		@log_lines=();
		local(@rank,%pt,%time_fl,$day=0,$st,@Slog,$line,%line,$i=0);
		open(IN,"$EST{log_path}rev_temp.cgi");
			while(<IN>){
				chop;
				@rank=split(/<>/,$_); #ID<>time�`��<>IP\n
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
					if(!$LC_kt){$kt_fl=1;} #�J�e�S���w��Ȃ�
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
		
		&unlock(); #���b�N����
	}
	##�݌v�̃����L���O���X�V(rev_rui)
	elsif($_[0] eq "rev_rui"){
		close(IN);
		&lock_rev(); #���b�N
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
					if(!$LC_kt){$kt_fl=1;} #�J�e�S���w��Ȃ�
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
		
		&unlock_rev(); #���b�N����
	}
	##������(format)
	elsif($_[0] eq "format"){
		close(IN);
		&lock(); #���b�N
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
		
		#�{�̃��O��������
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
		
		&unlock(); #���b�N����
	}
	else{&mes("&make_rev�̈������s���ł�","�G���[","java");}



}

sub make_rank_rui{
#(1.1.2)�݌v�l�C�����L���O���X�V(&make_rank_rui)
	close(IN);
		&lock_rev(); #���b�N
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
					if(!$LC_kt){$kt_fl=1;} #�J�e�S���w��Ȃ�
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
		
		&unlock_rev(); #���b�N����

}

sub link{
#(2)�����N�W�����v����(&link)
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

sub r_link{
#(2.1)�A�N�Z�X�W�����v����(&r_link)
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
$EST{location}=0; #refresh�W�����v�ɂ���
&location($EST{rev_url});
}

#(3)�L�[���[�h�����L���O�\�����(&PR_keyrank)
sub PR_keyrank{
require "$EST{log_path}task_ys.cgi";
print "Content-type: text/html\n\n";
require "$EST{temp_path}keyrank.html";
&print_keyrank;
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






