#!/usr/bin/perl

#��perl�̃p�X�������̊��ɍ��킹�ď��������܂��B
#���́A�u#!/usr/bin/perl�v�@���@�u#!/usr/local/bin/perl�v�ł��B
#����Ȃ��ꍇ�̓T�[�o�[�Ǘ���(�������̓v���o�C�_�[)��
#�m�F���Ă��������B

##�J�E���^���[�h�̐ݒ�
#SSI���g�p(�����\��)=1/JavaScript���g�p(�摜�\��)=2/
$Ec_mode="2";

##�J�E���^�p�摜�f�B���N�g���ւ̃p�X
#count.cgi��ݒu����f�B���N�g������̃p�X���w�肷��
#SSI���J�E���^�̏ꍇ�ɂ͕s�v
$Ec_dir="img/count/";

#-----�������܂Őݒ聪-----#
$hyouji="";
if($ENV{QUERY_STRING} eq "today"){$hyouji=2;}
elsif($ENV{QUERY_STRING} eq "yesterday"){$hyouji=3;}
else{$hyouji=1;}

require "pl/count/count_ys.cgi";
&index_count(1,$hyouji,$Ec_mode);
exit;

