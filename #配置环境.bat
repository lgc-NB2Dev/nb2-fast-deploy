:: GB2312
@echo off

py -3.10 -V > nul
if not %errorlevel%==0 (
    echo �㻹û�а�װ Python 3.10 ����� Python 3.10 ���� PATH �У����鰲װ
    goto end
)

set needset=0
choice /m "�Ƿ���Ҫʹ���廪 pypi ����Դ����Y ͬ�⣬N �ܾ���"
if %errorlevel%==1 (
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
    echo.
    echo ���ֶ��鿴 pyproject.toml �ļ��ĵ� 59 ���Ƿ�ע��
) else (
    pip config unset global.index-url
    echo.
    echo ���ֶ�ע�� pyproject.toml �ļ��ĵ� 59 ��
)

echo.
echo Ĭ�ϻᰲװ OneBot �������������ڷ��� ws ��������
echo ���Ա༭ pyproject.toml �ļ�����װ��������������������
echo ׼�������𣿰��»س����������밲װ����~
pause > nul

echo.
echo ��װPoetry�����Ե�
py -3.10 -m pip install poetry -U
if not %errorlevel%==0 (
    echo ��װ Poetry ʧ�ܣ�
    goto end
)

echo.
echo ��װ��Ŀ���������Ե�
py -3.10 -m poetry install
if not %errorlevel%==0 (
    echo ��װ��Ŀ����ʧ�ܣ�
    goto end
)

echo.
echo ������Ŀ���������Ե�
py -3.10 -m poetry update
if not %errorlevel%==0 (
    echo ������Ŀ����ʧ�ܣ�
    goto end
)

echo.
echo ��ϲ��ִ�гɹ�~ ����������ԣ�
echo.
echo - �� .env �ļ����༭һЩ��������糬���û��� Bot �ǳƵ�
echo - �� .env.prod �ļ��༭ NoneBot ������ IP ��˿�
echo - ���ʹ���� ForwardDriver����ע�� bot.py �ĵ� 23 ��
echo - �����װ����������������ȡ�� bot.py ��Ӧע��
echo.
echo ���������Щ�������Ժ�ֻ��Ҫ�� #����.bat �Ϳ������� NoneBot ����
echo ��װ����Ȳ������Կ� README.md �ĵ���
echo.
echo �������ڰ�����һ�����Բ���״̬�õ� ping ���
echo ���úó����û�����֮������ GoCQ �� NoneBot
echo ������ Bot ����ָ�� ping ����� Bot �ظ��˾ʹ�������û��������~
echo ��ɾ���������Ļ���ɾ�� src/plugins/ping.py �Ϳ�����
echo.
echo ףʹ�����~
echo.

:end
echo ��������ر�
pause > nul