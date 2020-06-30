Application names and window titles are nominal variables. In order to make their processing easier, I give an integer code for each possible value. 
In addition, also the task names are coded as integers. Please see below for the integer codes and and the relating functions in tools_dic.py for their use.

---------------------------------------------------

For exe name, I use the following integer exe codes:

1 : excel
2 : explorer
3 : sakura
4 : devenv
5 : iexplore
6 : notepad
7 : bcompare
8 : airsovly
9 : firefox
10 : editplus
11 : tortoiseproc
12 : symphony
13 : sofficebin
14 : msimn
15 : ipmsg
16 : aliim
17 : rundll32
18 : airspsam
19 : taskpit
20 : dwwin

---------------------------------------------------

For windows titles, I use the following integer title codes:

01	Debug, DEBUG, debug, デバッグ, ﾃﾞﾊﾞｯｸﾞ, 
02	テスト, ﾃｽﾄ, test, TEST, Test
03	出退勤
04	OGA
05	OGT
06	OGU
07	OGV
08	OLT
09	OLV
10	VOL
11	AIRS_PSAM
12	PSAM_変換仕様書
13	出力系調査報告書
14	帳票定義体
15	画面定義体
16	娘
17	童
18	淘宝
19	常来返
20	taobao
21	百度搜索
22	百度百科
23	百度知道
24	服装
25	SQL
26	搜房网
27	AIRS
28	THICK変換ﾃｰﾌﾞﾙ
29	POINT変換ﾃｰﾌﾞﾙ
30	SIZE変換ﾃｰﾌﾞﾙ
31	漢字コード変換表
32	ＢＭＳ
33	ＩＢＭ漢字コード変換対応表
34	調査報告書
35	ATTRパターン
36	ＦＩＥＬＤ文
37	Q&A管理台帳
38	搜索
39	不具合対応
40	天猫
41	支付宝
42	ReverseServer
43	Error
44	ＤＡＴＡ文（項目定義）の変換
45	ﾛｸﾞﾌｧｲﾙ
46	解析Log
47	解析ｿｰｽ
48	報告書
49	査読シート
50	ファイル内の検索
---------------------------------------------------

For tasks, I use the following integer task codes:

0: unknown
1: program
2: test
3: administration
4: leisure (includes leisure, browser, messenger)
5: document creation/confirmation

Debug is not a separate category. It is involved in programming or testing.

