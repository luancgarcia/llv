<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>Lápis Vermelho - Multiplan</title>
</head>

<body>

<script type="text/javascript">
var userAgent = navigator.userAgent.toLowerCase();
var devices = new Array('nokia','iphone','blackberry','sony','lg',
'htc_tattoo','samsung','symbian','SymbianOS','elaine','palm',
'series60','windows ce','android','obigo','netfront',
'openwave','mobilexplorer','operamini','ipad','BlackBerry');
var url_redirect = 'https://www.liquidacaolapisvermelho.com.br';

function mobiDetect(userAgent, devices) {
for(var i = 0; i < devices.length; i++) {

if (userAgent.search(devices[i]) > 0) {
return true;
}
}
return false;
}

if (mobiDetect(userAgent, devices)) {
window.location.href = url_redirect;
}
else
{
	window.location.href = 'https://www.facebook.com/LiquidacaoLapisVermelho/app_213439928802953';
}

</script>
</body>
</html>
